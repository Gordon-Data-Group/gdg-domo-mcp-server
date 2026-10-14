"""Users tools — user CRUD, search, bulk ops, profile pictures.

API reference: api-definitions-md/35-users.md
"""
from __future__ import annotations

from typing import Annotated, Any, Literal

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="users", read_only=True)
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
    return auth.post_read("/identity/v1/users/search", body=body, explain=explain)


@domo_tool(toolset="users", read_only=True)
def users_list(
    limit: Annotated[int | None, "Max users to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    attributes: Annotated[str | None, "identity API only: comma-separated attributes to include"] = None,
    active: Annotated[bool | None, "content_v3 API only: filter by active status"] = None,
    api: Annotated[Literal["identity", "content_v3"], "identity (/identity/v1, attribute selection) or content_v3 (/content/v3, active filter)"] = "identity",
) -> Any:
    """List users with optional pagination."""
    if api == "content_v3":
        return auth.get("/content/v3/users/", limit=limit, offset=offset, active=active)
    return auth.get("/identity/v1/users/", limit=limit, offset=offset, attributes=attributes)


@domo_tool(toolset="users", read_only=True)
def users_get_bulk(
    cv_user_ids: Annotated[str, "Comma-separated list of user IDs to fetch"],
) -> Any:
    """Fetch multiple users by ID in a single request."""
    return auth.get_root("/users/index", cvUserIds=cv_user_ids)


@domo_tool(toolset="users", read_only=True)
def users_get(
    user_id: Annotated[str, "User ID"],
    attributes: Annotated[str | None, "identity API only: comma-separated attributes to return"] = None,
    parts: Annotated[str | None, "identity API only: comma-separated parts: DETAILED, GROUPS, ROLE, MINIMAL"] = None,
    api: Annotated[
        Literal["identity", "content_v2", "content_v3"],
        "identity (/identity/v1, attribute/part selection), content_v2 (full profile detail: title, department, etc.), or content_v3",
    ] = "identity",
) -> Any:
    """Get a single user by ID."""
    if api == "content_v2":
        return auth.get(f"/content/v2/users/{user_id}")
    if api == "content_v3":
        return auth.get(f"/content/v3/users/{user_id}")
    return auth.get(f"/identity/v1/users/{user_id}", attributes=attributes, parts=parts)


@domo_tool(toolset="users", read_only=True)
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


@domo_tool(toolset="users", read_only=True)
def users_get_two_factor_status(
    user_id: Annotated[str, "User ID"],
    keys: Annotated[str | None, "Comma-separated state keys to retrieve"] = None,
) -> Any:
    """Get two-factor authentication state for a user."""
    return auth.get(f"/content/v2/users/{user_id}/state", keys=keys)


@domo_tool(toolset="users", read_only=False)
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


@domo_tool(toolset="users", read_only=False)
def users_update(
    user_id: Annotated[str, "User ID"],
    attributes: Annotated[
        list[dict[str, Any]] | None,
        "Partial update (identity/v1 PATCH): list of attribute patches, each with 'key' (attribute name) and 'values' (list of strings)",
    ] = None,
    full_user: Annotated[
        dict[str, Any] | None,
        (
            "Full replace (content/v3 PUT) — pass instead of attributes. Complete user object; "
            "id is set from user_id. Must include invitorUserId and detail.pending. Other keys: "
            "displayName, avatarKey, role, roleId, detail (title, email, alternateEmail, "
            "phoneNumber, deskPhoneNumber, employeeNumber, location, timeZone, locale, active, "
            "department, employeeId, hireDate, subjectId), trial, socialDetail, groups"
        ),
    ] = None,
) -> Any:
    """Update a user: patch specific attributes, or replace the whole user record."""
    if (attributes is None) == (full_user is None):
        raise ValueError("Provide exactly one of attributes (partial update) or full_user (full replace).")
    if full_user is not None:
        return auth.put("/content/v3/users", body={**full_user, "id": int(user_id)})
    return auth.patch(f"/identity/v1/users/{user_id}", body={"attributes": attributes})


@domo_tool(toolset="users", read_only=False)
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


@domo_tool(toolset="users", read_only=False)
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


@domo_tool(toolset="users", read_only=False)
def users_update_landing_page(
    user_id: Annotated[str, "User ID"],
    page_id: Annotated[str, "Page ID to set as the landing page"],
    platform: Annotated[str, "Platform to set landing page for: 'DESKTOP' or 'MOBILE'"],
) -> Any:
    """Set the desktop or mobile landing page for a user."""
    return auth.put(f"/content/v1/landings/target/{platform}/entity/PAGE/id/{page_id}/{user_id}")


@domo_tool(toolset="users", read_only=False)
def users_delete(
    user_id: Annotated[str, "User ID to delete"],
) -> Any:
    """Delete a user by ID."""
    return auth.delete(f"/identity/v1/users/{user_id}")
