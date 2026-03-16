"""SERP analysis via SerpAPI.

Returns organic results, AI Overview presence and cited sources,
People Also Ask questions, and Knowledge Panel data for a keyword.
"""

from __future__ import annotations

from typing import Any

import httpx


SERPAPI_BASE = "https://serpapi.com/search.json"


async def get_serp(
    keyword: str,
    serpapi_key: str,
    user_agent: str = "PractitionerSEO/0.1",
    gl: str = "us",
    hl: str = "en",
) -> dict[str, Any]:
    """Query SerpAPI for SERP data on a keyword.

    Args:
        keyword: The search query to analyze.
        serpapi_key: SerpAPI API key.
        user_agent: User-Agent for the request.
        gl: Google country code (default "us").
        hl: Google language code (default "en").

    Returns:
        Structured SERP data including organic results, AIO, PAA, and KP.
    """
    params = {
        "q": keyword,
        "api_key": serpapi_key,
        "engine": "google",
        "gl": gl,
        "hl": hl,
        "num": 10,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(SERPAPI_BASE, params=params)
        response.raise_for_status()

    data = response.json()

    # Organic results
    organic = []
    for result in data.get("organic_results", [])[:10]:
        organic.append({
            "position": result.get("position"),
            "title": result.get("title", ""),
            "url": result.get("link", ""),
            "snippet": result.get("snippet", ""),
            "displayed_url": result.get("displayed_link", ""),
        })

    # AI Overview
    ai_overview = {"present": False, "text": "", "cited_sources": []}
    # SerpAPI returns AI overviews under various keys depending on the query
    for key in ("ai_overview", "answer_box"):
        if key in data:
            block = data[key]
            ai_overview["present"] = True
            ai_overview["text"] = block.get("snippet", block.get("answer", ""))
            # Extract cited sources if available
            sources = block.get("sources", block.get("cited_sources", []))
            if isinstance(sources, list):
                for src in sources:
                    if isinstance(src, dict):
                        ai_overview["cited_sources"].append({
                            "title": src.get("title", ""),
                            "url": src.get("link", src.get("url", "")),
                            "domain": src.get("domain", src.get("source", "")),
                        })
            break

    # People Also Ask
    paa = []
    for item in data.get("related_questions", []):
        paa.append({
            "question": item.get("question", ""),
            "snippet": item.get("snippet", ""),
            "source": item.get("link", ""),
        })

    # Knowledge Panel
    knowledge_panel = {"present": False}
    if "knowledge_graph" in data:
        kg = data["knowledge_graph"]
        knowledge_panel = {
            "present": True,
            "title": kg.get("title", ""),
            "type": kg.get("type", ""),
            "description": kg.get("description", ""),
            "source": kg.get("source", {}).get("link", ""),
        }

    # Related searches
    related_searches = [
        item.get("query", "")
        for item in data.get("related_searches", [])
    ]

    return {
        "keyword": keyword,
        "organic_results": organic,
        "ai_overview": ai_overview,
        "people_also_ask": paa,
        "knowledge_panel": knowledge_panel,
        "related_searches": related_searches,
    }
