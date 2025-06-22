import pytest
from app.tools.document_retriever import DocumentRetriever
from app.config.settings import Settings
from unittest.mock import Mock
from io import BytesIO
import os

@pytest.fixture
def document_retriever(tmp_path):
    settings = Settings(openai_api_key="test_key", vector_store_path=str(tmp_path))
    return DocumentRetriever(settings)

def test_add_documents(document_retriever, mocker):
    # Mock a text file
    mock_text_file = Mock()
    mock_text_file.name = "test.txt"
    mock_text_file.read.return_value = b"Test document content"
    
    # Mock a PDF file
    mock_pdf_file = Mock()
    mock_pdf_file.name = "test.pdf"
    mock_pdf_file.read.return_value = b"%PDF-1.0\nTest PDF content"
    
    # Mock PyPDF2.PdfReader
    mock_pdf_reader = Mock()
    mock_pdf_reader.pages = [Mock(extract_text=lambda: "Test PDF content")]
    mocker.patch("PyPDF2.PdfReader", return_value=mock_pdf_reader)
    
    # Add documents
    document_retriever.add_documents([mock_text_file, mock_pdf_file])
    
    # Verify documents were added
    results = document_retriever.retrieve("Test content")
    assert len(results) > 0
    assert any(doc["content"] == "Test document content" for doc in results)
    assert any(doc["content"] == "Test PDF content" for doc in results)
    
    # Verify ChromaDB persistence
    assert os.path.exists(os.path.join(document_retriever.settings.vector_store_path, "chroma.sqlite3"))

def test_vector_store_initialization(document_retriever):
    # Verify sample documents are initialized
    results = document_retriever.retrieve("renewable energy")
    assert len(results) > 0
    assert any("Renewable energy reduces carbon emissions" in doc["content"] for doc in results)