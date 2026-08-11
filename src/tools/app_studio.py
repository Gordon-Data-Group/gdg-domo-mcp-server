"""App Studio tools — low-code app management, views, sharing.

API reference: api-definitions-md/08-app-studio.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="app_studio", read_only=True)
def app_studio_list(
    parts: Annotated[str | None, "Comma-separated parts to include in the response"] = None,
    include_hidden_views: Annotated[bool | None, "Include hidden views"] = None,
    authoring: Annotated[bool | None, "Filter to apps in authoring mode"] = None,
) -> Any:
    """List all App Studio apps."""
    return auth.get(
        "/content/v1/dataapps",
        parts=parts,
        includeHiddenViews=include_hidden_views,
        authoring=authoring,
    )


@domo_tool(toolset="app_studio", read_only=True)
def app_studio_list_admin_summary(
    body: Annotated[
        dict[str, Any],
        (
            "Admin summary filter. Keys: includeTitleClause (bool), includeOwnerClause (bool), "
            "orderBy (str e.g. 'title'), ascending (bool), titleSearchText (str)"
        ),
    ],
    limit: Annotated[int | None, "Max apps to return"] = None,
    skip: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List apps with admin summary information."""
    return auth.post(
        "/content/v1/dataapps/adminsummary",
        body=body,
        limit=limit,
        skip=skip,
    )


@domo_tool(toolset="app_studio", read_only=True)
def app_studio_get(
    app_id: Annotated[str, "App ID"],
) -> Any:
    """Get an App Studio app by ID."""
    return auth.get(f"/content/v1/dataapps/{app_id}")


@domo_tool(toolset="app_studio", read_only=True)
def app_studio_get_admin_summary(
    app_id: Annotated[str, "App ID"],
) -> Any:
    """Get admin summary details for an App Studio app."""
    return auth.get(f"/content/v1/dataapps/{app_id}/adminsummary")


@domo_tool(toolset="app_studio", read_only=True)
def app_studio_get_access(
    app_id: Annotated[str, "App ID"],
) -> Any:
    """Get access details for an App Studio app."""
    return auth.get(f"/content/v1/dataapps/{app_id}/access")


@domo_tool(toolset="app_studio", read_only=False)
def app_studio_share(
    data_app_ids: Annotated[list[str], "List of app IDs to share"],
    recipients: Annotated[list[dict[str, Any]], "List of recipients, each with 'id' (int) and 'type' (e.g. 'user')"],
    message: Annotated[str | None, "Message to include with the share"] = None,
    send_email: Annotated[bool | None, "Send email notification to recipients"] = None,
) -> Any:
    """Share App Studio apps with users or groups."""
    body: dict[str, Any] = {"dataAppIds": data_app_ids, "recipients": recipients}
    if message is not None:
        body["message"] = message
    return auth.post("/content/v1/dataapps/share", body=body, sendEmail=send_email)


@domo_tool(toolset="app_studio", read_only=False)
def app_studio_create_view(
    app_id: Annotated[str, "App ID"],
    title: Annotated[str, "View title"],
    type: Annotated[str | None, "View type (e.g. 'dataappview')"] = None,
    has_layout: Annotated[bool | None, "Whether the view has a layout"] = None,
) -> Any:
    """Create a new view (page) in an App Studio app."""
    body: dict[str, Any] = {"title": title}
    if type is not None:
        body["type"] = type
    if has_layout is not None:
        body["hasLayout"] = has_layout
    return auth.post(f"/content/v1/dataapps/{app_id}/views", body=body)


@domo_tool(toolset="app_studio", read_only=False)
def app_studio_bulk_add_owners(
    entity_ids: Annotated[list[str], "App IDs to add owners to"],
    owners: Annotated[list[dict[str, Any]], "Owners to add, each with 'type' and 'id'"],
    note: Annotated[str | None, "Note to include with the ownership change"] = None,
    send_email: Annotated[bool | None, "Send email notification"] = None,
) -> Any:
    """Add owners to multiple App Studio apps."""
    body: dict[str, Any] = {"entityIds": entity_ids, "owners": owners}
    if note is not None:
        body["note"] = note
    if send_email is not None:
        body["sendEmail"] = send_email
    return auth.put("/content/v1/dataapps/bulk/owners", body=body)


@domo_tool(toolset="app_studio", read_only=False)
def app_studio_duplicate(
    app_id: Annotated[str, "App ID to duplicate"],
    body: Annotated[
        dict[str, Any],
        "Duplicate options. Keys: title (str), duplicateCards (bool), beacon (int), cardPrefix (str), worksheetToApp (bool)",
    ],
) -> Any:
    """Duplicate an App Studio app (async)."""
    return auth.put(f"/content/v1/dataapps/{app_id}/duplicate", body=body)


@domo_tool(toolset="app_studio", read_only=False)
def app_studio_duplicate_sync(
    app_id: Annotated[str, "App ID to duplicate"],
    body: Annotated[
        dict[str, Any],
        "Duplicate options. Keys: title (str), duplicateCards (bool), beacon (int), cardPrefix (str), worksheetToApp (bool)",
    ],
) -> Any:
    """Duplicate an App Studio app (synchronous)."""
    return auth.put(f"/content/v1/dataapps/{app_id}/duplicate/synchronous", body=body)


@domo_tool(toolset="app_studio", read_only=False)
def app_studio_delete(
    app_id: Annotated[str, "App ID to delete"],
) -> Any:
    """Delete an App Studio app."""
    return auth.delete(f"/content/v1/dataapps/{app_id}")


@domo_tool(toolset="app_studio", read_only=False)
def app_studio_delete_view(
    app_id: Annotated[str, "App ID"],
    view_id: Annotated[str, "View ID to delete"],
) -> Any:
    """Delete a view (page) from an App Studio app."""
    return auth.delete(f"/content/v1/dataapps/{app_id}/views/{view_id}")


@domo_tool(toolset="app_studio", read_only=False)
def app_studio_bulk_remove_owners(
    entity_ids: Annotated[list[str], "App IDs to remove owners from"],
    owners: Annotated[
        list[dict[str, Any]],
        "Owners to remove, each with 'type', 'id', and 'displayName'",
    ],
) -> Any:
    """Remove owners from multiple App Studio apps."""
    return auth.post(
        "/content/v1/dataapps/bulk/owners/remove",
        body={"entityIds": entity_ids, "owners": owners},
    )
