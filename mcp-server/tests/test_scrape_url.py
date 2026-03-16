"""Tests for the scrape_url tool."""

import pytest
import respx
import httpx

from practitioner_seo.tools.scrape_url import scrape_url


@pytest.mark.asyncio
@respx.mock
async def test_scrape_url_returns_all_links_with_protocol(sample_html):
    """scrape_url must return links with their protocol (http vs https)."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await scrape_url(url)

    http_links = [
        link for link in result["links"]
        if link["protocol"] == "http" and link["is_internal"]
    ]
    assert len(http_links) >= 1, (
        "scrape_url must detect HTTP internal links -- this is the critical "
        "difference from fetch_page for link auditing"
    )


@pytest.mark.asyncio
@respx.mock
async def test_scrape_url_returns_anchor_text(sample_html):
    """scrape_url should return anchor text for every link."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await scrape_url(url)

    sharpening_links = [
        link for link in result["links"]
        if "sharpening" in link["url"]
    ]
    assert len(sharpening_links) >= 1
    assert sharpening_links[0]["anchor_text"] == "sharpening guide"


@pytest.mark.asyncio
@respx.mock
async def test_scrape_url_marks_internal_external(sample_html):
    """scrape_url should correctly classify internal vs external links."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await scrape_url(url)

    external = [link for link in result["links"] if not link["is_internal"]]
    internal = [link for link in result["links"] if link["is_internal"]]

    assert any("amzn.to" in link["url"] for link in external)
    assert len(internal) >= 2


@pytest.mark.asyncio
@respx.mock
async def test_scrape_url_extracts_og_tags(sample_html):
    """scrape_url should extract Open Graph tags."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await scrape_url(url)

    assert "og:title" in result["og_tags"]
    assert result["og_tags"]["og:title"] == "Best Hand Planes"


@pytest.mark.asyncio
@respx.mock
async def test_scrape_url_extracts_canonical(sample_html):
    """scrape_url should extract the canonical URL."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await scrape_url(url)

    assert result["canonical"] == "https://benchcraftworkshop.com/best-hand-planes/"


@pytest.mark.asyncio
@respx.mock
async def test_scrape_url_includes_heading_html(sample_html):
    """scrape_url should include raw HTML for headings (for cross-reference)."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await scrape_url(url)

    assert all("html" in h for h in result["headings"])
    h1_entry = result["headings"][0]
    assert "<h1>" in h1_entry["html"]
