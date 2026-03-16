# SEO Methodology -- Practitioner SEO

This is the evidence-based ranking model that all three Practitioner SEO skills
operate from. It is opinionated by design. Every claim cites a source or
describes the evidence that supports it. Advanced users can override specific
sections via `SITE_CONFIG.methodology_overrides`.

This document is a reference, not a checklist. The execution protocols
(Optimizer, Strategist, Writer) tell you what to do. This document tells you
why.

---

## What actually matters (confirmed 2024--2026)


### Search intent alignment

The prerequisite above all else. If the page's content type does not match what
Google is rewarding for the query, no amount of on-page optimization will fix
it. A how-to guide cannot rank where Google wants forum threads. A ranked list
cannot rank where Google wants a wiki article.

Diagnosis: compare the target page's format against positions 1--5 in the SERP.
If the SERP rewards a content type the page is not, this is a strategic
misalignment that tactics cannot solve.


### Semantic and entity coverage

Semantic coverage dominates on-page signals. The Surfer SEO 1M-page study
found that term coverage matters while raw text length optimizes to zero
weight. The operative unit is entities and topic coverage, not keyword density
or word count.

Use entity-based gap analysis (what named things, concepts, and subtopics do
competitors cover that the target page does not?) rather than keyword frequency
metrics.


### NavBoost and engagement signals

NavBoost is a confirmed ranking factor (Google API leak, May 2024 + DOJ
antitrust testimony, Oct 2024). Google tracks:

- **goodClicks** -- positive engagement signals
- **badClicks** -- pogo-sticking back to the SERP (negative)
- **lastLongestClicks** -- which result the user engaged with longest (positive)

Pogo-sticking is a direct negative signal. Dwell time is a direct positive
signal. The structural implication: pages must answer the query within the
first two sentences after the H1. Intro copy that leads with credentials,
history, or preamble before answering the question increases pogo-sticking.

Additional NavBoost-aligned practices:
- Pages over 2,000 words need a Table of Contents or jump links. Without
  navigation aids, readers on long pages are more likely to leave before
  scrolling to their answer.
- Direct answers should appear immediately after the relevant H2, not at the
  end of a long section.
- Calls to action belong after value delivery, not before it. Pre-value CTAs
  increase bounce rate.


### Freshness

Pages updated at least once per year gain an average of 4.6 positions (First
Page Sage, 2025). AI systems cite content that is 25.7% fresher than the
average organic result (Ahrefs, Dec 2025). Fake freshness (changing
`dateModified` without changing content) is actively penalized since the Dec
2025 core update.

**Default freshness framework:**

| Age since last update | Status   | Action                                    |
|-----------------------|----------|-------------------------------------------|
| < 90 days             | Fresh    | No action needed                          |
| 90--180 days          | Monitor  | Flag if content is time-sensitive          |
| 180--365 days         | Stale    | Recommend specific content update          |
| > 365 days            | Critical | Update urgently; likely losing freshness signal |

This framework is overridable in `SITE_CONFIG.freshness_thresholds` for niches
with different update cadences (news sites need tighter windows; evergreen
reference sites can tolerate longer intervals).

A genuine content update means adding, removing, or rewriting substantive
content -- not touching a date field. After a real update, changing
`dateModified` is the correct signal.


### Internal linking

"Super critical" per John Mueller (Google Search Relations, 2024).

Key principles:
- Contextual body links carry significantly more weight than navigation links.
  A page that links to the target only through site navigation is not
  effectively linked.
- Anchor text matters. Descriptive anchors beat generic ones ("here", "this",
  "read more").
- HTTP-to-HTTPS internal links leak a small amount of PageRank on every crawl
  through the redirect. Sites that migrated to HTTPS but still have internal
  links pointing to `http://` URLs should fix them.
- Bidirectional linking between pillar pages and supporting posts reinforces
  topical authority for both.


### E-E-A-T as structural infrastructure

E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) is not
decorative. It is not about author bio boxes -- SearchPilot A/B tested author
bios across a large sample and found zero ranking impact.

What does work:
- Schema infrastructure: Person entity with `sameAs` links to authoritative
  profiles, `knowsAbout` properties, consistent `@id` across pages
- Knowledge Panel presence for branded queries (confirms Google has established
  the author entity)
- Explicit credential prose where it adds information, not as a bio box
- Consistent author entity reference across all pages on the site

The entity infrastructure is what matters. Boilerplate author boxes do not
move rankings.


### AI Overview impact

AI Overviews (AIOs) reduce organic position-1 CTR by approximately 58%
(Ahrefs, 300K keywords, Dec 2025). Being cited in an AIO generates
approximately 35% more organic clicks than not being cited (Seer Interactive,
2025). Approximately 70% of AIO cited page sets rotate within 2--3 months
(Authoritas, 2025).

Zero-click searches now represent approximately 69% of all queries (Similarweb,
May 2025).

For informational queries, being cited in the AIO is often more commercially
valuable than organic position 1. This is especially true for niches where
Reddit or other community platforms hold structural position-1 advantages.

**AIO citation levers:**
- Structured Q&A content (FAQ blocks, question-format H2s with direct answers)
- Named entities (specific people, products, dates, measurements)
- Freshness (AI systems preferentially cite fresher content)
- Factual specificity (concrete claims with numbers, dates, and sources outperform general advice)

**AIO structural reality for ranked lists:** For "best [X]" queries, AIOs
almost always cite peer-recommendation sources (Reddit, Facebook groups,
forums) rather than single-author ranked lists. This is structural, not
fixable by optimization. Factual supporting content (specific guides, how-to
pages, comparison pages) earns AIO citations more reliably than the
ranked-list format.


### Branded search as prerequisite signal

The Dec 2025 core update confirmed that content activity only compounds into
ranking gains after branded search demand is established. Branded queries
(searching for the author name or site name) showing in GSC data is a healthy
signal. Near-zero branded search volume means new content investment may not
produce ranking gains until brand demand is present.

This is a causal gate, not a vanity metric. Surface branded query status
explicitly in any site-wide analysis.


### Knowledge Panel

Knowledge Panel presence for branded queries confirms that Google has
established the author/brand entity. Check `knowledge_panel` in SERP results
for author-related or brand-related queries. Absence on branded queries
indicates an entity signal gap.

Building a Knowledge Panel requires consistent entity signals: schema Person
markup with `sameAs` links to authoritative profiles (Wikipedia, Wikidata,
LinkedIn, industry-specific directories), published works with ISBNs, and
mentions on third-party authoritative sources.


### Topical authority clusters

A site's ability to rank for a topic is influenced by how many related pages it
has covering adjacent queries. A site with one pillar page and no supporting
posts on adjacent queries will lose cluster authority to a site with five
shallower pages covering the same territory. Missing supporting content is
often the proximate cause of a pillar page underperforming.

GSC queries at positions 20--50 often indicate the site is relevant to a query
but lacks a dedicated page for it. These are new content opportunities, not
on-page fixes for the existing page.


---

## What does NOT matter (debunked)


### Word count

Word count is not a ranking factor. The Surfer SEO 1M-page study found that
raw text length optimizes to zero weight. Longer content correlates with higher
rankings in some studies because longer content tends to cover more entities and
subtopics, not because length itself is the signal. Target semantic coverage,
not a word count.


### "LSI keywords"

"LSI" (Latent Semantic Indexing) is a debunked concept from 1980s Bell Labs
research on static databases. It was never part of Google's algorithm. Tools
that claim to provide "LSI keywords" are selling a fiction. Use entity and
semantic coverage analysis instead.


### FAQ rich results

FAQ rich results in Google SERPs have been restricted to government and health
websites since August 2023. That restriction remains in effect as of 2026.

FAQPage JSON-LD schema still has value for three reasons:
1. AI system citation eligibility -- ChatGPT, Perplexity, and Google AI
   Overviews assign higher confidence to structured Q&A content
2. Voice search matching
3. Content structure signaling

Include FAQ schema for those reasons. Do not expect SERP rich results from it.


### Author bios as a direct ranking lever

SearchPilot A/B tested author bios and found zero ranking impact. Author bios
are not harmful, but they are not a ranking lever. The entity infrastructure
(schema, Knowledge Panel, sameAs links) is what moves the needle.


### Fake freshness

Changing `dateModified` without changing content is actively penalized since
the Dec 2025 core update. Only update the date when you have made a genuine
content change.


---

## Title tag reality

Google rewrites 76% of title tags (Q1 2025, Search Engine Land data).

Key findings:
- Unchanged titles cluster at 30--60 characters. Titles outside this range are
  rewritten at significantly higher rates.
- Matching the H1 to the title tag reduces rewrite probability significantly.
- When Google rewrites a title, it uses the H1 as the primary input.
- H1 quality therefore matters as much as title tag quality.
- A title that is over 60 characters, keyword-stuffed, or mismatched to the H1
  will almost certainly be rewritten.

**Rewrite risk assessment:**
- **HIGH:** Title > 60 chars, OR contains site name in non-standard position,
  OR mismatched to H1, OR Google is already displaying a different title in
  SERP
- **MEDIUM:** Title 55--60 chars, OR contains keyword repetition, OR H1 and
  title differ meaningfully
- **LOW:** Title 30--55 chars, matches H1 closely, keyword-forward


---

## Core Web Vitals thresholds

| Metric            | Good        | Needs improvement | Poor      |
|-------------------|-------------|-------------------|-----------|
| LCP               | < 2,500ms   | 2,500--4,000ms    | > 4,000ms |
| CLS               | < 0.1       | 0.1--0.25         | > 0.25    |
| INP               | < 200ms     | 200--600ms        | > 600ms   |
| Performance score | 90--100     | 50--89            | 0--49     |

INP replaced FID in March 2024. TBT (Total Blocking Time) serves as the lab
proxy for INP when field data is not available.

**Dec 2025 update note:** Pages with LCP above 2,300ms showed ranking drops in
the Dec 2025 core update. Flag any LCP between 2,300ms and 2,500ms as
precautionary amber even though it passes the official 2,500ms threshold.


---

## CTR benchmarks by position

| Position | Expected CTR |
|----------|-------------|
| 1        | ~30%        |
| 3        | ~10%        |
| 5--7     | ~7%         |
| 10       | ~2.5%       |
| 11+      | < 1.5%      |

Near-zero CTR at position 30+ is statistically expected behavior, not a
title/meta problem. Fix ranking first before optimizing title and meta
description.


---

## Featured snippet optimization

Answer-first paragraphs of 40--60 words yield 2.2x better featured snippet
odds (Digital Applied study of 10,000+ top-ranking pages).

Requirements:
- Page must already rank in the top 10 to be eligible for a featured snippet
- The direct answer should appear as the first sentence(s) under the relevant
  H2, followed by expanded context and nuance
- This is not about compressing the full section into 40--60 words. It is about
  front-loading the answer tightly, then elaborating.


---

## GSC position interpretation framework

| Situation                              | Root cause                    | Primary fix                        |
|----------------------------------------|-------------------------------|------------------------------------|
| Position 1--10, CTR below expected     | Title/meta underperformance   | Rewrite title + meta               |
| Position 11--30, high impressions      | Ranking problem, page is relevant | Content depth + authority       |
| Position 30+, any impressions          | Ranking + likely intent gap   | Content overhaul or keyword pivot  |
| Position 1--10, good CTR, low clicks   | Low search volume             | Target additional related queries  |
| Low impressions across all queries     | Not matching query space      | Keyword strategy problem           |

**Position bands for opportunity classification:**
- 1--10: Owned (optimize title/meta/schema, not content strategy)
- 11--20: Competitive (one content improvement from page 1)
- 21--50: Visible but unserved (Google sees relevance but won't promote)
- 51+: No meaningful signal (verify intent alignment before investing)


---

## CMS-specific considerations

### WordPress + Yoast

**Schema array-nesting conflict:** Yoast outputs a `@graph` array containing
WebPage, Person, BreadcrumbList, and WebSite schemas. When a Custom HTML block
contains a JSON-LD array `[{...},{...}]`, Yoast nests the array inside
`@graph` rather than outputting it as a separate script tag, producing invalid
structure.

Fix: always use two separate `<script type="application/ld+json">` tags, each
containing a single JSON object. Never use an array wrapper.

**Inline tag concatenation bug:** `<em>` tags around words in headings or link
anchor text without surrounding spaces can cause text to run together in the
WordPress editor. In any CMS that uses a visual editor with inline formatting,
verify that inline tags have spaces on both sides.

### WordPress + RankMath

RankMath uses a similar `@graph` approach but handles custom schema blocks
differently. Test custom JSON-LD blocks against RankMath's output before
assuming the Yoast fix applies.

### Shopify

Shopify themes frequently inject Product schema automatically. Custom schema
blocks must not conflict with theme-generated schema. Check for duplicate
schema types before adding custom blocks.

### Other CMS platforms

For HubSpot, Squarespace, and custom platforms: verify schema output behavior
with a structured data testing tool before adding custom JSON-LD blocks.
CMS-specific quirks are documented in `SITE_CONFIG.cms_quirks` after
onboarding.


---

## Commercial section placement model

The commercial section (affiliate links, product promotion, lead generation
CTA, or author's own works) belongs in the bottom third of any page -- after
the reader has received full informational value.

This is not arbitrary. NavBoost engagement data shows that pre-value CTAs
increase bounce rate and pogo-sticking. Readers who encounter a sales pitch
before their question is answered are more likely to return to the SERP.

Commercial section handling is configured per site:

| `SITE_CONFIG.content.commercial_model` | What the writer includes                     |
|----------------------------------------|----------------------------------------------|
| `affiliate`                            | Product recommendations with affiliate links |
| `direct_sales`                         | Author's own product/service promotion        |
| `lead_gen`                             | CTA section for lead capture                  |
| `none`                                 | No commercial section                         |

Placement is governed by `SITE_CONFIG.content.commercial_section_placement`
(default: `bottom_third`).


---

## Schema implementation patterns

### Author entity

Every page should reference the author entity by `@id`, not duplicate the full
Person entity. The full Person entity (with `sameAs`, `knowsAbout`, etc.) is
defined once on the site (typically on the about page or via the CMS SEO
plugin). All other pages reference it:

```json
"author": {
  "@type": "Person",
  "@id": "{SITE_CONFIG.author.entity_id}",
  "name": "{SITE_CONFIG.author.name}"
}
```

### Article schema

For guides, posts, and articles:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[H1 text]",
  "author": {
    "@type": "Person",
    "@id": "{SITE_CONFIG.author.entity_id}"
  },
  "datePublished": "[ISO date]",
  "dateModified": "[ISO date]"
}
```

### FAQPage schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer text]"
      }
    }
  ]
}
```

Reminder: FAQPage schema does not produce rich results (restricted to
government/health since Aug 2023). Its value is AI citation eligibility, voice
search, and structure signaling.

### ItemList schema for tables

Any table containing enumerable named entities (products, categories, items,
periods) should have a companion `ItemList` JSON-LD block. This is delivered as
a separate `<script>` tag, never nested in the same block as other schema.

Type selection for the `item` property:
- Rows representing individual books --> `Book`
- Rows representing series --> `BookSeries`
- Rows representing products --> `Product`
- Rows representing concepts, categories, or periods --> `Thing`
- If rows don't map to a specific type, use `name` + `description` on the
  `ListItem` only (omit the `item` property)


---

## Methodology version

**Version:** 1.0
**Last updated:** 2026-03-16
**Evidence window:** 2024--2026

This methodology will be updated as new evidence emerges. If you disagree with
a specific claim, you can override it in `SITE_CONFIG.methodology_overrides`
with a note explaining why.
