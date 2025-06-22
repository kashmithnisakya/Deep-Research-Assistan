from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from config.settings import Settings
from workflows.state import ResearchState
import json
import tiktoken
import logging

logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self, settings: Settings):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openai_api_key,
            temperature=0.7
        )
        self.settings = settings
        try:
            self.encoding = tiktoken.encoding_for_model(settings.llm_model)
        except KeyError:
            print(f"Warning: No tokenizer found for model '{settings.llm_model}'. Falling back to 'cl100k_base'.")
            self.encoding = tiktoken.get_encoding("cl100k_base")  # Fallback tokenizer
        self.max_tokens = 900000  # Safe limit for context window

    def _truncate_text(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within max_tokens."""
        tokens = self.encoding.encode(text)
        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
            text = self.encoding.decode(tokens)
            text = text[:text.rfind(" ")] + "..."  # Avoid cutting mid-word
        return text

    def _truncate_context_and_sources(self, context: List[str], sources: List[str], max_tokens: int) -> tuple[List[str], List[str]]:
        """Truncate context and sources to fit within max_tokens."""
        total_tokens = sum(len(self.encoding.encode(item)) for item in context + sources)
        if total_tokens <= max_tokens:
            return context, sources

        # Allocate half to context, half to sources
        context_max = max_tokens // 2
        sources_max = max_tokens - context_max
        context_tokens = 0
        new_context = []
        for item in context:
            item_tokens = len(self.encoding.encode(item))
            if context_tokens + item_tokens <= context_max:
                new_context.append(item)
                context_tokens += item_tokens
            else:
                remaining = context_max - context_tokens
                if remaining > 0:
                    new_context.append(self._truncate_text(item, remaining))
                break

        sources_tokens = 0
        new_sources = []
        for item in sources:
            item_tokens = len(self.encoding.encode(item))
            if sources_tokens + item_tokens <= sources_max:
                new_sources.append(item)
                sources_tokens += item_tokens
            else:
                remaining = sources_max - sources_tokens
                if remaining > 0:
                    new_sources.append(self._truncate_text(item, remaining))
                break

        return new_context, new_sources

    def plan_and_reason(self, state: ResearchState) -> ResearchState:
        logger.info(f"Planning for query: {state['query']}")
        prompt = f"""
        You are a research assistant tasked with creating a step-by-step plan to answer the following query accurately: "{state['query']}"

        **Available Tools**:
        - **web_search**: Use this to retrieve up-to-date information or recent data from the internet. This is ideal for queries about current events, trends, or topics requiring fresh information.
        - **document_retrieval**: Use this to retrieve relevant information from a pre-indexed set of documents. This is ideal for queries requiring domain-specific knowledge or detailed insights from a curated dataset.

        **Instructions**:
        1. Analyze the query to determine which tools are most appropriate:
           - If the query involves recent events, trends, or general knowledge, include "web_search" in the plan.
           - If the query requires in-depth or domain-specific information (e.g., about renewable energy, scientific studies), include "document_retrieval" in the plan.
           - You may include both tools if the query benefits from both recent data and curated documents.
        2. Create a step-by-step plan to answer the query. Each step should be concise and actionable.
        3. Use the exact tool names "web_search" and "document_retrieval" in the plan to indicate when these tools should be used.
        4. Return the plan as a JSON object with a 'plan' key containing a list of steps.

        **Example**:
        For query: "What are the latest advancements in renewable energy?"
        {{
            "plan": [
                "web_search: Search for recent articles and news on renewable energy advancements",
                "document_retrieval: Retrieve studies or reports from the document store on renewable energy"
            ]
        }}

        **Your Task**:
        Create a JSON plan for the query: "{state['query']}"
        """
        response = self.llm.invoke(prompt)
        try:
            plan_data = json.loads(response.content)
            state["plan"] = plan_data["plan"]
            logger.info(f"Generated plan: {state['plan']}")
        except json.JSONDecodeError:
            # Fallback: Split by newlines if JSON parsing fails
            state["plan"] = ["web_search", "document_retrieval"]
            logger.warning("LLM response was not valid JSON. Using default plan.")
        return state
        return state

    def generate_final_answer(self, state: ResearchState) -> ResearchState:
        prompt = f"""
        Query: {state['query']}
        Context: {state['context']}
        Sources: {state['sources']}
        Generate a detailed, well-structured answer to the query.
        Return the final answer as a string.
        """
        logger.info(f"Generating final answer for query: {state['query']}")
        response = self.llm.invoke(prompt)
        state["answer"] = response.content
        return state