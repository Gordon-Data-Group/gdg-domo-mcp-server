"""DataSets & Streams tools — dataset CRUD, queries, uploads, PDP policies, data repair, streams.

API reference: api-definitions-md/17-datasets-and-streams.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


# ── Core DataSets ─────────────────────────────────────────────────────────────

@mcp.tool()
def datasets_search(
    body: Annotated[dict[str, Any], "Search body. Key fields: query (wildcard string), filters (list), count (int), offset (int), sort"],
) -> Any:
    """Search DataSets using Domo's search engine. Returns matching datasets with metadata."""
    return auth.post("/data/ui/v3/datasources/search", body=body)


@mcp.tool()
def datasets_list(
    limit: Annotated[int | None, "Max datasets to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    name_like: Annotated[str | None, "Filter by name substring or wildcard"] = None,
    owner_id: Annotated[str | None, "Filter by owner user ID"] = None,
    part: Annotated[str | None, "Extra detail parts to include (e.g. 'schema')"] = None,
    include_hidden: Annotated[bool | None, "Include hidden datasets"] = None,
    order_by: Annotated[str | None, "Sort field"] = None,
    display_type: Annotated[str | None, "Filter by display type"] = None,
    type: Annotated[str | None, "Filter by dataset type"] = None,
    data_provider_type: Annotated[str | None, "Filter by data provider type"] = None,
    created_since: Annotated[str | None, "ISO timestamp — only datasets created after this"] = None,
) -> Any:
    """List DataSets in the Domo instance with optional filters and pagination."""
    return auth.get(
        "/data/v3/datasources",
        limit=limit,
        offset=offset,
        nameLike=name_like,
        ownerId=owner_id,
        part=part,
        includeHidden=include_hidden,
        orderBy=order_by,
        displayType=display_type,
        type=type,
        dataProviderType=data_provider_type,
        createdSince=created_since,
    )


@mcp.tool()
def datasets_list_tags() -> Any:
    """List all tags that exist on any DataSet in the instance."""
    return auth.get("/data/ui/v3/datasources/search/tags/all")


@mcp.tool()
def datasets_get_bulk(
    dataset_ids: Annotated[list[str], "List of dataset UUIDs to fetch"],
    include_private: Annotated[bool | None, "Include private datasets"] = None,
    include_all_details: Annotated[bool | None, "Include full schema and metadata"] = None,
) -> Any:
    """Fetch multiple DataSets by UUID in a single request."""
    return auth.post(
        "/data/v3/datasources/bulk",
        body=dataset_ids,
        includePrivate=include_private,
        includeAllDetails=include_all_details,
    )


@mcp.tool()
def datasets_get_owned_by(
    owners: Annotated[list[dict[str, Any]], "Owner filter list, e.g. [{'id': 1234, 'type': 'USER'}] or [{'id': 5, 'type': 'GROUP'}]"],
) -> Any:
    """Get all DataSets owned by specific users or groups."""
    return auth.post("/data/ui/v3/datasources/ownedBy", body=owners)


@mcp.tool()
def datasets_get(
    dataset_id: Annotated[str, "Dataset UUID"],
    include_all_details: Annotated[bool | None, "Include full schema and connector metadata"] = None,
    part: Annotated[str | None, "Extra detail parts to include (e.g. 'schema')"] = None,
) -> Any:
    """Get a single DataSet by UUID."""
    return auth.get(
        f"/data/v3/datasources/{dataset_id}",
        includeAllDetails=include_all_details,
        part=part,
    )


@mcp.tool()
def datasets_get_saved_filters(
    query_profile: Annotated[str | None, "Filter profile name, e.g. 'DATACENTER'"] = None,
) -> Any:
    """Get saved Datacenter filter views for the current user."""
    return auth.get("/search/v1/saved", queryProfile=query_profile)


@mcp.tool()
def datasets_get_lineage(
    dataset_id: Annotated[str, "Dataset UUID"],
    traverse_up: Annotated[bool | None, "Include upstream source dependencies"] = None,
    traverse_down: Annotated[bool | None, "Include downstream dependents (cards, dataflows)"] = None,
    request_entities: Annotated[str | None, "Comma-separated entity types to include"] = None,
    max_depth: Annotated[int | None, "Max traversal depth (default: unlimited)"] = None,
) -> Any:
    """Get the data lineage graph for a DataSet — upstream sources and downstream dependents."""
    return auth.get(
        f"/data/v1/lineage/DATA_SOURCE/{dataset_id}",
        traverseUp=traverse_up,
        traverseDown=traverse_down,
        requestEntities=request_entities,
        maxDepth=max_depth,
    )


@mcp.tool()
def datasets_get_impact_counts(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """Get counts of cards, dataflows, and other resources that depend on a DataSet."""
    return auth.get(f"/data/v1/impacts/DATA_SOURCE/{dataset_id}")


@mcp.tool()
def datasets_get_schema(
    dataset_id: Annotated[str, "Dataset UUID"],
    include_hidden: Annotated[bool | None, "Include hidden/system columns"] = None,
) -> Any:
    """Get the indexed column schema (names, types) for a DataSet."""
    return auth.get(
        f"/query/v1/datasources/{dataset_id}/schema/indexed",
        includeHidden=include_hidden,
    )


@mcp.tool()
def datasets_get_wrangle(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """Get column tags, descriptions, display names, and order for a DataSet."""
    return auth.get(f"/query/v1/datasources/{dataset_id}/wrangle")


@mcp.tool()
def datasets_query(
    dataset_id: Annotated[str, "Dataset UUID"],
    body: Annotated[dict[str, Any], "Structured query body. Must contain a 'query' object with columns, limit/offset, and optional where/groupByColumns/orderByColumns. See API docs for full schema."],
) -> Any:
    """Query a DataSet using Domo's structured query format. Use datasets_query_sql for SQL instead."""
    return auth.post(f"/query/v1/execute/{dataset_id}", body=body)


@mcp.tool()
def datasets_query_sql(
    dataset_id: Annotated[str, "Dataset UUID"],
    sql: Annotated[str, "SQL SELECT statement to run against the dataset"],
) -> Any:
    """Query a DataSet with a SQL SELECT statement. Returns rows and column metadata."""
    return auth.post(f"/query/v1/execute/{dataset_id}", body={"sql": sql})


@mcp.tool()
def datasets_query_preview(
    body: Annotated[dict[str, Any], "Views Explorer query-preview body with schema, query, viewTemplate, and tableAliases fields"],
) -> Any:
    """Run a query preview in the Views Explorer (for Views-based datasets)."""
    return auth.post("/query/v1/views/query-preview", body=body)


@mcp.tool()
def datasets_create_view(
    body: Annotated[dict[str, Any], "View definition with dataSourceName, schema (tables + viewTemplate), trigger (source datasetId), and responsibleUserId"],
) -> Any:
    """Create a new dataset View in the Views Explorer."""
    return auth.post("/query/v1/views", body=body)


@mcp.tool()
def datasets_bulk_add_tags(
    dataset_ids: Annotated[list[str], "List of dataset UUIDs to tag"],
    tags: Annotated[list[str], "Tags to add to all specified datasets"],
) -> Any:
    """Add one or more tags to multiple DataSets at once."""
    return auth.post(
        "/data/v1/ui/bulk/tag",
        body={
            "bulkItems": {"ids": dataset_ids, "type": "DATA_SOURCE"},
            "tags": tags,
        },
    )


@mcp.tool()
def datasets_defrost(
    dataset_id: Annotated[str, "UUID of the vaulted (frozen) dataset to restore"],
) -> Any:
    """Defrost (unvault) a DataSet that was archived to long-term storage."""
    return auth.post(f"/data/ui/v3/datasources/{dataset_id}/defrost")


@mcp.tool()
def datasets_share(
    dataset_id: Annotated[str, "Dataset UUID"],
    permissions: Annotated[list[dict[str, Any]], "Permission objects, e.g. [{'type': 'USER', 'id': '123', 'accessLevel': 'CAN_SHARE'}]. accessLevel: CAN_VIEW, CAN_SHARE, CAN_EDIT, OWNER"],
    send_email: Annotated[bool, "Send a notification email to recipients"] = False,
) -> Any:
    """Share a DataSet with users or groups."""
    return auth.post(
        f"/data/v3/datasources/{dataset_id}/share",
        body={"permissions": permissions, "sendEmail": send_email},
    )


@mcp.tool()
def datasets_append_webhook(
    dataset_id: Annotated[str, "UUID of the Webhook DataSet to append data to"],
) -> Any:
    """Trigger an append to a Webhook DataSet."""
    return auth.post(f"/iot/v1/webhook/data/{dataset_id}")


@mcp.tool()
def datasets_update_wrangle(
    dataset_id: Annotated[str, "Dataset UUID"],
    columns: Annotated[list[dict[str, Any]], "Column definitions. Each object: {name, id, type, visible, order, referenceDataSourceId, invalid, newName}"],
) -> Any:
    """Update column tags, descriptions, display names, and order (wrangle) for a DataSet."""
    return auth.post(
        f"/query/v1/datasources/{dataset_id}/wrangle",
        body={"columns": columns},
    )


@mcp.tool()
def datasets_update_name_description(
    dataset_id: Annotated[str, "Dataset UUID"],
    name: Annotated[str, "New dataset name"],
    description: Annotated[str, "New dataset description (pass empty string to clear)"] = "",
) -> Any:
    """Update the name and/or description of a DataSet."""
    return auth.put(
        f"/data/v3/datasources/{dataset_id}/properties",
        body={"dataSourceName": name, "dataSourceDescription": description},
    )


@mcp.tool()
def datasets_update_owner(
    dataset_id: Annotated[str, "Dataset UUID"],
    user_id: Annotated[str, "User ID (as string) of the new responsible owner"],
) -> Any:
    """Change the responsible/owner user for a DataSet."""
    return auth.put(
        f"/data/v2/datasources/{dataset_id}/responsibleUsers",
        body={"responsibleUserId": str(user_id)},
    )


@mcp.tool()
def datasets_bulk_update_owners(
    user_id: Annotated[str, "User ID who will become owner of all specified datasets"],
    dataset_ids: Annotated[list[str], "List of dataset UUIDs to reassign"],
) -> Any:
    """Reassign ownership of multiple DataSets to a single user (v2 endpoint)."""
    return auth.put(
        f"/data/v2/datasources/responsible-user/{user_id}",
        body=dataset_ids,
    )


@mcp.tool()
def datasets_bulk_update_owners_v1(
    dataset_ids: Annotated[list[str], "List of dataset UUIDs to reassign"],
    user_id: Annotated[int | None, "User ID of the new owner (provide user_id or group_id, not both)"] = None,
    group_id: Annotated[int | None, "Group ID of the new owner (provide user_id or group_id, not both)"] = None,
) -> Any:
    """Bulk reassign DataSet ownership (v1 endpoint). Provide either user_id or group_id."""
    body: dict[str, Any] = {"type": "DATA_SOURCE", "ids": dataset_ids}
    if user_id is not None:
        body["userId"] = user_id
    if group_id is not None:
        body["groupId"] = group_id
    return auth.post("/data/v1/ui/bulk/reassign", body=body)


@mcp.tool()
def datasets_bulk_delete(
    dataset_ids: Annotated[list[str], "List of dataset UUIDs to delete"],
) -> Any:
    """Delete multiple DataSets in a single request. Use datasets_delete_check first to preview impact."""
    return auth.post(
        "/data/v1/ui/bulk/delete",
        body={"type": "DATA_SOURCE", "ids": dataset_ids},
    )


@mcp.tool()
def datasets_update_tags(
    dataset_id: Annotated[str, "Dataset UUID"],
    tags: Annotated[list[str], "Complete replacement tag list — this overwrites all existing tags on the dataset"],
) -> Any:
    """Replace all tags on a DataSet with a new list."""
    return auth.post(f"/data/ui/v3/datasources/{dataset_id}/tags", body=tags)


@mcp.tool()
def datasets_sync_cloud_amplifier(
    cloud_id: Annotated[str, "Cloud Amplifier account/cloud ID to refresh"],
) -> Any:
    """Trigger a polling refresh/sync for a Cloud Amplifier DataSet."""
    return auth.put(f"/query/v1/byos/accounts/{cloud_id}/polling/refresh")


@mcp.tool()
def datasets_delete(
    dataset_id: Annotated[str, "Dataset UUID"],
    delete_method: Annotated[str | None, "Deletion method: 'HARD' (permanent) or 'SOFT' (recoverable). Defaults to SOFT."] = None,
) -> Any:
    """Delete a DataSet. Use datasets_delete_check first to preview what will be affected."""
    return auth.delete(f"/data/v3/datasources/{dataset_id}", deleteMethod=delete_method)


@mcp.tool()
def datasets_delete_check(
    dataset_ids: Annotated[list[str], "Dataset UUIDs to check before deletion"],
) -> Any:
    """Preview what cards, dataflows, and other resources would be affected by deleting these DataSets."""
    return auth.post(
        "/data/v1/ui/bulk/delete/check",
        body={"type": "DATA_SOURCE", "ids": dataset_ids},
    )


# ── Streams ───────────────────────────────────────────────────────────────────

@mcp.tool()
def streams_get(
    stream_id: Annotated[int, "Stream ID (integer)"],
    fields: Annotated[str | None, "Comma-separated list of fields to include in the response"] = None,
) -> Any:
    """Get a Stream (connector configuration) by ID."""
    return auth.get(f"/data/v1/streams/{stream_id}", fields=fields)


@mcp.tool()
def streams_get_executions(
    stream_id: Annotated[int, "Stream ID"],
) -> Any:
    """List recent execution history for a Stream."""
    return auth.get(f"/data/v1/streams/{stream_id}/executions")


@mcp.tool()
def streams_get_execution(
    stream_id: Annotated[int, "Stream ID"],
    execution_id: Annotated[int, "Execution ID"],
) -> Any:
    """Get details and status of a specific Stream execution."""
    return auth.get(f"/data/v1/streams/{stream_id}/executions/{execution_id}")


@mcp.tool()
def streams_create(
    body: Annotated[dict[str, Any], "Stream definition. Required: dataSource (name, description), updateMethod (REPLACE/APPEND), transport, dataProvider, account. Optional: scheduleExpression, configuration."],
) -> Any:
    """Create a new Stream and its backing DataSet."""
    return auth.post("/data/v1/streams", body=body)


@mcp.tool()
def streams_run(
    stream_id: Annotated[int, "Stream ID to trigger"],
) -> Any:
    """Trigger an immediate execution of a Stream (runs the connector now)."""
    return auth.post(f"/data/v1/streams/{stream_id}/executions")


@mcp.tool()
def streams_update(
    stream_id: Annotated[int, "Stream ID"],
    body: Annotated[dict[str, Any], "Updated stream definition. Must include id, dataSource, dataProvider, and schedule fields. See streams_get for current values."],
) -> Any:
    """Update a Stream's schedule, account, schema, or configuration."""
    return auth.put(f"/data/v1/streams/{stream_id}", body=body)


@mcp.tool()
def streams_abort(
    stream_id: Annotated[int, "Stream ID"],
    execution_id: Annotated[int, "Execution ID to abort"],
    message: Annotated[str, "Reason for aborting"] = "Aborted by user",
) -> Any:
    """Abort a currently running Stream execution."""
    return auth.put(
        f"/data/v1/streams/{stream_id}/executions/{execution_id}",
        body={"category": "CONNECTOR", "message": message},
    )


# ── AI Readiness / Data Dictionary ────────────────────────────────────────────

@mcp.tool()
def datasets_get_data_dictionary(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """Get the AI Readiness data dictionary for a DataSet (column descriptions, synonyms, agent settings)."""
    return auth.get(f"/ai/readiness/v1/data-dictionary/dataset/{dataset_id}")


@mcp.tool()
def datasets_create_data_dictionary(
    dataset_id: Annotated[str, "Dataset UUID"],
    body: Annotated[dict[str, Any], "Dictionary body: {name, description, unitOfAnalysis, columns: [{name, description, synonyms, agentEnabled, beastmodeId}]}"],
) -> Any:
    """Create an AI Readiness data dictionary for a DataSet."""
    return auth.post(f"/ai/readiness/v1/data-dictionary/dataset/{dataset_id}", body=body)


@mcp.tool()
def datasets_update_data_dictionary(
    dataset_id: Annotated[str, "Dataset UUID"],
    body: Annotated[dict[str, Any], "Updated dictionary body: {id, datasetId, name, description, columns: [{columnId, name, description, synonyms, agentEnabled}]}. Omit columnId to add a new column entry."],
) -> Any:
    """Update the AI Readiness data dictionary for a DataSet."""
    return auth.put(f"/ai/readiness/v1/data-dictionary/dataset/{dataset_id}", body=body)


# ── Data Repair ───────────────────────────────────────────────────────────────

@mcp.tool()
def datasets_list_data_versions(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """List available historical data versions (snapshots) for a DataSet (v3)."""
    return auth.get(f"/data/v3/datasources/{dataset_id}/dataversions/details")


@mcp.tool()
def datasets_list_data_versions_v2(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """List available historical data versions for a DataSet (v2)."""
    return auth.get(f"/data/v2/datasources/{dataset_id}/dataversions")


@mcp.tool()
def datasets_get_data_version(
    dataset_id: Annotated[str, "Dataset UUID"],
    version_id: Annotated[str, "Data version ID from datasets_list_data_versions"],
    exclude_appended_data: Annotated[bool | None, "Exclude rows added via APPEND operations"] = None,
    row_limit: Annotated[int | None, "Max rows to return from this version"] = None,
) -> Any:
    """Get the data content of a specific historical data version."""
    return auth.get(
        f"/data/v2/datasources/{dataset_id}/dataversions/{version_id}",
        excludeAppendedData=exclude_appended_data,
        rowLimit=row_limit,
    )


@mcp.tool()
def datasets_insert_data_version(
    dataset_id: Annotated[str, "Dataset UUID"],
    repair_data_version_id: Annotated[str | None, "Version ID to restore as the current data"] = None,
    repair_action: Annotated[str | None, "Repair action type (e.g. 'REPAIR')"] = None,
) -> Any:
    """Restore a historical data version as the current live data for a DataSet."""
    return auth.post_no_body(
        f"/data/v3/datasources/{dataset_id}/dataversions",
        repairDataVersionId=repair_data_version_id,
        repairAction=repair_action,
    )


@mcp.tool()
def datasets_delete_data_versions(
    dataset_id: Annotated[str, "Dataset UUID"],
    version_ids: Annotated[list[int], "List of data version IDs (integers) to permanently delete"],
) -> Any:
    """Permanently delete specific historical data versions from a DataSet."""
    return auth.delete(
        f"/data/v2/datasources/{dataset_id}/dataversions",
        body=version_ids,
    )


# ── PDP — Column ──────────────────────────────────────────────────────────────

@mcp.tool()
def datasets_get_column_pdp_policies(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """Get all Column-level PDP policies for a DataSet."""
    return auth.get(f"/query/v2/data-control/{dataset_id}/policy-group")


@mcp.tool()
def datasets_get_column_pdp_mapping(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """Get the Column PDP policy-to-column mapping for a DataSet."""
    return auth.get(f"/query/v2/data-control/{dataset_id}/column-policy-mapping")


# ── PDP — Row ─────────────────────────────────────────────────────────────────

@mcp.tool()
def datasets_get_row_pdp_policies(
    dataset_id: Annotated[str, "Dataset UUID"],
    options: Annotated[str | None, "Optional filter string"] = None,
) -> Any:
    """Get all Row-level PDP filter policies for a DataSet."""
    return auth.get(
        f"/query/v1/data-control/{dataset_id}/filter-groups",
        options=options,
    )


@mcp.tool()
def datasets_create_row_pdp_policy(
    dataset_id: Annotated[str, "Dataset UUID"],
    body: Annotated[dict[str, Any], "Policy body: {name, dataSourceId, userIds, groupIds, dataSourcePermissions, parameters: [{type, name, values, operator, ignoreCase}]}"],
) -> Any:
    """Create a Row-level PDP filter policy for a DataSet."""
    return auth.post(f"/query/v1/data-control/{dataset_id}/filter-groups", body=body)


@mcp.tool()
def datasets_update_row_pdp_policy(
    dataset_id: Annotated[str, "Dataset UUID"],
    policy_id: Annotated[str, "Row PDP policy (filter group) ID to update"],
    body: Annotated[dict[str, Any], "Updated policy body: {name, filterGroupId, userIds, dataSourcePermissions, parameters, order}"],
) -> Any:
    """Update a Row-level PDP filter policy."""
    return auth.put(
        f"/query/v1/data-control/{dataset_id}/filter-groups/{policy_id}",
        body=body,
    )


@mcp.tool()
def datasets_delete_row_pdp_policy(
    dataset_id: Annotated[str, "Dataset UUID"],
    policy_id: Annotated[str, "Row PDP policy (filter group) ID to delete"],
) -> Any:
    """Delete a Row-level PDP filter policy from a DataSet."""
    return auth.delete(f"/query/v1/data-control/{dataset_id}/filter-groups/{policy_id}")


# ── PDP — Status ──────────────────────────────────────────────────────────────

@mcp.tool()
def datasets_get_pdp_status(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """Get the PDP enabled/disabled status and configuration for a DataSet."""
    return auth.get(f"/query/v2/data-control/{dataset_id}")


@mcp.tool()
def datasets_get_pdp_impacted_resources(
    dataset_id: Annotated[str, "Dataset UUID"],
) -> Any:
    """Get resources (cards, etc.) impacted by PDP settings on a DataSet."""
    return auth.get(f"/data/v3/datasources/{dataset_id}/impacted-resources")


@mcp.tool()
def datasets_enable_disable_pdp(
    dataset_id: Annotated[str, "Dataset UUID"],
    enabled: Annotated[bool, "True to enable Row PDP, False to disable"],
    secured: Annotated[bool, "Block access for users not covered by any policy"] = False,
    external: Annotated[bool, "Enable PDP for Domo Everywhere (embedded) access"] = False,
    enabled_column: Annotated[bool, "Also enable Column PDP"] = True,
) -> Any:
    """Enable or disable Row/Column PDP on a DataSet."""
    return auth.put(
        f"/query/v1/data-control/{dataset_id}",
        body={
            "enabled": enabled,
            "secured": secured,
            "external": external,
            "enabledColumn": enabled_column,
        },
    )


# ── Uploads (multi-part) ──────────────────────────────────────────────────────

@mcp.tool()
def datasets_create_upload(
    dataset_id: Annotated[str, "Dataset UUID to upload data into"],
    action: Annotated[str, "Upload action: 'REPLACE' to overwrite all data or 'APPEND' to add rows"] = "REPLACE",
    message: Annotated[str, "Human-readable label for this upload"] = "Uploading",
    append_id: Annotated[str, "Append session ID — use 'latest' for standard uploads"] = "latest",
) -> Any:
    """Start a new multi-part upload session for a DataSet. Returns an uploadId to use in subsequent calls."""
    return auth.post(
        f"/data/v3/datasources/{dataset_id}/uploads",
        body={"action": action, "message": message, "appendId": append_id},
    )


@mcp.tool()
def datasets_upload_part(
    dataset_id: Annotated[str, "Dataset UUID"],
    upload_id: Annotated[str, "Upload session ID returned by datasets_create_upload"],
    part_number: Annotated[int, "Part index, 1-based. Include the header row in part 1 only."],
    csv_data: Annotated[str, "Raw CSV text for this chunk. Include column headers on part 1 only."],
) -> Any:
    """Upload a CSV data chunk to an active upload session."""
    return auth.put_text(
        f"/data/v3/datasources/{dataset_id}/uploads/{upload_id}/parts/{part_number}",
        text=csv_data,
        content_type="text/csv",
    )


@mcp.tool()
def datasets_commit_upload(
    dataset_id: Annotated[str, "Dataset UUID"],
    upload_id: Annotated[str, "Upload session ID returned by datasets_create_upload"],
    index: Annotated[bool, "Index the data after committing (required for query access)"] = True,
    append_id: Annotated[str, "Must match the appendId used in datasets_create_upload"] = "latest",
    message: Annotated[str, "Commit message"] = "Upload complete",
) -> Any:
    """Commit a completed multi-part upload, making the uploaded data live in the DataSet."""
    return auth.put(
        f"/data/v3/datasources/{dataset_id}/uploads/{upload_id}/commit",
        body={"index": index, "appendId": append_id, "message": message},
    )


# ── File upload (create PUSH dataset from file) ───────────────────────────────

@mcp.tool()
def datasets_upload_file(
    file_path: Annotated[str, "Absolute path to a local CSV or XLSX file"],
    dataset_name: Annotated[str | None, "Dataset display name. Defaults to the filename stem."] = None,
) -> Any:
    """Create a new Domo PUSH dataset from a local CSV or XLSX file and upload all rows.

    Workflow:
      1. Parse file to infer column schema (names + Domo types)
      2. Create PUSH dataset via POST /data/v2/datasources
      3. Convert data to CSV and upload via the 3-step process (create → part → commit)
      4. Return the created dataset metadata (includes id, name, rowCount, schema, etc.)

    Column types are inferred automatically:
      int   → LONG      float → DECIMAL
      date  → DATE      datetime → DATETIME
      str   → STRING    (CSV files default all columns to STRING)

    XLSX requires openpyxl: pip install openpyxl
    """
    import csv
    import io
    import pathlib
    from datetime import date, datetime

    path = pathlib.Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    _ALLOWED_DIRS = (
        pathlib.Path.home() / "Downloads",
        pathlib.Path.home() / "Documents",
        pathlib.Path.home() / "Desktop",
        pathlib.Path("/tmp"),
    )
    if not any(str(path).startswith(str(d)) for d in _ALLOWED_DIRS):
        raise PermissionError(
            f"'{path}' is outside the allowed upload directories "
            f"(~/Downloads, ~/Documents, ~/Desktop, /tmp). "
            "Move the file to one of those locations and retry."
        )

    name = dataset_name or path.stem
    suffix = path.suffix.lower()

    # ── 1. Parse file ─────────────────────────────────────────────────────────
    if suffix in (".xlsx", ".xls"):
        try:
            import openpyxl
        except ImportError:
            raise ImportError("openpyxl is required for XLSX uploads: pip install openpyxl")
        wb = openpyxl.load_workbook(str(path), data_only=True)
        ws = wb.active
        all_rows = list(ws.iter_rows(values_only=True))
        if not all_rows:
            raise ValueError("Spreadsheet is empty")
        headers = [str(h) if h is not None else f"col_{i}" for i, h in enumerate(all_rows[0])]
        data_rows = all_rows[1:]
        native_types = True   # openpyxl returns Python native types
    elif suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as fh:
            reader = csv.reader(fh)
            headers = next(reader)
            data_rows = list(reader)
        native_types = False  # CSV values are strings
    else:
        raise ValueError(f"Unsupported file type: {suffix} — use .csv or .xlsx")

    # ── 2. Infer column types ──────────────────────────────────────────────────
    def _domo_type(val: Any) -> str:
        if isinstance(val, bool):     return "STRING"
        if isinstance(val, datetime): return "DATETIME"
        if isinstance(val, date):     return "DATE"
        if isinstance(val, int):      return "LONG"
        if isinstance(val, float):    return "DECIMAL"
        return "STRING"

    if native_types:
        col_types = ["STRING"] * len(headers)
        for row in data_rows[:200]:
            for i, val in enumerate(row):
                if val is not None and col_types[i] == "STRING":
                    t = _domo_type(val)
                    if t != "STRING":
                        col_types[i] = t
    else:
        col_types = ["STRING"] * len(headers)

    schema_cols = [{"name": h, "type": t} for h, t in zip(headers, col_types)]

    # ── 3. Create PUSH dataset ─────────────────────────────────────────────────
    ds = auth.post("/data/v2/datasources", body={
        "dataSourceName": name,
        "type": "PUSH",
        "schema": {"columns": schema_cols},
    })
    ds_id = ds["dataSource"]["dataSourceId"]

    # ── 4. Serialize to CSV ────────────────────────────────────────────────────
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    for row in data_rows:
        out = []
        for val in row:
            if val is None:
                out.append("")
            elif isinstance(val, (datetime, date)):
                out.append(val.isoformat())
            else:
                out.append(str(val))
        writer.writerow(out)
    csv_text = buf.getvalue()

    # ── 5. Upload (create session → upload part → commit) ─────────────────────
    upload_resp = auth.post(
        f"/data/v3/datasources/{ds_id}/uploads",
        body={"action": "REPLACE", "message": f"Initial upload from {path.name}", "appendId": "latest"},
    )
    upload_id = upload_resp["uploadId"] if isinstance(upload_resp, dict) else upload_resp

    auth.put_text(
        f"/data/v3/datasources/{ds_id}/uploads/{upload_id}/parts/1",
        text=csv_text,
        content_type="text/csv",
    )

    auth.put(
        f"/data/v3/datasources/{ds_id}/uploads/{upload_id}/commit",
        body={"index": True, "appendId": "latest", "message": "Initial upload complete"},
    )

    return {"id": ds_id, "name": name, "rowCount": len(data_rows), "schema": {"columns": schema_cols}}


# ── Webforms ──────────────────────────────────────────────────────────────────

@mcp.tool()
def datasets_get_webform_data(
    dataset_id: Annotated[str, "UUID of the Webform DataSet"],
) -> Any:
    """Get the current grid data (rows and columns) from a Webform DataSet."""
    return auth.get(f"/data/v2/webforms/{dataset_id}/grid")


@mcp.tool()
def datasets_update_webform_data(
    stream_id: Annotated[str, "Stream ID of the Webform DataSet"],
    name: Annotated[str, "Dataset name"],
    columns: Annotated[list[dict[str, Any]], "Column definitions: [{name, type}]. Types: STRING, LONG, DOUBLE, DATE, DATETIME."],
    rows: Annotated[list[list[Any]], "Row data. Each row is a list of values in the same order as columns."],
) -> Any:
    """Replace all data in a Webform DataSet with new rows and columns."""
    return auth.put(
        f"/data/v2/webforms/{stream_id}",
        body={"name": name, "columns": columns, "rows": rows, "cloudId": None},
    )
