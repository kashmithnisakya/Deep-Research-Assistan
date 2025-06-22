from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from config.settings import Settings
from workflows.state import ResearchState
import json

class ResearchAgent:
    def __init__(self, settings: Settings):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openai_api_key,
            temperature=0.7
        )
        self.settings = settings

    def plan_and_reason(self, state: ResearchState) -> ResearchState:
        prompt = f"""
        Given the query: {state['query']}
        Create a step-by-step plan to answer the query accurately. Consider using web search or document retrieval if needed.
        Return a JSON object with a 'plan' key containing a list of steps.
        Example: {{"plan": ["Step 1: Perform web search", "Step 2: Retrieve documents"]}}
        """
        response = self.llm.invoke(prompt)
        try:
            plan_data = json.loads(response.content)
            state["plan"] = plan_data["plan"]
        except json.JSONDecodeError:
            # Fallback: Split by newlines if JSON parsing fails
            state["plan"] = response.content.split("\n")
        return state

    def generate_final_answer(self, state: ResearchState) -> ResearchState:
        prompt = f"""
        Query: {state['query']}
        Context: {state['context']}
        Sources: {state['sources']}
        Generate a detailed, well-structured answer to the query.
        Return the final answer as a string.
        """
        response = self.llm.invoke(prompt)
        state["answer"] = response.content
        return state