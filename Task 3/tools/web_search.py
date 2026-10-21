import time
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

_search = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search the web for real-time information.
    Input should be a concise, specific query."""
    last_err = None
    for attempt in range(3):
        try:
            return _search.run(query)
        except Exception as e:
            last_err = e
            time.sleep(1 + attempt)  # 1s, 2s, 3s backoff
    return f"Search failed after 3 attempts: {last_err}"