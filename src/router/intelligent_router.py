from src.router.request_analyzer import RequestAnalyzer
from src.router.provider_selector import ProviderSelector
from src.providers.mock_provider import MockProvider
from src.cache.cache_manager import CacheManager

from src.observability.metrics import metrics_collector
from src.metrics.store import track_cost, calculate_cost
from src.observability.tracing import trace_collector
from src.resilience.circuit_breaker import CircuitBreaker
from src.resilience.retry_handler import RetryHandler

import time


class IntelligentRouter:

    def __init__(self):
        self.cache = CacheManager()
        self.analyzer = RequestAnalyzer()
        self.selector = ProviderSelector()
        self.fallback = MockProvider()
        self.retry_handler = RetryHandler()

        self.breakers = {
            "GroqProvider": CircuitBreaker(),
            "GeminiProvider": CircuitBreaker()
        }

    # ================= NORMAL ROUTE ================= #
    def route(self, prompt: str):

        trace_id = trace_collector.start_trace()

        try:
            # -------- Exact Cache -------- #
            start = time.time()
            cached = self.cache.get_exact(prompt)
            trace_collector.record_stage(trace_id, "exact_cache_lookup", time.time() - start)

            if cached:
                metrics_collector.record_exact_hit()
                trace_collector.add_metadata(trace_id, "cache_status", "exact_hit")
                return cached, "Cache"

            # -------- Semantic Cache -------- #
            start = time.time()
            semantic = self.cache.search_semantic(prompt)
            trace_collector.record_stage(trace_id, "semantic_cache_lookup", time.time() - start)

            if semantic:
                metrics_collector.record_semantic_hit()
                trace_collector.add_metadata(trace_id, "cache_status", "semantic_hit")
                return semantic, "Cache"

            metrics_collector.record_cache_miss()

            # -------- Analysis -------- #
            start = time.time()
            analysis = self.analyzer.analyze(prompt)
            trace_collector.record_stage(trace_id, "analysis", time.time() - start)

            provider = self.selector.select(analysis)
            provider_name = provider.__class__.__name__
            breaker = self.breakers.get(provider_name)

            # -------- Circuit Breaker -------- #
            if breaker and not breaker.allow_request():
                print(f"[CircuitBreaker] {provider_name} OPEN → Using fallback")
                trace_collector.add_metadata(trace_id, "circuit_breaker", "open")
                return self.fallback.generate(prompt), "CircuitBreakerFallback"

            trace_collector.add_metadata(trace_id, "provider", provider_name)
            metrics_collector.record_provider_usage(provider_name)

            print(f"[Router] Selected Provider: {provider_name}")

            # ⭐ Retry wrapped provider call
            start = time.time()
            response = self.retry_handler.execute(
                provider.generate,
                prompt
            )
            execution_time = time.time() - start

            trace_collector.record_stage(trace_id, "provider_execution", execution_time)

            if breaker:
                breaker.record_success()

            # -------- Cache -------- #
            self.cache.set_exact(prompt, response)
            self.cache.store_semantic(prompt, response)

            # -------- Cost -------- #
            input_tokens = len(prompt.split())
            output_tokens = len(response.split())

            cost = calculate_cost(provider_name, input_tokens, output_tokens)
            track_cost(provider_name, input_tokens + output_tokens, cost)

            trace_collector.add_metadata(trace_id, "tokens", input_tokens + output_tokens)
            trace_collector.add_metadata(trace_id, "cost", cost)

            return response, provider_name

        except Exception as e:

            print(f"Provider failed → Using fallback: {e}")

            if 'breaker' in locals() and breaker:
                breaker.record_failure()

            trace_collector.add_metadata(trace_id, "fallback", True)

            return self.fallback.generate(prompt), "FallbackProvider"

        finally:
            trace = trace_collector.end_trace(trace_id)
            print("[TRACE]", trace)

    # ================= STREAM ROUTE ================= #
    def route_stream(self, prompt: str):

        trace_id = trace_collector.start_trace()
        full_response = ""

        try:
            cached = self.cache.get_exact(prompt)
            if cached:
                metrics_collector.record_exact_hit()
                trace_collector.add_metadata(trace_id, "cache_status", "exact_hit")
                yield cached
                return

            semantic = self.cache.search_semantic(prompt)
            if semantic:
                metrics_collector.record_semantic_hit()
                trace_collector.add_metadata(trace_id, "cache_status", "semantic_hit")
                yield semantic
                return

            metrics_collector.record_cache_miss()

            analysis = self.analyzer.analyze(prompt)
            provider = self.selector.select(analysis)

            provider_name = provider.__class__.__name__
            breaker = self.breakers.get(provider_name)

            if breaker and not breaker.allow_request():
                print(f"[CircuitBreaker] {provider_name} OPEN → Streaming fallback")
                yield self.fallback.generate(prompt)
                return

            trace_collector.add_metadata(trace_id, "provider", provider_name)
            metrics_collector.record_provider_usage(provider_name)

            print(f"[Router] Streaming Provider: {provider_name}")

            # ⭐ Retry wrapped streaming call
            def stream_call():
                return provider.generate_stream(prompt)

            start = time.time()

            for chunk in self.retry_handler.execute_stream(stream_call):
                full_response += chunk
                yield chunk

            execution_time = time.time() - start
            trace_collector.record_stage(trace_id, "provider_execution", execution_time)

            if breaker:
                breaker.record_success()

            self.cache.set_exact(prompt, full_response)
            self.cache.store_semantic(prompt, full_response)

            input_tokens = len(prompt.split())
            output_tokens = len(full_response.split())

            cost = calculate_cost(provider_name, input_tokens, output_tokens)
            track_cost(provider_name, input_tokens + output_tokens, cost)

            trace_collector.add_metadata(trace_id, "tokens", input_tokens + output_tokens)
            trace_collector.add_metadata(trace_id, "cost", cost)

        except Exception as e:

            print(f"Streaming failed → Using fallback: {e}")

            if 'breaker' in locals() and breaker:
                breaker.record_failure()

            yield self.fallback.generate(prompt)

        finally:
            trace = trace_collector.end_trace(trace_id)
            print("[STREAM TRACE]", trace)
