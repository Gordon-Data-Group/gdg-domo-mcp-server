"""Code Engine tools — serverless function packages and execution.

API reference: api-definitions-md/14-code-engine.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="code_engine", read_only=True)
def code_engine_search_packages(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: query (str), entityList (e.g. [['package']]), count (int), "
            "offset (int), sort ({isRelevance, fieldSorts}), filters (list), "
            "useEntities (bool), combineResults (bool), facetValueLimit (int), "
            "hideSearchObjects (bool), state (str)"
        ),
    ],
) -> Any:
    """Search Code Engine packages using the global search API."""
    return auth.post("/search/v1/query", body=body)


@domo_tool(toolset="code_engine", read_only=True)
def code_engine_get_package(
    package_id: Annotated[str, "Package ID (UUID)"],
    parts: Annotated[str | None, "Comma-separated parts to include"] = None,
) -> Any:
    """Get a Code Engine package by ID."""
    return auth.get(f"/codeengine/v2/packages/{package_id}", parts=parts)


@domo_tool(toolset="code_engine", read_only=True)
def code_engine_get_package_version(
    package_id: Annotated[str, "Package ID (UUID)"],
    version: Annotated[str, "Version string (e.g. '1.0.0')"],
    parts: Annotated[str | None, "Comma-separated parts to include"] = None,
) -> Any:
    """Get a specific version of a Code Engine package."""
    return auth.get(
        f"/codeengine/v2/packages/{package_id}/versions/{version}",
        parts=parts,
    )


@domo_tool(toolset="code_engine", read_only=True)
def code_engine_get_package_permissions(
    package_id: Annotated[str, "Package ID (UUID)"],
) -> Any:
    """Get permissions for a Code Engine package."""
    return auth.get(f"/codeengine/v2/packages/{package_id}/permissions")


@domo_tool(toolset="code_engine", read_only=False)
def code_engine_run_function(
    package_id: Annotated[str, "Package ID (UUID)"],
    version: Annotated[str, "Package version (e.g. '1.0.0')"],
    function: Annotated[str, "Function name to invoke"],
    input_variables: Annotated[dict[str, Any] | None, "Input variable key-value pairs"] = None,
    get_logs: Annotated[bool | None, "Return execution logs"] = None,
) -> Any:
    """Run a function from a Code Engine package."""
    body: dict[str, Any] = {}
    if input_variables is not None:
        body["inputVariables"] = input_variables
    if get_logs is not None:
        body["settings"] = {"getLogs": get_logs}
    return auth.post(
        f"/codeengine/v2/packages/{package_id}/versions/{version}/functions/{function}",
        body=body,
    )


@domo_tool(toolset="code_engine", read_only=False)
def code_engine_deploy_package(
    package_id: Annotated[str, "Package ID (UUID)"],
    version: Annotated[str, "Version to release (e.g. '1.0.0')"],
) -> Any:
    """Release (deploy) a version of a Code Engine package."""
    return auth.post(
        f"/codeengine/v2/packages/{package_id}/versions/{version}/release"
    )


@domo_tool(toolset="code_engine", read_only=False)
def code_engine_update_package(
    body: Annotated[
        dict[str, Any],
        (
            "Package definition. Keys: name (str), version (str), code (str), "
            "environment (str e.g. 'LAMBDA'), id (str UUID), language (str e.g. 'JAVASCRIPT'), "
            "manifest ({functions: [...], configuration: {accountsMapping: [...]}})"
        ),
    ],
) -> Any:
    """Create or update a Code Engine package."""
    return auth.post("/codeengine/v2/packages", body=body)


@domo_tool(toolset="code_engine", read_only=False)
def code_engine_update_package_owner(
    package_id: Annotated[str, "Package ID (UUID)"],
    owner: Annotated[int, "New owner user ID"],
) -> Any:
    """Update the owner of a Code Engine package."""
    return auth.put(
        f"/codeengine/v2/packages/{package_id}",
        body={"owner": owner},
    )


@domo_tool(toolset="code_engine", read_only=False)
def code_engine_update_package_perms(
    package_id: Annotated[str, "Package ID (UUID)"],
    permissions: Annotated[
        list[dict[str, Any]],
        "List of permission entries, each with id (str), name (str), type (str), permissions (list of str)",
    ],
) -> Any:
    """Update permissions for a Code Engine package."""
    return auth.post(
        f"/codeengine/v2/packages/{package_id}/permissions",
        body=permissions,
    )
