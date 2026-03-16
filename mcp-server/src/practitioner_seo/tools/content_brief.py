"""Competitor heading structure extraction for content briefs.

Scrapes 3-4 competitor pages and extracts H1-H3 structure, word count,
and identifies must-cover topics (headings present on 2+ competitors).
"""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


async def content_brief(
    urls: list[str],
    user_agent: str = "PractitionerSEO/0.1",
) -> dict[str, Any]:
    """Extract heading structure from competitor pages.

    Args:
        urls: List of competitor URLs to analyze (3-4 recommended).
        user_agent: User-Agent header for requests.

    Returns:
        Per-competitor heading structure, word counts, and must-cover topics.
    """
    competitors = []
    all_h2_topics: Counter[str] = Counter()

    for url in urls:
        try:
            result = await _fetch_competitor(url, user_agent)
            competitors.append(result)
            for h in result.get("headings", []):
                if h["level"] == "h2":
                    normalized = _normalize_heading(h["text"])
                    if normalized:
                        all_h2_topics[normalized] += 1
        except Exception as e:
            competitors.append({
                "url": url,
                "domain": urlparse(url).netloc,
                "error": str(e),
                "headings": [],
                "word_count": 0,
            })

    must_cover = [
        {"topic": topic, "competitor_count": count}
        for topic, count in all_h2_topics.most_common()
        if count >= 2
    ]

    return {
        "competitors": competitors,
        "must_cover_topics": must_cover,
        "total_competitors_analyzed": len(
            [c for c in competitors if "error" not in c]
        ),
        "total_competitors_blocked": len(
            [c for c in competitors if "error" in c]
        ),
    }


async def _fetch_competitor(url: str, user_agent: str) -> dict[str, Any]:
    """Fetch and analyze a single competitor page."""
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=30.0,
        headers={"User-Agent": user_agent},
    ) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    domain = urlparse(url).netloc

    h1_tag = soup.find("h1")
    h1 = h1_tag.get_text(strip=True) if h1_tag else ""

    headings = []
    for tag in soup.find_all(re.compile(r"^h[1-3]$")):
        headings.append({
            "level": tag.name,
            "text": tag.get_text(strip=True),
        })

    body = soup.find("body")
    body_text = body.get_text(separator=" ", strip=True) if body else ""
    word_count = len(body_text.split())

    words = body_text.split()
    intro = " ".join(words[:150])

    schema_types = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and "@type" in data:
                schema_types.append(data["@type"])
        except (json.JSONDecodeError, TypeError):
            pass

    return {
        "url": url,
        "domain": domain,
        "h1": h1,
        "headings": headings,
        "word_count": word_count,
        "intro_approach": intro[:200],
        "schema_types": schema_types,
    }


def _normalize_heading(text: str) -> str:
    """Normalize a heading for topic comparison."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
