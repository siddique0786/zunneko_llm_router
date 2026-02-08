import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


class MetricsCollector:

    def record_exact_hit(self):
        redis_client.incr("metrics:exact_cache_hits")

    def record_semantic_hit(self):
        redis_client.incr("metrics:semantic_cache_hits")

    def record_cache_miss(self):
        redis_client.incr("metrics:cache_misses")

    def record_provider_usage(self, provider_name):
        redis_client.hincrby("metrics:provider_usage", provider_name, 1)

    def report(self):
        return {
            "exact_cache_hits": int(redis_client.get("metrics:exact_cache_hits") or 0),
            "semantic_cache_hits": int(redis_client.get("metrics:semantic_cache_hits") or 0),
            "cache_misses": int(redis_client.get("metrics:cache_misses") or 0),
            "provider_usage": redis_client.hgetall("metrics:provider_usage")
        }


metrics_collector = MetricsCollector()
