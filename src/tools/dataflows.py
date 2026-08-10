"""DataFlows tools — ETL/ELT flow management, execution, tags.

API reference: api-definitions-md/16-dataflows.md

Preferred dataflow type: MagicETL (databaseType='MAGIC'). Avoid MySQL dataflows.
See dataflows_create for full MagicETL action node documentation.
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="dataflows", read_only=True)
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


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_list(
    limit: Annotated[int | None, "Max DataFlows to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    order_by: Annotated[str | None, "Sort field"] = None,
) -> Any:
    """List DataFlows."""
    return auth.get("/dataprocessing/v2/dataflows", limit=limit, offset=offset, orderBy=order_by)


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_list_versions(
    dataflow_id: Annotated[str, "DataFlow ID"],
) -> Any:
    """List versions of a DataFlow."""
    return auth.get(f"/dataprocessing/v1/dataflows/{dataflow_id}/versions")


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_get(
    dataflow_id: Annotated[str, "DataFlow ID"],
) -> Any:
    """Get a DataFlow by ID."""
    return auth.get(f"/dataprocessing/v2/dataflows/{dataflow_id}")


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_export(
    dataflow_id: Annotated[str, "DataFlow ID"],
    file_path: Annotated[str, "Absolute local path to write the DataFlow definition JSON to, e.g. /Users/me/exports/1234.json"],
) -> Any:
    """Fetch a DataFlow's full definition and write it directly to a local JSON file.

    Same GET as dataflows_get, but the definition is written straight to disk
    instead of being returned through the MCP connection — useful for bulk
    export loops where passing every definition back through context is wasteful.
    """
    import json
    import pathlib

    path = pathlib.Path(file_path).resolve()
    home = pathlib.Path.home().resolve()
    if home not in path.parents and path != home:
        raise PermissionError(
            f"'{path}' is outside the allowed export directory ({home}). "
            "Choose a destination under your home directory."
        )

    definition = auth.get(f"/dataprocessing/v2/dataflows/{dataflow_id}")

    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(definition, indent=2)
    path.write_text(text)

    return {"dataflow_id": dataflow_id, "file_path": str(path), "size_bytes": len(text.encode())}


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_get_version(
    dataflow_id: Annotated[str, "DataFlow ID"],
    version_id: Annotated[str, "Version ID"],
) -> Any:
    """Get a specific version of a DataFlow by version ID."""
    return auth.get(f"/dataprocessing/v2/dataflows/{dataflow_id}/versions/{version_id}")


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_get_version_by_number(
    dataflow_id: Annotated[str, "DataFlow ID"],
    version_number: Annotated[str, "Version number"],
) -> Any:
    """Get a specific version of a DataFlow by version number."""
    return auth.get(f"/dataprocessing/v3/dataflows/{dataflow_id}/versions/{version_number}")


@domo_tool(toolset="dataflows", read_only=True)
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


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_get_execution(
    dataflow_id: Annotated[str, "DataFlow ID"],
    execution_id: Annotated[str, "Execution ID"],
) -> Any:
    """Get a specific execution of a DataFlow."""
    return auth.get(
        f"/dataprocessing/v1/dataflows/{dataflow_id}/executions/{execution_id}"
    )


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_get_tags(
    dataflow_id: Annotated[str, "DataFlow ID"],
) -> Any:
    """Get the tags (subscription info) for a DataFlow."""
    return auth.get(f"/dataprocessing/v1/dataflows/{dataflow_id}/subscription")


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_get_saved_filters(
    query_profile: Annotated[str | None, "Query profile filter"] = None,
) -> Any:
    """Get saved datacenter search filters."""
    return auth.get("/search/v1/saved", queryProfile=query_profile)


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_get_timezones() -> Any:
    """Get available timezones for DataFlows."""
    return auth.get("/dataprocessing/v1/dataflows/timezones")


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_get_sql_functions() -> Any:
    """Get available SQL functions for DataFlow expressions."""
    return auth.get("/dataprocessing/v1/expression-docs")


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_count_by_type() -> Any:
    """Count DataFlows grouped by type."""
    return auth.get("/dataprocessing/v2/dataflows/filters/dataflowType")


@domo_tool(toolset="dataflows", read_only=False)
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


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_bulk_run(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs to run"],
) -> Any:
    """Trigger multiple DataFlow executions."""
    return auth.post(
        "/dataprocessing/v1/dataflows/bulk/execute",
        body={"dataFlowIds": dataflow_ids},
    )


@domo_tool(toolset="dataflows", read_only=True)
def dataflows_run_preview(
    body: Annotated[
        dict[str, Any],
        "Preview body. Keys: databaseType (str), engineProperties (dict), actions (list), settings ({zoneId})",
    ],
) -> Any:
    """Run a DataFlow preview without persisting results."""
    return auth.post("/dataprocessing/v1/dataflows/previews/run", body=body)


@domo_tool(toolset="dataflows", read_only=False)
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
            "--- Action types (22 total): --- "
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
            "  Offset: {name, operation: {type: 'OFFSET', operationType: 'LAG'|'LEAD', column, "
            "  amount: int, defaultValue: null}}. "
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
            "DateCalculator — date arithmetic. Fields: input (action ID), "
            "  calculations (list of {fieldName: 'output_col', calcType: str, "
            "  fieldA: 'date_col', fieldB: 'date_col'|null, fieldC: str|null, "
            "  constantA: value|null, constantB: value|null, constantC: value|null, "
            "  exprA: null, exprB: null, exprC: null}). "
            "  calcType values: 'DATE_DIFF_HR' (hours between fieldA and fieldB), "
            "  'YEAR_OF_DATE' (extract year from fieldA), 'ADD_SUBTRACT_DATE' (add/subtract units). "
            "SetValueField — replace a column's values with values from another column. Fields: input (action ID), "
            "  fields (list of {name: 'target_col', replaceby: 'source_col'}). "
            "ConcatFields — concatenate multiple columns into one. Fields: input (action ID), "
            "  separator (str), targetFieldName (str), removeSelectedFields (bool), "
            "  fields (list of {name: 'col_to_concat'}). "
            "TextFormatting — transform text column values. Fields: input (action ID), "
            "  fields (list of {name: 'col', letterCaseMod: 'UPPER'|'LOWER'|null, "
            "  numberMod: 'REMOVE'|null}). "
            "NormalizeAll — dynamic unpivot: all non-id columns become rows. Fields: input (action ID), "
            "  idFields (list of column name strings to keep as row identifiers), "
            "  keyField (str, new column that holds original column names), "
            "  valueField (str, new column that holds the values). "
            "Normalizer — selective unpivot: specify which columns to unpivot. Fields: input (action ID), "
            "  typefield (str, new column for category label), "
            "  fields (list of {sourceField: 'src_col', typefieldValue: 'label', destField: 'value_col'}). "
            "PythonEngineAction — PREMIUM FEATURE: do NOT use unless the user explicitly requests it. "
            "  Run a Python script. Fields: inputs (list of action IDs), "
            "  condaEnv ('domo-2'), script (Python code string), "
            "  additions (list of {name: 'output_col', dataType: 'STRING'|'LONG'|'DOUBLE'|'DATE'}), "
            "  removeByDefault (bool, true = output only additions cols), fillMissingWithNull (bool). "
            "  Use domomagic package: read_dataframe('action_name') and write_dataframe(df). "
            "MLInferenceAction — PREMIUM FEATURE: do NOT use unless the user explicitly requests it. "
            "  Apply an AutoML model. Fields: input (action ID), "
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


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_add_tag(
    dataflow_id: Annotated[str, "DataFlow ID"],
    tag: Annotated[str, "Tag name to add"],
) -> Any:
    """Add a single tag to a DataFlow."""
    return auth.post(
        f"/dataprocessing/v1/dataflows/{dataflow_id}/tags",
        body={"tag": tag},
    )


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_bulk_add_tags(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs"],
    tag_names: Annotated[list[str], "List of tag names to add"],
) -> Any:
    """Add tags to multiple DataFlows."""
    return auth.put(
        "/dataprocessing/v1/dataflows/bulk/tag",
        body={"dataFlowIds": dataflow_ids, "tagNames": tag_names},
    )


@domo_tool(toolset="dataflows", read_only=False)
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


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_update_owner_name_desc(
    dataflow_id: Annotated[str, "DataFlow ID"],
    body: Annotated[
        dict[str, Any],
        "Patch fields. Keys: databaseType, description, enabled (bool), name, password, responsibleUserId (int), restore (bool), restoreFlow (bool), useLegacyTriggerBehavior (bool)",
    ],
) -> Any:
    """Update a DataFlow's owner, name, or description."""
    return auth.put(f"/dataprocessing/v1/dataflows/{dataflow_id}/patch", body=body)


@domo_tool(toolset="dataflows", read_only=False)
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


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_delete(
    dataflow_id: Annotated[str, "DataFlow ID to delete"],
) -> Any:
    """Delete a DataFlow."""
    return auth.delete(f"/dataprocessing/v1/dataflows/{dataflow_id}")


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_bulk_delete(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs to delete"],
) -> Any:
    """Delete multiple DataFlows."""
    return auth.put(
        "/dataprocessing/v1/dataflows/bulk/delete",
        body={"dataFlowIds": dataflow_ids},
    )


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_remove_all_tags(
    dataflow_id: Annotated[str, "DataFlow ID"],
) -> Any:
    """Remove all tags from a DataFlow."""
    return auth.delete(f"/dataprocessing/v1/dataflows/{dataflow_id}/tags")


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_remove_tag(
    dataflow_id: Annotated[str, "DataFlow ID"],
    tag: Annotated[str, "Tag name to remove"],
) -> Any:
    """Remove a specific tag from a DataFlow."""
    return auth.delete(f"/dataprocessing/v1/dataflows/{dataflow_id}/tags/{tag}")


@domo_tool(toolset="dataflows", read_only=False)
def dataflows_bulk_remove_tags(
    dataflow_ids: Annotated[list[int], "List of DataFlow IDs"],
    tag_names: Annotated[list[str], "List of tag names to remove"],
) -> Any:
    """Remove tags from multiple DataFlows."""
    return auth.put(
        "/dataprocessing/v1/dataflows/bulk/tag/delete",
        body={"dataFlowIds": dataflow_ids, "tagNames": tag_names},
    )
