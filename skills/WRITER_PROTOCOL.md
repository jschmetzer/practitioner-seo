# Page Writer -- Execution Protocol

## What this skill does

Given a keyword (and optionally a brief or outline), this skill:

1. Researches SERP intent, competitor structure, PAA boxes, and GSC data
2. Determines page type (pillar vs. post) and H2 structure
3. Checkpoints only if keyword intent is ambiguous
4. Writes a complete draft: body copy, FAQ block, schema, reverse link table
5. Produces title tag, H1, and meta description ready to paste into CMS
6. Produces `ItemList` JSON-LD schema for every table containing enumerable
   named entities
7. Validates the draft against all content system rules before delivering

**Required input:** A keyword or topic
**Optional:** A brief, an outline, a target URL slug, or a page type
**SERP, PAA, and GSC data are pulled automatically**

**Methodology reference:** `SEO_METHODOLOGY.md` contains the evidence base.
This protocol references it rather than duplicating it.


## Content system files (read at runtime)

Before writing any draft, read these project files:

- `{SITE_CONFIG.context.voice_guide_file}` -- sentence-level patterns, tone
  registers by page type, what not to do
- `{SITE_CONFIG.context.forbidden_words_file}` -- forbidden words, phrases,
  constructions, and formatting rules
- `{SITE_CONFIG.context.site_context_file}` -- internal link catalog; all
  internal links must come from this file
{{#if SITE_CONFIG.context.formatting_rules_file}}
- `{SITE_CONFIG.context.formatting_rules_file}` -- niche-specific formatting
  and terminology rules
{{/if}}
{{#if SITE_CONFIG.context.commercial_list_file}}
- `{SITE_CONFIG.context.commercial_list_file}` -- commercial/affiliate URLs
  for featured products or services
{{/if}}

Do not write any draft until you have read all applicable files in this
session.


## Tool reference

| Tool                          | Purpose                                              |
|-------------------------------|------------------------------------------------------|
| `seo-suite:get_serp`          | SERP intent, competitors, PAA, AIO presence           |
| `seo-suite:get_gsc_data`      | Per-URL GSC data for cannibalization check             |
| `seo-suite:pillar_research`   | Keyword expansion, related queries, question variants |
| `seo-suite:content_brief`     | Competitor heading structure (if needed)               |


## Execution protocol


### Step 1: Read the content system files

Read all applicable files listed above. This is not optional.


### Step 2: Research the keyword

Run all three research tasks:

**Task A -- SERP intent and structure:**
Call `seo-suite:get_serp` with the keyword.
Extract: SERP content type (listicle, guide, forum, wiki), top 3 competitor
titles and H2 structures if visible, PAA questions, AI Overview presence,
position of `{SITE_CONFIG.site.domain}` if it appears.

**Task B -- Cannibalization check:**
Inspect the SERP results from Task A. If `{SITE_CONFIG.site.domain}` appears
in organic results, call `seo-suite:get_gsc_data` on that URL.
Extract: overlapping queries, current position, impressions. If the site
already owns position 1--10 for the target keyword on an existing page, flag
cannibalization risk in NOTES and do not proceed without resolving it.
If the site does not appear in the SERP, note zero cannibalization signal.

**Task C -- Pillar research (topic map):**
Call `seo-suite:pillar_research` with the keyword.
Extract: related query clusters, adjacent keywords, question variants. Use
these to identify H2 candidates and FAQ questions.


### Step 3: Determine page type and structure

**Pillar page if any of:**
- Keyword is a head term or near-head term (broad, high-volume category)
- SERP is dominated by list/guide formats (not forum threads)
- Topic warrants 800+ words and multiple H2 sections
- The outline specifies a pillar structure

**Blog post if any of:**
- Keyword is a specific question or narrow long-tail query
- SERP shows Q&A, forum, or opinion-format results
- Topic is narrow, time-bound, or single-subject
- The outline specifies a post

**If ambiguous:** Stop. Present: the keyword, inferred intent, proposed page
type, and proposed H2 structure. Ask the user to confirm before writing.

**If not ambiguous:** Proceed without interrupting.


### Step 4: Build the H2 structure

Derive the H2 list from:
1. The outline (if provided) -- use it; don't reorganize
2. PAA questions from SERP (confirmed user queries)
3. GSC related queries clustering around the target keyword
4. Competitor H2 patterns -- cover what competitors cover, plus at minimum one
   section they don't

**H2 rules:**
- Question H2s require answer-first treatment (first sentence directly answers
  the question)
- For question H2s: keep the direct answer to 40--60 words. Expanded context
  follows the direct answer. Don't compress the full section; front-load the
  answer tightly. (Featured snippet eligibility requires top-10 ranking first.)
- Commercial section is always in the bottom third -- after full informational
  value is delivered
- FAQ is always last in body copy; nothing follows it

**Mandatory sections for pillar pages:**
- Intro (no H2 -- flows directly from H1)
- Minimum 4 topical H2 sections
{{#if SITE_CONFIG.content.commercial_model != "none"}}
- Commercial section (bottom third only)
{{/if}}
- FAQ (HTML block, last)

**Mandatory sections for blog posts:**
- Intro (no H2)
- Minimum 2 topical H2 sections
- FAQ (HTML block, last)
- Commercial section is optional; include only if topically natural


### Step 5: Write the draft

Write the complete page in Markdown, following all rules from the content
system files.

**Voice:**
- Follow `{SITE_CONFIG.context.voice_guide_file}` precisely. The voice guide
  is the authoritative source for sentence patterns, tone, POV, and
  anti-patterns.
- Practitioner framing. Not aggregation of other sources. Not community
  consensus as primary authority.
- Lead every paragraph with the claim. Context follows.
- Specific always beats general. Name the product, the technique, the source.
- Measured opinion. State it. Don't hedge.
- The professional aside ("In my experience...") is available but use it
  sparingly -- only when it adds information unavailable elsewhere.

**Formatting:**
{{#if SITE_CONFIG.context.formatting_rules_file}}
- Apply all rules from `{SITE_CONFIG.context.formatting_rules_file}` with
  zero tolerance. These are niche-specific requirements that override defaults.
{{/if}}

**Structure:**
- H1: title case, matches target keyword phrase
- H2s: title case for H2, sentence case for H3 and below
- Question H2s: first sentence must directly answer the question
- No numbered lists inside prose paragraphs
{{#if SITE_CONFIG.cms == "wordpress"}}
- Tables are written as raw HTML, not Markdown. Reason: switching between a
  WordPress Custom HTML block and the visual editor corrupts table formatting.
  All tables must be delivered as HTML and pasted into a Custom HTML block.
{{else}}
- Tables can be written as HTML or Markdown per CMS preference.
{{/if}}
- Every table containing enumerable named entities requires a companion
  `ItemList` schema block (see Step 5a)

**Table HTML template:**

```html
<table>
  <thead>
    <tr>
      <th>[Column 1 header]</th>
      <th>[Column 2 header]</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>[Row label]</strong></td>
      <td>[Content]</td>
    </tr>
  </tbody>
</table>
```

Table HTML rules:
- Column headers in `<th>` tags (CSS handles styling)
- Row labels in `<strong>` tags within `<td>`
- Use `&amp;` for ampersands in cell content
- No inline styles
- Oxford comma required

**Internal links:**
- Pillar pages: minimum 4 internal links
- Blog posts: minimum 2 internal links
- All URLs must come from `{SITE_CONFIG.context.site_context_file}`
- Place links where they genuinely serve the reader -- not clustered at
  section ends

{{#if SITE_CONFIG.content.commercial_model == "affiliate"}}
**Commercial section (affiliate model):**
- 3--4 products from `{SITE_CONFIG.context.commercial_list_file}`
- Select for: variety across categories, at least one accessible/entry-level
  option, connection to page's primary topic
- Per-product paragraph: context, audience fit, one social proof signal
- No superlatives. No comparative claims.
- Inline hyperlinks using exact URLs from the commercial list file
{{/if}}

{{#if SITE_CONFIG.content.commercial_model == "direct_sales"}}
**Commercial section (direct sales model):**
- Feature the author's/site owner's own products or services
- Per-product paragraph: what it is, who it's for, connection to page topic
- No superlatives. No comparative claims.
- Links to product pages using URLs from `{SITE_CONFIG.context.commercial_list_file}`
{{/if}}

{{#if SITE_CONFIG.content.commercial_model == "lead_gen"}}
**Commercial section (lead generation model):**
- CTA section connected to the page's primary topic
- Clear value proposition for the reader
- Single CTA -- do not scatter multiple CTAs through the page
{{/if}}

**Forbidden words:**
- Every word and construction in `{SITE_CONFIG.context.forbidden_words_file}`
  is banned. Run a final pass before delivering.


### Step 5a: Write ItemList schema for tables

Every table with rows representing named, enumerable entities needs a
companion `ItemList` JSON-LD schema block, delivered as a separate CMS block.

**What this covers:** Tables where rows represent products, categories,
periods, books, items, people, or other distinct named entities. If the table
has a header row and multiple data rows of the same type, it needs an
`ItemList` block.

**Structure pattern:**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "[Descriptive name for the list]",
  "description": "[One sentence: what the list covers and its purpose]",
  "author": {
    "@type": "Person",
    "@id": "{SITE_CONFIG.author.entity_id}"
  },
  "numberOfItems": [integer],
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "[Row label -- matches first column]",
      "description": "[Expanded context useful for AI citation]",
      "item": {
        "@type": "[Most specific type: Book, Product, Thing, etc.]",
        "name": "[Primary entity name]"
      }
    }
  ]
}
</script>
```

**Type selection for `item` property:**
- Individual books --> `Book` (with `author` if applicable)
- Product series --> `ProductGroup`
- Individual products --> `Product`
- Concepts, categories, periods --> `Thing`
- If rows don't map to a specific type, omit `item` and use `name` +
  `description` on `ListItem` only

**Rules:**
- `numberOfItems` must match actual row count
- `position` values: sequential integers starting at 1
- `name` must match or closely paraphrase the table's first-column value
- `description` should expand beyond the table cell for AI citation value
- Author `@id` is always `{SITE_CONFIG.author.entity_id}`
{{#if SITE_CONFIG.cms_quirks.schema_array_nesting}}
- Deliver as a separate `<script>` tag, never wrapped in an array with other
  schema blocks (CMS array-nesting conflict)
{{/if}}
- Place immediately after the table in the CMS


### Step 6: Write the title tag, H1, and meta description

Produce before writing the FAQ block. Deliver as a clearly labeled block.

**Title tag rules:**
- 50--60 characters
- Target keyword near the front
- No keyword stuffing
- Must not mirror the meta description

**H1 rules:**
- Title case
- Can match the title tag exactly or vary slightly (matching reduces Google
  rewrite probability)
- Must contain the target keyword phrase

**Meta description rules:**
- 135--155 characters
- Leads with the strongest signal -- practitioner credential, specific product
  name, or the specific angle no competitor offers
- Does not repeat the title tag phrasing
- No "in this post" or "this guide covers" constructions

Deliver as:

```
## TITLE, H1, AND META

Title tag: [exact text -- 50--60 chars]
H1: [exact text]
Meta description: [exact text -- 135--155 chars]
```


### Step 7: Write the FAQ block

Produce 4--6 FAQ entries. Source questions from:
- PAA boxes from Step 2
- GSC related queries from Step 2
- Logical questions the target reader would have after reading the page
- Questions that would support AI Overview citation (factual, specific,
  answerable in 1--3 sentences)

FAQ entries follow the answer-first rule: first sentence answers the question
directly.

**Schema note:** FAQPage JSON-LD schema does NOT generate rich results (restricted
to government/health sites since August 2023). Include it for: (1) AI system
citation eligibility, (2) voice search matching, (3) content structure
signaling.

**Deliver as a single self-contained HTML block:**

```html
<!-- FAQ block -->

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[QUESTION -- must match summary text exactly]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[ANSWER -- must match p tag text exactly]"
      }
    }
  ]
}
</script>

<div class="faq-block">
  <details>
    <summary>[Question text]</summary>
    <p>[Answer text]</p>
  </details>
</div>
```

Rules:
- `name` field and `<summary>` text must be identical
- `text` field and `<p>` text must be identical
- No inline styles
- One `<details>` per entry
- In HTML tags, use proper HTML formatting for any niche-specific terms. In
  JSON-LD `text` fields, use plain text (JSON-LD does not render HTML).


### Step 8: Produce the reverse link table

Identify 3--6 pages from `{SITE_CONFIG.context.site_context_file}` that should
link to the newly written page.

Criteria:
- Topically relevant -- the link would genuinely serve the reader
- The anchor text fits naturally at a specific point in that page

Format:

```
## REVERSE LINKS

| Page to update | Suggested placement | Anchor text |
|---|---|---|
| [URL] | [Where in that page] | [Exact anchor text] |
```


### Step 9: Pre-delivery validation

Before delivering, run these checks:

**Forbidden words check:**
- Scan the full draft for every word and phrase in the forbidden file
- Fix violations before delivering -- do not flag them for the user

{{#if SITE_CONFIG.context.formatting_rules_file}}
**Formatting rules check:**
- All niche-specific formatting rules applied correctly
{{/if}}

**Internal link check:**
- Minimum count met (4 for pillar, 2 for post)
- All URLs confirmed present in site context file

{{#if SITE_CONFIG.content.commercial_model == "affiliate"}}
**Commercial section check (pillar only):**
- All commercial URLs confirmed present in commercial list file
- No superlatives, no comparative claims
{{/if}}

**Answer-first check:**
- Every question H2 section starts with a direct answer to the question


---

## Output format

Deliver in this exact order:

1. **Research summary** (3--5 bullet points): SERP intent, PAA questions used
   as H2s, GSC findings, cannibalization risk if any
2. **TITLE, H1, AND META block** (copy-paste ready)
3. **Complete Markdown draft** (all body sections)
4. **ItemList schema block(s)** (one per table, self-contained, labeled)
5. **FAQ HTML block** (self-contained)
6. **REVERSE LINKS table**
7. **NOTES** (cannibalization risk, freshness dependency, schema conflict risk,
   suggested URL slug, missing commercial URLs if applicable)

Start immediately with the research summary. No preamble.


---

## Site-specific rules

These are populated from `SITE_CONFIG.md` at runtime:

1. **Author entity `@id`** is `{SITE_CONFIG.author.entity_id}`. Reference by
   `@id`; don't duplicate the full Person entity.

{{#if SITE_CONFIG.cms_quirks.schema_array_nesting}}
2. **Schema array-nesting conflict** -- use separate `<script>` tags, each
   containing a single JSON object, never an array wrapper.
{{/if}}

{{#if SITE_CONFIG.cms_quirks.inline_tag_concatenation}}
3. **Inline tag concatenation bug** -- inline formatting tags without
   surrounding spaces cause text to run together in the CMS editor. Always
   include spaces around inline-formatted terms.
{{/if}}

4. **Structural competitors:** `{SITE_CONFIG.competitive_landscape.structural_competitors}`
   have advantages for navigational head terms. Target long-tail, practitioner-
   specific, and reader-service queries. Realistic ceiling for head terms:
   position 6--10. Real opportunity: positions 11--25 that are one good page
   from page 1.

5. **AI citation is a primary goal alongside traditional ranking.** Structure
   factual content with named sources, specific dates, specific numbers. FAQ
   entries that answer discrete factual questions are the primary AI citation
   lever.

{{#if SITE_CONFIG.content.commercial_model == "affiliate"}}
6. **Commercial links** come from
   `{SITE_CONFIG.context.commercial_list_file}` only. Do not construct your
   own commercial URLs. If a product referenced in the draft is not in the
   list, note it in NOTES.
{{/if}}


---

## Graceful degradation

| Tool unavailable      | Fallback                                                              |
|-----------------------|-----------------------------------------------------------------------|
| GSC tools             | Skip cannibalization check; note "GSC not configured"                 |
| SerpAPI tools         | Fall back to `web_search` (reduced output)                            |
| Scraper/fetch tools   | Fall back to `web_fetch`; note reduced accuracy                       |
