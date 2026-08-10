"""Functions (Beast Modes & Variables) tools — calculated field CRUD.

API reference: api-definitions-md/23-functions-beast-modes-and-variables-.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="functions", read_only=True)
def functions_list(
    body: Annotated[
        dict[str, Any],
        "Search body. Keys: name (str), filters (list), sort ({field, ascending}), limit (int), offset (int)",
    ],
) -> Any:
    """List/search beast mode functions."""
    return auth.post("/query/v1/functions/search", body=body)


@domo_tool(toolset="functions", read_only=True)
def functions_get_bulk(
    ids: Annotated[list[str], "List of function IDs to fetch"],
) -> Any:
    """Get multiple functions by ID."""
    return auth.post("/query/v1/functions/list/id", body={"ids": ids})


@domo_tool(toolset="functions", read_only=True)
def functions_get(
    function_id: Annotated[str, "Function ID"],
    hidden: Annotated[bool | None, "Include hidden functions"] = None,
) -> Any:
    """Get a function by ID."""
    return auth.get(f"/query/v1/functions/template/{function_id}", hidden=hidden)


@domo_tool(toolset="functions", read_only=True)
def functions_get_card_usage(
    datasource_id: Annotated[str | None, "Dataset ID to filter by"] = None,
    formula_id: Annotated[str | None, "Function ID to filter by"] = None,
) -> Any:
    """Get the cards that use a specific function."""
    return auth.get(
        "/content/v2/cards/formulausage",
        datasourceId=datasource_id,
        formulaId=formula_id,
    )


@domo_tool(toolset="functions", read_only=False)
def functions_create(
    body: Annotated[
        dict[str, Any],
        (
            "Function definition. Keys: name (str), owner (int), locked (bool), global (bool), "
            "expression (str SQL), checkSum, links (list), aggregated (bool), analytic (bool), "
            "nonAggregatedColumns (list), dataType (str), status (str), cacheWindow (str), "
            "columnPositions (list), functions (list), functionTemplateDependencies (list), "
            "archived (bool), hidden (bool), variable (bool)"
        ),
    ],
    strict: Annotated[bool | None, "Strict validation mode"] = None,
) -> Any:
    """Create a new beast mode function."""
    return auth.post("/query/v1/functions/template", body=body, strict=strict)


@domo_tool(toolset="functions", read_only=False)
def functions_update(
    function_id: Annotated[str, "Function ID"],
    body: Annotated[
        dict[str, Any],
        "Function update. Keys: expression (str), id (int), name (str), status (str), persistedOnDataSource (bool), archived (bool), certification (dict)",
    ],
    strict: Annotated[bool | None, "Strict validation mode"] = None,
) -> Any:
    """Update a beast mode function."""
    return auth.put(f"/query/v1/functions/template/{function_id}", body=body, strict=strict)


@domo_tool(toolset="functions", read_only=False)
def functions_lock(
    function_id: Annotated[str, "Function ID"],
    locked: Annotated[bool, "True to lock, False to unlock"],
) -> Any:
    """Lock or unlock a beast mode function."""
    return auth.put(f"/query/v1/functions/template/{function_id}", body={"locked": locked})


@domo_tool(toolset="functions", read_only=False)
def functions_delete(
    function_id: Annotated[str, "Function ID to delete"],
) -> Any:
    """Delete a beast mode function."""
    return auth.delete(f"/query/v1/functions/template/{function_id}")


@domo_tool(toolset="functions", read_only=False)
def functions_bulk_delete(
    function_ids: Annotated[list[int], "List of function IDs to delete"],
) -> Any:
    """Bulk delete beast mode functions."""
    return auth.post("/query/v1/functions/bulk/template", body={"delete": function_ids})
