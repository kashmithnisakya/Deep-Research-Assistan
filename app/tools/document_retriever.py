from typing import List, Dict
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from config.settings import Settings
import os

class DocumentRetriever:
    def __init__(self, settings: Settings):
        self.embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
        self.persist_directory = settings.vector_store_path
        # Initialize with sample documents if store doesn't exist
        if not os.path.exists(os.path.join(self.persist_directory, "chroma.sqlite3")):
            documents = [
                Document(page_content="Renewable energy reduces carbon emissions...", metadata={"source": "energy_report.pdf"}),
                Document(page_content="Solar power adoption has increased...", metadata={"source": "solar_trends.docx"}),
                Document(page_content="Wind energy is cost-competitive...", metadata={"source": "wind_study.html"}),
            ]
            self.vector_store = Chroma.from_documents(
                documents, self.embeddings, persist_directory=self.persist_directory
            )
        else:
            self.vector_store = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)

    def retrieve(self, query: str) -> List[Dict]:
        docs = self.vector_store.similarity_search(query, k=3)
        return [{"content": doc.page_content, "source": doc.metadata.get("source", "unknown")} for doc in docs]