"""DataFlows tools — ETL/ELT flow management, execution, tags.

API reference: api-definitions-md/16-dataflows.md

Preferred dataflow type: MagicETL (databaseType='MAGIC'). Avoid MySQL dataflows.
See dataflows_create for full MagicETL action node documentation.
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def dataflows_search(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: entities (list e.g. ['DATAFLOW']), filters (list), "
            "combineResults (bool), query (str), count (int), offset (int), "
            "sort ({isRelevance, fieldSorts})"
        ),
    ],
) -> Any:
    """Search DataFlows using the global search API."""
    return auth.post("/search/v1/query", body=body)


@mcp.tool()
def dataflows_list(
    limit: Annotated[int | None, "Max DataFlows to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    order_by: Annotated[str | None, "Sort field"] = None,
) -> Any:
    """List DataFlows."""
    return auth.get("/dataprocessing/v2/dataflows", limit=limit, offset=offset, orderBy=order_by)


@mcp.tool()
def dataflows_list_versions(
    dataflow_id: Annotated[str, "DataFlow ID"],
) -> Any:
    """List versions of a DataFlow."""
    return auth.get(f"/dataprocessing/v1/dataflows/{dataflow_id}/versions")


@mcp.tool()
def dataflows_get(
    dataflow_id: Annotated[str, "DataFlow ID"],
) -> Any:
    """Get a DataFlow by ID."""
    return auth.get(f"/dataprocessing/v2/dataflows/{dataflow_id}")


@mcp.tool()
def dataflows_get_version(
    dataflow_id: Annotated[str, "DataFlow ID"],
    version_id: Annotated[str, "Version ID"],
) -> Any:
    """Get a specific version of a DataFlow by version ID."""
    return auth.get(f"/dataprocessing/v2/dataflows/{dataflow_id}/versions/{version_id}")


@mcp.tool()
def dataflows_get_version_by_number(
    dataflow_id: Annotated[str, "DataFlow ID"],
    version_number: Annotated[str, "Version number"],
) -> Any:
    """Get a specific version of a DataFlow by version number."""
    return auth.get(f"/dataprocessing/v3/dataflows/{dataflow_id}/versions/{version_number}")


@mcp.tool()
def dataflows_get_executions(
    dataflow_id: Annotated[str, "DataFlow ID"],
    limit: Annotated[int | None, "Max executions to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """Get execution history for a DataFlow."""
    return auth.get(
        f"/dataprocessing/v1/dataflows/{dataflow_id}/executions",
        limit=limit,
        offset=offset,
    )


@mcp.tool()
def dataflows_get_execution(
    dataflow_id: Annotated[str, "DataFlow ID"],
    execution_id: Annotated[str, "Execution ID"],
) -> Any:
    """Get a specific execution of a DataFlow."""
    return auth.get(
        f"/dataprocessing/v1/dataflows/{dataflow_id}/executions/{execution_id}"
    )


@mcp.tool()
def dataflows_get_tags(
    dataflow_id: Annotated[str, "DataFlow ID"],
) -> Any:
    """Get the tags (subscription info) for a DataFlow."""
    return auth.get(f"/dataprocessing/v1/dataflows/{dataflow_id}/subscription")


@mcp.tool()
def dataflows_get_saved_filters(
    query_profile: Annotated[str | None, "Query profile filter"] = None,
) -> Any:
    """Get saved datacenter search filters."""
    return auth.get("/search/v1/saved", queryProfile=query_profile)


@mcp.tool()
def dataflows_get_timezones() -> Any:
    """Get available timezones for DataFlows."""
    return auth.get("/dataprocessing/v1/dataflows/timezones")


@mcp.tool()
def dataflows_get_sql_functions() -> Any:
    """Get available SQL functions for DataFlow expressions."""
    return auth.get("/dataprocessing/v1/expression-docs")


@mcp.tool()
def dataflows_count_by_type() -> Any:
    """Count DataFlows grouped by type."""
    return auth.get("/dataprocessing/v2/dataflows/filters/dataflowType")


@mcp.tool()
def dataflows_run(
    dataflow_id: Annotated[str, "DataFlow ID to run"],
    activation_type_override: Annotated[str | None, "Activation type override"] = None,
    create_pending_execution: Annotated[bool | None, "Create a pending execution"] = None,
) -> Any:
    """Trigger a DataFlow execution."""
    return auth.post(
        f"/dataprocessing/v1/dataflows/{dataflow_id}/executions",
        activationTypeOverride=activation_type_override,
        createPendingExecution=create_pending_execution,
    )


@mcp.tool()
def dataflows_bulk_run(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs to run"],
) -> Any:
    """Trigger multiple DataFlow executions."""
    return auth.post(
        "/dataprocessing/v1/dataflows/bulk/execute",
        body={"dataFlowIds": dataflow_ids},
    )


@mcp.tool()
def dataflows_run_preview(
    body: Annotated[
        dict[str, Any],
        "Preview body. Keys: databaseType (str), engineProperties (dict), actions (list), settings ({zoneId})",
    ],
) -> Any:
    """Run a DataFlow preview without persisting results."""
    return auth.post("/dataprocessing/v1/dataflows/previews/run", body=body)


@mcp.tool()
def dataflows_create(
    body: Annotated[
        dict[str, Any],
        (
            "Full DataFlow definition. Required keys: name (str), databaseType (str), actions (list). "
            "Optional top-level keys: description, engineProperties, gui, inputs, outputs, settings, triggerSettings. "
            "--- MagicETL v2 (ALWAYS prefer over MySQL for new dataflows): --- "
            "Set databaseType='MAGIC', engineProperties={'kettle.mode':'STRICT'}, settings={'sqlDialect':'MAGIC'}. "
            "Optionally add useGraphUI=true for the newer canvas UI. "
            "Each action node requires: type (str), id (str UUID, or prefix with type e.g. 'LoadFromVault-<uuid>'), "
            "name (str), dependsOn (list of upstream action IDs). "
            "New actions support settings={'preferredDatabaseEntityType':'TEMP_VIEW'} for better performance. "
            "--- Action types (16 total): --- "
            "LoadFromVault — load an input dataset. Fields: dataSourceId (str), executeFlowWhenUpdated (bool). "
            "  Optional: propagateAi (bool), filterPolicy ('LEGACY'), truncateTextColumns (bool), "
            "  truncateRows (bool), onlyLoadNewVersions (bool), recentVersionCutoffMs (int), "
            "  sourceType ('AUTO'), previewRowLimit (int). "
            "ExpressionEvaluator — add computed columns using SQL expressions. Fields: input (upstream action ID), "
            "  expressions (list of {expression: 'SQL expr', fieldName: 'col', settings: {}}). "
            "  Available: SUBSTRING_INDEX, DATEDIFF([unit,]e1,e2), DATE, YEAR, MONTH, MONTHNAME, DAYNAME, "
            "  DAYOFWEEK, HOUR, CASE WHEN, CONCAT, TRIM, standard arithmetic. "
            "  System vars: @@DX_DATAFLOW_NAME, @@DX_DATAFLOW_ID, @@DX_ACTION_NAME. "
            "  NOT in STRICT mode: LOCATE, TIMESTAMPDIFF. "
            "Metadata — rename, drop, or cast columns. Fields: input (action ID), "
            "  fields (list of {name: str, rename: str|null, type: 'STRING'|'LONG'|'DOUBLE'|'DATE'|null, "
            "  dateFormat: str|null, remove: bool}). "
            "MergeJoin — join two upstream steps. Fields: step1 (action ID), step2 (action ID), "
            "  joinType ('LEFT OUTER'|'INNER'|'RIGHT OUTER'|'FULL OUTER'), "
            "  relationshipType ('ONE_TO_ONE'|'ONE_TO_MANY'|'MANY_TO_ONE'|'MANY_TO_MANY'), "
            "  keys1 (join column names from step1), keys2 (join column names from step2). "
            "  Optional: schemaModification1/schemaModification2 (list of {name, rename, remove}) to rename/drop "
            "  columns from each side inline. IMPORTANT: all column name conflicts between step1 and step2 must be "
            "  resolved before the join (via Metadata or schemaModification) or execution fails with DP-0008. "
            "UnionAll — stack rows from multiple steps. Fields: inputs (list of action IDs), "
            "  unionType ('INCLUDE_ALL' keep all cols | 'INCLUDE_FROM' use schemaSource cols), "
            "  schemaSource (action ID whose schema to use), strict (bool, false = coerce types). "
            "Filter — keep rows matching a condition. Fields: input (action ID), "
            "  filterList (list of filter objects). Structured filter: {leftField: 'col', "
            "  operator: 'EQ'|'NE'|'GT'|'GE'|'LT'|'LE'|'CONTAINS'|'NOT_CONTAINS'|'IS_NULL'|'IS_NOT_NULL', "
            "  rightValue: {value: 'x', type: 'STRING'|'LONG'|'DOUBLE'|'DATE'}, andFilterList: []}. "
            "  Expression filter: {expression: 'SQL_EXPR', andFilterList: []}. "
            "SelectValues — select and reorder columns. Fields: input (action ID), "
            "  fields (list of {name, rename, type, dateFormat, settings, remove: false}). "
            "  Only listed columns pass through. "
            "GroupBy — aggregate rows. Fields: input (action ID), groups (list of {name} for GROUP BY cols), "
            "  fields (list of {name: 'output_col', source: 'input_col', "
            "  type: 'SUM'|'COUNT'|'AVG'|'MIN'|'MAX'|'FIRST'|'LAST'|'COUNT_DISTINCT'|'COUNT_ALL', "
            "  expression: 'SUM(col)'}). Optional: addLineNumber (bool), giveBackRow (bool), allRows (bool). "
            "WindowAction — window/analytic functions. Fields: input (action ID), "
            "  groupRules (list of {column, caseSensitive} PARTITION BY), "
            "  orderRules (list of {column, caseSensitive, ascending} ORDER BY), "
            "  additions (list of window column defs). Framed: {name, operation: {type: 'FRAMED', "
            "  operationType: 'SUM'|'AVG'|'MIN'|'MAX'|'COUNT', column, preceding: int, following: int}}. "
            "  Ranking: {name, operation: {type: 'RANKING', operationType: 'RANK'|'ROW_NUMBER'|'DENSE_RANK'}}. "
            "Denormaliser — pivot row values into columns. Fields: input (action ID), "
            "  keyField (column whose distinct values become new column names), "
            "  group (list of {name} for row grouping cols), "
            "  fields (list of {fieldName: 'agg_col', keyValue: 'pivot_val', targetName: 'new_col', targetType}). "
            "Unique — deduplicate rows. Fields: input (action ID), "
            "  fields (list of {name, caseInsensitive: false} columns to deduplicate on). "
            "  Optional: countRows (bool, add a count column instead of deduplicating). "
            "Constant — add a constant-value column. Fields: input (action ID), "
            "  fields (list of {type: 'STRING'|'LONG'|'DOUBLE'|'DATE', name: 'col', value: 'x', expr: null}). "
            "SQL — raw SQL transformation. Fields: inputs (list of upstream action IDs), "
            "  statements (list of SQL strings), settings: {sqlDialect: 'MAGIC'}, columnSettings: {}. "
            "  Reference upstream steps by their action name in backticks, e.g. SELECT * FROM `step_name`. "
            "PythonEngineAction — PREMIUM FEATURE: do NOT use unless the user explicitly requests it. "
            "  Run a Python script. Fields: inputs (list of action IDs), "
            "  condaEnv ('domo-2'), script (Python code string), "
            "  additions (list of {name: 'output_col', dataType: 'STRING'|'LONG'|'DOUBLE'|'DATE'}), "
            "  removeByDefault (bool, true = output only additions cols), fillMissingWithNull (bool). "
            "  Use domomagic package: read_dataframe('action_name') and write_dataframe(df). "
            "MLInferenceAction — apply an AutoML model. Fields: input (action ID), "
            "  mlModelId (int), includeInputData (bool), inferenceColumnRename (str), columnSettings: {}. "
            "PublishToVault — write output dataset. Fields: inputs (list of action IDs), "
            "  dataSource ({guid: str, type: 'DataFlow', name: str, cloudId: 'domo'}), "
            "  versionChainType ('REPLACE'|'APPEND'), schemaSource ('DATAFLOW'). "
            "  Use existing dataset guid to update it, or a new UUID to create a new dataset. "
            "  For partitioned append: partitioned: true, partitionIdColumns: ['col']."
        ),
    ],
) -> Any:
    """Create a new DataFlow. Prefer MagicETL (databaseType='MAGIC') over MySQL for all new dataflows."""
    return auth.post("/dataprocessing/v1/dataflows", body=body)


@mcp.tool()
def dataflows_add_tag(
    dataflow_id: Annotated[str, "DataFlow ID"],
    tag: Annotated[str, "Tag name to add"],
) -> Any:
    """Add a single tag to a DataFlow."""
    return auth.post(
        f"/dataprocessing/v1/dataflows/{dataflow_id}/tags",
        body={"tag": tag},
    )


@mcp.tool()
def dataflows_bulk_add_tags(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs"],
    tag_names: Annotated[list[str], "List of tag names to add"],
) -> Any:
    """Add tags to multiple DataFlows."""
    return auth.put(
        "/dataprocessing/v1/dataflows/bulk/tag",
        body={"dataFlowIds": dataflow_ids, "tagNames": tag_names},
    )


@mcp.tool()
def dataflows_update(
    dataflow_id: Annotated[str, "DataFlow ID"],
    body: Annotated[
        dict[str, Any],
        (
            "Full DataFlow definition with id. Keys: id (int, required), name, actions, gui, inputs, outputs, "
            "settings, triggerSettings, databaseType, engineProperties, dapDataFlowId, responsibleUserId, "
            "onboardFlowVersion, etc. "
            "WARNING: This endpoint requires the COMPLETE dataflow object including internal fields like "
            "dapDataFlowId, responsibleUserId, gui, onboardFlowVersion. Omitting them causes a 400 error. "
            "To safely modify a dataflow, use dataflows_get to retrieve the full object first, mutate it, "
            "then pass the full object here. For large structural changes, delete and recreate instead."
        ),
    ],
) -> Any:
    """Replace a DataFlow's full definition (PUT). Requires the complete object — use dataflows_get first to retrieve all fields."""
    return auth.put(f"/dataprocessing/v1/dataflows/{dataflow_id}", body=body)


@mcp.tool()
def dataflows_update_owner_name_desc(
    dataflow_id: Annotated[str, "DataFlow ID"],
    body: Annotated[
        dict[str, Any],
        "Patch fields. Keys: databaseType, description, enabled (bool), name, password, responsibleUserId (int), restore (bool), restoreFlow (bool), useLegacyTriggerBehavior (bool)",
    ],
) -> Any:
    """Update a DataFlow's owner, name, or description."""
    return auth.put(f"/dataprocessing/v1/dataflows/{dataflow_id}/patch", body=body)


@mcp.tool()
def dataflows_bulk_update_owner(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs"],
    responsible_user_id: Annotated[int, "New owner user ID"],
    restore: Annotated[bool | None, "Restore deleted DataFlows"] = None,
    enabled: Annotated[bool | None, "Enable or disable DataFlows"] = None,
) -> Any:
    """Bulk update owner for multiple DataFlows."""
    body: dict[str, Any] = {
        "dataFlowIds": dataflow_ids,
        "responsibleUserId": responsible_user_id,
    }
    if restore is not None:
        body["restore"] = restore
    if enabled is not None:
        body["enabled"] = enabled
    return auth.put("/dataprocessing/v1/dataflows/bulk/patch", body=body)


@mcp.tool()
def dataflows_delete(
    dataflow_id: Annotated[str, "DataFlow ID to delete"],
) -> Any:
    """Delete a DataFlow."""
    return auth.delete(f"/dataprocessing/v1/dataflows/{dataflow_id}")


@mcp.tool()
def dataflows_bulk_delete(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs to delete"],
) -> Any:
    """Delete multiple DataFlows."""
    return auth.put(
        "/dataprocessing/v1/dataflows/bulk/delete",
        body={"dataFlowIds": dataflow_ids},
    )


@mcp.tool()
def dataflows_remove_all_tags(
    dataflow_id: Annotated[str, "DataFlow ID"],
) -> Any:
    """Remove all tags from a DataFlow."""
    return auth.delete(f"/dataprocessing/v1/dataflows/{dataflow_id}/tags")


@mcp.tool()
def dataflows_remove_tag(
    dataflow_id: Annotated[str, "DataFlow ID"],
    tag: Annotated[str, "Tag name to remove"],
) -> Any:
    """Remove a specific tag from a DataFlow."""
    return auth.delete(f"/dataprocessing/v1/dataflows/{dataflow_id}/tags/{tag}")


@mcp.tool()
def dataflows_bulk_remove_tags(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs"],
    tag_names: Annotated[list[str], "List of tag names to remove"],
) -> Any:
    """Remove tags from multiple DataFlows."""
    return auth.put(
        "/dataprocessing/v1/dataflows/bulk/tag/delete",
        body={"dataFlowIds": dataflow_ids, "tagNames": tag_names},
    )
