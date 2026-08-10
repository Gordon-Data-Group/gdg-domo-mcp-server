"""Projects & Tasks tools — project/task management, lists, attachments.

API reference: api-definitions-md/28-projects-and-tasks.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_list(
    limit: Annotated[int | None, "Max projects to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    status: Annotated[str | None, "Filter by status"] = None,
) -> Any:
    """List projects."""
    return auth.get("/content/v1/projects", limit=limit, offset=offset, status=status)


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_list_tags(
    q: Annotated[str | None, "Search query for tags"] = None,
) -> Any:
    """List task tags."""
    return auth.get("/content/v1/tags", q=q)


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_get_for_user(
    user_id: Annotated[str, "User ID"],
    limit: Annotated[int | None, "Max projects to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    status: Annotated[str | None, "Filter by status"] = None,
) -> Any:
    """Get projects for a specific user."""
    return auth.get(
        f"/content/v2/users/{user_id}/projects",
        limit=limit,
        offset=offset,
        status=status,
    )


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_get_tasks(
    project_id: Annotated[str, "Project ID"],
    search: Annotated[str | None, "Search term"] = None,
    archived: Annotated[bool | None, "Include archived tasks"] = None,
    assigned_to_owner_id: Annotated[int | None, "Filter by assignee user ID"] = None,
) -> Any:
    """Get tasks for a project."""
    return auth.get(
        f"/content/v1/projects/{project_id}/tasks",
        search=search,
        archived=archived,
        assignedToOwnerId=assigned_to_owner_id,
    )


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_get_list_tasks(
    project_id: Annotated[str, "Project ID"],
    list_id: Annotated[str, "List ID"],
    fields: Annotated[str | None, "Comma-separated fields to include"] = None,
) -> Any:
    """Get tasks in a specific project list."""
    return auth.get(
        f"/content/v1/projects/{project_id}/lists/{list_id}/tasks",
        fields=fields,
    )


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_get_user_task_assign(
    user_id: Annotated[str, "User ID"],
    limit: Annotated[int | None, "Max results to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    status: Annotated[str | None, "Filter by status"] = None,
) -> Any:
    """Get task assignments for a user."""
    return auth.get(
        f"/content/v2/users/{user_id}/tasks/assignments",
        limit=limit,
        offset=offset,
        status=status,
    )


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_get_lists(
    project_id: Annotated[str, "Project ID"],
    archived: Annotated[bool | None, "Include archived lists"] = None,
) -> Any:
    """Get lists for a project."""
    return auth.get(f"/content/v1/projects/{project_id}/lists", archived=archived)


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_get_project_tags(
    project_id: Annotated[str, "Project ID"],
    archived: Annotated[bool | None, "Include archived tags"] = None,
) -> Any:
    """Get tags for a project."""
    return auth.get(f"/content/v1/projects/{project_id}/tags", archived=archived)


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_get(
    project_id: Annotated[str, "Project ID"],
) -> Any:
    """Get a project by ID."""
    return auth.get(f"/content/v1/projects/{project_id}")


@domo_tool(toolset="projects_tasks", read_only=True)
def projects_get_task(
    task_id: Annotated[str, "Task ID"],
) -> Any:
    """Get a task by ID."""
    return auth.get(f"/content/v1/tasks/{task_id}")


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_create(
    body: Annotated[
        dict[str, Any],
        "Project definition. Keys: projectName (str), description (str), invalidProjectName (bool), hidden (bool), members (list of int), dueDate (int epoch ms)",
    ],
) -> Any:
    """Create a new project."""
    return auth.post("/content/v1/projects", body=body)


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_create_task(
    project_id: Annotated[str, "Project ID"],
    list_id: Annotated[str, "List ID"],
    body: Annotated[
        dict[str, Any],
        "Task definition. Keys: id (int), taskName (str), disabled (bool), owners (list of {assignedTo: int}), priority (int)",
    ],
) -> Any:
    """Create a task in a project list."""
    return auth.post(
        f"/content/v1/projects/{project_id}/lists/{list_id}/tasks",
        body=body,
    )


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_create_user_task(
    user_id: Annotated[str, "User ID"],
    body: Annotated[
        dict[str, Any],
        "Task definition. Keys: attachments (list), realProjectListId, tags (list of {tag}), contributors (list of {assignedTo}), taskName (str), dueDate (int), primaryTaskOwner (int), description (str)",
    ],
) -> Any:
    """Create a personal task for a user."""
    return auth.post(f"/content/v2/users/{user_id}/tasks", body=body)


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_create_list(
    project_id: Annotated[str, "Project ID"],
    name: Annotated[str, "List name"],
    type: Annotated[str | None, "List type (e.g. 'complete', 'todo')"] = None,
    list_order: Annotated[int | None, "List display order"] = None,
) -> Any:
    """Create a new list in a project."""
    body: dict[str, Any] = {"name": name}
    if type is not None:
        body["type"] = type
    if list_order is not None:
        body["listOrder"] = list_order
    return auth.post(f"/content/v1/projects/{project_id}/lists", body=body)


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_create_task_attachment(
    task_id: Annotated[str, "Task ID"],
    data_file_id: Annotated[int, "File ID to attach"],
    name: Annotated[str, "Attachment name"],
    type: Annotated[str, "Attachment type"],
    preview_image: Annotated[str | None, "Base64-encoded preview image (data:<mime>;base64,<data>)"] = None,
) -> Any:
    """Attach a file to a task."""
    body: dict[str, Any] = {"dataFileId": data_file_id, "name": name, "type": type}
    if preview_image is not None:
        body["previewImage"] = preview_image
    return auth.post(f"/content/v1/tasks/{task_id}/attachments", body=body)


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_update(
    project_id: Annotated[str, "Project ID"],
    body: Annotated[dict[str, Any], "Full project object to replace"],
) -> Any:
    """Update a project."""
    return auth.put(f"/content/v1/projects/{project_id}", body=body)


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_update_task(
    task_id: Annotated[str, "Task ID"],
    body: Annotated[dict[str, Any], "Full task object to replace"],
) -> Any:
    """Update a task."""
    return auth.put(f"/content/v1/tasks/{task_id}", body=body)


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_update_list(
    project_id: Annotated[str, "Project ID"],
    list_id: Annotated[str, "List ID"],
    body: Annotated[dict[str, Any], "Full list object to replace"],
) -> Any:
    """Update a project list."""
    return auth.put(f"/content/v1/projects/{project_id}/lists/{list_id}", body=body)


@domo_tool(toolset="projects_tasks", read_only=False)
def projects_delete(
    project_id: Annotated[str, "Project ID to delete"],
) -> Any:
    """Delete a project."""
    return auth.delete(f"/content/v1/projects/{project_id}")
