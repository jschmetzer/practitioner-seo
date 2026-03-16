"""Site-wide GSC keyword rankings.

Returns up to 50 rows of keyword data across the entire site property,
optionally filtered by a keyword string. Complements get_gsc_data which
is per-URL; this tool gives a site-wide demand picture.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Optional

from googleapiclient.discovery import build

from practitioner_seo.auth.oauth import get_oauth_credentials
from practitioner_seo.auth.service_account import get_service_account_credentials
from practitioner_seo.config import Config


async def keyword_rankings(
    site_url: str,
    config: Config,
    days: int = 90,
    keyword: Optional[str] = None,
) -> dict[str, Any]:
    """Fetch site-wide keyword ranking data from GSC.

    Args:
        site_url: GSC property identifier (e.g., "sc-domain:example.com").
        config: Server configuration with GSC auth settings.
        days: Number of days to look back (default 90).
        keyword: Optional keyword filter -- only return queries containing
                 this string.

    Returns:
        Dictionary with up to 50 keyword rows sorted by impressions desc.
    """
    creds = _get_credentials(config)
    if creds is None:
        return {"error": "GSC not configured", "keywords": []}

    service = build("searchconsole", "v1", credentials=creds)

    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=days)

    request_body: dict[str, Any] = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": ["query"],
        "rowLimit": 50,
        "startRow": 0,
    }

    if keyword:
        request_body["dimensionFilterGroups"] = [
            {
                "filters": [
                    {
                        "dimension": "query",
                        "operator": "contains",
                        "expression": keyword,
                    }
                ]
            }
        ]

    response = (
        service.searchanalytics()
        .query(siteUrl=site_url, body=request_body)
        .execute()
    )

    rows = response.get("rows", [])

    keywords = []
    for row in rows:
        keywords.append({
            "query": row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0), 4),
            "position": round(row.get("position", 0), 1),
        })

    # Sort by impressions descending
    keywords.sort(key=lambda x: x["impressions"], reverse=True)

    return {
        "site_url": site_url,
        "period_days": days,
        "keyword_filter": keyword,
        "total_rows": len(keywords),
        "keywords": keywords,
    }


def _get_credentials(config: Config) -> Optional[Any]:
    """Get GSC credentials using the configured auth method."""
    if config.gsc.auth_method == "service_account":
        return get_service_account_credentials(config.gsc)
    else:
        return get_oauth_credentials(config.gsc)
