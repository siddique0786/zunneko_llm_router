from google import genai
from src.providers.base import BaseProvider
from src.settings import settings


class GeminiProvider(BaseProvider):

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-3-flash-preview"

    def generate(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text


    # ⭐ NEW — Streaming Generation
    def generate_stream(self, prompt: str):

        stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=prompt
        )

        for chunk in stream:
            if chunk.text:
                yield chunk.text


    def health_check(self) -> bool:
        return True