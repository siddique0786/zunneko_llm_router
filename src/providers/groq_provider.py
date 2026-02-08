from groq import Groq
from src.providers.base import BaseProvider
from src.settings import settings


class GroqProvider(BaseProvider):

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "openai/gpt-oss-20b"

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content


    # ⭐ NEW — Streaming Generation
    def generate_stream(self, prompt: str):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


    def health_check(self) -> bool:
        return True
