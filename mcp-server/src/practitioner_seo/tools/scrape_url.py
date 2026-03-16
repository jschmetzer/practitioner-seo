"""Raw URL scraper for link auditing and heading analysis.

Returns all headings, all links with protocol and anchor text, full body
text, and Open Graph tags. This tool catches inline formatting issues that
fetch_page may normalize, and critically: it returns ALL links regardless
of protocol (http vs https), making it mandatory for link audits.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup, Tag


async def scrape_url(url: str, user_agent: str = "PractitionerSEO/0.1") -> dict[str, Any]:
    """Scrape a URL and return raw structural data.

    Args:
        url: The URL to scrape.
        user_agent: User-Agent header for the request.

    Returns:
        Dictionary with headings, links, text, and OG tags.
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

    # All headings with raw text (preserving whitespace artifacts for
    # cross-reference with fetch_page)
    headings = []
    for tag in soup.find_all(re.compile(r"^h[1-6]$")):
        headings.append({
            "level": tag.name,
            "text": tag.get_text(strip=True),
            "html": str(tag),
        })

    # All links with full detail
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)
        is_internal = (
            parsed.netloc == base_domain
            or parsed.netloc == ""
            or parsed.netloc == f"www.{base_domain}"
        )
        anchor = a_tag.get_text(strip=True)
        links.append({
            "url": full_url,
            "raw_href": href,
            "anchor_text": anchor,
            "is_internal": is_internal,
            "protocol": parsed.scheme,
        })

    # Full body text
    body = soup.find("body")
    body_text = body.get_text(separator=" ", strip=True) if body else ""

    # Open Graph tags
    og_tags = {}
    for meta in soup.find_all("meta"):
        if isinstance(meta, Tag):
            prop = meta.get("property", "")
            if isinstance(prop, str) and prop.startswith("og:"):
                og_tags[prop] = meta.get("content", "")

    # Canonical URL
    canonical_tag = soup.find("link", rel="canonical")
    canonical = ""
    if canonical_tag and isinstance(canonical_tag, Tag):
        canonical = canonical_tag.get("href", "")

    return {
        "url": url,
        "headings": headings,
        "links": links,
        "body_text": body_text,
        "word_count": len(body_text.split()),
        "og_tags": og_tags,
        "canonical": canonical,
    }
