import pytest
from app.agents.research_agent import ResearchAgent
from app.config.settings import Settings

@pytest.fixture
def research_agent():
    settings = Settings(openai_api_key="test_key")
    return ResearchAgent(settings)

def test_plan_and_reason(research_agent, mocker):
    mocker.patch.object(research_agent.llm, "invoke", return_value={"content": [{"step": "search web"}]})
    state = {"query": "test query"}
    result = research_agent.plan_and_reason(state)
    assert result["plan"] == [{"step": "search web"}]