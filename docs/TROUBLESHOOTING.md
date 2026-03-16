# Troubleshooting

Common issues and their fixes.

---

## Installation issues

### "No module named 'practitioner_seo'"

The package is not installed, or it's installed in a different Python
environment than Claude Desktop is using.

**Fix:**
1. Verify installation: `python -c "import practitioner_seo; print('OK')"`
2. If that fails, reinstall: `pip install practitioner-seo`
3. If using uv, make sure the Claude Desktop config uses `uvx` as the
   command (see SETUP.md)
4. If installed in a virtualenv, Claude Desktop may not have access to it.
   Install globally or use the full path to the virtualenv's Python.

### "Python version 3.x is not supported"

Practitioner SEO requires Python 3.10 or higher.

**Fix:** Install Python 3.10+ from https://python.org or via your system
package manager. Then reinstall the package with the correct Python version:
`python3.12 -m pip install practitioner-seo`

### pip install fails with dependency conflicts

**Fix:** Try installing in a fresh virtual environment:

```bash
python -m venv practitioner-seo-env
source practitioner-seo-env/bin/activate  # macOS/Linux
# or: practitioner-seo-env\Scripts\activate  # Windows
pip install practitioner-seo
```

Then use the full path to the venv's `practitioner-seo` script in your
Claude Desktop config.

---

## Claude Desktop connection issues

### MCP server does not appear in Claude Desktop

1. **Restart Claude Desktop fully** -- quit the application completely
   (not just close the window) and reopen it
2. **Check config file syntax** -- the JSON must be valid. A missing comma
   or bracket will cause silent failure. Validate with:
   `python -m json.tool < claude_desktop_config.json`
3. **Check the command path** -- if `practitioner-seo` is not on your PATH,
   use the full path in the config. Find it with: `which practitioner-seo`
4. **Check Claude Desktop logs** -- on macOS:
   `~/Library/Logs/Claude/mcp*.log`

### "Server disconnected" or tools not responding

1. The MCP server may have crashed. Check Claude Desktop logs for error
   messages.
2. If the server crashes on startup, run it manually to see the error:
   `practitioner-seo` (this should hang waiting for stdio input; if it
   crashes instead, you'll see the error)
3. Stdout pollution: if any dependency prints to stdout during import, it
   corrupts the MCP JSON-RPC stream. This is rare but can happen with
   certain library versions.

---

## API key issues

### "SerpAPI not configured" / "GSC not configured" / "PageSpeed not configured"

The tool could not find its API key. Check:

1. Config file exists at `~/.practitioner-seo/config.yaml`
2. The key name is spelled correctly (see API_KEYS.md for exact field names)
3. The key value is a non-empty string, properly quoted in YAML
4. If using environment variables, verify they are set:
   `echo $PRACTITIONER_SEO_SERPAPI_KEY`

### GSC returns 403 Forbidden

The most common cause: **wrong property format**.

- Domain properties: `sc-domain:example.com`
- URL-prefix properties: `https://example.com`

These are different properties in GSC. Check your property type in GSC
under Settings > Property type, and make sure `SITE_CONFIG.site.gsc_property`
matches exactly.

Also check:
- If using a service account: is the SA email added as a user in the GSC
  property settings?
- If using OAuth: did you authorize with a Google account that has access
  to this GSC property?

### GSC OAuth flow fails / browser does not open

1. Delete cached credentials: `rm ~/.practitioner-seo/gsc_credentials.json`
2. Verify your OAuth client_id and client_secret are correct in config
3. Make sure the Google Cloud project has the Search Console API enabled
4. Make sure your email is listed as a test user in the OAuth consent screen
   (required while the app is in "Testing" mode)

### SerpAPI returns errors

1. Verify the key at https://serpapi.com/manage-api-key
2. Check your search quota -- free tier is 100/month
3. If you're getting 429 (rate limit), wait and retry

### PageSpeed returns 429

The API quota is approximately 400 queries/day. If exceeded:
- Wait until the next day (quota resets daily)
- Use the manual URL the tool provides to run the test in your browser
- The optimizer will skip CWV items in the action checklist

---

## Skill issues

### "SITE_CONFIG.md not found" or similar file errors

The skills expect configuration files in the Claude Project. After
onboarding, these should be present:
- `SITE_CONFIG.md`
- `VOICE_GUIDE.md`
- `FORBIDDEN.md`
- `SITE_CONTEXT.md`

If any are missing, run onboarding again: "Set up Practitioner SEO"

### Voice guide does not match my writing style

The voice analysis is automated and may not perfectly capture your voice.
After onboarding generates the voice guide, review it and edit:
- Add patterns it missed
- Remove patterns it incorrectly attributed
- Adjust the "What NOT to do" section

### Optimizer reports heading concatenation bugs that don't exist

The raw scraper (`scrape_url`) strips HTML tags and can produce false
concatenation artifacts (e.g., "theBestProducts" from
`the <em>Best</em> Products`). The optimizer protocol instructs Claude
to verify against the rendered page source before reporting. If you see
a false positive, it means the protocol's verification step was skipped.
Point Claude to the relevant instruction in `OPTIMIZER_PROTOCOL.md`
Step 1, cross-reference section.

### Internal link audit misses links

The optimizer must use `scrape_url` (not `fetch_page`) for link auditing
because `fetch_page` may silently drop HTTP protocol links. If the audit
appears incomplete, verify Claude is using the correct tool by checking
that it calls `seo-suite:scrape_url` on every page in the site context
file.

---

## Performance issues

### Tool calls are slow

- `fetch_page` and `scrape_url` depend on the target site's response time
- `pillar_research` with `expansion_depth: "full"` makes 5-8 SerpAPI calls
  sequentially; this can take 30-60 seconds
- `get_pagespeed` calls the PageSpeed Insights API which runs a full
  Lighthouse audit; 15-30 seconds is normal
- Internal link audit in the optimizer scrapes every page on the site
  sequentially; for a 20-page site this takes 30-60 seconds

These are API-limited, not code-limited. The tools are as fast as the
external services they call.
