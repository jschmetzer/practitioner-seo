# Page Optimizer -- Execution Protocol

## What this skill does

Given a URL from `{SITE_CONFIG.site.domain}`, this skill:

1. Fetches and analyzes the target page (with cross-referenced structural data
   and CMS-specific schema conflict checks)
2. Pulls GSC performance data automatically
3. Runs PageSpeed Insights (mobile lab data) for Core Web Vitals assessment
4. Queries SerpAPI for SERP intent, competitors, AI Overview, PAA, and
   Knowledge Panel
5. Attempts to fetch top competitor pages (with graceful fallback)
6. Audits internal links in both directions
7. Assesses freshness, NavBoost engagement signals, and image alt text
8. Produces a complete, copy-ready optimization plan

**Required input:** A URL from `{SITE_CONFIG.site.domain}`
**Optional:** A specific keyword override (if the slug doesn't reflect the
true target keyword)
**GSC, SERP, and competitor data are pulled automatically**

**Methodology reference:** `SEO_METHODOLOGY.md` contains the evidence base
for every recommendation this protocol produces. This protocol tells you
what to do; the methodology tells you why.


## Content system files (read at runtime)

Before running the optimizer, read:

- `{SITE_CONFIG.context.site_context_file}` -- internal link catalog; the
  canonical list of what pages exist on the site
- `{SITE_CONFIG.context.formatting_rules_file}` -- niche-specific formatting
  rules (if present)

These files are ground truth. Do not reference pages not in the site context
file.


## Tool reference

All tools are on the `seo-suite` MCP server. If a tool is unavailable, follow
the graceful degradation rules at the end of this protocol.

| Tool                        | Purpose                                          |
|-----------------------------|--------------------------------------------------|
| `seo-suite:fetch_page`      | Structured SEO extraction (title, meta, H1, headings, schema, internal links, images, word count, intro) |
| `seo-suite:scrape_url`      | Raw scraper (all headings, all links with protocol/anchor, full text, OG tags) |
| `seo-suite:get_gsc_data`    | Per-URL GSC data (queries, positions, impressions, CTR) |
| `seo-suite:get_serp`        | SERP results, AI Overview, PAA, Knowledge Panel   |
| `seo-suite:get_pagespeed`   | PageSpeed Insights mobile lab data                |
| `seo-suite:fetch_page`      | Also used for competitor page analysis             |
| `seo-suite:content_brief`   | Competitor heading structure extraction            |


## Execution protocol


### Step 1: Fetch the target page -- two tools, cross-referenced

Run both tools on the target URL:

**Tool 1:** `seo-suite:fetch_page` -- returns structured SEO data: inferred
keyword from slug, title, meta, H1, headings, schema, internal links, images
missing alt, word count, intro text.

**Tool 2:** `seo-suite:scrape_url` -- returns raw data for headings and links,
catching inline formatting issues that fetch_page may normalize. Also returns
OG tags for image identification.

**Cross-reference specifically for:**

- **Heading text discrepancies** -- if the two tools return different text for
  the same heading, do not assume a page bug. Raw scrapers strip HTML tags and
  collapse whitespace inconsistently, producing false concatenation (e.g.,
  `"theBestProducts"` from `the <em>Best</em> Products`). Before flagging any
  heading discrepancy, fetch the rendered page source via `web_fetch` and
  inspect the actual HTML. Only flag a concatenation bug if the raw HTML
  confirms missing spaces around the inline tag. Discrepancies that exist only
  in scrape_url output are scraper artifacts -- do not report them.

- **Schema presence and types** -- verify schema blocks are present and note
  their types.

- **CMS schema conflicts** -- check for CMS-specific schema issues:
  {{#if SITE_CONFIG.cms_quirks.schema_array_nesting}}
  If `json_ld` contains an array nested inside a `@graph` structure, the page
  has the schema array-nesting bug common to
  `{SITE_CONFIG.cms_quirks.schema_array_nesting.plugin}`. Flag explicitly with
  the fix: use separate `<script type="application/ld+json">` tags, each
  containing a single JSON object, never an array wrapper.
  {{/if}}

- **`dateModified`** -- record the exact date from schema. If more than 6
  months old, flag for freshness assessment in Step 6.

**From these two tools, extract and record:**

- Inferred keyword (from slug -- this IS the target keyword unless overridden)
- Title tag (exact text + character count)
- Meta description (exact text + character count, or "none found")
- H1 (exact text, noting any confirmed concatenation issue)
- All H2s and H3s in document order
- First 150 words of body text (intro hook approach)
- Existing schema types present
- `dateModified` from schema (for freshness check)
- Internal links (anchor text + destination)
- Images missing alt text (list src URLs, not just count)
- Estimated word count
- Page type (see classification below)
- Whether page has a TOC, jump links, or other navigation aids

**Page type classification:**

- **Reader guide** -- "reading order", "guide", "how to", "where to start" in
  slug or H1
- **Craft/expertise article** -- "writing", "how I", "craft", expertise topic
  in slug
- **Author/bio page** -- root domain or `/about/` slug
- **Blog/news post** -- date in slug, news/announcement content
- **List/ranking page** -- "best", "top", "ranked" in slug
- **Product/review page** -- product name, "review", "comparison" in slug


### Step 2: Pull GSC data

Call `seo-suite:get_gsc_data` with the target URL and
`{SITE_CONFIG.site.gsc_property}`, 90-day lookback.

Returns: aggregate clicks, impressions, avg CTR, avg position; top 25 queries
by clicks with per-query metrics.

**Interpret using the CTR benchmark framework from SEO_METHODOLOGY.md:**

| Situation                              | Root cause                    | Primary fix                        |
|----------------------------------------|-------------------------------|------------------------------------|
| Position 1--10, CTR below expected     | Title/meta underperformance   | Rewrite title + meta               |
| Position 11--30, high impressions      | Ranking problem, page relevant | Content depth + authority          |
| Position 30+, any impressions          | Ranking + likely intent gap   | Content overhaul or keyword pivot  |
| Position 1--10, good CTR, low clicks   | Low search volume             | Target additional related queries  |
| Low impressions across all queries     | Not matching query space      | Keyword strategy problem           |

**Identify from GSC data:**

- The single highest-impression query that isn't converting -- usually the
  biggest opportunity
- Queries at positions 11--15 (just off page 1) -- nearest-term ranking
  opportunities
- Queries at positions 40+ with any impressions -- likely content/intent
  mismatch; flag for caveat section
- Whether the inferred keyword from slug appears in top GSC queries -- if not,
  flag slug/targeting misalignment
- **Topical authority gaps:** Queries at positions 20--50 that are clearly
  adjacent topics -- these are new dedicated page candidates, not on-page fixes.
  List them separately as "Supporting content opportunities."
- **Branded query check:** Does `{SITE_CONFIG.author.name}` or
  `{SITE_CONFIG.site.domain}` appear in the GSC data? If yes, note branded
  search demand as a healthy signal. If not visible, note as unable to confirm
  from this page's GSC data alone.


### Step 2.5: Core Web Vitals -- PageSpeed Insights (mobile lab data)

Call `seo-suite:get_pagespeed` with the target URL.

**If the tool returns a 429 or quota error:** There is no automated fallback.
Do all three of the following:
1. Note in Section F: "PageSpeed data unavailable -- API quota exhausted."
2. Skip all CWV items in Section G Tier 1. Do not fabricate scores.
3. Provide the manual URL:
   `https://pagespeed.web.dev/analysis?url=[TARGET_URL_ENCODED]&form_factor=mobile`

Do not retry. Do not attempt alternative tools.

**What to extract and record:**

- Performance score (0--100)
- LCP value (ms)
- CLS value
- TBT value (ms) -- lab proxy for INP
- FCP value
- Speed Index value
- LCP element (node label or snippet)
- Top 3 Lighthouse opportunities with estimated ms savings

**Threshold assessment -- flag each metric per SEO_METHODOLOGY.md thresholds.**
Pages with LCP > 2,300ms get precautionary amber (Dec 2025 update signal)
even though they pass the official 2,500ms threshold.


### Step 3: SERP analysis

Call `seo-suite:get_serp` with the inferred keyword.

**Extract and record:**

- **Intent type:** Informational / Navigational / Commercial / Transactional
- **Content type Google rewards:** List? Guide? Forum thread? Author page? Wiki? Product page?
- **Who ranks positions 1--10:** Note structural competitors from
  `{SITE_CONFIG.competitive_landscape.structural_competitors}` that appear.
  These have advantages that optimization cannot overcome.
- **AI Overview:** Present or absent. If present: what it says, whether
  `{SITE_CONFIG.site.domain}` is cited, all cited sources listed.
- **People Also Ask:** List all PAA questions -- these are H2/FAQ candidates.
- **Knowledge Panel:** Present or absent. If present for a branded query,
  author entity is confirmed. If absent, flag as entity gap.

**Intent alignment verdict:** Does the target page's content TYPE match what
Google is rewarding? If the SERP shows forum threads at positions 1--3 and
the target page is an authored list, note the partial mismatch and its ceiling
implications.

**AIO citation analysis:** If an AIO is present and
`{SITE_CONFIG.site.domain}` is NOT cited, examine the cited sources
structurally. What patterns do they share? Identify the 1--2 most actionable
structural changes that would increase citation likelihood.

**Title rewrite probability:** Based on the SERP, what is Google displaying
for the target page? If Google is already rewriting the title, note what it's
using -- this is the strongest signal of what Google wants the title to be.


### Step 4: Competitor page analysis

For the top 3 organic results that are NOT forums, social platforms, or sites
that block scrapers, call `seo-suite:fetch_page` on each URL.

**If a competitor returns a 403/blocked error:** Use SERP snippet data (title,
displayed URL, meta description) from Step 3. Note which competitors were
blocked. For Reddit and Facebook specifically -- do not attempt to fetch; use
snippet only.

For each successfully fetched competitor, record:
- Title and H1
- All H2s (topic coverage map)
- First 150 words (intro approach)
- Schema types present
- Approximate word count
- Any unique structural element (comparison table, calculator, TOC, interactive tool)
- Whether it has navigation aids for long content

Build the **topic gap table** comparing competitor H2 coverage against the
target page's H2s. Topics covered by 2+ competitors but absent from the
target page = priority gaps.


### Step 5: Internal link audit (two directions)

#### Part A: Inbound internal links (links pointing TO the target page)

**Scope: check every page on the site.**

The only way to know whether a page links to the target is to scrape it.
Inferring from topic overlap produces false negatives.

**Tool: `seo-suite:scrape_url` -- mandatory for all link checking.**

Do NOT use `fetch_page` for link auditing. `fetch_page` may silently drop
links using non-canonical protocols (e.g., `http://` instead of `https://`).
`scrape_url` returns all links regardless of protocol.

**How to execute:**

1. Load `{SITE_CONFIG.context.site_context_file}`. Extract every URL.
2. Call `seo-suite:scrape_url` on every URL in the catalog.
3. For each page scraped, search the `links` array for any entry whose `url`
   field contains the target page's slug.
4. Record the result for every page.

Do not skip pages because they seem topically unrelated.

**For each page, record:**
- Link to target present? (yes / no / could not verify)
- If yes: exact URL used (protocol?), exact anchor text
- If no: is there a natural editorial insertion point? Suggest anchor text and
  a one-sentence insertion.

**Flag these issues (in order of SEO impact):**

- **HTTP instead of HTTPS** -- link exists but uses wrong protocol, leaking
  PageRank through redirect on every crawl
- **Weak or generic anchor** -- "here", "this", single words. Propose
  descriptive replacement.
- **Missing link** -- no link exists; recommend adding one with specific
  anchor and sentence.
- **Nav-only links** -- page links to target only through site navigation, not
  body copy. Nav links carry significantly less weight than contextual body
  links.
{{#if SITE_CONFIG.cms_quirks.inline_tag_concatenation}}
- **Concatenation bug in anchor text** -- anchor reads as concatenated words
  due to inline tag spacing issue. Fix: add spaces around inline-formatted
  words in the CMS link text.
{{/if}}

**Build an inbound link table:**

| Source page (slug) | Links to target? | Protocol | Anchor text | Issue | Fix |
|---|---|---|---|---|---|
| /example/ | Yes | https | "descriptive anchor" | None | -- |
| /example-2/ | Yes | http | "ConcatenatedText" | HTTP leak + anchor bug | Fix protocol; fix spacing |
| /example-3/ | No | -- | -- | Missing | Add in [section] with anchor "[text]" |

Every page in the site context file must appear in this table. "Could not
verify" is acceptable; omitting a page is not.


#### Part B: Outbound internal links (links pointing FROM the target page)

**Use the `seo-suite:scrape_url` result from Step 1** (already fetched -- no
additional call needed).

From the `links` array, separate into:
- **Nav links** -- URLs matching site nav destinations, anchors matching nav labels
- **Internal body links** -- `is_internal: true`, not nav
- **External/affiliate links** -- `is_internal: false`

**Quantity and distribution:**
- How many unique internal destinations does the page link to (excluding nav)?
- If zero body-copy internal links: flag as critical isolation.

**Anchor text quality audit:**
- List every internal link with empty, single-word, or generic anchor text
- For each, propose a descriptive replacement

**Missing high-value outbound links:**
- Based on the page's topic and the site's content cluster, are there obvious
  pages it should link to but doesn't?
- Check whether it links to related posts visible from GSC data in Step 2.

{{#if SITE_CONFIG.content.commercial_model == "affiliate"}}
**Affiliate link audit:**
- List all affiliate link codes used on the page
- Cross-reference against `{SITE_CONFIG.context.commercial_list_file}`
- Flag any codes NOT in the current list as legacy links needing verification
- Flag empty-anchor image links wrapping affiliate images -- these pass no
  anchor signal
{{/if}}


### Step 6: Additional signals audit

#### A: Freshness assessment

From Step 1, the page's `dateModified` is recorded. Apply the freshness
framework from SEO_METHODOLOGY.md.

When recommending an update, identify specific content that is genuinely stale
-- not "update the page" but "add [specific new information], remove [specific
outdated claim]." After a genuine content update, updating `dateModified` is
the correct signal.

#### B: NavBoost engagement audit

Assess structural engagement signals:

- **Intro hook quality:** Does the first 150 words immediately answer the
  implied query, or does it lead with preamble? Flag if the target keyword's
  core answer does not appear within the first 2 sentences.
- **Scannability:** If word count > 2,000, does the page have a TOC or jump
  links?
- **Answer placement:** For informational queries, does the direct answer
  appear immediately after the relevant H2, or at the end of a long section?
- **CTA placement:** Are CTAs placed before the reader has received value?

#### C: Image alt text assessment

For each image missing alt text (from Step 1):
- Infer content from: src URL filename, surrounding page context, OG image tag
- Write a specific, descriptive alt text recommendation
- Format: `<img src="[url]" alt="[proposed alt text]">`
- If content cannot be inferred, note "requires visual inspection"

#### D: Title rewrite probability

Assess using data from Steps 1 and 3, applying the framework from
SEO_METHODOLOGY.md (HIGH / MEDIUM / LOW risk with specific criteria).

If risk is HIGH or MEDIUM, the proposed title in Section B should match the H1
as closely as possible, since H1 is Google's primary rewrite input.


### Step 7: Build the optimization plan

Output the following sections in order, with no preamble before Section A.


#### SECTION A: Diagnostic Summary

One paragraph (4--6 sentences):
- Current GSC performance in plain numbers
- Intent alignment verdict with one-sentence explanation
- The single most important finding
- Realistic ceiling given the competitive landscape


#### SECTION B: Ready-to-implement copy

**Title tag**
- Current: [exact text] ([N] chars)
- Proposed: [new title, 30--55 chars preferred, keyword-forward, matches H1]
- Character count: [N]
- Rewrite risk: [LOW / MEDIUM / HIGH] -- [rationale]

**Meta description**
- Current: [exact text or "none found"] ([N] chars)
- Proposed: [new meta, 140--155 chars, benefit-led]
- Character count: [N]
- Rationale: [1--2 sentences]

**H1**
- Current: [exact text]
- Proposed: [new H1 aligned with title]
- Fix required: [plain text change / spacing fix / other]

**Intro hook rewrite** (if current intro does not answer the query within the
first two sentences)
- Current approach: [describe]
- Proposed replacement copy: [write actual 50--100 word replacement]
- Rationale: [NavBoost signal this improves]


#### SECTION C: Schema markup

Determine schema type from page classification in Step 1. Check existing
schema first -- note what's present, output only additions or corrections.

{{#if SITE_CONFIG.cms_quirks.schema_array_nesting}}
If Step 1 detected the schema array-nesting conflict, flag it before providing
schema. Instruct: use separate `<script>` tags, each containing a single JSON
object, never an array wrapper.
{{/if}}

Author entity reference:
```json
"author": {
  "@type": "Person",
  "@id": "{SITE_CONFIG.author.entity_id}",
  "name": "{SITE_CONFIG.author.name}"
}
```

Produce ready-to-paste JSON-LD. If FAQ schema is included, add:
> FAQPage schema will NOT produce rich results (restricted to government/health
> sites since August 2023). Its value is AI citation eligibility and content
> structure signaling.


#### SECTION D: Content gap analysis

**Gap table** (only rows where at least one competitor covers the topic):

| Topic / H2 | Comp 1 | Comp 2 | Comp 3 | This page | Priority |
|------------|--------|--------|--------|-----------|---------|
| [topic] | Yes/No/blocked | Yes/No/blocked | Yes/No/blocked | Yes/No | High/Med/Low |

Note blocked competitors in headers.

**Add these H2 sections** (priority order, with recommended text):
1. `[H2 text]` -- [query it targets] -- [~word count] -- [rationale]

**Reframe these existing H2s** (for snippet / PAA alignment):
- Current: [H2]
- Proposed: [H2 as question matching PAA or GSC query]

**PAA integration:** For each PAA question not covered by an existing H2 or
FAQ entry, recommend adding as either H2 or FAQ entry.

**Supporting content opportunities** (from Step 2 GSC analysis):
Queries at positions 20--50 better served by a new page than by expanding
this one. Format: `[query] (position [N], [N] impressions) -> suggested page: "[title]"`


#### SECTION E: Internal link findings

**Inbound link table** (from Step 5 Part A -- exhaustive):

| Source page | Links here? | Protocol | Anchor | Issue | Fix |
|---|---|---|---|---|---|
| [slug] | Yes/No | http/https/-- | "[text]" | [issue] | [fix] |

**Outbound link summary** (from Step 5 Part B):
- Contextual body links: [N] to [N] unique destinations
- Links with weak/empty anchor: [N] -- [list each with fix]
- Missing high-value outbound links: [list]


#### SECTION F: Additional signal findings

**Core Web Vitals (PageSpeed Insights -- mobile lab data):**

Performance score: [N]/100

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| LCP | [value] | < 2,500ms (caution > 2,300ms) | PASS / CAUTION / FAIL |
| CLS | [value] | < 0.10 | PASS / FAIL |
| TBT (INP proxy) | [value] | < 200ms | PASS / FAIL |
| FCP | [value] | < 1,800ms | PASS / FAIL |

LCP element: [node label or snippet]

Top Lighthouse Opportunities:
1. [Opportunity] -- ~[N]ms savings
2. [Opportunity] -- ~[N]ms savings
3. [Opportunity] -- ~[N]ms savings

**Freshness:** `dateModified` = [date] ([N] days ago) -- [Fresh / Monitor / Stale / Critical]

**NavBoost engagement flags:**
- Intro hook: [Pass / Flag]
- Long-page navigation: [N/A / TOC present / TOC missing]
- Answer placement: [Pass / Flag]
- CTA placement: [Pass / Flag]

**Image alt text:** [N] images missing alt
- [For each: proposed alt text or "requires visual inspection"]

**Title rewrite probability:** [LOW / MEDIUM / HIGH] -- [rationale]

**Knowledge Panel:** [Present / Absent / Not checked] -- [details]


#### SECTION G: Tiered action checklist

**Tier 1 -- This week (high impact, low effort)**
- [ ] [Specific action with exact copy or instruction]
- [ ] [If CWV fails or Lighthouse opportunity > 500ms: specific fix]
- [ ] Submit URL for reindex in Search Console after all Tier 1 changes

**Tier 2 -- This month (high impact, higher effort)**
- [ ] [Content additions with specific H2 text and ~word target]
- [ ] [Intro rewrite if applicable]
- [ ] [Freshness update if stale -- specific content to add]
- [ ] Image alt text fixes: [list each]
- [ ] Internal links -- inbound fixes: [list each from Part A]
- [ ] Internal links -- outbound fixes: [list each from Part B]
{{#if SITE_CONFIG.content.commercial_model == "affiliate"}}
- [ ] Affiliate link audit: [list findings]
{{/if}}

**Tier 3 -- Strategic (AI citation + long-term authority)**
- [ ] [AIO citation play -- specific structural change]
- [ ] [Entity/schema strengthening if Knowledge Panel absent]
- [ ] [Supporting content: new page title + target query]
- [ ] Monitor AIO citation status after content changes


#### SECTION H: One honest caveat

**Always include this section.** If no caveats exist, say so explicitly.
Otherwise state clearly if any apply:

- SERP dominated by content types optimization cannot displace -- name the
  ceiling position
- Realistic ceiling is position 3--5, not 1, due to structural advantages
- Keyword has insufficient search volume to justify significant effort
- Slug/page targets the wrong keyword (GSC shows zero impressions for
  slug-inferred keyword)
- Strategic misalignment (wrong content type for query intent) that tactics
  cannot fix
- Freshness so stale that recovery requires full content refresh

Do not soften this section. A clear ceiling is more useful than false optimism.


---

## Graceful degradation

| Tool unavailable      | Fallback                                                              |
|-----------------------|-----------------------------------------------------------------------|
| GSC tools             | Skip GSC sections; note "GSC not configured"; recommend setup         |
| SerpAPI tools         | Fall back to `web_search` (reduced output: no AIO details, no PAA, no structured competitor list) |
| PageSpeed             | Provide manual URL; skip CWV items in action checklist                |
| Scraper tools         | Fall back to `web_fetch`; note reduced link audit accuracy            |


---

## Output format rules

- Start immediately with Section A -- no preamble
- All proposed copy in Sections B and C must be copy-paste ready
- Section D gap table must include blocked competitor notation
- Section E tables must be based on actual tool results, not assumptions
- Section F must report actual `dateModified` date and actual images missing
  alt -- no approximations
- Section G must be a true executable checklist -- every item actionable
  without further clarification
- Section H is mandatory in every output
- Do not pad -- every sentence should contain a decision or a fact
