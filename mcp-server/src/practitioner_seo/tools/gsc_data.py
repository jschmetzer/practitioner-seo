"""Per-URL Google Search Console data retrieval.

Fetches queries, positions, impressions, and CTR for a specific URL
over a configurable lookback period.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Optional

from googleapiclient.discovery import build

from practitioner_seo.auth.oauth import get_oauth_credentials
from practitioner_seo.auth.service_account import get_service_account_credentials
from practitioner_seo.config import Config


async def get_gsc_data(
    url: str,
    site_url: str,
    config: Config,
    days: int = 90,
) -> dict[str, Any]:
    """Fetch GSC performance data for a specific URL.

    Args:
        url: The page URL to get data for.
        site_url: GSC property identifier (e.g., "sc-domain:example.com").
        config: Server configuration with GSC auth settings.
        days: Number of days to look back (default 90).

    Returns:
        Dictionary with aggregate metrics and per-query breakdown.
    """
    creds = _get_credentials(config)
    if creds is None:
        return {"error": "GSC not configured", "queries": []}

    service = build("searchconsole", "v1", credentials=creds)

    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=days)

    request_body = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": ["query"],
        "dimensionFilterGroups": [
            {
                "filters": [
                    {
                        "dimension": "page",
                        "operator": "equals",
                        "expression": url,
                    }
                ]
            }
        ],
        "rowLimit": 25,
        "startRow": 0,
    }

    response = (
        service.searchanalytics()
        .query(siteUrl=site_url, body=request_body)
        .execute()
    )

    rows = response.get("rows", [])

    total_clicks = sum(r.get("clicks", 0) for r in rows)
    total_impressions = sum(r.get("impressions", 0) for r in rows)
    avg_ctr = total_clicks / total_impressions if total_impressions > 0 else 0
    avg_position = (
        sum(r.get("position", 0) * r.get("impressions", 0) for r in rows)
        / total_impressions
        if total_impressions > 0
        else 0
    )

    queries = []
    for row in rows:
        queries.append({
            "query": row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0), 4),
            "position": round(row.get("position", 0), 1),
        })

    return {
        "url": url,
        "site_url": site_url,
        "period_days": days,
        "aggregate": {
            "clicks": total_clicks,
            "impressions": total_impressions,
            "ctr": round(avg_ctr, 4),
            "position": round(avg_position, 1),
        },
        "queries": queries,
    }


def _get_credentials(config: Config) -> Optional[Any]:
    """Get GSC credentials using the configured auth method."""
    if config.gsc.auth_method == "service_account":
        return get_service_account_credentials(config.gsc)
    else:
        return get_oauth_credentials(config.gsc)
