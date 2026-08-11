"""FileSets tools — file collections with folder structure, search, AI query.

API reference: api-definitions-md/21-filesets.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="filesets", read_only=True)
def filesets_list(
    body: Annotated[
        dict[str, Any],
        "Search filter. Keys: fieldSort (list of {field, order}), filters (list), dateFilters (list)",
    ],
    limit: Annotated[int | None, "Max filesets to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List/search filesets."""
    return auth.post("/files/v1/filesets/search", body=body, limit=limit, offset=offset)


@domo_tool(toolset="filesets", read_only=True)
def filesets_search_files(
    fileset_id: Annotated[str, "Fileset ID"],
    body: Annotated[
        dict[str, Any],
        "Search filter. Keys: fieldSort (list of {field, order}), filters (list), dateFilters (list)",
    ],
    directory_path: Annotated[str | None, "Directory path to search within"] = None,
    immediate_children: Annotated[bool | None, "Return only immediate children"] = None,
    limit: Annotated[int | None, "Max files to return"] = None,
    next: Annotated[str | None, "Pagination cursor"] = None,
) -> Any:
    """Search files in a fileset."""
    return auth.post(
        f"/files/v1/filesets/{fileset_id}/files/search",
        body=body,
        directoryPath=directory_path,
        immediateChildren=immediate_children,
        limit=limit,
        next=next,
    )


@domo_tool(toolset="filesets", read_only=True)
def filesets_query_with_ai(
    fileset_id: Annotated[str, "Fileset ID"],
    query: Annotated[str, "Natural language query"],
    directory_path: Annotated[str | None, "Directory path to scope the query"] = None,
    top_k: Annotated[int | None, "Number of results to return"] = None,
) -> Any:
    """Query fileset files using AI."""
    body: dict[str, Any] = {"query": query}
    if directory_path is not None:
        body["directoryPath"] = directory_path
    if top_k is not None:
        body["topK"] = top_k
    return auth.post(f"/files/v1/filesets/{fileset_id}/query", body=body)


@domo_tool(toolset="filesets", read_only=True)
def filesets_get(
    fileset_id: Annotated[str, "Fileset ID"],
) -> Any:
    """Get a fileset by ID."""
    return auth.get(f"/files/v1/filesets/{fileset_id}")


@domo_tool(toolset="filesets", read_only=True)
def filesets_get_file(
    fileset_id: Annotated[str, "Fileset ID"],
    file_id: Annotated[str, "File ID"],
) -> Any:
    """Get a file from a fileset by ID."""
    return auth.get(f"/files/v1/filesets/{fileset_id}/files/{file_id}")


@domo_tool(toolset="filesets", read_only=True)
def filesets_get_file_by_path(
    fileset_id: Annotated[str, "Fileset ID"],
    path: Annotated[str, "File path within the fileset"],
) -> Any:
    """Get a file from a fileset by path."""
    return auth.get(f"/files/v1/filesets/{fileset_id}/path", path=path)


@domo_tool(toolset="filesets", read_only=True)
def filesets_get_access(
    fileset_id: Annotated[str, "Fileset ID"],
) -> Any:
    """Get access permissions for a fileset."""
    return auth.get(f"/files/v1/filesets/{fileset_id}/access")


@domo_tool(toolset="filesets", read_only=True)
def filesets_get_stats(
    fileset_id: Annotated[str, "Fileset ID"],
) -> Any:
    """Get storage statistics for a fileset."""
    return auth.get(f"/files/v1/filesets/{fileset_id}/stats")


@domo_tool(toolset="filesets", read_only=True)
def filesets_download_file(
    fileset_id: Annotated[str, "Fileset ID"],
    file_id: Annotated[str, "File ID"],
) -> Any:
    """Download a file from a fileset."""
    return auth.get(f"/files/v1/filesets/{fileset_id}/files/{file_id}/download")


@domo_tool(toolset="filesets", read_only=True)
def filesets_download_file_by_path(
    fileset_id: Annotated[str, "Fileset ID"],
    path: Annotated[str, "File path within the fileset"],
) -> Any:
    """Download a file from a fileset by path."""
    return auth.get(f"/files/v1/filesets/{fileset_id}/path/download", path=path)


@domo_tool(toolset="filesets", read_only=False)
def filesets_create(
    name: Annotated[str, "Fileset name"],
    description: Annotated[str | None, "Fileset description"] = None,
    ai_enabled: Annotated[bool | None, "Enable AI querying on this fileset"] = None,
    batch_type: Annotated[str | None, "Batch type (e.g. 'INCREMENTAL')"] = None,
    connector: Annotated[str | None, "Connector type (e.g. 'DOMO')"] = None,
    account_id: Annotated[str | None, "Account ID for the connector"] = None,
) -> Any:
    """Create a new fileset."""
    body: dict[str, Any] = {"name": name}
    if description is not None:
        body["description"] = description
    if ai_enabled is not None:
        body["aiEnabled"] = ai_enabled
    if batch_type is not None:
        body["batchType"] = batch_type
    if connector is not None:
        body["connector"] = connector
    if account_id is not None:
        body["accountId"] = account_id
    return auth.post("/files/v1/filesets", body=body)


@domo_tool(toolset="filesets", read_only=False)
def filesets_create_folder(
    fileset_id: Annotated[str, "Fileset ID"],
    directory_path: Annotated[str, "Path for the new folder"],
) -> Any:
    """Create a folder in a fileset."""
    return auth.post(
        f"/files/v1/filesets/{fileset_id}/files",
        body={"directoryPath": directory_path},
    )


@domo_tool(toolset="filesets", read_only=False)
def filesets_upload_file(
    fileset_id: Annotated[str, "Fileset ID"],
) -> Any:
    """Upload a file to a fileset (returns the upload endpoint details)."""
    return auth.post(f"/files/v1/filesets/{fileset_id}/files")


@domo_tool(toolset="filesets", read_only=False)
def filesets_update(
    fileset_id: Annotated[str, "Fileset ID"],
    name: Annotated[str | None, "New fileset name"] = None,
    description: Annotated[str | None, "New fileset description"] = None,
    ai_enabled: Annotated[bool | None, "Enable or disable AI querying"] = None,
) -> Any:
    """Update a fileset's metadata."""
    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if description is not None:
        body["description"] = description
    if ai_enabled is not None:
        body["aiEnabled"] = ai_enabled
    return auth.post(f"/files/v1/filesets/{fileset_id}", body=body)


@domo_tool(toolset="filesets", read_only=False)
def filesets_update_access(
    fileset_id: Annotated[str, "Fileset ID"],
    file_set_access: Annotated[
        list[dict[str, Any]],
        "List of access entries, each with entityId (int), entityType (str), permission (str)",
    ],
) -> Any:
    """Update access permissions for a fileset."""
    return auth.post(
        f"/files/v1/filesets/{fileset_id}/access",
        body={"fileSetAccess": file_set_access},
    )


@domo_tool(toolset="filesets", read_only=False)
def filesets_update_owner(
    fileset_id: Annotated[str, "Fileset ID"],
    user_id: Annotated[int, "New owner user ID"],
) -> Any:
    """Update the owner of a fileset."""
    return auth.post(
        f"/files/v1/filesets/{fileset_id}/ownership",
        body={"userId": user_id},
    )


@domo_tool(toolset="filesets", read_only=False)
def filesets_delete(
    fileset_id: Annotated[str, "Fileset ID to delete"],
) -> Any:
    """Delete a fileset."""
    return auth.delete(f"/files/v1/filesets/{fileset_id}")


@domo_tool(toolset="filesets", read_only=False)
def filesets_delete_file(
    fileset_id: Annotated[str, "Fileset ID"],
    file_id: Annotated[str, "File ID to delete"],
) -> Any:
    """Delete a file from a fileset."""
    return auth.delete(f"/files/v1/filesets/{fileset_id}/files/{file_id}")


@domo_tool(toolset="filesets", read_only=False)
def filesets_delete_file_by_path(
    fileset_id: Annotated[str, "Fileset ID"],
    path: Annotated[str, "File path to delete"],
) -> Any:
    """Delete a file from a fileset by path."""
    return auth.delete(f"/files/v1/filesets/{fileset_id}/path", path=path)
