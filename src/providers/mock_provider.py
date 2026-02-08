from src.providers.base import BaseProvider


class MockProvider(BaseProvider):

    def generate(self, prompt: str) -> str:
        return f"[Fallback Mock Response] {prompt}"

    def health_check(self) -> bool:
        return True
