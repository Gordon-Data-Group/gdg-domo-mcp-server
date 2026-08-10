"""Bricks / Pro-Code Apps tools — custom app designs, instances, versions, file assets.

API reference: api-definitions-md/10-bricks-and-pro-code-apps.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="bricks", read_only=True)
def bricks_list_designs(
    check_admin_authority: Annotated[bool | None, "Check admin authority"] = None,
    creator: Annotated[str | None, "Filter by creator"] = None,
    deleted: Annotated[bool | None, "Include deleted designs"] = None,
    order: Annotated[str | None, "Sort field"] = None,
    direction: Annotated[str | None, "Sort direction"] = None,
    limit: Annotated[int | None, "Max results to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    search: Annotated[str | None, "Search term"] = None,
    with_permission: Annotated[str | None, "Filter by permission"] = None,
    parts: Annotated[str | None, "Comma-separated parts to include"] = None,
) -> Any:
    """List Bricks/Pro-Code app designs."""
    return auth.get(
        "/apps/v1/designs",
        checkAdminAuthority=check_admin_authority,
        creator=creator,
        deleted=deleted,
        order=order,
        direction=direction,
        limit=limit,
        offset=offset,
        search=search,
        withPermission=with_permission,
        parts=parts,
    )


@domo_tool(toolset="bricks", read_only=True)
def bricks_get_app(
    app_id: Annotated[str, "App instance ID"],
) -> Any:
    """Get a Bricks app instance by ID."""
    return auth.get(f"/domoapps/apps/v2/{app_id}")


@domo_tool(toolset="bricks", read_only=True)
def bricks_get_design(
    design_id: Annotated[str, "Design ID"],
    parts: Annotated[str | None, "Comma-separated parts to include"] = None,
) -> Any:
    """Get a Bricks app design by ID."""
    return auth.get(f"/apps/v1/designs/{design_id}", parts=parts)


@domo_tool(toolset="bricks", read_only=True)
def bricks_get_app_file(
    design_id: Annotated[str, "Design ID"],
    version_number: Annotated[str, "Version number (e.g. '0.0.1')"],
    file_path: Annotated[str | None, "File path within the design assets"] = None,
) -> Any:
    """Get a file asset from a Bricks app design version."""
    params: dict[str, Any] = {}
    if file_path is not None:
        params["path"] = file_path
    return auth.get(
        f"/v1/designs/{design_id}/versions/{version_number}/assets",
        **params,
    )


@domo_tool(toolset="bricks", read_only=True)
def bricks_get_app_version(
    design_id: Annotated[str, "Design ID"],
    version_number: Annotated[str, "Version number (e.g. '0.0.1')"],
) -> Any:
    """Get a specific version of a Bricks app design."""
    return auth.get(f"/v1/designs/{design_id}/versions/{version_number}")


@domo_tool(toolset="bricks", read_only=True)
def bricks_get_app_context(
    context_id: Annotated[str, "Context ID"],
) -> Any:
    """Get the context (dataset/account mappings) for a Bricks app."""
    return auth.get(f"/domoapps/apps/v2/contexts/{context_id}")


@domo_tool(toolset="bricks", read_only=True)
def bricks_count_designs(
    check_admin_authority: Annotated[bool | None, "Check admin authority"] = None,
    creator: Annotated[str | None, "Filter by creator"] = None,
    deleted: Annotated[bool | None, "Include deleted designs"] = None,
    search: Annotated[str | None, "Search term"] = None,
    with_permission: Annotated[str | None, "Filter by permission"] = None,
) -> Any:
    """Count Bricks/Pro-Code app designs."""
    return auth.get(
        "/apps/v1/designs/count",
        checkAdminAuthority=check_admin_authority,
        creator=creator,
        deleted=deleted,
        search=search,
        withPermission=with_permission,
    )


@domo_tool(toolset="bricks", read_only=False)
def bricks_create_instance(
    design_id: Annotated[str, "Design ID (UUID)"],
    design_version: Annotated[str, "Design version (e.g. '0.0.1')"],
    temporary: Annotated[bool | None, "Create as a temporary instance"] = None,
) -> Any:
    """Create a new Bricks app instance."""
    return auth.post(
        "/apps/v1/instances",
        body={"designId": design_id, "designVersion": design_version, "id": None},
        temporary=temporary,
    )


@domo_tool(toolset="bricks", read_only=False)
def bricks_share_design(
    design_id: Annotated[str, "Design ID"],
    permissions: Annotated[str, "Permission level to grant (e.g. 'READ')"],
    user_ids: Annotated[list[str], "List of user IDs to share with"],
) -> Any:
    """Share a Bricks app design with users."""
    return auth.post(
        f"/apps/v1/designs/{design_id}/permissions/{permissions}",
        body=user_ids,
    )


@domo_tool(toolset="bricks", read_only=False)
def bricks_update_app_file(
    design_id: Annotated[str, "Design ID"],
    version_number: Annotated[str, "Version number"],
    body: Annotated[
        dict[str, Any],
        "File metadata. Keys: id (str UUID), name (str), version (str), datasetsMapping (list), size ({width, height})",
    ],
    file_path: Annotated[str | None, "File path within the design assets"] = None,
) -> Any:
    """Update a file asset in a Bricks app design version."""
    params: dict[str, Any] = {}
    if file_path is not None:
        params["path"] = file_path
    return auth.post(
        f"/apps/v1/designs/{design_id}/versions/{version_number}/assets",
        body=body,
        **params,
    )


@domo_tool(toolset="bricks", read_only=False)
def bricks_update_instance(
    instance_id: Annotated[str, "Instance ID"],
    body: Annotated[
        dict[str, Any],
        (
            "Instance update. Keys: id, designId, designVersion, datasetsMapping, "
            "collectionsMapping, databasesMapping, accountsMapping, actionsMapping, "
            "workflowsMapping, packagesMapping, owner, createdBy, createdDate, "
            "updatedBy, updatedDate, disabled"
        ),
    ],
) -> Any:
    """Update a Bricks app instance's configuration."""
    return auth.put(f"/apps/v1/instances/{instance_id}", body=body)


@domo_tool(toolset="bricks", read_only=False)
def bricks_update_app_context(
    context_id: Annotated[str, "Context ID"],
    body: Annotated[
        dict[str, Any],
        (
            "Context update. Keys: id, designId, designVersion, mapping (list), "
            "collections (list), accountMapping (list), actionMapping (list), "
            "workflowMapping (list), packageMapping (list), isDisabled (bool)"
        ),
    ],
) -> Any:
    """Update the context (mappings) for a Bricks app."""
    return auth.put(f"/domoapps/apps/v2/contexts/{context_id}", body=body)


@domo_tool(toolset="bricks", read_only=False)
def bricks_delete_design_v1(
    design_id: Annotated[str, "Design ID to delete"],
) -> Any:
    """Delete a Bricks app design (apps/v1 endpoint)."""
    return auth.delete(f"/apps/v1/designs/{design_id}")


@domo_tool(toolset="bricks", read_only=False)
def bricks_delete_instance(
    instance_id: Annotated[str, "Instance ID to delete"],
) -> Any:
    """Delete a Bricks app instance."""
    return auth.delete(f"/apps/v1/instances/{instance_id}")


@domo_tool(toolset="bricks", read_only=False)
def bricks_restore_design(
    design_id: Annotated[str, "Design ID to restore from deleted state"],
) -> Any:
    """Restore a deleted Bricks app design."""
    return auth.put(f"/apps/v1/designs/{design_id}/undelete")
