"""Achievements tools — user achievement badges.

API reference: api-definitions-md/02-achievements.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def achievements_list(
    limit: Annotated[int | None, "Max achievements to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List all achievements in the instance."""
    return auth.get("/content/v1/achievements/bulk", limit=limit, offset=offset)


@mcp.tool()
def achievements_get(
    achievement_id: Annotated[str, "Achievement ID"],
) -> Any:
    """Get an achievement by ID."""
    return auth.get(f"/content/v1/achievements/{achievement_id}")


@mcp.tool()
def achievements_get_admins(
    achievement_id: Annotated[str, "Achievement ID"],
) -> Any:
    """Get administrators for an achievement."""
    return auth.get(f"/content/v1/achievements/{achievement_id}/admins")


@mcp.tool()
def achievements_create(
    body: Annotated[
        dict[str, Any],
        (
            "Achievement definition. Keys: name (str), description (str), "
            "image (str, base64-encoded), administrators (list of {userId: int})"
        ),
    ],
) -> Any:
    """Create a new achievement."""
    return auth.post("/content/v1/achievements", body=body)


@mcp.tool()
def achievements_create_admin(
    achievement_id: Annotated[str, "Achievement ID"],
    user_id: Annotated[int, "User ID to add as administrator"],
) -> Any:
    """Add an administrator to an achievement."""
    return auth.post(
        f"/content/v1/achievements/{achievement_id}/admins",
        body={"userId": user_id},
    )


@mcp.tool()
def achievements_update(
    achievement_id: Annotated[str, "Achievement ID"],
    body: Annotated[
        dict[str, Any],
        "Achievement update. Keys: name (str), description (str), image (str, base64-encoded)",
    ],
) -> Any:
    """Update an achievement."""
    return auth.put(f"/content/v1/achievements/{achievement_id}", body=body)


@mcp.tool()
def achievements_delete(
    achievement_id: Annotated[str, "Achievement ID to delete"],
) -> Any:
    """Delete an achievement."""
    return auth.delete(f"/content/v1/achievements/{achievement_id}")


@mcp.tool()
def achievements_delete_admin(
    achievement_id: Annotated[str, "Achievement ID"],
    admin_id: Annotated[str, "Admin ID to remove"],
) -> Any:
    """Remove an administrator from an achievement."""
    return auth.delete(f"/content/v1/achievements/{achievement_id}/admins/{admin_id}")
