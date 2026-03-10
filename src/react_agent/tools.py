"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast

from langchain_tavily import TavilySearch
from langgraph.runtime import get_runtime

from react_agent.context import Context

# add the wiki search tool instead of the tavily search tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import wikipedia
wikipedia.wikipedia.API_URL = "https://wikiless.org/api.php"

from langchain_community.tools import DuckDuckGoSearchRun,DuckDuckGoSearchResults

# async def search(query: str) -> Optional[str]:
#     """Search for general web results.

#     This function performs a search using the Wiki search engine, which is designed
#     to provide comprehensive, accurate, and trusted results. It's particularly useful
#     for answering questions about current events.
#     """
#     wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
#     search_res = wikipedia.run(query)
#     print(f"Raw search results for query '{query}': {search_res}")
#     return search_res
search_tool = DuckDuckGoSearchResults(
    num_results=5,     # 返回条数
)   

async def search(query:str)-> Optional[str]:
    """Search for general web results using DuckDuckGo.
    This function performs a search using the DuckDuckGo search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    res = await search_tool.arun(query)
    print(f"Raw search results for query '{query}': {res}")
    return res
    

# i want to pass the search results from tavily
# async def search(query: str) -> Optional[dict[str, Any]]:
#     """Search for general web results.

#     This function performs a search using the Tavily search engine, which is designed
#     to provide comprehensive, accurate, and trusted results. It's particularly useful
#     for answering questions about current events.
#     """
#     runtime = get_runtime(Context)
#     wrapped = TavilySearch(max_results=runtime.context.max_search_results)
    

#     # qiuyk's modify,it maybe useful for the log
#     raw = cast(dict[str, Any], await wrapped.ainvoke({"query": query}))
#     # print(f"Raw search results for query '{query}': {raw}")
#     blocks: list[str] = [f"[Search Query]\n{query}\n\n[Search Results]\n"]

#     for r in raw.get("results", []):
#         title = " ".join(str(r.get("title") or "").split())
#         content = " ".join(str(r.get("content") or r.get("snippet") or "").split())
#         url = " ".join(str(r.get("url") or "").split())

#         block = (
#             "[Source]\n"
#             f"Title: {title}\n"
#             f"URL: {url}\n"
#             f"Content: {content}\n"
#         )

#         blocks.append(block)

#     final_text = "\n---\n".join(blocks)

#     return final_text

TOOLS: List[Callable[..., Any]] = [search]

