# Google Search Console Setup

This guide walks through setting up Google Search Console (GSC) access
for Practitioner SEO. GSC powers the `get_gsc_data` and `keyword_rankings`
tools, which provide the query-level performance data that drives most
of the optimizer's and strategist's recommendations.

---

## Prerequisites

- A Google account with access to the target site's Search Console property
- The site must be verified in Google Search Console

If the site is not yet in Search Console, add it at
https://search.google.com/search-console

---

## Authentication options

### Option 1: OAuth (recommended for most users)

OAuth opens a browser window on first run. You authorize read-only access
to Search Console, and credentials are cached locally. This is the simplest
setup for individual users.

### Option 2: Service account (for headless/server environments)

A service account uses a JSON key file instead of a browser flow. Useful
for automated environments where no browser is available. Requires adding
the service account email as a user in your GSC property.

---

## OAuth setup (step by step)

### 1. Create a Google Cloud project

1. Go to https://console.cloud.google.com
2. Click the project dropdown at the top and select "New Project"
3. Name it something like "Practitioner SEO" and create it
4. Make sure the new project is selected

### 2. Enable the Search Console API

1. Go to https://console.cloud.google.com/apis/library
2. Search for "Google Search Console API"
3. Click on it and click "Enable"

### 3. Configure the OAuth consent screen

1. Go to https://console.cloud.google.com/apis/credentials/consent
2. Select "External" user type (unless you have a Google Workspace org
   and want "Internal")
3. Fill in the required fields:
   - App name: "Practitioner SEO"
   - User support email: your email
   - Developer contact: your email
4. Click "Save and Continue"
5. On the "Scopes" page, click "Add or Remove Scopes"
6. Search for `https://www.googleapis.com/auth/webmasters.readonly`
7. Check the box and click "Update", then "Save and Continue"
8. On "Test users", add your Google email address
9. Click "Save and Continue", then "Back to Dashboard"

### 4. Create OAuth credentials

1. Go to https://console.cloud.google.com/apis/credentials
2. Click "Create Credentials" and select "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "Practitioner SEO"
5. Click "Create"
6. Copy the **Client ID** and **Client Secret**

### 5. Add credentials to your config

Add to `~/.practitioner-seo/config.yaml`:

```yaml
gsc:
  auth_method: "oauth"
  client_id: "your-client-id-here.apps.googleusercontent.com"
  client_secret: "your-client-secret-here"
```

Or via environment variables:

```bash
export PRACTITIONER_SEO_GSC_CLIENT_ID="your-client-id-here.apps.googleusercontent.com"
export PRACTITIONER_SEO_GSC_CLIENT_SECRET="your-client-secret-here"
```

### 6. First authorization

The first time a GSC tool runs, it will:
1. Open your default browser to Google's OAuth consent screen
2. Ask you to sign in and authorize read-only Search Console access
3. Redirect back to a local URL (the OAuth flow handles this automatically)
4. Cache your credentials at `~/.practitioner-seo/gsc_credentials.json`

Subsequent runs use the cached credentials with automatic refresh.

### 7. Identify your GSC property format

Your GSC property identifier goes into `SITE_CONFIG.md` during onboarding.
The format matters:

- **Domain property:** `sc-domain:example.com`
  (covers all URLs on the domain, including subdomains and both protocols)
- **URL-prefix property:** `https://example.com`
  (covers only URLs under that exact prefix)

Check which type you have in GSC under Settings > Property type. Using the
wrong format will cause 403 errors.

---

## Service account setup

### 1. Create a service account

1. Go to https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "Create Service Account"
3. Name: "practitioner-seo"
4. Click "Create and Continue"
5. Skip the optional permissions steps
6. Click "Done"

### 2. Create a key

1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" then "Create new key"
4. Select JSON format
5. Download the key file
6. Save it somewhere secure (e.g., `~/.practitioner-seo/gsc-sa-key.json`)

### 3. Add the service account to GSC

1. Go to https://search.google.com/search-console
2. Select your property
3. Go to Settings > Users and permissions
4. Click "Add user"
5. Enter the service account email (found in the JSON key file under
   `client_email`, looks like `name@project.iam.gserviceaccount.com`)
6. Set permission to "Restricted" (read-only is sufficient)
7. Click "Add"

### 4. Configure

Add to `~/.practitioner-seo/config.yaml`:

```yaml
gsc:
  auth_method: "service_account"
  service_account_file: "/path/to/gsc-sa-key.json"
```

Or via environment variable:

```bash
export PRACTITIONER_SEO_GSC_AUTH_METHOD="service_account"
export PRACTITIONER_SEO_GSC_SERVICE_ACCOUNT_FILE="/path/to/gsc-sa-key.json"
```

---

## Troubleshooting

**403 Forbidden on GSC calls:**
- Verify the property format in your SITE_CONFIG matches exactly what GSC
  shows. `sc-domain:example.com` and `https://example.com` are different
  properties with different access.
- If using a service account, verify it has been added as a user in the GSC
  property settings.

**OAuth flow opens browser but fails to redirect:**
- Make sure no other application is using the port the OAuth flow needs
- Try closing other browser tabs and retrying
- If the redirect fails, the terminal will show a URL you can paste manually

**Credentials expired / refresh failed:**
- Delete `~/.practitioner-seo/gsc_credentials.json` and re-authorize
- The next GSC tool call will trigger a fresh OAuth flow

**"API not enabled" error:**
- Go to https://console.cloud.google.com/apis/library and verify the
  "Google Search Console API" is enabled for your project
