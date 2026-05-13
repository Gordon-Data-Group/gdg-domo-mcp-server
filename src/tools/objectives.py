"""Objectives (Goals) tools — OKR objectives, key results, periods, tags.

API reference: api-definitions-md/26-objectives-goals-.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def objectives_list(
    filter_key_results: Annotated[bool | None, "Filter to objectives with key results"] = None,
    period_id: Annotated[int | None, "Period ID to filter by"] = None,
    query: Annotated[str | None, "Search query"] = None,
) -> Any:
    """List/search objectives."""
    return auth.get(
        "/social/v1/objectives/search",
        filterKeyResults=filter_key_results,
        periodId=period_id,
        query=query,
    )


@mcp.tool()
def objectives_list_personal(
    filter_key_results: Annotated[bool | None, "Filter to objectives with key results"] = None,
    include_sample_goal: Annotated[bool | None, "Include sample goal"] = None,
    owner_id: Annotated[int | None, "Owner user ID"] = None,
    period_id: Annotated[int | None, "Period ID"] = None,
    type: Annotated[str | None, "Objective type (e.g. 'PERSONAL')"] = None,
) -> Any:
    """List personal objectives for a user."""
    return auth.get(
        "/social/v2/objectives/profile",
        filterKeyResults=filter_key_results,
        includeSampleGoal=include_sample_goal,
        ownerId=owner_id,
        periodId=period_id,
        type=type,
    )


@mcp.tool()
def objectives_list_team(
    filter_key_results: Annotated[bool | None, "Filter to objectives with key results"] = None,
    owner_id: Annotated[int | None, "Owner user ID"] = None,
    period_id: Annotated[int | None, "Period ID"] = None,
) -> Any:
    """List team objectives."""
    return auth.get(
        "/social/v2/objectives/teams-profile",
        filterKeyResults=filter_key_results,
        ownerId=owner_id,
        periodId=period_id,
    )


@mcp.tool()
def objectives_list_periods(
    all: Annotated[bool | None, "Include all periods (past and future)"] = None,
) -> Any:
    """List objective periods."""
    return auth.get("/social/v1/objectives/periods", all=all)


@mcp.tool()
def objectives_list_events() -> Any:
    """List objective events."""
    return auth.get("/social/v1/objectives/events")


@mcp.tool()
def objectives_list_tags(
    all: Annotated[bool | None, "Include all tags"] = None,
) -> Any:
    """List objective tags."""
    return auth.get("/social/v1/objectives/tags", all=all)


@mcp.tool()
def objectives_list_tag_categories(
    all: Annotated[bool | None, "Include all tag categories"] = None,
) -> Any:
    """List objective tag categories."""
    return auth.get("/social/v1/objectives/tags/categories", all=all)


@mcp.tool()
def objectives_list_needs_update(
    filter_key_results: Annotated[bool | None, "Filter to objectives with key results"] = None,
    period_id: Annotated[int | None, "Period ID"] = None,
    user_id: Annotated[int | None, "User ID filter"] = None,
) -> Any:
    """List objectives that need an update."""
    return auth.get(
        "/social/v1/objectives/needs-update",
        filterKeyResults=filter_key_results,
        periodId=period_id,
        userId=user_id,
    )


@mcp.tool()
def objectives_list_drafts(
    filter_key_results: Annotated[bool | None, "Filter to objectives with key results"] = None,
    period_id: Annotated[int | None, "Period ID"] = None,
    user_id: Annotated[int | None, "User ID filter"] = None,
) -> Any:
    """List draft objectives."""
    return auth.get(
        "/social/v2/objectives/draft",
        filterKeyResults=filter_key_results,
        periodId=period_id,
        userId=user_id,
    )


@mcp.tool()
def objectives_get_company_report(
    filter_key_results: Annotated[bool | None, "Filter to objectives with key results"] = None,
    period_id: Annotated[int | None, "Period ID"] = None,
    type: Annotated[str | None, "Objective type"] = None,
) -> Any:
    """Get the company objectives report."""
    return auth.get(
        "/social/v2/objectives/report",
        filterKeyResults=filter_key_results,
        periodId=period_id,
        type=type,
    )


@mcp.tool()
def objectives_get_key_result_chart(
    key_result_id: Annotated[str, "Key result ID"],
) -> Any:
    """Get the chart data for a key result."""
    return auth.get(f"/social/v1/objectives/key-results/{key_result_id}/chart")


@mcp.tool()
def objectives_get_key_result_values(
    key_result_id: Annotated[str, "Key result ID"],
) -> Any:
    """Get the historical values for a key result."""
    return auth.get(f"/social/v1/objectives/key-results/{key_result_id}/values")


@mcp.tool()
def objectives_create(
    body: Annotated[
        dict[str, Any],
        "Objective definition. Keys: name, description, startsAt, expiresAt, status, owners (list), assignees (list), periodId, parentId, keyResults (list), tags (list), type",
    ],
) -> Any:
    """Create a new objective."""
    return auth.post("/social/v1/objectives", body=body)


@mcp.tool()
def objectives_create_key_result(
    body: Annotated[
        dict[str, Any],
        "Key result wrapped in 'keyResult' key. Fields: state, ownerId, ownerType, owners (list), name, description, startValue, currentValue, targetValue, status, operator, startsAt, expiresAt, etc.",
    ],
) -> Any:
    """Create a new key result."""
    return auth.post("/social/v1/objectives/key-results", body=body)


@mcp.tool()
def objectives_create_tag(
    name: Annotated[str, "Tag name"],
    category_id: Annotated[int | None, "Category ID"] = None,
    category_name: Annotated[str | None, "Category name"] = None,
) -> Any:
    """Create an objective tag."""
    body: dict[str, Any] = {"name": name}
    if category_id is not None or category_name is not None:
        body["category"] = {"id": category_id, "name": category_name}
    return auth.post("/social/v1/objectives/tags", body=body)


@mcp.tool()
def objectives_create_tag_category(
    name: Annotated[str, "Category name"],
) -> Any:
    """Create an objective tag category."""
    return auth.post("/social/v1/objectives/tags/categories", body={"name": name})


@mcp.tool()
def objectives_update(
    objective_id: Annotated[str, "Objective ID"],
    body: Annotated[dict[str, Any], "Full objective object to replace"],
    period_id: Annotated[int | None, "Period ID"] = None,
) -> Any:
    """Update an objective."""
    return auth.put(f"/social/v1/objectives/{objective_id}", body=body, periodId=period_id)


@mcp.tool()
def objectives_update_key_result(
    key_result_id: Annotated[str, "Key result ID"],
    body: Annotated[dict[str, Any], "Full key result object to replace"],
) -> Any:
    """Update a key result."""
    return auth.put(f"/social/v1/objectives/key-results/{key_result_id}", body=body)


@mcp.tool()
def objectives_update_key_result_tags(
    key_result_id: Annotated[str, "Key result ID"],
    tag_ids: Annotated[list[int], "List of tag IDs to assign"],
    period_id: Annotated[int | None, "Period ID"] = None,
) -> Any:
    """Update the tags on a key result."""
    return auth.put(
        f"/social/v1/objectives/key-results/{key_result_id}/tags",
        body=tag_ids,
        periodId=period_id,
    )


@mcp.tool()
def objectives_update_tag(
    tag_id: Annotated[str, "Tag ID"],
    body: Annotated[dict[str, Any], "Tag update. Keys: id (int), name (str), category ({id, name})"],
) -> Any:
    """Update an objective tag."""
    return auth.put(f"/social/v1/objectives/tags/{tag_id}", body=body)


@mcp.tool()
def objectives_update_tag_category(
    category_id: Annotated[str, "Category ID"],
    body: Annotated[dict[str, Any], "Category update. Keys: id (int), name (str)"],
) -> Any:
    """Update an objective tag category."""
    return auth.put(f"/social/v1/objectives/tags/categories/{category_id}", body=body)


@mcp.tool()
def objectives_delete(
    objective_id: Annotated[str, "Objective ID to delete"],
) -> Any:
    """Delete an objective."""
    return auth.delete(f"/social/v1/objectives/{objective_id}")


@mcp.tool()
def objectives_delete_key_result(
    key_result_id: Annotated[str, "Key result ID to delete"],
) -> Any:
    """Delete a key result."""
    return auth.delete(f"/social/v1/objectives/key-results/{key_result_id}")


@mcp.tool()
def objectives_delete_tag(
    tag_id: Annotated[str, "Tag ID to delete"],
) -> Any:
    """Delete an objective tag."""
    return auth.delete(f"/social/v1/objectives/tags/{tag_id}")


@mcp.tool()
def objectives_delete_tag_category(
    category_id: Annotated[str, "Category ID to delete"],
) -> Any:
    """Delete an objective tag category."""
    return auth.delete(f"/social/v1/objectives/tags/categories/{category_id}")
