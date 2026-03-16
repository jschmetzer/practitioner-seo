"""Google OAuth browser flow for Search Console read-only access.

First run opens a browser to the Google consent screen. User authorizes
read-only Search Console access. Credentials are stored in
~/.practitioner-seo/gsc_credentials.json and auto-refresh on subsequent runs.

Users must create their own OAuth client in Google Cloud Console:
1. Create a project at https://console.cloud.google.com
2. Enable the Search Console API
3. Create OAuth 2.0 credentials (Desktop application type)
4. Add client_id and client_secret to config.yaml
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from practitioner_seo.config import GSC_CREDENTIALS_FILE, GSCConfig, ensure_config_dir

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def get_oauth_credentials(gsc_config: GSCConfig) -> Optional[Credentials]:
    """Get valid OAuth credentials, launching browser flow if needed.

    Args:
        gsc_config: GSC configuration containing client_id and client_secret.

    Returns:
        Valid Credentials object, or None if auth fails.
    """
    creds = _load_cached_credentials()

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_credentials(creds)
            return creds
        except Exception:
            # Refresh failed; fall through to full auth flow
            pass

    # Full OAuth flow
    if not gsc_config.client_id or not gsc_config.client_secret:
        return None

    client_config = {
        "installed": {
            "client_id": gsc_config.client_id,
            "client_secret": gsc_config.client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    try:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)
        _save_credentials(creds)
        return creds
    except Exception:
        return None


def _load_cached_credentials() -> Optional[Credentials]:
    """Load credentials from the cache file if it exists."""
    if not GSC_CREDENTIALS_FILE.exists():
        return None

    try:
        with open(GSC_CREDENTIALS_FILE) as f:
            data = json.load(f)
        return Credentials.from_authorized_user_info(data, SCOPES)
    except Exception:
        return None


def _save_credentials(creds: Credentials) -> None:
    """Save credentials to the cache file."""
    ensure_config_dir()
    data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes) if creds.scopes else SCOPES,
    }
    with open(GSC_CREDENTIALS_FILE, "w") as f:
        json.dump(data, f, indent=2)
