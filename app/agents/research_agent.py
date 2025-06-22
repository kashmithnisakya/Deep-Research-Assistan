from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from config.settings import Settings

class ResearchAgent:
    def __init__(self, settings: Settings):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openai_api_key,
            temperature=0.7
        )
        self.settings = settings

    def plan_and_reason(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Given the query: {state['query']}
        Create a step-by-step plan to answer the query accurately. Consider using web search or document retrieval if needed.
        Return a JSON object with a 'plan' key containing a list of steps.
        """
        response = self.llm.invoke(prompt)
        plan = response.content
        state["plan"] = plan
        return state

    def generate_final_answer(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Query: {state['query']}
        Context: {state['context']}
        Sources: {state['sources']}
        Generate a detailed, well-structured answer to the query.
        Return a JSON object with an 'answer' key containing the final answer as a string.
        """
        response = self.llm.invoke(prompt)
        state["answer"] = response.content
        return state