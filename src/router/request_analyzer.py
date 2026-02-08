class RequestAnalyzer:

    def analyze(self, prompt: str):

        length = len(prompt.split())

        # Simple heuristic classification
        if length < 30:
            complexity = "simple"
        elif length < 100:
            complexity = "moderate"
        else:
            complexity = "complex"

        if "explain" in prompt.lower() or "why" in prompt.lower():
            complexity = "reasoning"

        return {
            "complexity": complexity,
            "word_count": length
        }
