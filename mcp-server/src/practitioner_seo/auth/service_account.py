"""Service account authentication for Google Search Console.

Fallback auth method for headless/server environments. User provides
a path to a service account JSON key file in config.yaml. The service
account must be added as a user in GSC property settings.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from google.oauth2.service_account import Credentials

from practitioner_seo.config import GSCConfig

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def get_service_account_credentials(
    gsc_config: GSCConfig,
) -> Optional[Credentials]:
    """Load service account credentials from the configured key file.

    Args:
        gsc_config: GSC configuration containing service_account_file path.

    Returns:
        Valid Credentials object, or None if the file is missing or invalid.
    """
    if not gsc_config.service_account_file:
        return None

    key_path = Path(gsc_config.service_account_file)
    if not key_path.exists():
        return None

    try:
        creds = Credentials.from_service_account_file(
            str(key_path), scopes=SCOPES
        )
        return creds
    except Exception:
        return None
