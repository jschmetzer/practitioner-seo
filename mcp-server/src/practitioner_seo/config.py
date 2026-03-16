"""Configuration loading and validation for Practitioner SEO.

Config file location: ~/.practitioner-seo/config.yaml

Required keys depend on which tools the user wants:
- serpapi_key: Required for get_serp, pillar_research
- pagespeed_key: Required for get_pagespeed (free from Google Cloud Console)
- gsc: Required for get_gsc_data, keyword_rankings

Missing keys are not fatal -- tools degrade gracefully with structured
error messages that include setup hints.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


CONFIG_DIR = Path.home() / ".practitioner-seo"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
GSC_CREDENTIALS_FILE = CONFIG_DIR / "gsc_credentials.json"


@dataclass
class GSCConfig:
    """Google Search Console authentication configuration."""

    auth_method: str = "oauth"
    service_account_file: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    @property
    def is_configured(self) -> bool:
        if self.auth_method == "oauth":
            return (
                self.client_id is not None
                and self.client_secret is not None
            )
        elif self.auth_method == "service_account":
            return (
                self.service_account_file is not None
                and Path(self.service_account_file).exists()
            )
        return False


@dataclass
class Config:
    """Top-level configuration for the Practitioner SEO MCP server."""

    serpapi_key: Optional[str] = None
    pagespeed_key: Optional[str] = None
    gsc: GSCConfig = field(default_factory=GSCConfig)
    user_agent: str = "PractitionerSEO/0.1"

    @property
    def has_serpapi(self) -> bool:
        return self.serpapi_key is not None and len(self.serpapi_key) > 0

    @property
    def has_pagespeed(self) -> bool:
        return self.pagespeed_key is not None and len(self.pagespeed_key) > 0

    @property
    def has_gsc(self) -> bool:
        return self.gsc.is_configured


def load_config() -> Config:
    """Load configuration from ~/.practitioner-seo/config.yaml.

    Falls back to environment variables if the config file does not exist:
    - PRACTITIONER_SEO_SERPAPI_KEY
    - PRACTITIONER_SEO_PAGESPEED_KEY
    - PRACTITIONER_SEO_GSC_AUTH_METHOD
    - PRACTITIONER_SEO_GSC_CLIENT_ID
    - PRACTITIONER_SEO_GSC_CLIENT_SECRET
    - PRACTITIONER_SEO_GSC_SERVICE_ACCOUNT_FILE

    Returns a Config object. Missing values are None, not errors.
    """
    config = Config()

    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            raw = yaml.safe_load(f)
        if raw and isinstance(raw, dict):
            config.serpapi_key = raw.get("serpapi_key")
            config.pagespeed_key = raw.get("pagespeed_key")
            config.user_agent = raw.get("user_agent", config.user_agent)

            gsc_raw = raw.get("gsc", {})
            if isinstance(gsc_raw, dict):
                config.gsc = GSCConfig(
                    auth_method=gsc_raw.get("auth_method", "oauth"),
                    service_account_file=gsc_raw.get("service_account_file"),
                    client_id=gsc_raw.get("client_id"),
                    client_secret=gsc_raw.get("client_secret"),
                )

    # Environment variable overrides
    env_serpapi = os.environ.get("PRACTITIONER_SEO_SERPAPI_KEY")
    if env_serpapi:
        config.serpapi_key = env_serpapi

    env_psi = os.environ.get("PRACTITIONER_SEO_PAGESPEED_KEY")
    if env_psi:
        config.pagespeed_key = env_psi

    env_gsc_method = os.environ.get("PRACTITIONER_SEO_GSC_AUTH_METHOD")
    if env_gsc_method:
        config.gsc.auth_method = env_gsc_method

    env_gsc_client_id = os.environ.get("PRACTITIONER_SEO_GSC_CLIENT_ID")
    if env_gsc_client_id:
        config.gsc.client_id = env_gsc_client_id

    env_gsc_secret = os.environ.get("PRACTITIONER_SEO_GSC_CLIENT_SECRET")
    if env_gsc_secret:
        config.gsc.client_secret = env_gsc_secret

    env_gsc_sa = os.environ.get("PRACTITIONER_SEO_GSC_SERVICE_ACCOUNT_FILE")
    if env_gsc_sa:
        config.gsc.service_account_file = env_gsc_sa

    return config


def ensure_config_dir() -> Path:
    """Create the config directory if it does not exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR


def setup_hint(tool_name: str, missing: str) -> str:
    """Return a human-readable setup hint for a missing dependency."""
    hints = {
        "serpapi_key": (
            f"Tool '{tool_name}' requires a SerpAPI key. "
            f"Get one at https://serpapi.com/manage-api-key and add it to "
            f"{CONFIG_FILE} as:\n  serpapi_key: \"your-key-here\"\n"
            f"Or set PRACTITIONER_SEO_SERPAPI_KEY environment variable."
        ),
        "pagespeed_key": (
            f"Tool '{tool_name}' requires a PageSpeed Insights API key. "
            f"Get one (free) at https://developers.google.com/speed/docs/insights/v5/get-started "
            f"and add it to {CONFIG_FILE} as:\n  pagespeed_key: \"your-key-here\"\n"
            f"Or set PRACTITIONER_SEO_PAGESPEED_KEY environment variable."
        ),
        "gsc": (
            f"Tool '{tool_name}' requires Google Search Console access. "
            f"See the GSC_SETUP.md documentation for OAuth configuration. "
            f"Add your OAuth client credentials to {CONFIG_FILE} under the gsc section:\n"
            f"  gsc:\n"
            f"    auth_method: \"oauth\"\n"
            f"    client_id: \"your-client-id\"\n"
            f"    client_secret: \"your-client-secret\"\n"
            f"Or set PRACTITIONER_SEO_GSC_CLIENT_ID and "
            f"PRACTITIONER_SEO_GSC_CLIENT_SECRET environment variables."
        ),
    }
    return hints.get(missing, f"Tool '{tool_name}' is missing configuration: {missing}")
