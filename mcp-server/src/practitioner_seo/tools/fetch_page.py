"""Structured SEO page extraction.

Fetches a URL and returns structured SEO data: title, meta description,
H1, all headings, schema/JSON-LD, internal links, images missing alt,
word count, and intro text.
"""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup, Tag


async def fetch_page(url: str, user_agent: str = "PractitionerSEO/0.1") -> dict[str, Any]:
    """Fetch a URL and extract structured SEO data.

    Args:
        url: The URL to fetch and analyze.
        user_agent: User-Agent header for the request.

    Returns:
        Dictionary containing structured SEO data.
    """
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=30.0,
        headers={"User-Agent": user_agent},
    ) as client:
        response = await client.get(url)
        response.raise_for_status()

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    base_domain = urlparse(url).netloc

    # Infer keyword from slug
    path = urlparse(url).path.strip("/")
    slug = path.split("/")[-1] if path else ""
    inferred_keyword = slug.replace("-", " ") if slug else ""

    # Title tag
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Meta description
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = ""
    if meta_desc_tag and isinstance(meta_desc_tag, Tag):
        meta_description = meta_desc_tag.get("content", "")

    # H1
    h1_tag = soup.find("h1")
    h1 = h1_tag.get_text(strip=True) if h1_tag else ""

    # All headings in document order
    headings = []
    for tag in soup.find_all(re.compile(r"^h[1-6]$")):
        headings.append({
            "level": tag.name,
            "text": tag.get_text(strip=True),
        })

    # JSON-LD schema blocks
    json_ld = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            json_ld.append(data)
        except (json.JSONDecodeError, TypeError):
            pass

    # Schema types present
    schema_types = set()
    for block in json_ld:
        if isinstance(block, dict):
            _extract_types(block, schema_types)
        elif isinstance(block, list):
            for item in block:
                if isinstance(item, dict):
                    _extract_types(item, schema_types)

    # dateModified from schema
    date_modified = None
    for block in json_ld:
        date_modified = _find_date_modified(block)
        if date_modified:
            break

    # Internal links
    internal_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)
        if parsed.netloc == base_domain or parsed.netloc == "":
            anchor = a_tag.get_text(strip=True)
            internal_links.append({
                "url": full_url,
                "anchor_text": anchor,
            })

    # Images missing alt
    images_missing_alt = []
    for img in soup.find_all("img"):
        alt = img.get("alt", None)
        if alt is None or alt.strip() == "":
            src = img.get("src", "")
            if src:
                images_missing_alt.append(urljoin(url, src))

    # Word count (body text only)
    body = soup.find("body")
    body_text = body.get_text(separator=" ", strip=True) if body else ""
    word_count = len(body_text.split())

    # Intro text (first 150 words)
    words = body_text.split()
    intro_text = " ".join(words[:150]) if words else ""

    return {
        "url": url,
        "inferred_keyword": inferred_keyword,
        "title": title,
        "title_length": len(title),
        "meta_description": meta_description,
        "meta_description_length": len(meta_description),
        "h1": h1,
        "headings": headings,
        "json_ld": json_ld,
        "schema_types": sorted(schema_types),
        "date_modified": date_modified,
        "internal_links": internal_links,
        "images_missing_alt": images_missing_alt,
        "word_count": word_count,
        "intro_text": intro_text,
    }


def _extract_types(obj: dict, types: set) -> None:
    """Recursively extract @type values from a JSON-LD object."""
    if "@type" in obj:
        t = obj["@type"]
        if isinstance(t, list):
            types.update(t)
        else:
            types.add(t)
    if "@graph" in obj and isinstance(obj["@graph"], list):
        for item in obj["@graph"]:
            if isinstance(item, dict):
                _extract_types(item, types)


def _find_date_modified(obj: Any) -> str | None:
    """Recursively search for dateModified in a JSON-LD structure."""
    if isinstance(obj, dict):
        if "dateModified" in obj:
            return str(obj["dateModified"])
        for v in obj.values():
            result = _find_date_modified(v)
            if result:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = _find_date_modified(item)
            if result:
                return result
    return None
