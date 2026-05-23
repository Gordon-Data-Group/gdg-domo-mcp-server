"""Groups tools — user group management, membership, dynamic rules.

API reference: api-definitions-md/24-groups.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def groups_list(
    ascending: Annotated[bool | None, "Sort ascending"] = None,
    sort: Annotated[str | None, "Sort field"] = None,
    limit: Annotated[int | None, "Max groups to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    include_full_membership: Annotated[bool | None, "Include full membership lists"] = None,
    owner: Annotated[str | None, "Filter by owner ID"] = None,
    owner_type: Annotated[str | None, "Owner type filter (e.g. 'USER')"] = None,
    group_type: Annotated[str | None, "Group type filter (e.g. 'dynamic')"] = None,
    created_after: Annotated[str | None, "Filter to groups created after this date"] = None,
    created_before: Annotated[str | None, "Filter to groups created before this date"] = None,
    members: Annotated[str | None, "Comma-separated member IDs to filter by"] = None,
    is_manageable: Annotated[bool | None, "Filter to manageable groups only"] = None,
    search: Annotated[str | None, "Search term"] = None,
) -> Any:
    """List groups."""
    return auth.get(
        "/content/v2/groups/grouplist",
        ascending=ascending,
        sort=sort,
        limit=limit,
        offset=offset,
        includeFullMembership=include_full_membership,
        owner=owner,
        ownerType=owner_type,
        groupType=group_type,
        createdAfter=created_after,
        createdBefore=created_before,
        members=members,
        isManageable=is_manageable,
        search=search,
    )


@mcp.tool()
def groups_get_bulk(
    group_ids: Annotated[list[str], "List of group IDs to fetch"],
    include_active: Annotated[bool | None, "Include active status"] = None,
    include_users: Annotated[bool | None, "Include member user details"] = None,
) -> Any:
    """Get multiple groups by ID."""
    return auth.post(
        "/content/v2/groups/get",
        body=group_ids,
        includeActive=include_active,
        includeUsers=include_users,
    )


@mcp.tool()
def groups_get(
    group_id: Annotated[str, "Group ID"],
) -> Any:
    """Get a group by ID."""
    return auth.get(f"/content/v2/groups/{group_id}")


@mcp.tool()
def groups_get_permissions(
    group_id: Annotated[str, "Group ID"],
    check_ownership: Annotated[bool | None, "Check ownership"] = None,
    include_users: Annotated[bool | None, "Include user details in permissions"] = None,
) -> Any:
    """Get permissions for a group."""
    return auth.get(
        f"/content/v2/groups/{group_id}/permissions",
        checkOwnership=check_ownership,
        includeUsers=include_users,
    )


@mcp.tool()
def groups_get_avatar(
    group_id: Annotated[str, "Group ID"],
    size: Annotated[str | None, "Avatar size"] = None,
    default_background: Annotated[str | None, "Default background color"] = None,
    default_foreground: Annotated[str | None, "Default foreground color"] = None,
    default_text: Annotated[str | None, "Default text"] = None,
) -> Any:
    """Get the avatar for a group."""
    return auth.get(
        f"/content/v1/avatar/GROUP/{group_id}",
        size=size,
        defaultBackground=default_background,
        defaultForeground=default_foreground,
        defaultText=default_text,
    )


@mcp.tool()
def groups_create(
    name: Annotated[str, "Group name"],
    type: Annotated[str | None, "Group type (e.g. 'dynamic')"] = None,
    description: Annotated[str | None, "Group description"] = None,
) -> Any:
    """Create a new group."""
    body: dict[str, Any] = {"name": name}
    if type is not None:
        body["type"] = type
    if description is not None:
        body["description"] = description
    return auth.post("/content/v2/groups", body=body)


@mcp.tool()
def groups_add_or_remove_owners(
    changes: Annotated[
        list[dict[str, Any]],
        "List of ownership changes. Each: groupId (int), addOwners (list of {type, id}), removeOwners (list of {type, id})",
    ],
) -> Any:
    """Add or remove owners from groups."""
    return auth.put("/content/v2/groups/access", body=changes)


@mcp.tool()
def groups_add_members(
    changes: Annotated[
        list[dict[str, Any]],
        "List of membership changes. Each: groupId (int), addMembers (list of {type, id})",
    ],
) -> Any:
    """Add members to groups."""
    return auth.put("/content/v2/groups/access", body=changes)


@mcp.tool()
def groups_update_dynamic_rules(
    updates: Annotated[
        list[dict[str, Any]],
        "List of dynamic rule updates. Each: groupId (int), dynamicDefinition ({expression: {operator, expressions}})",
    ],
) -> Any:
    """Update dynamic membership rules for groups."""
    return auth.put("/content/v2/groups", body=updates)


@mcp.tool()
def groups_delete(
    group_id: Annotated[str, "Group ID to delete"],
) -> Any:
    """Delete a group."""
    return auth.delete(f"/content/v2/groups/{group_id}")


@mcp.tool()
def groups_bulk_delete(
    group_ids: Annotated[list[int], "List of group IDs to delete"],
) -> Any:
    """Delete multiple groups."""
    return auth.delete("/content/v2/groups", body=group_ids)
