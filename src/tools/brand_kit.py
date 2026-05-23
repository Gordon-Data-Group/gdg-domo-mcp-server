"""Brand Kit tools — color palettes, email configs, login settings.

API reference: api-definitions-md/09-brand-kit.md
"""
from __future__ import annotations

from typing import Any

from src.app import mcp
from src import auth


@mcp.tool()
def brand_kit_list_color_palettes() -> Any:
    """List all chart color palettes defined in the brand kit."""
    return auth.get("/brandkit/v1/chartColorPalettes/all")


@mcp.tool()
def brand_kit_list_email_configs() -> Any:
    """List all email notification configurations."""
    return auth.get("/messaging/v1/email/configurations")


@mcp.tool()
def brand_kit_get_login_settings() -> Any:
    """Get the login page settings for the instance."""
    return auth.get("/content/v1/login-settings/v1")


@mcp.tool()
def brand_kit_get_email_template() -> Any:
    """Get the default email notification template."""
    return auth.get("/messaging/v1/email/configurations/template")


@mcp.tool()
def brand_kit_get_hot_url() -> Any:
    """Get the backlink (hot URL) used in email notifications."""
    return auth.get("/messaging/v1/email/configurations/backlink")
