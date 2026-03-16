"""PageSpeed Insights API integration.

Returns mobile lab data: performance score, LCP, CLS, TBT, FCP,
Speed Index, LCP element, and top Lighthouse opportunities.
"""

from __future__ import annotations

from typing import Any

import httpx


PSI_API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


async def get_pagespeed(
    url: str,
    api_key: str,
) -> dict[str, Any]:
    """Run PageSpeed Insights analysis on a URL.

    Args:
        url: The URL to analyze.
        api_key: PageSpeed Insights API key (free from Google Cloud Console).

    Returns:
        Structured performance data with metrics, thresholds, and opportunities.
    """
    params = {
        "url": url,
        "key": api_key,
        "strategy": "mobile",
        "category": "performance",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(PSI_API, params=params)

        if response.status_code == 429:
            return {
                "error": "quota_exceeded",
                "message": "PageSpeed Insights API quota exhausted.",
                "manual_url": (
                    f"https://pagespeed.web.dev/analysis"
                    f"?url={url}&form_factor=mobile"
                ),
            }

        response.raise_for_status()

    data = response.json()

    # Extract Lighthouse results
    lighthouse = data.get("lighthouseResult", {})
    categories = lighthouse.get("categories", {})
    audits = lighthouse.get("audits", {})

    # Performance score
    perf = categories.get("performance", {})
    performance_score = round((perf.get("score", 0) or 0) * 100)

    # Core metrics
    def _metric(audit_id: str) -> dict[str, Any]:
        audit = audits.get(audit_id, {})
        return {
            "value": audit.get("displayValue", ""),
            "score": audit.get("score"),
            "numeric_value": audit.get("numericValue"),
        }

    lcp = _metric("largest-contentful-paint")
    cls_metric = _metric("cumulative-layout-shift")
    tbt = _metric("total-blocking-time")
    fcp = _metric("first-contentful-paint")
    speed_index = _metric("speed-index")

    # LCP element
    lcp_element_audit = audits.get("largest-contentful-paint-element", {})
    lcp_element = ""
    items = lcp_element_audit.get("details", {}).get("items", [])
    if items:
        node = items[0].get("node", {})
        lcp_element = node.get("snippet", node.get("nodeLabel", ""))

    # Top opportunities (sorted by estimated savings)
    opportunities = []
    for audit_id, audit in audits.items():
        details = audit.get("details", {})
        if details.get("type") == "opportunity":
            savings = details.get("overallSavingsMs", 0)
            if savings and savings > 0:
                opportunities.append({
                    "title": audit.get("title", audit_id),
                    "savings_ms": round(savings),
                    "description": audit.get("description", ""),
                })

    opportunities.sort(key=lambda x: x["savings_ms"], reverse=True)

    return {
        "url": url,
        "performance_score": performance_score,
        "metrics": {
            "lcp": lcp,
            "cls": cls_metric,
            "tbt": tbt,
            "fcp": fcp,
            "speed_index": speed_index,
        },
        "lcp_element": lcp_element,
        "opportunities": opportunities[:5],
    }
