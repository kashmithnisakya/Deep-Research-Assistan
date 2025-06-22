from langgraph.graph import StateGraph, END
from typing import Dict, Any, List
from agents.research_agent import ResearchAgent
from agents.tool_agent import ToolAgent
from config.settings import Settings

class ResearchGraph:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.research_agent = ResearchAgent(settings)
        self.tool_agent = ToolAgent(settings)
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph()

        graph.add_node("research_agent", self.research_agent.plan_and_reason)
        graph.add_node("tool_agent", self.tool_agent.execute_tools)
        graph.add_node("final_answer", self.research_agent.generate_final_answer)

        graph.set_entry_point("research_agent")
        graph.add_edge("research_agent", "tool_agent")
        graph.add_edge("tool_agent", "final_answer")
        graph.add_edge("final_answer", END)

        return graph.compile()

    def run(self, query: str) -> Dict[str, Any]:
        state = {"query": query, "plan": [], "context": [], "sources": []}
        return self.graph.invoke(state)