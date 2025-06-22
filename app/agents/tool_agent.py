from typing import Dict, Any
from tools.web_search import WebSearchTool
from tools.document_retriever import DocumentRetriever
from config.settings import Settings
from workflows.state import ResearchState
import logging

logger = logging.getLogger(__name__)

class ToolAgent:
    def __init__(self, settings: Settings):
        self.web_search = WebSearchTool(settings)
        self.doc_retriever = DocumentRetriever(settings)
        self.settings = settings

    def execute_tools(self, state: ResearchState) -> ResearchState:
        logger.info(f"Executing tools for query: {state['query']}")
        plan = state["plan"]
        context = []
        sources = []

        for step in plan:
            if "web_search" in step.lower():
                logger.info(f"Performing web search for step: {step}")
                results = self.web_search.search(state["query"])
                context.extend([r["content"] for r in results])
                sources.extend([r["url"] for r in results])
            elif "document_retrieval" in step.lower():
                logger.info(f"Retrieving documents for step: {step}")
                docs = self.doc_retriever.retrieve(state["query"])
                context.extend([doc["content"] for doc in docs])
                sources.extend([doc["source"] for doc in docs])

        state["context"] = context
        state["sources"] = sources
        return state