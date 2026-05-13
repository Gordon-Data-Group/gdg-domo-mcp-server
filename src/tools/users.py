"""Users tools — user CRUD, search, bulk ops, profile pictures.

API reference: api-definitions-md/35-users.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def users_search(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Supported keys: offset (int), limit (int), "
            "showCount (bool), count (bool), includeDeleted (bool), "
            "onlyDeleted (bool), includeSupport (bool), "
            "sort ({field, order}), filters (list of {field, values, operator, filterType}), "
            "ids (list of id strings), attributes (list of attribute names), "
            "parts (list of 'DETAILED'|'GROUPS'|'ROLE'|'MINIMAL'), cacheBuster (int)"
        ),
    ],
    explain: Annotated[bool | None, "Return query explanation instead of results"] = None,
) -> Any:
    """Search users with filters, sorting, and field selection."""
    return auth.post("/identity/v1/users/search", body=body, explain=explain)


@mcp.tool()
def users_list(
    limit: Annotated[int | None, "Max users to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    attributes: Annotated[str | None, "Comma-separated list of attributes to include"] = None,
) -> Any:
    """List users via identity/v1 with optional pagination and field selection."""
    return auth.get("/identity/v1/users/", limit=limit, offset=offset, attributes=attributes)


@mcp.tool()
def users_list_v3(
    limit: Annotated[int | None, "Max users to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    active: Annotated[bool | None, "Filter by active status"] = None,
) -> Any:
    """List users via content/v3 with optional active filter."""
    return auth.get("/content/v3/users/", limit=limit, offset=offset, active=active)


@mcp.tool()
def users_get_bulk(
    cv_user_ids: Annotated[str, "Comma-separated list of user IDs to fetch"],
) -> Any:
    """Fetch multiple users by ID in a single request."""
    return auth.get_root("/users/index", cvUserIds=cv_user_ids)


@mcp.tool()
def users_get(
    user_id: Annotated[str, "User ID"],
    attributes: Annotated[str | None, "Comma-separated list of attributes to return"] = None,
    parts: Annotated[str | None, "Comma-separated parts: DETAILED, GROUPS, ROLE, MINIMAL"] = None,
) -> Any:
    """Get a single user by ID via identity/v1."""
    return auth.get(f"/identity/v1/users/{user_id}", attributes=attributes, parts=parts)


@mcp.tool()
def users_get_v2(
    user_id: Annotated[str, "User ID"],
) -> Any:
    """Get a single user by ID via content/v2."""
    return auth.get(f"/content/v2/users/{user_id}")


@mcp.tool()
def users_get_v3(
    user_id: Annotated[str, "User ID"],
) -> Any:
    """Get a single user by ID via content/v3."""
    return auth.get(f"/content/v3/users/{user_id}")


@mcp.tool()
def users_get_locations(
    limit: Annotated[int | None, "Max locations to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    search: Annotated[str | None, "Search string to filter locations"] = None,
) -> Any:
    """Get distinct employee location values for typeahead/autocomplete."""
    return auth.get(
        "/content/v2/users/attributeTypeahead/EMPLOYEELOCATION",
        limit=limit,
        offset=offset,
        search=search,
    )


@mcp.tool()
def users_get_two_factor_status(
    user_id: Annotated[str, "User ID"],
    keys: Annotated[str | None, "Comma-separated state keys to retrieve"] = None,
) -> Any:
    """Get two-factor authentication state for a user."""
    return auth.get(f"/content/v2/users/{user_id}/state", keys=keys)


@mcp.tool()
def users_create(
    display_name: Annotated[str, "User's display name"],
    role_id: Annotated[int, "Role ID to assign"],
    email: Annotated[str, "User's email address"],
    send_invite: Annotated[bool | None, "Send an invite email to the new user"] = None,
) -> Any:
    """Create a new user."""
    body: dict[str, Any] = {
        "displayName": display_name,
        "roleId": role_id,
        "detail": {"email": email},
    }
    return auth.post("/content/v3/users", body=body, sendInvite=send_invite)


@mcp.tool()
def users_update(
    user_id: Annotated[str, "User ID"],
    attributes: Annotated[
        list[dict[str, Any]],
        "List of attribute patches, each with 'key' (attribute name) and 'values' (list of strings)",
    ],
) -> Any:
    """Patch a user's attributes via identity/v1 (partial update)."""
    return auth.patch(f"/identity/v1/users/{user_id}", body={"attributes": attributes})


@mcp.tool()
def users_update_v3(
    body: Annotated[
        dict[str, Any],
        (
            "Full user object to replace. Required: id (int). Optional top-level keys: "
            "displayName, avatarKey, role, roleId, invitorUserId, detail (title, email, "
            "alternateEmail, phoneNumber, deskPhoneNumber, employeeNumber, pending, location, "
            "timeZone, locale, active, department, employeeId, hireDate, subjectId), "
            "trial, socialDetail, groups"
        ),
    ],
) -> Any:
    """Replace a user record via content/v3 (full update)."""
    return auth.put("/content/v3/users", body=body)


@mcp.tool()
def users_bulk_update(
    users: Annotated[
        list[dict[str, Any]],
        (
            "List of user objects to update. Each object: id (str, required), "
            "displayName, emailAddress, title, phoneNumber, employeeLocation, "
            "timeZone, employeeNumber, employeeId, department, hireDate (int epoch), "
            "reportsTo (user id str)"
        ),
    ],
    transaction_id: Annotated[
        str | None,
        "UUID transaction identifier for the bulk operation",
    ] = None,
) -> Any:
    """Bulk-update multiple users via content/v2."""
    body: dict[str, Any] = {"users": users}
    if transaction_id is not None:
        body["transactionId"] = transaction_id
    return auth.put("/content/v2/users/bulk", body=body)


@mcp.tool()
def users_update_profile_pics(
    entity_ids: Annotated[list[str], "List of user IDs whose avatar should be updated"],
    base64_image: Annotated[str, "Base64-encoded image, e.g. 'data:image/jpeg;base64,<data>'"],
    is_open: Annotated[bool | None, "Whether the avatar is publicly visible"] = None,
    transaction_id: Annotated[str | None, "UUID transaction identifier"] = None,
) -> Any:
    """Bulk-update profile pictures for one or more users."""
    body: dict[str, Any] = {
        "entityIds": entity_ids,
        "entityType": "USER",
        "base64Image": base64_image,
    }
    if is_open is not None:
        body["isOpen"] = is_open
    if transaction_id is not None:
        body["transactionId"] = transaction_id
    return auth.post("/content/v1/avatar/bulk", body=body)


@mcp.tool()
def users_update_landing_page(
    user_id: Annotated[str, "User ID"],
    page_id: Annotated[str, "Page ID to set as the landing page"],
    platform: Annotated[str, "Platform to set landing page for: 'DESKTOP' or 'MOBILE'"],
) -> Any:
    """Set the desktop or mobile landing page for a user."""
    return auth.put(f"/content/v1/landings/target/{platform}/entity/PAGE/id/{page_id}/{user_id}")


@mcp.tool()
def users_delete(
    user_id: Annotated[str, "User ID to delete"],
) -> Any:
    """Delete a user by ID."""
    return auth.delete(f"/identity/v1/users/{user_id}")
