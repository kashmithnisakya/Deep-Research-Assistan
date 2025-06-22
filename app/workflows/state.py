from typing import TypedDict, List

class ResearchState(TypedDict):
    query: str
    plan: List[str]
    context: List[str]
    sources: List[str]
    answer: str