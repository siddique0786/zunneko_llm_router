import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()
