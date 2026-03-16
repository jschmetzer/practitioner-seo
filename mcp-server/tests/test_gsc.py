"""Tests for GSC tools (get_gsc_data and keyword_rankings).

These tests focus on graceful degradation -- verifying that the tools
return structured error messages when GSC is not configured, rather
than crashing.
"""

import json
import pytest

from practitioner_seo.config import Config, GSCConfig


class TestGSCGracefulDegradation:
    """GSC tools should return structured errors when not configured."""

    @pytest.mark.asyncio
    async def test_get_gsc_data_without_config(self, sample_config):
        """get_gsc_data should return a structured error when GSC is not configured."""
        from practitioner_seo.tools.gsc_data import get_gsc_data

        result = await get_gsc_data(
            url="https://example.com/page/",
            site_url="sc-domain:example.com",
            config=sample_config,
            days=90,
        )

        assert "error" in result
        assert result["queries"] == []

    @pytest.mark.asyncio
    async def test_keyword_rankings_without_config(self, sample_config):
        """keyword_rankings should return a structured error when GSC is not configured."""
        from practitioner_seo.tools.keyword_rankings import keyword_rankings

        result = await keyword_rankings(
            site_url="sc-domain:example.com",
            config=sample_config,
            days=90,
        )

        assert "error" in result
        assert result["keywords"] == []


class TestGSCConfigDetection:
    """Config should correctly detect GSC availability."""

    def test_unconfigured_gsc(self):
        """Default config should report GSC as not available."""
        config = Config()
        assert config.has_gsc is False

    def test_oauth_needs_both_credentials(self):
        """OAuth requires both client_id and client_secret."""
        gsc = GSCConfig(
            auth_method="oauth",
            client_id="some-id",
            client_secret=None,
        )
        assert gsc.is_configured is False

        gsc_full = GSCConfig(
            auth_method="oauth",
            client_id="some-id",
            client_secret="some-secret",
        )
        assert gsc_full.is_configured is True

    def test_service_account_needs_existing_file(self, tmp_path):
        """Service account requires an existing key file."""
        gsc = GSCConfig(
            auth_method="service_account",
            service_account_file="/nonexistent/path.json",
        )
        assert gsc.is_configured is False

        key_file = tmp_path / "sa-key.json"
        key_file.write_text("{}")
        gsc_real = GSCConfig(
            auth_method="service_account",
            service_account_file=str(key_file),
        )
        assert gsc_real.is_configured is True
