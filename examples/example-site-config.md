# Site Configuration -- benchcraftworkshop.com

```yaml
# ============================================================================
# SITE BASICS
# ============================================================================

site:
  domain: "benchcraftworkshop.com"
  gsc_property: "sc-domain:benchcraftworkshop.com"
  cms: "wordpress"
  seo_plugin: "yoast"


# ============================================================================
# AUTHOR / ENTITY SETUP
# ============================================================================

author:
  name: "Sarah Chen"
  entity_id: "https://benchcraftworkshop.com/#author"
  credentials: "Professional furniture maker with 20 years of experience. Author of The Unplugged Workshop and Joinery by Hand. Teaches weekend hand tool workshops at her Vermont studio."

  profile_urls:
    linkedin: "https://www.linkedin.com/in/sarahchenwoodworking"
    amazon_author: "https://www.amazon.com/stores/Sarah-Chen/author/B00EXAMPLE"
    goodreads: "https://www.goodreads.com/author/show/12345.Sarah_Chen"
    wikipedia: ""
    wikidata_qid: ""

  knowledge_panel: false
  # Sarah's books are on Amazon and Goodreads but she does not yet have a
  # Knowledge Panel. Entity-building actions should be recommended.


# ============================================================================
# COMPETITIVE LANDSCAPE
# ============================================================================

competitive_landscape:
  structural_competitors:
    - domain: "reddit.com"
      dominates: "community recommendation queries ('best hand plane', 'best chisel set'), troubleshooting, opinion threads"
    - domain: "popularwoodworking.com"
      dominates: "technique guides, tool reviews, educational content"
    - domain: "finewoodworking.com"
      dominates: "premium technique content, project plans, expert reviews"
    - domain: "leevalley.com"
      dominates: "product pages, tool specifications, commercial queries"

  forum_dominance: true
  forum_query_types: "best X recommendations, tool comparisons, beginner advice, community opinions on techniques"


# ============================================================================
# CONTENT ARCHITECTURE
# ============================================================================

content:
  commercial_model: "affiliate"
  commercial_section_placement: "bottom_third"
  pillar_cluster_status: "developing"
  cannibalization_risk: "high"
  # High because multiple posts target "best hand plane for beginners",
  # "how to sharpen chisels", and similar overlapping queries.


# ============================================================================
# CONTENT SYSTEM FILE PATHS
# ============================================================================

context:
  site_context_file: "SITE_CONTEXT.md"
  voice_guide_file: "VOICE_GUIDE.md"
  forbidden_words_file: "FORBIDDEN.md"
  formatting_rules_file: "FORMATTING_RULES.md"
  commercial_list_file: "AFFILIATE_LIST.md"


# ============================================================================
# CMS QUIRKS
# ============================================================================

cms_quirks:
  schema_array_nesting: true
  # WordPress + Yoast: custom JSON-LD arrays get nested inside Yoast's
  # @graph. Use separate <script> tags.

  inline_tag_concatenation: true
  # WordPress: <em> tags without surrounding spaces cause concatenation
  # in the visual editor.

  theme_product_schema: false


# ============================================================================
# TOOL AVAILABILITY
# ============================================================================

tools:
  gsc_available: true
  serpapi_available: true
  pagespeed_available: true
  scraper_available: true
```
