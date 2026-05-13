"""Task Center tools — queue-based human task routing and completion.

API reference: api-definitions-md/33-task-center.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def task_center_list_queues(
    combine_attributes: Annotated[bool | None, "Combine attributes in the response"] = None,
    archived: Annotated[bool | None, "Include archived queues"] = None,
) -> Any:
    """List Task Center queues."""
    return auth.get("/queues/v1", combineAttributes=combine_attributes, archived=archived)


@mcp.tool()
def task_center_search_queues(
    body: Annotated[
        dict[str, Any],
        "Search body. Keys: query (str), entityList (e.g. [['queue']]), count (int), offset (int), sort, filters (list), useEntities (bool), combineResults (bool), facetValueLimit (int), hideSearchObjects (bool), state (str)",
    ],
) -> Any:
    """Search Task Center queues using the global search API."""
    return auth.post("/search/v1/query", body=body)


@mcp.tool()
def task_center_list_tasks(
    body: Annotated[
        dict[str, Any],
        "Task list filter. Keys: queueId (list), displayType (list), status (list), assignedBy (list), assignedTo (list), createdOn (list), createdBy (list), assignedOn (list), updatedOn (list), completedOn (list), completedBy (list), orderByString (list), version (list)",
    ],
    limit: Annotated[int | None, "Max tasks to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    render: Annotated[bool | None, "Include rendered form data"] = None,
    render_parts: Annotated[str | None, "Comma-separated parts to render"] = None,
    direction: Annotated[str | None, "Sort direction"] = None,
    order_by: Annotated[str | None, "Sort field"] = None,
) -> Any:
    """List tasks across queues with filters."""
    return auth.post(
        "/queues/v1/tasks/list",
        body=body,
        limit=limit,
        offset=offset,
        render=render,
        renderParts=render_parts,
        direction=direction,
        orderBy=order_by,
    )


@mcp.tool()
def task_center_get_queue(
    queue_id: Annotated[str, "Queue ID (UUID)"],
) -> Any:
    """Get a Task Center queue by ID."""
    return auth.get(f"/queues/v1/{queue_id}")


@mcp.tool()
def task_center_get_task(
    queue_id: Annotated[str, "Queue ID (UUID)"],
    task_id: Annotated[str, "Task ID"],
    render: Annotated[bool | None, "Include rendered form data"] = None,
) -> Any:
    """Get a specific task from a queue."""
    return auth.get(f"/queues/v1/{queue_id}/tasks/{task_id}", render=render)


@mcp.tool()
def task_center_save_task_progress(
    queue_id: Annotated[str, "Queue ID (UUID)"],
    task_id: Annotated[str, "Task ID"],
    outputs: Annotated[dict[str, Any], "Output variable key-value pairs to save"],
) -> Any:
    """Save progress on a Task Center task."""
    return auth.put(f"/queues/v1/{queue_id}/tasks/{task_id}/outputs", body=outputs)


@mcp.tool()
def task_center_complete_task(
    queue_id: Annotated[str, "Queue ID (UUID)"],
    task_id: Annotated[str, "Task ID"],
    version: Annotated[str | None, "Task version"] = None,
) -> Any:
    """Mark a Task Center task as complete."""
    return auth.post(
        f"/queues/v1/{queue_id}/tasks/{task_id}/complete",
        body={},
        version=version,
    )


@mcp.tool()
def task_center_transfer_to_queue(
    current_queue_id: Annotated[str, "Current queue ID (UUID)"],
    task_id: Annotated[str, "Task ID"],
    target_queue_id: Annotated[str, "Target queue ID to transfer to"],
) -> Any:
    """Transfer a task to another queue."""
    return auth.put(
        f"/queues/v1/{current_queue_id}/tasks/{task_id}/move",
        targetQueueId=target_queue_id,
    )


@mcp.tool()
def task_center_transfer_to_user(
    queue_id: Annotated[str, "Queue ID (UUID)"],
    task_id: Annotated[str, "Task ID"],
    type: Annotated[str, "Assignee type ('USER' or 'GROUP')"],
    user_id: Annotated[str, "User or group ID to assign to"],
    tasks_id: Annotated[list[str] | None, "Additional task IDs to transfer"] = None,
) -> Any:
    """Transfer a task to another user or group."""
    return auth.put(
        f"/queues/v1/{queue_id}/tasks/{task_id}/assign",
        body={"tasksId": tasks_id or [], "type": type, "userId": user_id},
    )


@mcp.tool()
def task_center_void_task(
    queue_id: Annotated[str, "Queue ID (UUID)"],
    task_id: Annotated[str, "Task ID"],
) -> Any:
    """Void a Task Center task."""
    return auth.post(f"/queues/v1/{queue_id}/tasks/{task_id}/void")


@mcp.tool()
def task_center_create_task(
    queue_id: Annotated[str, "Queue ID (UUID)"],
    body: Annotated[
        dict[str, Any],
        "Task definition. Keys: attributes, queueId, version, status, assigneeType, sourceSystem, sourceInfo, displayType, displayId, displayEntity, contract, inputVariables, outputVariables, etc.",
    ],
) -> Any:
    """Create a new task in a queue."""
    return auth.post(f"/queues/v1/{queue_id}/tasks", body=body)


@mcp.tool()
def task_center_update_queue_perms(
    queue_id: Annotated[str, "Queue ID (UUID)"],
    permissions: Annotated[
        list[dict[str, Any]],
        "Permission entries. Each: id (str), permissions (list of str), name (str), type (str 'USER' or 'GROUP')",
    ],
) -> Any:
    """Update permissions for a Task Center queue."""
    return auth.post(f"/queues/v1/{queue_id}/permissions", body=permissions)


@mcp.tool()
def task_center_update_queue_owner(
    queue_id: Annotated[str, "Queue ID (UUID)"],
    owner_id: Annotated[str, "New owner user ID"],
) -> Any:
    """Update the owner of a Task Center queue."""
    return auth.put(f"/queues/v1/{queue_id}/owner/{owner_id}")
