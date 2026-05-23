"""Categories tools — certified attributes / entity category tags.

API reference: api-definitions-md/12-categories-certified-attributes-.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def categories_list() -> Any:
    """List all certified attribute categories."""
    return auth.get("/entity/v1/properties/category")


@mcp.tool()
def categories_list_usage() -> Any:
    """List category usage counts across entities."""
    return auth.get("/entity/v1/properties/category/usage")


@mcp.tool()
def categories_get_entity_categories(
    entity_type: Annotated[str, "Entity type (e.g. 'CARD' or 'DATASET')"],
    entity_id: Annotated[str, "Entity ID"],
) -> Any:
    """Get the categories assigned to a specific entity."""
    return auth.get(f"/entity/v1/properties/entity/{entity_type}/{entity_id}")


@mcp.tool()
def categories_create(
    key: Annotated[str, "Category key"],
    description: Annotated[str, "Category description"],
    values: Annotated[list[str], "List of allowed values for this category"],
) -> Any:
    """Create a new certified attribute category."""
    return auth.post(
        "/entity/v1/properties/category",
        body={"key": key, "description": description, "values": values},
    )


@mcp.tool()
def categories_upsert_entity_categories(
    entity_type: Annotated[str, "Entity type (e.g. 'CARD' or 'DATASET')"],
    entity_id: Annotated[str, "Entity ID"],
    categories: Annotated[
        list[dict[str, Any]],
        "List of category assignments, each with 'key' (str) and 'values' (list of str)",
    ],
) -> Any:
    """Set (upsert) categories on a specific entity."""
    return auth.put(
        f"/entity/v1/properties/entity/{entity_type}/{entity_id}",
        body=categories,
    )
