from typing import List, Dict
from config.settings import Settings
import requests
import logging

logger = logging.getLogger(__name__)

class WebSearchTool:
    def __init__(self, settings: Settings):
        self.api_key = settings.serper_api_key
        self.endpoint = "https://google.serper.dev/search"

    def search(self, query: str) -> List[Dict]:
        logger.info(f"Performing web search for query: {query}")
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        payload = {"q": query}
        response = requests.post(self.endpoint, json=payload, headers=headers)
        response.raise_for_status()
        results = response.json().get("organic", [])
        return [{"content": r["snippet"], "url": r["link"]} for r in results]