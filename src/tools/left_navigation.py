"""Left Navigation tools — nav pin management.

API reference: api-definitions-md/25-left-navigation.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def left_navigation_get_pins() -> Any:
    """Get the current user's left navigation pins."""
    return auth.get("/nav/v1/pins")


@mcp.tool()
def left_navigation_create_pin(
    body: Annotated[
        dict[str, Any],
        (
            "Pin definition. Keys: action ({id, type, newTab}), icon (str), "
            "iconColor (str hex), iconBackgroundColor (str hex), label (str), userId (int)"
        ),
    ],
) -> Any:
    """Append a new pin to the left navigation."""
    return auth.post("/nav/v1/pins/append", body=body)


@mcp.tool()
def left_navigation_update_pins(
    pins: Annotated[
        list[dict[str, Any]],
        (
            "Full ordered list of pins. Each pin: id (int), userId (int), order (int), "
            "icon (str), iconColor (str hex), iconBackgroundColor (str hex), label (str), "
            "action ({type, id, newTab})"
        ),
    ],
) -> Any:
    """Replace all left navigation pins with a new ordered list."""
    return auth.post("/nav/v1/pins/append", body=pins)
