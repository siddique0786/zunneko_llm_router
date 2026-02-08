from src.providers.groq_provider import GroqProvider
from src.providers.gemini_provider import GeminiProvider


class ProviderSelector:

    def __init__(self):
        self.groq = GroqProvider()
        self.gemini = GeminiProvider()

    def select(self, analysis):

        complexity = analysis["complexity"]

        if complexity == "simple":
            return self.groq

        if complexity in ["complex", "reasoning"]:
            return self.gemini

        return self.groq
