"""Elevation tools — OTP-based session elevation.

API reference: api-definitions-md/19-elevation.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def elevation_get_setting() -> Any:
    """Get the OTP elevation setting for the instance."""
    return auth.get("/customer/v1/properties/authentication.otp_elevation")


@mcp.tool()
def elevation_authenticate_otp(
    user_id: Annotated[str, "User ID to elevate"],
    time_based_one_time_password: Annotated[str, "TOTP code for elevation"],
) -> Any:
    """Authenticate with a time-based OTP to elevate privileges."""
    return auth.put(
        f"/identity/v1/authentication/elevations/{user_id}",
        body={"timeBasedOneTimePassword": time_based_one_time_password},
    )


@mcp.tool()
def elevation_update_setting(
    value: Annotated[str, "New setting value (e.g. 'true' or 'false')"],
) -> Any:
    """Update the OTP elevation setting for the instance."""
    return auth.put(
        "/customer/v1/properties/authentication.otp_elevation",
        body={"value": value},
    )
