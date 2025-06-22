from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    openai_api_key: str
    serper_api_key: str
    llm_model: str = "gpt-4o-mini"
    vector_store_path: str = os.path.join(os.path.dirname(__file__), "../data/vector_store")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"