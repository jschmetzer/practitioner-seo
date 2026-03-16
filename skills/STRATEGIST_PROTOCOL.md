# Content Strategist -- Execution Protocol

## What this skill does

Three distinct modes depending on input:

**Mode 1 -- Site-wide gap audit**
Input: none (or "what are we missing" / "what should I write next")
Output: prioritized new-content brief list organized by opportunity cluster

**Mode 2 -- Cluster diagnostic**
Input: a URL + seed keyword (e.g., `/best-hand-planes/` + "best hand planes")
Output: gap analysis of the cluster -- what queries it owns, what it's losing,
what supporting posts exist, what's missing

**Mode 3 -- Competitor topic audit**
Input: a keyword
Output: topic coverage matrix comparing site pages against AIO-cited and
top-ranking competitor pages

When input is ambiguous (just a keyword with no clear mode), infer Mode 3.
When input is just a URL, infer Mode 2 and derive the seed keyword from the
slug.

**Methodology reference:** `SEO_METHODOLOGY.md` contains the evidence base.
This protocol references it rather than duplicating it.


## Content system files (read at runtime)

Before running any mode, read:

- `{SITE_CONFIG.context.site_context_file}` -- internal link catalog and
  content inventory; the canonical list of what pages exist
{{#if SITE_CONFIG.context.commercial_list_file}}
- `{SITE_CONFIG.context.commercial_list_file}` -- commercial URLs; used in
  Mode 2 to verify commercial section coverage
{{/if}}

Do not skip these files. The site context file is ground truth for what pages
exist. Do not reference pages not in that file.


## Tool reference

All tools are on the `seo-suite` MCP server.

| Tool                            | Purpose                                              |
|---------------------------------|------------------------------------------------------|
| `seo-suite:keyword_rankings`    | Site-wide GSC keyword data (up to 50 rows per call)  |
| `seo-suite:get_gsc_data`        | Per-URL GSC data (queries, positions, CTR)            |
| `seo-suite:get_serp`            | SERP results, AI Overview, PAA, Knowledge Panel       |
| `seo-suite:pillar_research`     | Keyword expansion (organic, PAA, PAS, stack-ranked)   |
| `seo-suite:content_brief`       | Competitor heading structure extraction                |
| `seo-suite:fetch_page`          | Target page analysis (headings, links, FAQ, schema)   |

**GSC property format:** Always call GSC tools with
`site_url: "{SITE_CONFIG.site.gsc_property}"`. Using the wrong property format
will return errors.

**`pillar_research` expansion depth:**
- Use `expansion_depth: "full"` for Mode 2 and Mode 3 (depth matters)
- Use `expansion_depth: "standard"` for Mode 1 (speed matters across
  multiple seeds)

**`keyword_rankings` vs. `get_gsc_data`:**
- `keyword_rankings` returns site-wide aggregate data with no per-URL breakdown
- `get_gsc_data` returns data for a specific URL
- The two tools are complementary: use `keyword_rankings` for demand signals,
  use `get_gsc_data` when you need to attribute a query to a specific URL


## Key strategic principles

These are elaborated in SEO_METHODOLOGY.md. Summary for strategy work:

**Topical authority clusters:** Missing supporting content is often the
proximate cause of a pillar page underperforming. A site with one pillar and
no supporting posts loses cluster authority to a site with five shallower
pages covering the same territory.

**GSC positions 21--50 as opportunity signals:** Google has identified the site
as relevant but won't promote it. For 21--30, one well-targeted post can move
to page 1 -- but only if the content type matches what Google rewards. For
30--50, verify intent alignment first.

**AIO citation for ranked lists:** For "best [X]" queries, AIOs almost always
cite peer-recommendation sources rather than single-author ranked lists. This
is structural. Factual supporting content earns AIO citations more reliably
than ranked-list format.

**Cannibalization:** Sites with multiple posts targeting near-identical queries
split relevance signals. Every cluster diagnostic must surface cannibalization.
Before recommending new content, check whether an existing post already covers
the topic. If it does, strengthen the existing post instead.

**Branded search as prerequisite:** Content activity only compounds into
ranking gains after branded search demand is established. If branded search
volume is near-zero, content gap recommendations must include a caveat.


---

## Mode 1: Site-wide gap audit

### When to use

No URL and no specific keyword provided. User asks "what should I write next"
or "what are we missing" or "give me a content plan."


### Execution protocol

**Step 1: Inventory existing content**

Read `{SITE_CONFIG.context.site_context_file}`. Extract every URL and title.
This is the complete content inventory. Count posts by apparent topic cluster
based on slug and title patterns.

**Step 2: Pull site-wide GSC data**

Call `seo-suite:keyword_rankings` with
`site_url: "{SITE_CONFIG.site.gsc_property}"` and `days: 90`.

Extract:
- All queries by impressions (descending)
- Queries at position 21--50 -- unserved demand signals
- Queries at position 1--10 with zero clicks -- possible title/meta mismatch
  or SERP feature displacement
- Top 3 clusters by query volume

For per-page attribution, call `seo-suite:get_gsc_data` on specific pages.

**Step 3: Run pillar research on top 3 seed keywords**

Identify the three highest-traffic clusters from GSC data (or from slug
frequency if GSC is unavailable). Run `seo-suite:pillar_research` with
`expansion_depth: "standard"` on each.

Extract: `stack_ranked_keywords` not currently matched by any existing page.
Higher `raw_count` = stronger demand signal.

**Step 4: Classify gaps**

For each gap keyword:
- Existing page targeting this? (check site context file)
- Cannibalizing an existing page, or genuinely unserved?
- Pillar-level topic or post-level topic?
- What page type would Google expect? (check SERP via `get_serp` if needed)

**Step 5: Prioritize**

Score each gap on three axes:
1. **Demand signal** -- raw_count from pillar research
2. **Competitive ceiling** -- SERP dominated by forums (hard) or thin content (easier)?
3. **Cluster fit** -- reinforces an existing pillar the site has invested in?

Tier 1 (build now), Tier 2 (this quarter), Tier 3 (low urgency or
structurally difficult).


### Output format -- Mode 1

```
## SITE-WIDE CONTENT GAP AUDIT

### Coverage inventory
[Table: Cluster | Existing pages | Gap signal | Notes]

### GSC opportunity signals (positions 21--50)
[List: Query | Current position | Current URL | Recommended action]

### Content brief list -- Tier 1 (build now)
For each:
- Proposed title and slug
- Target keyword
- Page type (pillar / post)
- Cluster it reinforces
- Why it ranks: what SERP format wins here
- Estimated difficulty (low / medium / high)
- Commercial section: [include / omit] with placement

### Content brief list -- Tier 2 (this quarter)
[Same format]

### Content brief list -- Tier 3 (low urgency)
[Same format]

### Cannibalization flags
[Existing pages targeting same query -- recommend: consolidate / differentiate / redirect]

### GSC anomalies
[Queries at position 1--10 with zero clicks; clusters with high impressions
and zero CTR; branded query status; any other signal worth investigating]
```


---

## Mode 2: Cluster diagnostic

### When to use

User provides a URL and/or a seed keyword. Also triggers for "is [page]
complete" or "what's missing from [page]" or "diagnose this cluster."


### Execution protocol

**Step 1: Fetch the target page**

Call `seo-suite:fetch_page` on the target URL.
Extract: H1, all H2s, word count, internal links (href + anchor), existing
FAQ questions, schema types.

Also call `seo-suite:get_gsc_data` on the same URL.
Extract: all queries with impressions, positions, CTR. Sort by impressions
descending. Classify: OWNED (1--10), COMPETITIVE (11--20), VISIBLE/UNSERVED
(21--50), DARK (51+).

**Step 2: Map SERP and AIO**

Call `seo-suite:get_serp` with the seed keyword.
Extract:
- SERP content type
- AIO present or absent
- AIO cited sources (list all domains)
- Whether `{SITE_CONFIG.site.domain}` is cited
- Competitor positions 1--5

**Step 3: Run full pillar research**

Call `seo-suite:pillar_research` with `expansion_depth: "full"`.
Extract from `stack_ranked_keywords`: keywords with score >= 3.
Extract from `extended_keywords`: keywords with raw_count >= 2.

**Step 4: Coverage gap analysis**

For every keyword from Step 3:
a) Does the target page answer this query? (check H2s and FAQ)
b) Does any other site page target this? (check site context file)
c) If (a) = no and (b) = no: gap -- no coverage anywhere
d) If (a) = no and (b) = yes: existing supporting post; check if it links
   to the pillar
e) If (a) = yes and (b) = yes: potential cannibalization

**Step 5: Supporting post audit**

From the site context file, identify all posts topically related to the
cluster (by slug pattern and title). For each:
- Does it link to the pillar page?
- Does the pillar link to it?
- What query does it target?
- Is it genuinely differentiated, or cannibalizing?

**Step 6: Competitor topic audit**

Call `seo-suite:content_brief` with the top 3 non-forum competitor URLs from
Step 2. Extract: must-cover topics (present on 2+ pages). Map each against
the target page's H2 structure. Flag missing must-cover topics.

Note: some competitor URLs will be blocked or return minimal data. Always
include at least one non-forum URL. Fall back to SERP snippet heading
structure if all URLs fail.

**Step 7: AIO citation gap**

For each AIO-cited source from Step 2:
- What format is it?
- What topics does it cover that the target page doesn't?
- What structural feature makes Google trust it?

This is often the most actionable section.


### Output format -- Mode 2

```
## CLUSTER DIAGNOSTIC: [URL]
Target keyword: [keyword]
Page word count: [N] | FAQ entries: [N] | Internal links out: [N]


### Section A: Query ownership
[Table: Query | Position | Impressions | Status]
Status: OWNED (1--10) | COMPETITIVE (11--20) | VISIBLE/UNSERVED (21--50) | DARK (51+)

Key finding: [1--2 sentence summary]


### Section B: Keyword demand universe
[Keywords with score >= 3 or raw_count >= 2]
[Table: Keyword | Score | On-page coverage | Supporting post | Gap?]
Coverage: COVERED | PARTIAL | MISSING


### Section C: Supporting post network
[Table: Post URL | Target query | Links to pillar? | Pillar links to it? | Cannibalization risk?]


### Section D: Content gaps -- recommended new posts
For each gap with no supporting post:
- Proposed post: [title + slug]
- Target keyword
- Query intent
- Priority: HIGH / MEDIUM / LOW
- Rationale
- Commercial section: [include / omit]


### Section E: On-page gaps -- recommended additions to existing page
For each missing must-cover topic:
- Missing topic
- Recommended H2 or FAQ entry text
- Why it matters (demand signal or competitor coverage)


### Section F: AIO citation analysis
AIO present: [YES / NO]
{SITE_CONFIG.site.domain} cited: [YES / NO]

[If not cited:]
Currently cited sources: [list each with format and trust reason]
Gap analysis: [specific structural features cited sources have that this page lacks]
Recommended actions: [specific, actionable suggestions]


### Section G: Cannibalization map
[Table: Query | Page A | Page B | Recommendation: consolidate / differentiate / redirect]


### Section H: Priority action list
Tier 1 -- Do now:
[ ] [Specific action]

Tier 2 -- This month:
[ ] [Specific action]

Tier 3 -- New content:
[ ] [Brief for new post]


### Section I: One honest ceiling
[State the realistic ranking ceiling plainly. If the SERP is structurally
dominated by community formats, say so. If AIO citation is the more
achievable target than position 1, say so explicitly.]
```


---

## Mode 3: Competitor topic audit

### When to use

User provides a keyword with no URL. They want to know what the competition
covers that the site doesn't.


### Execution protocol

**Step 1: SERP and AIO**

Call `seo-suite:get_serp`. Extract: top 5 URLs, AIO cited sources, PAA.
Classify each result: forum/community, wiki/list, editorial/guide, video.

**AIO framing:** If an AIO is present, the cited sources are the primary
competition, not the organic top 5. For informational queries, AIOs reduce
position-1 CTR by ~58% and zero-click searches represent ~69% of all queries.
Being cited in the AIO is often more commercially valuable than organic
position 1. Build the topic coverage matrix against AIO-cited sources first;
include organic top 5 as secondary competition.

**Step 2: Content brief from competitors**

Call `seo-suite:content_brief` with the top 3--4 non-forum competitors.
Extract: heading structure, must-cover topics.

**Step 3: Site inventory check**

From `{SITE_CONFIG.context.site_context_file}`, identify every page that could
address the keyword or any must-cover topic. Note coverage status: covered,
partial, absent.

**Step 4: Pillar research**

Call `seo-suite:pillar_research` with `expansion_depth: "standard"`.
Cross-reference stack-ranked keywords against must-cover topics and existing
pages.


### Output format -- Mode 3

```
## COMPETITOR TOPIC AUDIT: "[keyword]"

SERP landscape:
[2--3 sentences on content format dominating this SERP and ceiling implications]

AIO: [present / absent] | {SITE_CONFIG.site.domain} cited: [yes / no]


### Topic coverage matrix
[Table: Topic | Competitor A | Competitor B | Competitor C | {SITE_CONFIG.site.domain}]
Values: YES / PARTIAL / NO


### Gap summary
Topics on 2+ competitors with NO coverage:
[List with recommendation: new post vs. add to existing page]

Topics partially covered:
[List with URL and specific gap]


### Recommended content
[Table: Proposed page | Target keyword | Type | Priority | Commercial section]


### Realistic ceiling
[Honest assessment. State explicitly: if AIO is present, organic position 1
CTR is reduced ~58% and zero-click searches represent ~69% of queries. State
which target (organic rank vs. AIO citation) is more achievable and
commercially valuable for this keyword.]
```


---

## Cross-mode rules

**Never invent page URLs.** All internal page references must come from the
site context file. If a page that should exist doesn't appear there, flag it
as a gap, not an existing asset.

**Cannibalization check is mandatory before recommending new content.** Check
whether an existing post already covers the topic. If it does, recommend
strengthening the existing post, not adding another.

**AIO citation analysis is mandatory in Modes 2 and 3.** It is often the most
actionable output.

**Honest ceiling section is mandatory in all modes.** State the structural
ceiling plainly, especially when the SERP is dominated by community formats
the site cannot displace.

**Commercial section specification is mandatory in all content briefs.**
Specify whether to include or omit, and placement, per
`{SITE_CONFIG.content.commercial_model}` and
`{SITE_CONFIG.content.commercial_section_placement}`.


---

## Graceful degradation

| Tool unavailable      | Fallback                                                              |
|-----------------------|-----------------------------------------------------------------------|
| GSC tools             | Skip GSC sections; note "GSC not configured"; recommend setup         |
| SerpAPI tools         | Fall back to `web_search` (reduced output)                            |
| Scraper/fetch tools   | Fall back to `web_fetch`; note reduced accuracy                       |


---

## Output format rules

- Start immediately with the relevant section -- no preamble
- Every gap recommendation must specify: keyword, page type, rationale,
  commercial section handling
- Every cannibalization flag must include a specific recommendation
  (consolidate / differentiate / redirect)
- AIO citation analysis is mandatory in Mode 2 and Mode 3
- Honest ceiling section is mandatory -- state structural limitations plainly
- Do not pad -- every sentence should contain a decision or a fact
