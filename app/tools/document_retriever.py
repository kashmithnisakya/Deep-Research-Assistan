from typing import List, Dict, Any
from config.settings import Settings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import os
import PyPDF2
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class DocumentRetriever:
    def __init__(self, settings: Settings):
        self.embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
        self.settings = settings
        self.vector_store = self._load_or_create_vector_store()

    def _load_or_create_vector_store(self):
        vector_store_path = self.settings.vector_store_path
        # Check if ChromaDB database exists
        chroma_db_path = os.path.join(vector_store_path, "chroma.sqlite3")
        
        if os.path.exists(chroma_db_path):
            return Chroma(
                persist_directory=vector_store_path,
                embedding_function=self.embeddings
            )
        else:
            # Initialize with sample documents
            documents = [
                Document(
                    page_content="Renewable energy reduces carbon emissions by replacing fossil fuels.",
                    metadata={"source": "energy_report.pdf"}
                ),
                Document(
                    page_content="Solar power adoption has increased by 20% annually since 2015.",
                    metadata={"source": "solar_trends.docx"}
                ),
                Document(
                    page_content="Wind energy is cost-competitive with traditional energy sources.",
                    metadata={"source": "wind_study.html"}
                ),
            ]
            os.makedirs(vector_store_path, exist_ok=True)
            vector_store = Chroma.from_documents(
                documents,
                self.embeddings,
                persist_directory=vector_store_path
            )
            print(f"Initialized Chroma vector store at {vector_store_path}")
            return vector_store

    def add_documents(self, uploaded_files: List[Any]) -> None:
        """Add uploaded documents to the Chroma vector store."""
        new_documents = []
        for uploaded_file in uploaded_files:
            file_name = getattr(uploaded_file, "name", "unknown")
            try:
                if file_name.endswith(".pdf"):
                    # Process PDF files
                    pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                    text = ""
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
                    if text.strip():  # Ensure text is not empty
                        new_documents.append(Document(page_content=text, metadata={"source": file_name}))
                    else:
                        print(f"Warning: No text extracted from {file_name}")
                elif file_name.endswith(".txt"):
                    # Process text files
                    text = uploaded_file.read().decode("utf-8")
                    if text.strip():  # Ensure text is not empty
                        new_documents.append(Document(page_content=text, metadata={"source": file_name}))
                    else:
                        print(f"Warning: No text extracted from {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
                continue

        if new_documents:
            # Add new documents to the Chroma vector store
            self.vector_store.add_documents(new_documents)
            print(f"Added {len(new_documents)} documents to the Chroma vector store.")
        else:
            raise ValueError("No valid documents were processed for indexing.")

    def retrieve(self, query: str) -> List[Dict]:
        logger.info(f"Retrieving documents for query: {query}")
        docs = self.vector_store.similarity_search(query, k=3)
        return [{"content": doc.page_content, "source": doc.metadata.get("source", "unknown")} for doc in docs]