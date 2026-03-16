# Setup Guide

Step-by-step installation and configuration for Practitioner SEO.

---

## Requirements

- Python 3.10 or higher
- pip or uv package manager
- Claude Desktop (Pro subscription minimum) or Claude Code
- Internet access for API calls

Check your Python version:

```bash
python --version
# or
python3 --version
```

If you need Python 3.10+, install it from https://python.org or via your
system package manager.

---

## Step 1: Install the MCP server

### Option A: pip install (recommended)

```bash
pip install practitioner-seo
```

### Option B: From source (for development)

```bash
git clone https://github.com/your-org/practitioner-seo.git
cd practitioner-seo/mcp-server
pip install -e .
```

### Option C: Using uv

```bash
uv pip install practitioner-seo
```

### Verify installation

```bash
python -c "from practitioner_seo.server import main; print('OK')"
```

If this prints `OK`, the package is installed correctly.

---

## Step 2: Configure API keys

Create the configuration directory and file:

```bash
mkdir -p ~/.practitioner-seo
```

Create `~/.practitioner-seo/config.yaml` with your API keys:

```yaml
serpapi_key: "your-serpapi-key-here"
pagespeed_key: "your-pagespeed-key-here"

gsc:
  auth_method: "oauth"
  client_id: "your-google-oauth-client-id"
  client_secret: "your-google-oauth-client-secret"

user_agent: "PractitionerSEO/0.1"
```

See `API_KEYS.md` for where to get each key, and `GSC_SETUP.md` for the
full Google Search Console OAuth walkthrough.

**Not all keys are required.** The server degrades gracefully:
- Without SerpAPI: SERP analysis and keyword research are unavailable
- Without PageSpeed: Core Web Vitals assessment is unavailable
- Without GSC: Search Console data is unavailable

You can add keys incrementally as you need each capability.

### Environment variable alternative

Every config value can also be set via environment variables:

```bash
export PRACTITIONER_SEO_SERPAPI_KEY="your-key"
export PRACTITIONER_SEO_PAGESPEED_KEY="your-key"
export PRACTITIONER_SEO_GSC_CLIENT_ID="your-client-id"
export PRACTITIONER_SEO_GSC_CLIENT_SECRET="your-client-secret"
```

Environment variables override config file values.

---

## Step 3: Connect to Claude Desktop

Locate your Claude Desktop configuration file:

| OS      | Path                                                        |
|---------|-------------------------------------------------------------|
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`               |
| Linux   | `~/.config/Claude/claude_desktop_config.json`               |

If the file does not exist, create it.

### If you installed with pip

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "practitioner-seo": {
      "command": "practitioner-seo"
    }
  }
}
```

If `practitioner-seo` is not on your PATH, use the full path:

```json
{
  "mcpServers": {
    "practitioner-seo": {
      "command": "/full/path/to/practitioner-seo"
    }
  }
}
```

Find the full path with:

```bash
which practitioner-seo
# or on Windows:
where practitioner-seo
```

### If you installed with uv

```json
{
  "mcpServers": {
    "practitioner-seo": {
      "command": "uvx",
      "args": ["practitioner-seo"]
    }
  }
}
```

### If you installed from source

```json
{
  "mcpServers": {
    "practitioner-seo": {
      "command": "python",
      "args": ["-m", "practitioner_seo.server"],
      "cwd": "/path/to/practitioner-seo/mcp-server"
    }
  }
}
```

### Verify the connection

1. Restart Claude Desktop (fully quit and reopen)
2. Open a new conversation
3. Check that the MCP server icon appears in the interface
4. Ask Claude: "List my available MCP tools"
5. You should see 8 tools from `practitioner-seo`

---

## Step 4: Set up your Claude Project

Create a new Claude Project and add the skill files:

1. Copy these files into the project:
   - `skills/SEO_METHODOLOGY.md`
   - `skills/OPTIMIZER_PROTOCOL.md`
   - `skills/STRATEGIST_PROTOCOL.md`
   - `skills/WRITER_PROTOCOL.md`
   - `skills/ONBOARDING.md`

2. Tell Claude: **"Set up Practitioner SEO"**

3. The onboarding skill will walk you through:
   - Site basics (domain, CMS, GSC property)
   - Author/entity setup
   - Competitive landscape
   - Content architecture
   - Voice analysis (provide 3-5 URLs of your best writing)
   - Site inventory

4. Onboarding generates your per-site configuration files:
   - `SITE_CONFIG.md`
   - `VOICE_GUIDE.md`
   - `FORBIDDEN.md`
   - `SITE_CONTEXT.md`
   - `FORMATTING_RULES.md`

These files stay in your Claude Project and are read by the skills at runtime.

---

## Step 5: First run

After onboarding, try one of these:

**Optimize your highest-traffic page:**
> Optimize https://yoursite.com/your-best-page/

**Run a site-wide content gap audit:**
> What should I write next?

**Draft a new page:**
> Write a post about [your keyword]

The first time you use a GSC tool, it will open a browser window for
Google OAuth authorization (if using OAuth auth method). Authorize the
read-only Search Console access. Credentials are cached for subsequent runs.

---

## Updating

```bash
pip install --upgrade practitioner-seo
```

Or from source:

```bash
cd practitioner-seo/mcp-server
git pull
pip install -e .
```

After updating, restart Claude Desktop to pick up the new server version.
