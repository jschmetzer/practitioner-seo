# API Keys

Practitioner SEO uses three external services. This document covers
where to get each key and what they cost.

---

## SerpAPI

**What it powers:** `get_serp` and `pillar_research` tools. SERP analysis,
AI Overview detection, People Also Ask extraction, Knowledge Panel checking,
and keyword expansion research.

**Cost:** Free tier includes 100 searches/month. Paid plans start at $50/month
for 5,000 searches. A single optimizer run uses 1 search. A full pillar
research run uses 3-8 searches depending on expansion depth.

**How to get a key:**

1. Go to https://serpapi.com
2. Create an account (free tier available)
3. Go to https://serpapi.com/manage-api-key
4. Copy your API key

**Add to config:**

```yaml
serpapi_key: "your-key-here"
```

Or: `export PRACTITIONER_SEO_SERPAPI_KEY="your-key-here"`

---

## PageSpeed Insights API

**What it powers:** `get_pagespeed` tool. Core Web Vitals assessment
(LCP, CLS, TBT/INP proxy), Lighthouse performance score, and optimization
opportunities.

**Cost:** Free. Google provides this API at no cost. There is a quota
(approximately 400 queries per day per key), but it is generous for
individual site optimization.

**How to get a key:**

1. Go to https://console.cloud.google.com
2. Select or create a project
3. Go to https://console.cloud.google.com/apis/library
4. Search for "PageSpeed Insights API" and enable it
5. Go to https://console.cloud.google.com/apis/credentials
6. Click "Create Credentials" then "API key"
7. Copy the key

Optional but recommended: restrict the key to only the PageSpeed Insights API
under "API restrictions" in the key settings.

**Add to config:**

```yaml
pagespeed_key: "your-key-here"
```

Or: `export PRACTITIONER_SEO_PAGESPEED_KEY="your-key-here"`

---

## Google Search Console

**What it powers:** `get_gsc_data` and `keyword_rankings` tools. Per-URL
query performance, site-wide keyword data, position tracking, CTR analysis.

**Cost:** Free. Google Search Console is a free service.

**Setup:** GSC requires OAuth or service account authentication rather than
a simple API key. See `GSC_SETUP.md` for the full walkthrough.

---

## Which keys do I need?

You can start with zero keys. The skills degrade gracefully, and each tool
returns a setup hint when its dependency is missing.

**Recommended order of setup:**

1. **SerpAPI** -- enables SERP analysis and keyword research, which power
   the most actionable sections of all three skills
2. **GSC** -- enables query-level performance data, which drives the
   optimizer's diagnostic and the strategist's gap analysis
3. **PageSpeed** -- enables Core Web Vitals assessment; less critical for
   content-focused sites but important if you suspect performance issues

---

## Verifying your keys

After adding keys to your config, you can verify them by asking Claude
to run a simple tool call:

> Run get_serp for "test query"

If the key is valid, you'll get SERP data back. If not, you'll get a
structured error with a setup hint.
