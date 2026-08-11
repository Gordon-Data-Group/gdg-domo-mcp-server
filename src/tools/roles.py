"""Roles & Authorities tools — role definitions and authority/grant assignments.

API reference: api-definitions-md/30-roles-and-authorities-grants-.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="roles", read_only=True)
def roles_list() -> Any:
    """List all roles defined in the Domo instance."""
    return auth.get("/authorization/v1/roles")


@domo_tool(toolset="roles", read_only=True)
def roles_list_authorities() -> Any:
    """List all available authority (grant) types."""
    return auth.get("/authorization/v1/authorities")


@domo_tool(toolset="roles", read_only=True)
def roles_get_authority_users(
    authorities: Annotated[str | None, "Comma-separated authority keys to filter by"] = None,
    limit: Annotated[int | None, "Max results to return"] = None,
    type: Annotated[str | None, "Entity type to return (e.g. 'USER' or 'GROUP')"] = None,
    filter: Annotated[str | None, "Name filter string"] = None,
    fields: Annotated[str | None, "Comma-separated fields to include in the response"] = None,
) -> Any:
    """Get users or groups that have a specific authority (grant)."""
    return auth.get(
        "/content/v1/typeahead",
        authorities=authorities,
        limit=limit,
        type=type,
        filter=filter,
        fields=fields,
    )


@domo_tool(toolset="roles", read_only=True)
def roles_get(
    role_id: Annotated[str, "Role ID"],
) -> Any:
    """Get a role by ID."""
    return auth.get(f"/authorization/v1/roles/{role_id}")


@domo_tool(toolset="roles", read_only=True)
def roles_get_authorities(
    role_id: Annotated[str, "Role ID"],
) -> Any:
    """Get the authorities (grants) assigned to a role."""
    return auth.get(f"/authorization/v1/roles/{role_id}/authorities")
