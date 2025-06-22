from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    openai_api_key: str
    serper_api_key: str
    llm_model: str = "gpt-4o-mini"
    vector_store_path: str = str(Path(__file__).parent.parent / "data" / "vector_store")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"