"""Pages (Dashboards) tools — CRUD, access, layouts, filter views.

API reference: api-definitions-md/27-pages-dashboards-.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def pages_list_admin_summary(
    body: Annotated[
        dict[str, Any],
        (
            "Filter/sort body. Supported keys: includePageTitleClause (bool), "
            "orderBy (str), pageTitleSearchText (str), addPageWithNoOwner (bool), "
            "ascending (bool), includeAllPages (bool), includeCardCountClause (bool), "
            "includeDetails (bool), includeLastModifiedDateClause (bool), "
            "lastModifiedDateOperand (str), lastModifiedStartDate (str YYYY-MM-DD), "
            "lastModifiedEndDate (str YYYY-MM-DD), includePermissionsList (bool), "
            "referenceId (str), referenceType (str e.g. 'GROUP')"
        ),
    ],
    limit: Annotated[int | None, "Max pages to return"] = None,
    skip: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List pages with admin-level metadata using flexible filters."""
    return auth.post("/content/v1/pages/adminsummary", body=body, limit=limit, skip=skip)


@mcp.tool()
def pages_get(
    page_id: Annotated[str, "Page ID"],
    parts: Annotated[str | None, "Comma-separated parts to include"] = None,
    include_v4_page_layouts: Annotated[bool | None, "Include v4 layout data"] = None,
    stack_load_context_id: Annotated[str | None, "Stack load context ID"] = None,
    stack_load_context: Annotated[str | None, "Stack load context value"] = None,
    stack_load_trigger: Annotated[str | None, "Stack load trigger"] = None,
) -> Any:
    """Get a page by ID."""
    return auth.get(
        f"/content/v3/stacks/{page_id}",
        parts=parts,
        includeV4PageLayouts=include_v4_page_layouts,
        stackLoadContextId=stack_load_context_id,
        stackLoadContext=stack_load_context,
        stackLoadTrigger=stack_load_trigger,
    )


@mcp.tool()
def pages_get_with_cards(
    page_id: Annotated[str, "Page ID"],
    parts: Annotated[str | None, "Comma-separated parts to include"] = None,
    include_v4_page_layouts: Annotated[bool | None, "Include v4 layout data"] = None,
    stack_load_context_id: Annotated[str | None, "Stack load context ID"] = None,
    stack_load_context: Annotated[str | None, "Stack load context value"] = None,
    stack_load_trigger: Annotated[str | None, "Stack load trigger"] = None,
) -> Any:
    """Get a page along with its cards."""
    return auth.get(
        f"/content/v3/stacks/{page_id}/cards",
        parts=parts,
        includeV4PageLayouts=include_v4_page_layouts,
        stackLoadContextId=stack_load_context_id,
        stackLoadContext=stack_load_context,
        stackLoadTrigger=stack_load_trigger,
    )


@mcp.tool()
def pages_get_access(
    page_id: Annotated[str, "Page ID"],
    filter: Annotated[str | None, "Filter string for access list"] = None,
    limit: Annotated[int | None, "Max entries to return"] = None,
    expand_users: Annotated[bool | None, "Expand group entries to show individual users"] = None,
) -> Any:
    """Get the access list for a page."""
    return auth.get(
        f"/content/v1/share/accesslist/page/{page_id}",
        filter=filter,
        limit=limit,
        expandUsers=expand_users,
    )


@mcp.tool()
def pages_get_navigation_order(
    include_start_page: Annotated[bool | None, "Include the start/home page in results"] = None,
    elevate_shared_page: Annotated[bool | None, "Elevate shared pages in the order"] = None,
    include_hidden: Annotated[bool | None, "Include hidden pages"] = None,
) -> Any:
    """Get the navigation page order for the current user."""
    return auth.get(
        "/content/v2/pages/navigation",
        includeStartPage=include_start_page,
        elevateSharedPage=elevate_shared_page,
        includeHidden=include_hidden,
    )


@mcp.tool()
def pages_create(
    title: Annotated[str, "Page title"],
    parent_page_id: Annotated[int | None, "Parent page ID (0 or omit for top-level)"] = None,
    has_layout: Annotated[bool | None, "Always pass True — creates a v4 layout with the page so cards can be positioned. Pages without a layout cannot use pages_update_layout."] = None,
) -> Any:
    """Create a new page (dashboard). Always pass has_layout=True so the page gets a v4 layout.

    NOTE: The create response does NOT include the layoutId. After creating the page, call
    pages_get_with_cards(page_id, include_v4_page_layouts=True) to retrieve the layoutId from
    the pageLayoutV4.layoutId field. Use that ID with:
    pages_create_writelock → pages_update_layout → pages_delete_writelock to position cards.
    """
    body: dict[str, Any] = {"title": title}
    if parent_page_id is not None:
        body["parentPageId"] = parent_page_id
    if has_layout is not None:
        body["hasLayout"] = has_layout
    return auth.post("/content/v1/pages", body=body)


@mcp.tool()
def pages_share_access(
    resources: Annotated[
        list[dict[str, Any]],
        "List of resources to share, each with 'type' (e.g. 'page') and 'id' (str)",
    ],
    recipients: Annotated[
        list[dict[str, Any]],
        "List of recipients, each with 'type' ('user' or 'group', lowercase) and 'id' (str)",
    ],
    message: Annotated[str | None, "Optional message to include with the share notification"] = None,
    send_email: Annotated[bool | None, "Send an email notification to recipients"] = None,
) -> Any:
    """Share one or more pages with users or groups."""
    body: dict[str, Any] = {"resources": resources, "recipients": recipients}
    if message is not None:
        body["message"] = message
    return auth.post("/content/v1/share", body=body, sendEmail=send_email)


@mcp.tool()
def pages_bulk_move(
    page_ids: Annotated[list[int], "List of page IDs to move"],
    page_permission: Annotated[str | None, "Permission to apply after move (e.g. 'ORIGINAL')"] = None,
    parent_page_id: Annotated[int | None, "Destination parent page ID; omit to move to top level"] = None,
) -> Any:
    """Move one or more pages to a new parent."""
    body: dict[str, Any] = {"pageIds": page_ids}
    if parent_page_id is not None:
        body["parentPageId"] = parent_page_id
    if page_permission is not None:
        body["pagePermission"] = page_permission
    return auth.put("/content/v1/pages/bulk/move", body=body)


@mcp.tool()
def pages_reorder(
    page_order_map: Annotated[
        dict[str, str],
        (
            "Map of parent-page-ID → comma-separated ordered child page IDs. "
            "Use key '0' to order top-level pages."
        ),
    ],
) -> Any:
    """Set the navigation page order for the current user."""
    return auth.put("/content/v1/pages/pageorder", body={"pageOrderMap": page_order_map})


@mcp.tool()
def pages_update(
    page_id: Annotated[str, "Page ID"],
    title: Annotated[str | None, "New page title"] = None,
    locked: Annotated[bool | None, "Whether the page is locked"] = None,
) -> Any:
    """Update a page's title or locked state."""
    body: dict[str, Any] = {}
    if title is not None:
        body["title"] = title
    if locked is not None:
        body["locked"] = locked
    return auth.put(f"/content/v1/pages/{page_id}", body=body)


@mcp.tool()
def pages_duplicate(
    page_id: Annotated[str, "Page ID to duplicate"],
    page_title: Annotated[str | None, "Title for the duplicated page"] = None,
    parent_page_id: Annotated[int | None, "Parent page ID for the duplicate"] = None,
    card_prefix: Annotated[str | None, "Prefix to prepend to duplicated card titles"] = None,
    beacon: Annotated[int | None, "Beacon value for tracking"] = None,
    do_not_duplicate_cards: Annotated[bool | None, "Create page structure without copying cards"] = None,
) -> Any:
    """Synchronously duplicate a page."""
    body: dict[str, Any] = {}
    if page_title is not None:
        body["pageTitle"] = page_title
    if parent_page_id is not None:
        body["parentPageId"] = parent_page_id
    if card_prefix is not None:
        body["cardPrefix"] = card_prefix
    if beacon is not None:
        body["beacon"] = beacon
    return auth.put(
        f"/content/v1/pages/{page_id}/duplicate",
        body=body,
        doNotDuplicateCards=do_not_duplicate_cards,
    )


@mcp.tool()
def pages_duplicate_async(
    page_id: Annotated[str, "Page ID to duplicate"],
    page_title: Annotated[str | None, "Title for the duplicated page"] = None,
    parent_page_id: Annotated[int | None, "Parent page ID for the duplicate"] = None,
    card_prefix: Annotated[str | None, "Prefix to prepend to duplicated card titles"] = None,
    beacon: Annotated[int | None, "Beacon value for tracking"] = None,
    do_not_duplicate_cards: Annotated[bool | None, "Create page structure without copying cards"] = None,
) -> Any:
    """Asynchronously duplicate a page; returns a job reference."""
    body: dict[str, Any] = {}
    if page_title is not None:
        body["pageTitle"] = page_title
    if parent_page_id is not None:
        body["parentPageId"] = parent_page_id
    if card_prefix is not None:
        body["cardPrefix"] = card_prefix
    if beacon is not None:
        body["beacon"] = beacon
    return auth.put(
        f"/content/v1/pages/{page_id}/duplicateAsync",
        body=body,
        doNotDuplicateCards=do_not_duplicate_cards,
    )


@mcp.tool()
def pages_delete(
    page_id: Annotated[str, "Page ID to delete"],
) -> Any:
    """Delete a page by ID."""
    return auth.delete(f"/content/v1/pages/{page_id}")


@mcp.tool()
def pages_remove_access(
    type: Annotated[str, "Recipient type ('user' or 'group')"],
    id: Annotated[str, "Recipient ID to remove"],
    resource_ids: Annotated[str | None, "Comma-separated page IDs to remove access from"] = None,
) -> Any:
    """Remove a user's or group's access from one or more pages."""
    return auth.delete(f"/content/v1/share/bulk/page/{type}/{id}", resourceIds=resource_ids)


@mcp.tool()
def pages_bulk_remove_owners(
    owners: Annotated[
        list[dict[str, Any]],
        "List of owners to remove, each with 'id' (int) and 'type' (e.g. 'USER')",
    ],
    page_ids: Annotated[list[int], "List of page IDs to remove the owners from"],
) -> Any:
    """Bulk-remove owners from multiple pages."""
    return auth.post(
        "/content/v1/pages/bulk/owners/remove",
        body={"owners": owners, "pageIds": page_ids},
    )


# ---------------------------------------------------------------------------
# Layouts
# ---------------------------------------------------------------------------

@mcp.tool()
def pages_get_layout(
    layout_id: Annotated[str, "Layout ID — this is the numeric layoutId from pageLayoutV4.layoutId, NOT the page ID"],
) -> Any:
    """Get a page layout by its layout ID (not the page ID).

    IMPORTANT: This endpoint may return empty/no output. Prefer calling
    pages_get_with_cards(page_id, include_v4_page_layouts=True) instead — it reliably returns
    the full pageLayoutV4 block including the layoutId, content[], and standard/compact templates.
    """
    return auth.get(f"/content/v4/pages/layouts/{layout_id}")


@mcp.tool()
def pages_create_writelock(
    layout_id: Annotated[str, "Layout ID to lock for editing"],
) -> Any:
    """Acquire a write lock on a page layout. MUST be called and succeed before pages_update_layout.

    Always call pages_delete_writelock after finishing the update to release the lock.
    The layout ID comes from the pageLayoutV4.layoutId field returned by pages_get or pages_get_with_cards
    (pass include_v4_page_layouts=True), or from pages_create when has_layout=True.
    """
    return auth.put(f"/content/v4/pages/layouts/{layout_id}/writelock")


@mcp.tool()
def pages_update_layout(
    layout_id: Annotated[str, "Layout ID (from pageLayoutV4.layoutId on the page)"],
    body: Annotated[
        dict[str, Any],
        (
            "Full layout definition. Required keys: layoutId (int), pageUrn (str, the page ID as string). "
            "Optional: printFriendly (bool), background (null), isDynamic (bool), hasPageBreaks (bool), style (null). "
            "content (list): each item maps a card to a contentKey. CARD item keys: "
            "  id (int, existing items keep their id; new items omit id), contentKey (int, unique index), "
            "  cardId (int), cardUrn (str), type ('CARD'), compactInteractionDefault (bool), "
            "  hideTitle (bool), hideDescription (bool), hideFooter (bool), hideWrench (bool), "
            "  hideMargins (bool), hideSummary (bool), summaryNumberOnly (bool), hideTimeframe (bool), "
            "  hideBorder (bool), hasSummary (bool), fitToFrame (bool), acceptFilters (bool), "
            "  acceptDateFilter (bool), acceptSegments (bool), showMoreContent (bool). "
            "HEADER item keys: contentKey (int), type ('HEADER'), text (str). "
            "standard (dict): desktop grid — aspectRatio (1.67), width (60), frameMargin (null), framePadding (null), "
            "  type ('STANDARD'), template (list of position objects). "
            "compact (dict): mobile grid — aspectRatio (1.0), width (12), type ('COMPACT'), template (list). "
            "template item keys: contentKey (int, matches a content item), x (int), y (int), "
            "  width (int), height (int), type (str, e.g. 'CARD'). "
            "  CRITICAL — virtual/virtualAppendix/children control whether Domo respects your positions: "
            "  Custom-positioned cards (fixed x/y/width/height): virtual=false, virtualAppendix=false, children=[]. "
            "  Auto-arranged appendix cards: virtual=true, virtualAppendix=true, children=null. "
            "  WARNING: if you set virtual=true on ALL items, Domo silently ignores every x/y/width/height "
            "  value and auto-generates the layout — the request succeeds (200) but positions are wrong. "
            "Special template types: PAGE_BREAK (height 0), SEPARATOR, HEADER — always virtual=true, virtualAppendix=true, children=null."
        ),
    ],
) -> Any:
    """Update a page layout (card positions and sizes). Call pages_create_writelock first; call pages_delete_writelock after."""
    return auth.put(f"/content/v4/pages/layouts/{layout_id}", body=body)


@mcp.tool()
def pages_delete_writelock(
    layout_id: Annotated[str, "Layout ID to release the write lock on"],
) -> Any:
    """Release the write lock on a page layout after finishing pages_update_layout."""
    return auth.delete(f"/content/v4/pages/layouts/{layout_id}/writelock")


# ---------------------------------------------------------------------------
# Filter Views
# ---------------------------------------------------------------------------

@mcp.tool()
def pages_list_filter_views(
    page_id: Annotated[str, "Page ID"],
) -> Any:
    """List named filter views for a page."""
    return auth.get(f"/content/v3/pages/{page_id}/analyzer/named")


@mcp.tool()
def pages_update_filter_view(
    page_id: Annotated[str, "Page ID"],
    body: Annotated[
        dict[str, Any],
        (
            "Filter view definition. Keys: analyzerId (int), name (str), type (str e.g. 'NAMED'), "
            "scope (str e.g. 'PAGE'), ownerId (str), isDefault (bool), order, "
            "filters (list of {column, operand, values, dataType, filterType, affectedCardUrns, key}), "
            "graphBy, functionOverrides (dict), segmentIds (list)"
        ),
    ],
) -> Any:
    """Create or update a named filter view on a page."""
    return auth.put(f"/content/v3/pages/{page_id}/analyzer", body=body)


@mcp.tool()
def pages_delete_filter_view(
    filter_view_id: Annotated[str, "Filter view ID to delete"],
) -> Any:
    """Delete a named filter view."""
    return auth.delete(f"/content/v3/pages/analyzer/{filter_view_id}")
