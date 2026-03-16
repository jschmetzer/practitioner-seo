"""Keyword expansion and pillar research via SerpAPI.

Maps the full keyword landscape around a seed term by running multiple
SerpAPI queries: the seed term, its PAA expansions, and People Also
Search expansions. Returns stack-ranked keywords by weighted frequency
(how many distinct expansion paths surfaced each keyword).
"""

from __future__ import annotations

from collections import Counter
from typing import Any

import httpx

SERPAPI_BASE = "https://serpapi.com/search.json"


async def pillar_research(
    keyword: str,
    serpapi_key: str,
    expansion_depth: str = "standard",
    gl: str = "us",
    hl: str = "en",
) -> dict[str, Any]:
    """Run keyword expansion research around a seed keyword.

    Args:
        keyword: The seed keyword to expand.
        serpapi_key: SerpAPI API key.
        expansion_depth: "standard" (faster, fewer expansions) or
                        "full" (more thorough, more API calls).
        gl: Google country code.
        hl: Google language code.

    Returns:
        Dictionary with organic results, PAA, related searches,
        stack-ranked keywords, and extended keywords.
    """
    all_keywords: Counter[str] = Counter()
    all_paa: list[str] = []
    all_related: list[str] = []

    # Phase 1: Seed query
    seed_data = await _search(keyword, serpapi_key, gl, hl)

    organic_results = []
    for result in seed_data.get("organic_results", [])[:10]:
        organic_results.append({
            "position": result.get("position"),
            "title": result.get("title", ""),
            "url": result.get("link", ""),
        })

    # Extract PAA questions
    for item in seed_data.get("related_questions", []):
        q = item.get("question", "")
        if q:
            all_paa.append(q)
            # Count words from PAA as keyword signals
            for word_group in _extract_keyword_phrases(q, keyword):
                all_keywords[word_group] += 1

    # Extract related searches
    for item in seed_data.get("related_searches", []):
        q = item.get("query", "")
        if q:
            all_related.append(q)
            all_keywords[q.lower()] += 1

    # Phase 2: Expand on top related searches
    max_expansions = 5 if expansion_depth == "full" else 2
    expansion_queries = all_related[:max_expansions]

    for eq in expansion_queries:
        try:
            exp_data = await _search(eq, serpapi_key, gl, hl)

            for item in exp_data.get("related_questions", []):
                q = item.get("question", "")
                if q and q not in all_paa:
                    all_paa.append(q)
                    for word_group in _extract_keyword_phrases(q, keyword):
                        all_keywords[word_group] += 1

            for item in exp_data.get("related_searches", []):
                q = item.get("query", "")
                if q and q not in all_related:
                    all_related.append(q)
                    all_keywords[q.lower()] += 1
        except Exception:
            # Non-fatal: we still have the seed data
            continue

    # Phase 3: If full depth, expand on PAA questions too
    if expansion_depth == "full":
        paa_queries = all_paa[:3]
        for pq in paa_queries:
            try:
                paa_data = await _search(pq, serpapi_key, gl, hl)
                for item in paa_data.get("related_searches", []):
                    q = item.get("query", "")
                    if q:
                        all_keywords[q.lower()] += 1
                        if q not in all_related:
                            all_related.append(q)
            except Exception:
                continue

    # Build stack-ranked keywords
    stack_ranked = []
    for kw, count in all_keywords.most_common(50):
        stack_ranked.append({
            "keyword": kw,
            "raw_count": count,
            "score": count,
        })

    # Extended keywords: those with raw_count >= 2
    extended = [k for k in stack_ranked if k["raw_count"] >= 2]

    return {
        "seed_keyword": keyword,
        "expansion_depth": expansion_depth,
        "organic_results": organic_results,
        "people_also_ask": all_paa,
        "related_searches": all_related,
        "stack_ranked_keywords": stack_ranked,
        "extended_keywords": extended,
        "total_unique_keywords": len(stack_ranked),
    }


async def _search(query: str, api_key: str, gl: str, hl: str) -> dict:
    """Run a single SerpAPI search."""
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "gl": gl,
        "hl": hl,
        "num": 10,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(SERPAPI_BASE, params=params)
        response.raise_for_status()
    return response.json()


def _extract_keyword_phrases(question: str, seed: str) -> list[str]:
    """Extract meaningful keyword phrases from a PAA question."""
    # Normalize
    q = question.lower().strip("?").strip()
    # Remove common question words
    for prefix in ("what is", "what are", "how to", "how do", "why is",
                   "why are", "where to", "when to", "can you", "should i",
                   "is it", "does"):
        if q.startswith(prefix):
            q = q[len(prefix):].strip()
    if q and len(q) > 3:
        return [q]
    return []
