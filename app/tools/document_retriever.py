from typing import List, Dict
from config.settings import Settings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class DocumentRetriever:
    def __init__(self, settings: Settings):
        self.embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
        self.vector_store = FAISS.load_local(settings.vector_store_path, self.embeddings)
        self.settings = settings

    def retrieve(self, query: str) -> List[Dict]:
        docs = self.vector_store.similarity_search(query, k=3)
        return [{"content": doc.page_content, "source": doc.metadata.get("source", "unknown")} for doc in docs]