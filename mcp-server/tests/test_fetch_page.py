"""Tests for the fetch_page tool."""

import pytest
import respx
import httpx

from practitioner_seo.tools.fetch_page import fetch_page


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_extracts_title(sample_html):
    """fetch_page should extract the title tag text."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    assert result["title"] == "Best Hand Planes for Every Skill Level (2026)"
    assert result["title_length"] == len(result["title"])


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_extracts_meta_description(sample_html):
    """fetch_page should extract the meta description."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    assert "Sarah Chen" in result["meta_description"]
    assert result["meta_description_length"] > 0


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_extracts_h1(sample_html):
    """fetch_page should extract the H1."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    assert result["h1"] == "Best Hand Planes for Every Skill Level"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_extracts_headings_in_order(sample_html):
    """fetch_page should return all headings in document order."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    levels = [h["level"] for h in result["headings"]]
    assert levels == ["h1", "h2", "h2", "h2", "h3"]


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_extracts_json_ld(sample_html):
    """fetch_page should parse JSON-LD schema blocks."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    assert len(result["json_ld"]) == 1
    assert result["json_ld"][0]["@type"] == "Article"
    assert "Article" in result["schema_types"]


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_extracts_date_modified(sample_html):
    """fetch_page should find dateModified from schema."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    assert result["date_modified"] == "2026-01-15"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_finds_images_missing_alt(sample_html):
    """fetch_page should list images with empty or missing alt text."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    # block.jpg has alt="" and jointer.jpg has no alt attribute
    assert len(result["images_missing_alt"]) == 2


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_infers_keyword_from_slug(sample_html):
    """fetch_page should infer the target keyword from the URL slug."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    assert result["inferred_keyword"] == "best hand planes"


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_extracts_internal_links(sample_html):
    """fetch_page should find internal links with anchor text."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    anchors = [link["anchor_text"] for link in result["internal_links"]]
    assert "sharpening guide" in anchors
    assert "Home" in anchors


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_counts_words(sample_html):
    """fetch_page should return a word count for the body."""
    url = "https://benchcraftworkshop.com/best-hand-planes/"
    respx.get(url).mock(return_value=httpx.Response(200, text=sample_html))

    result = await fetch_page(url)

    assert result["word_count"] > 50
