# from src.config.provider_costs import PROVIDER_COSTS
from ..config.provider_costs import PROVIDER_COSTS



metrics_data = {
    "exact_cache_hits": 0,
    "semantic_cache_hits": 0,
    "cache_misses": 0,
    "provider_usage": {},

    # ⭐ NEW
    "total_tokens": 0,
    "total_cost": 0.0,
    "provider_cost_breakdown": {}
}





def track_cost(provider_name: str, tokens_used: int, cost: float):

    metrics_data["total_tokens"] += tokens_used
    metrics_data["total_cost"] += cost

    # Track provider wise cost
    if provider_name not in metrics_data["provider_cost_breakdown"]:
        metrics_data["provider_cost_breakdown"][provider_name] = 0.0

    metrics_data["provider_cost_breakdown"][provider_name] += cost


def calculate_cost(provider_name: str, input_tokens: int, output_tokens: int):

    pricing = PROVIDER_COSTS.get(provider_name)

    if not pricing:
        return 0.0

    input_cost = (input_tokens / 1000) * pricing["input_per_1k_tokens"]
    output_cost = (output_tokens / 1000) * pricing["output_per_1k_tokens"]

    return input_cost + output_cost


print(calculate_cost("GroqProvider", 500, 500))