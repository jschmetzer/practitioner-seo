"""Tests for the get_serp tool."""

import json

import pytest
import respx
import httpx

from practitioner_seo.tools.serp import get_serp


MOCK_SERPAPI_RESPONSE = {
    "organic_results": [
        {
            "position": 1,
            "title": "Best Hand Planes 2026 - Reddit",
            "link": "https://reddit.com/r/woodworking/best-hand-planes",
            "snippet": "Community recommendations for hand planes.",
            "displayed_link": "reddit.com",
        },
        {
            "position": 2,
            "title": "Hand Plane Buying Guide - Popular Woodworking",
            "link": "https://popularwoodworking.com/hand-planes",
            "snippet": "Expert reviews of hand planes.",
            "displayed_link": "popularwoodworking.com",
        },
    ],
    "related_questions": [
        {
            "question": "What is the best hand plane for beginners?",
            "snippet": "A No. 4 smoothing plane is the most versatile choice.",
            "link": "https://example.com/answer1",
        },
        {
            "question": "How much should I spend on a hand plane?",
            "snippet": "Quality hand planes range from $50 to $400.",
            "link": "https://example.com/answer2",
        },
    ],
    "related_searches": [
        {"query": "best hand plane for beginners"},
        {"query": "hand plane vs electric planer"},
    ],
    "knowledge_graph": {
        "title": "Hand plane",
        "type": "Tool",
        "description": "A hand plane is a tool for shaping wood.",
        "source": {"link": "https://en.wikipedia.org/wiki/Hand_plane"},
    },
}


@pytest.mark.asyncio
@respx.mock
async def test_get_serp_returns_organic_results():
    """get_serp should return structured organic results."""
    respx.get("https://serpapi.com/search.json").mock(
        return_value=httpx.Response(200, json=MOCK_SERPAPI_RESPONSE)
    )

    result = await get_serp("best hand planes", "fake-key")

    assert len(result["organic_results"]) == 2
    assert result["organic_results"][0]["position"] == 1
    assert "reddit.com" in result["organic_results"][0]["url"]


@pytest.mark.asyncio
@respx.mock
async def test_get_serp_returns_paa():
    """get_serp should extract People Also Ask questions."""
    respx.get("https://serpapi.com/search.json").mock(
        return_value=httpx.Response(200, json=MOCK_SERPAPI_RESPONSE)
    )

    result = await get_serp("best hand planes", "fake-key")

    assert len(result["people_also_ask"]) == 2
    assert "beginners" in result["people_also_ask"][0]["question"]


@pytest.mark.asyncio
@respx.mock
async def test_get_serp_returns_knowledge_panel():
    """get_serp should detect Knowledge Panel presence."""
    respx.get("https://serpapi.com/search.json").mock(
        return_value=httpx.Response(200, json=MOCK_SERPAPI_RESPONSE)
    )

    result = await get_serp("best hand planes", "fake-key")

    assert result["knowledge_panel"]["present"] is True
    assert result["knowledge_panel"]["title"] == "Hand plane"


@pytest.mark.asyncio
@respx.mock
async def test_get_serp_handles_no_knowledge_panel():
    """get_serp should handle missing Knowledge Panel gracefully."""
    response_no_kp = {k: v for k, v in MOCK_SERPAPI_RESPONSE.items()
                      if k != "knowledge_graph"}
    respx.get("https://serpapi.com/search.json").mock(
        return_value=httpx.Response(200, json=response_no_kp)
    )

    result = await get_serp("best hand planes", "fake-key")

    assert result["knowledge_panel"]["present"] is False


@pytest.mark.asyncio
@respx.mock
async def test_get_serp_returns_related_searches():
    """get_serp should return related searches."""
    respx.get("https://serpapi.com/search.json").mock(
        return_value=httpx.Response(200, json=MOCK_SERPAPI_RESPONSE)
    )

    result = await get_serp("best hand planes", "fake-key")

    assert "best hand plane for beginners" in result["related_searches"]
