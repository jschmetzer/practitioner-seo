"""Practitioner SEO MCP Server.

Single unified MCP server exposing 8 SEO tools. Each tool checks API key
availability at call time and returns structured errors with setup hints
when dependencies are missing.

Entry point: `practitioner-seo` console script (runs stdio transport).
"""

from __future__ import annotations

import json
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from practitioner_seo.config import Config, load_config, setup_hint
from practitioner_seo.tools import (
    fetch_page as fetch_page_mod,
    scrape_url as scrape_url_mod,
    gsc_data as gsc_data_mod,
    keyword_rankings as keyword_rankings_mod,
    serp as serp_mod,
    pagespeed as pagespeed_mod,
    pillar_research as pillar_research_mod,
    content_brief as content_brief_mod,
)

mcp = FastMCP("Practitioner SEO")

# Global config -- loaded once at startup
_config: Optional[Config] = None


def _get_config() -> Config:
    """Lazy-load config on first tool call."""
    global _config
    if _config is None:
        _config = load_config()
    return _config


# ---------------------------------------------------------------------------
# Tool 1: fetch_page
# ---------------------------------------------------------------------------

@mcp.tool()
async def fetch_page(url: str) -> str:
    """Fetch a URL and extract structured SEO data.

    Returns: title, meta description, H1, all headings, JSON-LD schema,
    internal links, images missing alt text, word count, and intro text.
    Infers the target keyword from the URL slug.

    No API key required.
    """
    config = _get_config()
    try:
        result = await fetch_page_mod.fetch_page(url, config.user_agent)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url})


# ---------------------------------------------------------------------------
# Tool 2: scrape_url
# ---------------------------------------------------------------------------

@mcp.tool()
async def scrape_url(url: str) -> str:
    """Scrape a URL and return raw structural data.

    Returns: all headings with raw HTML, all links with protocol and anchor
    text, full body text, Open Graph tags, and canonical URL. This tool
    returns ALL links regardless of protocol (http vs https), making it
    mandatory for internal link audits.

    No API key required.
    """
    config = _get_config()
    try:
        result = await scrape_url_mod.scrape_url(url, config.user_agent)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url})


# ---------------------------------------------------------------------------
# Tool 3: get_gsc_data
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_gsc_data(
    url: str,
    site_url: str,
    days: int = 90,
) -> str:
    """Fetch Google Search Console performance data for a specific URL.

    Returns: aggregate clicks, impressions, CTR, position; and top 25
    queries with per-query metrics. Use this when you need to know which
    queries a specific page ranks for.

    Args:
        url: The page URL to get data for.
        site_url: GSC property identifier (e.g., "sc-domain:example.com").
        days: Number of days to look back (default 90).

    Requires: GSC OAuth or service account credentials.
    """
    config = _get_config()
    if not config.has_gsc:
        return json.dumps({
            "error": "GSC not configured",
            "setup_hint": setup_hint("get_gsc_data", "gsc"),
        })
    try:
        result = await gsc_data_mod.get_gsc_data(url, site_url, config, days)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url})


# ---------------------------------------------------------------------------
# Tool 4: keyword_rankings
# ---------------------------------------------------------------------------

@mcp.tool()
async def keyword_rankings(
    site_url: str,
    days: int = 90,
    keyword: str = "",
) -> str:
    """Fetch site-wide keyword ranking data from Google Search Console.

    Returns up to 50 rows of keyword data sorted by impressions. Use this
    for site-wide demand signals. Complements get_gsc_data which is per-URL.

    Args:
        site_url: GSC property identifier (e.g., "sc-domain:example.com").
        days: Number of days to look back (default 90).
        keyword: Optional filter -- only return queries containing this string.

    Requires: GSC OAuth or service account credentials.
    """
    config = _get_config()
    if not config.has_gsc:
        return json.dumps({
            "error": "GSC not configured",
            "setup_hint": setup_hint("keyword_rankings", "gsc"),
        })
    try:
        kw_filter = keyword if keyword else None
        result = await keyword_rankings_mod.keyword_rankings(
            site_url, config, days, kw_filter
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "site_url": site_url})


# ---------------------------------------------------------------------------
# Tool 5: get_serp
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_serp(keyword: str) -> str:
    """Query Google SERP for a keyword via SerpAPI.

    Returns: organic results (positions 1-10), AI Overview presence and
    cited sources, People Also Ask questions, Knowledge Panel data, and
    related searches.

    Args:
        keyword: The search query to analyze.

    Requires: SerpAPI key.
    """
    config = _get_config()
    if not config.has_serpapi:
        return json.dumps({
            "error": "SerpAPI not configured",
            "setup_hint": setup_hint("get_serp", "serpapi_key"),
        })
    try:
        result = await serp_mod.get_serp(
            keyword, config.serpapi_key, config.user_agent  # type: ignore
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "keyword": keyword})


# ---------------------------------------------------------------------------
# Tool 6: get_pagespeed
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_pagespeed(url: str) -> str:
    """Run PageSpeed Insights analysis on a URL (mobile, performance).

    Returns: performance score, LCP, CLS, TBT (INP proxy), FCP, Speed
    Index, LCP element identification, and top Lighthouse opportunities
    with estimated ms savings.

    Args:
        url: The URL to analyze.

    Requires: PageSpeed Insights API key (free from Google Cloud Console).
    """
    config = _get_config()
    if not config.has_pagespeed:
        return json.dumps({
            "error": "PageSpeed Insights not configured",
            "setup_hint": setup_hint("get_pagespeed", "pagespeed_key"),
        })
    try:
        result = await pagespeed_mod.get_pagespeed(
            url, config.pagespeed_key  # type: ignore
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "url": url})


# ---------------------------------------------------------------------------
# Tool 7: pillar_research
# ---------------------------------------------------------------------------

@mcp.tool()
async def pillar_research(
    keyword: str,
    expansion_depth: str = "standard",
) -> str:
    """Map the keyword landscape around a seed keyword.

    Runs multiple SerpAPI queries to build a demand map: the seed term,
    PAA expansions, and related search expansions. Returns stack-ranked
    keywords by weighted frequency (raw_count = how many distinct
    expansion paths surfaced that keyword; higher = stronger signal).

    Args:
        keyword: The seed keyword to expand.
        expansion_depth: "standard" (faster, 2 expansions) or "full"
                        (thorough, 5+ expansions).

    Requires: SerpAPI key.
    """
    config = _get_config()
    if not config.has_serpapi:
        return json.dumps({
            "error": "SerpAPI not configured",
            "setup_hint": setup_hint("pillar_research", "serpapi_key"),
        })
    try:
        result = await pillar_research_mod.pillar_research(
            keyword, config.serpapi_key, expansion_depth  # type: ignore
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e), "keyword": keyword})


# ---------------------------------------------------------------------------
# Tool 8: content_brief
# ---------------------------------------------------------------------------

@mcp.tool()
async def content_brief(urls: str) -> str:
    """Extract heading structure from competitor pages for content briefs.

    Scrapes competitor pages and returns H1-H3 structure, word counts, intro
    approach, and must-cover topics (headings present on 2+ competitors).

    Args:
        urls: Comma-separated list of competitor URLs to analyze (3-4
              recommended). Example: "https://example.com/page1,https://example.com/page2"

    No API key required.
    """
    config = _get_config()
    url_list = [u.strip() for u in urls.split(",") if u.strip()]
    if not url_list:
        return json.dumps({"error": "No URLs provided"})
    try:
        result = await content_brief_mod.content_brief(
            url_list, config.user_agent
        )
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server with stdio transport (for Claude Desktop)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
