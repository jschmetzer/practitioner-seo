# Onboarding -- Practitioner SEO Setup

## What this skill does

Guides a new user through a structured interview to generate all per-site
configuration files needed by the three Practitioner SEO skills (Optimizer,
Strategist, Writer). The interview includes automated voice analysis -- the
skill reads the user's existing content and extracts their writing patterns
to generate a voice guide.

**Trigger:** "Set up Practitioner SEO", "configure my site", "onboard", or
detection that no `SITE_CONFIG.md` exists in the project.

**Output:** Five configuration files, a readiness checklist, and suggested
first actions.


## Interview flow

Run each phase in order. Collect all answers before generating output files.
Present each phase as a clear set of questions. Do not skip phases.


### Phase 1: Site basics (required)

Collect:
- **Domain** (e.g., `benchcraftworkshop.com`)
- **CMS** [WordPress / Shopify / HubSpot / Squarespace / Custom]
- **If WordPress:** SEO plugin [Yoast / RankMath / SEOPress / None]
- **If Shopify:** Theme name (for schema conflict checking)
- **GSC property format** -- auto-detect from domain. Domain properties use
  `sc-domain:example.com`. URL-prefix properties use
  `https://example.com`. Confirm with user which format their GSC uses.

**CMS quirks auto-population:** Based on the CMS + plugin combination, auto-
populate the `cms_quirks` section of SITE_CONFIG:

| CMS + Plugin         | Auto-populated quirks                                |
|----------------------|------------------------------------------------------|
| WordPress + Yoast    | `schema_array_nesting: true`, `inline_tag_concatenation: true` |
| WordPress + RankMath | `inline_tag_concatenation: true` (test schema separately) |
| WordPress + None     | `inline_tag_concatenation: true`                      |
| Shopify              | `theme_product_schema: true` (check for duplicates)   |
| Other                | No auto-populated quirks; note for manual testing     |


### Phase 2: Author/entity setup (required)

Collect:
- **Primary author name** (as it should appear in schema and bylines)
- **Credentials** (1--2 sentences describing expertise -- this becomes the
  E-E-A-T signal in schema and copy)
- **Profile URLs** -- collect all that apply:
  - LinkedIn
  - Amazon Author page
  - Goodreads
  - Industry-specific directories or databases
  - Wikipedia (if exists)
  - Wikidata QID (if exists)
  - Any other authoritative profile
- **Knowledge Panel status:** Does searching the author name on Google show a
  Knowledge Panel? [Yes / No / Not sure]
- **Author entity `@id`:** Help the user find or generate this.
  - If the site already has Person schema: extract the `@id` from it
  - If not: generate as `https://{domain}/#author`
  - Confirm the `@id` with the user


### Phase 3: Competitive landscape (required)

Collect:
- **Structural competitors:** 2--5 domains that consistently outrank the site.
  For each: what query types they dominate.
- **Forum/Reddit dominance:** Does Reddit, a forum, or a community platform
  dominate any significant query types in this niche? [Yes / No / Which types]
  - This informs the "honest ceiling" sections in all three skills. If
    community platforms structurally dominate head terms, the skills will
    recommend targeting long-tail queries and AIO citation rather than
    organic position 1.


### Phase 4: Content architecture (required)

Collect:
- **Commercial model:** [Affiliate / Direct sales / Lead gen / None]
- **If affiliate or direct sales:**
  - Does a commercial URL list exist? [Upload it / Generate a blank template]
  - The list should contain: product/service name, URL, category, and a brief
    description
- **Commercial section placement:** [Bottom third / Contextual / None]
  - Default recommendation: bottom third (NavBoost evidence supports value-
    first, commercial-after)
- **Pillar/cluster architecture status:** [Yes, established / Developing / No]
- **Cannibalization risk:** [High / Medium / Low]
  - High: multiple pages targeting near-identical queries (common on sites
    with 20+ posts in a niche)
  - Medium: some overlap but pages are mostly differentiated
  - Low: each page targets a distinct query


### Phase 5: Voice analysis (required, automated)

This is the differentiating step. Most users cannot articulate their own
writing voice from scratch. This phase extracts it from their existing content.

**Step 1:** Ask the user to provide 3--5 URLs representing their best writing
on the site. These should be pages they consider representative of their voice,
not guest posts or pages written by someone else.

**Step 2:** Fetch each URL via `seo-suite:scrape_url`. If the MCP server is
not yet configured, fall back to `web_fetch`.

**Step 3:** Analyze across all pages. Extract:

- **Sentence length distribution:** mean, median, range. Short punchy
  sentences (< 12 words avg) vs. complex constructions (> 20 words avg)?
- **Paragraph length patterns:** single-sentence paragraphs? 3--5 sentence
  norm? Long-form blocks?
- **POV and person:** first-person ratio vs. third-person. Consistent or
  mixed? "I" vs. "we" vs. passive constructions?
- **Hedging frequency:** Count instances of "might", "perhaps", "arguably",
  "it seems", "could be", "it's possible", "in some cases". High hedging =
  the writer avoids strong claims. Low hedging = they state opinions directly.
- **Opener patterns:** How do paragraphs and sections begin? Question leads,
  declarative leads, anecdote leads, credential leads, data leads?
- **Closing patterns:** How do sections and pages end? CTA, summary, forward
  reference, open question, recommendation?
- **Jargon/technical density:** How much domain-specific vocabulary appears?
  Are terms explained or assumed known?
- **Tone register:** Authoritative, conversational, academic, casual, or a
  specific mix?
- **Evidence patterns:** Does the writer cite specific sources, dates, and
  numbers? Or make general claims without specifics?
- **Practitioner signals:** Presence of "in my experience", "I've found",
  "when I build/teach/coach/write", "in my shop/studio/practice". These
  signal first-hand expertise rather than aggregation.

**Step 4:** Generate a draft `VOICE_GUIDE.md` from the analysis.

The voice guide follows this structure:

```markdown
# Voice Guide -- {domain}

## Tone register
[Extracted summary: e.g., "Direct and authoritative. States opinions as
facts, supported by specific evidence. Conversational but not casual --
assumes the reader is competent."]

## Sentence patterns
[Length distribution, rhythm, variety. E.g., "Average sentence length:
14 words. Mix of short declarative sentences (8--10 words) and medium
compound sentences (18--22 words). Rarely exceeds 25 words."]

## Paragraph patterns
[Length, structure. E.g., "2--4 sentences per paragraph. Leads with the
claim; supporting detail follows. Single-sentence paragraphs used for
emphasis, not as a default."]

## POV and person
[E.g., "First person throughout. 'I' not '[author name]'. Avoids 'we'
unless referring to a specific group."]

## Authority signals
[How credentials are deployed. E.g., "Professional experience referenced
when it adds information unavailable elsewhere. Not used as throat-
clearing or credentialism. Specific: names the project, the year, the
outcome."]

## Evidence patterns
[E.g., "Names specific tools, products, and techniques. Cites measurements
and dimensions. Avoids general claims without specifics."]

## What NOT to do
[Anti-patterns extracted from what the author avoids. E.g., "Never uses
superlatives ('the best', 'absolutely essential'). Never hedges with
'might' or 'perhaps' -- states the opinion or omits it. Never opens
with a question the reader didn't ask."]
```

**Step 5:** Present the draft voice guide to the user. Ask them to review and
edit. Incorporate their changes.

**Step 6:** Save the final voice guide to the project.


### Phase 6: Site inventory (required for full functionality)

Collect:
- **Internal link catalog:** Does the user have an existing site context file?
  - If yes: upload it
  - If no: offer to generate one. Two options:
    a. **From sitemap:** Provide the sitemap URL (usually `/sitemap.xml`).
       The skill fetches it and builds a SITE_CONTEXT.md with URLs and titles.
    b. **Manual:** Generate a blank SITE_CONTEXT template for the user to fill
       in.
  - The site context file is the ground truth for internal links and page
    inventory. All three skills depend on it.

- **Forbidden words list:**
  - Seed from the voice analysis anti-patterns (Phase 5 "What NOT to do")
  - Ask the user to add any additional forbidden words or phrases
  - Common offenders to suggest: "game-changer", "must-have", "you won't
    believe", "in this post", "this guide covers", "without further ado",
    "let's dive in", "at the end of the day", "it goes without saying"

- **Niche formatting rules:**
  - Does this niche have specific formatting conventions? (Trademark
    requirements, measurement standards, naming conventions, title
    formatting, technical notation)
  - If yes: upload or create a formatting rules file
  - If no: skip (file will not be referenced)


---

## Onboarding output

Generate these files:

### 1. `SITE_CONFIG.md`

Structured YAML-in-markdown. Use `SITE_CONFIG_TEMPLATE.md` as the skeleton.
Populate every field from the interview answers. Include inline comments
explaining each field.

### 2. `VOICE_GUIDE.md`

Generated from Phase 5 voice analysis, user-reviewed.

### 3. `FORBIDDEN.md`

Seeded from voice analysis anti-patterns + user additions + common offenders.

### 4. `SITE_CONTEXT.md`

From upload, sitemap crawl, or blank template.

### 5. `FORMATTING_RULES.md`

From upload or empty template. If the user has no niche-specific formatting
rules, create a minimal file noting that no rules are configured.

### 6. Readiness checklist

After generating files, assess tool availability:

```
## READINESS CHECKLIST

MCP Server: [Installed / Not installed]
  - If not installed: provide install command

API Keys:
  - SerpAPI: [Configured / Not configured]
  - PageSpeed Insights: [Configured / Not configured]
  - GSC: [Configured / Not configured]

Configuration files:
  - SITE_CONFIG.md: [Complete]
  - VOICE_GUIDE.md: [Complete / Needs review]
  - FORBIDDEN.md: [Complete]
  - SITE_CONTEXT.md: [Complete / Needs population]
  - FORMATTING_RULES.md: [Complete / Not applicable]

Ready to run:
  - Page Optimizer: [Yes / Needs: {missing items}]
  - Content Strategist: [Yes / Needs: {missing items}]
  - Page Writer: [Yes / Needs: {missing items}]
```

### 7. Suggested first actions

Based on readiness status:
- If all tools are configured: "Run the optimizer on your highest-traffic
  page" or "Run a site-wide gap audit"
- If GSC is not configured: "Set up GSC authentication first -- it powers the
  most actionable features"
- If site context is incomplete: "Populate your site context file -- internal
  link audits and reverse link tables depend on it"


---

## Error handling

- If the user provides fewer than 3 URLs for voice analysis, ask for more.
  The minimum for reliable pattern extraction is 3 pages.
- If URLs return errors during voice analysis, note which failed and analyze
  what's available. If fewer than 2 pages are analyzable, ask for alternatives.
- If the user's site has no existing content (brand new site), skip voice
  analysis and generate a voice guide template for them to fill in manually.
  Note in NOTES that the voice guide should be regenerated after 5+ pages
  are published.
- If the MCP server is not yet installed during onboarding, use `web_fetch`
  as fallback for all URL fetching. Note in the readiness checklist that
  the MCP server needs installation.
