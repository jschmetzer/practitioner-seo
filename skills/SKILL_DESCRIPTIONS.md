# Skill Descriptions -- Practitioner SEO

<!-- These descriptions control when Claude activates each skill. Copy the
     description text into the skill's description field in your Claude
     Project configuration. -->


## Page Optimizer

**Filename:** `OPTIMIZER_PROTOCOL.md`

**Description:**
```
Analyzes any page on the configured site and produces a complete, evidence-backed SEO optimization plan. Trigger this skill whenever the user provides a URL from their site and wants to improve rankings, audit a page, diagnose what's holding a page back, or understand its SEO status. Trigger phrases: "optimize this page", "audit this URL", "what's wrong with this page", "improve my rankings", "look at this page", "what should I fix", "analyze this page", "SEO audit", or simply pasting a site URL. No keyword required -- the skill infers the target keyword from the URL slug. Produces: diagnostic summary, ready-to-implement copy (title, meta, H1, intro), schema markup, content gap table, internal link audit (bidirectional), Core Web Vitals assessment, engagement audit, freshness assessment, and a tiered action checklist. Requires SITE_CONFIG.md and SITE_CONTEXT.md in the project. Reads SEO_METHODOLOGY.md for evidence base.
```


## Content Strategist

**Filename:** `STRATEGIST_PROTOCOL.md`

**Description:**
```
Maps the keyword landscape across the configured site to identify content gaps, cluster weaknesses, and new content opportunities. Three modes: (1) site-wide gap audit -- no input needed, scans all pages against aggregate keyword demand; (2) cluster diagnostic -- provide a URL and optional seed keyword for a full gap analysis of one pillar and its supporting posts; (3) competitor topic audit -- provide a keyword to get a topic coverage matrix showing what ranked and AIO-cited sources cover that the site doesn't. Trigger phrases: "what are we missing", "content gaps", "audit the cluster", "what should I write next", "is this page complete", "what topics don't we cover", "diagnose this URL", "content strategy", "content plan", or any request for a bird's-eye view of site coverage. Requires SITE_CONFIG.md and SITE_CONTEXT.md in the project. Reads SEO_METHODOLOGY.md for evidence base.
```


## Page Writer

**Filename:** `WRITER_PROTOCOL.md`

**Description:**
```
Researches a keyword and writes a complete, publish-ready page or post -- including body copy, FAQ block with JSON-LD schema, tables with ItemList schema, commercial section (if configured), and a reverse link table. Trigger this skill whenever the user provides a keyword, topic, or writing brief and wants new content drafted. Trigger phrases: "write a page about", "draft a post on", "create content for", "I want to target the keyword", "write me a", "new post about", or any request that results in new content for the site. Also triggers when the user provides a keyword plus outline and asks for a draft. If keyword intent is ambiguous, checkpoints before writing; otherwise researches and drafts without interruption. Requires SITE_CONFIG.md, VOICE_GUIDE.md, FORBIDDEN.md, and SITE_CONTEXT.md in the project. Reads SEO_METHODOLOGY.md for evidence base.
```


## Onboarding

**Filename:** `ONBOARDING.md`

**Description:**
```
Guides setup of Practitioner SEO for a new site. Runs a structured interview covering site basics, author/entity setup, competitive landscape, content architecture, and automated voice analysis -- then generates all per-site configuration files. Trigger phrases: "set up Practitioner SEO", "configure my site", "onboard", "set up SEO", "initialize", "get started". Also triggers automatically if SITE_CONFIG.md does not exist in the project. Produces: SITE_CONFIG.md, VOICE_GUIDE.md (from automated voice analysis of existing content), FORBIDDEN.md, SITE_CONTEXT.md, FORMATTING_RULES.md, a readiness checklist, and suggested first actions.
```


## SEO Methodology (reference document, not a triggered skill)

**Filename:** `SEO_METHODOLOGY.md`

This is not a triggered skill. It is a reference document read by the three
execution protocols. It does not need a skill description. Place it in the
project alongside the protocol files so they can reference it at runtime.
