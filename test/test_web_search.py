import pytest
from app.tools.web_search import WebSearchTool
from app.config.settings import Settings

@pytest.fixture
def web_search_tool():
    settings = Settings(serper_api_key="test_key")
    return WebSearchTool(settings)

def test_search(web_search_tool, mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"organic": [{"snippet": "test", "link": "http://test.com"}]}
    mocker.patch("requests.post", return_value=mock_response)
    results = web_search_tool.search("test query")
    assert len(results) == 1
    assert results[0]["content"] == "test"