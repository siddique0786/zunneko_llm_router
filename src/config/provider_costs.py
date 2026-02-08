"""
Example:

If Groq generates 1000 tokens → cost = $0.0004

If Gemini generates 1000 tokens → cost = $0.0015
"""



PROVIDER_COSTS = {
    "GroqProvider": {
        "input_per_1k_tokens": 0.0002,
        "output_per_1k_tokens": 0.0004
    },
    "GeminiProvider": {
        "input_per_1k_tokens": 0.0005,
        "output_per_1k_tokens": 0.0015
    }
}

# print(PROVIDER_COSTS)

