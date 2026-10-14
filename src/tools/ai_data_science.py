"""AI / Data Science tools — AutoML, AI service layer, Jupyter workspaces.

API reference: api-definitions-md/04-ai-data-science.md
"""
from __future__ import annotations

from typing import Annotated, Any, Literal

from src.toolsets import domo_tool
from src import auth


# ---------------------------------------------------------------------------
# AutoML
# ---------------------------------------------------------------------------

@domo_tool(toolset="ai_data_science", read_only=True)
def ai_automl_list_models(
    dataset_id: Annotated[str, "Dataset ID to list AutoML models for"],
    include_details: Annotated[bool | None, "Include detailed model information"] = None,
) -> Any:
    """List AutoML models trained on a dataset."""
    return auth.get(
        f"/dataprocessing/v1/ml/{dataset_id}/automl/job",
        includeDetails=include_details,
    )


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_automl_get_model(
    dataset_id: Annotated[str, "Dataset ID"],
    model_id: Annotated[str, "AutoML model ID"],
    include_candidates: Annotated[bool | None, "Include candidate model details"] = None,
) -> Any:
    """Get a specific AutoML model."""
    return auth.get(
        f"/dataprocessing/v1/ml/{dataset_id}/automl/job/{model_id}",
        includeCandidates=include_candidates,
    )


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_automl_get_model_schema(
    model_id: Annotated[str, "AutoML model ID"],
) -> Any:
    """Get the input/output schema for an AutoML model."""
    return auth.get(f"/dataprocessing/v1/ml/automl/job/{model_id}/schema")


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_automl_explain_model(
    model_id: Annotated[str, "AutoML model ID"],
) -> Any:
    """Get feature importance and explainability data for an AutoML model."""
    return auth.get(f"/dataprocessing/v1/ml/automl/job/{model_id}/explain")


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_automl_add_model_to_dataset(
    dataset_id: Annotated[str, "Dataset ID to attach the model to"],
    automl_job_id: Annotated[int, "AutoML job ID"],
    candidate_name: Annotated[str, "Candidate model name within the job"],
    display_name: Annotated[str, "Display name for the model"],
) -> Any:
    """Add an AutoML model to a dataset for scoring."""
    return auth.post(
        f"/dataprocessing/v1/ml/{dataset_id}/model",
        body={
            "automlJobId": automl_job_id,
            "candidateName": candidate_name,
            "displayName": display_name,
        },
    )


# ---------------------------------------------------------------------------
# AI Models (user-generated)
# ---------------------------------------------------------------------------

@domo_tool(toolset="ai_data_science", read_only=True)
def ai_models_list(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: limit (int), "
            "sortFieldMap (dict e.g. {'CREATED': 'DESC'}), "
            "searchFieldMap (dict e.g. {'NAME': ''}), "
            "filters (list of {type, values}), "
            "metricFilters (dict), dateFilters (dict), sortMetricMap (dict)"
        ),
    ],
) -> Any:
    """List or search user-generated AI models."""
    return auth.post_read("/datascience/ml/v1/search/models", body=body)


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_models_get(
    model_id: Annotated[str, "Model ID (UUID)"],
) -> Any:
    """Get a user-generated AI model by ID."""
    return auth.get(f"/datascience/ml/v1/models/{model_id}")


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_models_update(
    model_id: Annotated[str, "Model ID (UUID)"],
    body: Annotated[
        dict[str, Any],
        (
            "Full model object. Required: id (str UUID). Keys: type, name, description, "
            "owner (str user ID), projectIds (list of UUIDs), tasks (list), "
            "executionTypes (list), training (metrics/hyperparameters/algorithm), "
            "autoMLModelContext, endpointStatus, permissionLevel"
        ),
    ],
) -> Any:
    """Replace a user-generated AI model definition."""
    return auth.put(f"/datascience/ml/v1/models/{model_id}", body=body)


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_models_update_owner(
    model_id: Annotated[str, "Model ID (UUID)"],
    user_id: Annotated[int, "New owner user ID"],
) -> Any:
    """Transfer ownership of a user-generated AI model."""
    return auth.post(f"/datascience/ml/v1/models/{model_id}/ownership", body={"userId": user_id})


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_models_delete(
    model_id: Annotated[str, "Model ID (UUID) to delete"],
) -> Any:
    """Delete a user-generated AI model."""
    return auth.delete(f"/datascience/ml/v1/models/{model_id}")


# ---------------------------------------------------------------------------
# AI Projects
# ---------------------------------------------------------------------------

@domo_tool(toolset="ai_data_science", read_only=True)
def ai_projects_list(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: limit (int), "
            "sortFieldMap (dict e.g. {'CREATED': 'DESC'}), "
            "searchFieldMap (dict e.g. {'NAME': ''}), "
            "filters (list of {type, values} — type options: 'TYPE', 'OWNER'), "
            "dateFilters (dict)"
        ),
    ],
) -> Any:
    """List or search AI projects."""
    return auth.post_read("/datascience/ml/v1/search/projects", body=body)


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_projects_get(
    project_id: Annotated[str, "Project ID (UUID)"],
) -> Any:
    """Get an AI project by ID."""
    return auth.get(f"/datascience/ml/v1/projects/{project_id}")


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_projects_update(
    project_id: Annotated[str, "Project ID (UUID)"],
    body: Annotated[
        dict[str, Any],
        (
            "Full project object. Required: id (str UUID). Keys: type, name, description, "
            "owner (str user ID), created, updated, modelCount (int), "
            "autoMLProjectContext ({dataSourceId, targetColumn}), "
            "customProjectContext (dict), permissionLevel"
        ),
    ],
) -> Any:
    """Replace an AI project definition."""
    return auth.put(f"/datascience/ml/v1/projects/{project_id}", body=body)


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_projects_update_owner(
    project_id: Annotated[str, "Project ID (UUID)"],
    user_id: Annotated[int, "New owner user ID"],
) -> Any:
    """Transfer ownership of an AI project."""
    return auth.post(f"/datascience/ml/v1/projects/{project_id}/ownership", body={"userId": user_id})


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_projects_delete(
    project_id: Annotated[str, "Project ID (UUID) to delete"],
) -> Any:
    """Delete an AI project."""
    return auth.delete(f"/datascience/ml/v1/projects/{project_id}")


# ---------------------------------------------------------------------------
# AI Service Layer — Text to SQL / Text Generation / Beast Mode /
# Summarization / Forecasting / Image to Text
# ---------------------------------------------------------------------------

AIService = Literal["sql", "generation", "beastmode", "summarization", "forecasting", "image"]
AIRunService = Literal["sql", "generation", "beastmode", "summarization", "image"]

_AI_RUN_PATHS = {
    "sql": "/ai/v1/text/sql",
    "generation": "/ai/v1/text/generation",
    "beastmode": "/ai/v1/text/beastmode",
    "summarization": "/ai/v1/text/summarize",
    "image": "/ai/v1/image/text",
}


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_services_list_models(
    service: Annotated[AIService, "AI service: sql (Text to SQL), generation, beastmode, summarization, forecasting, image (Image to Text)"],
) -> Any:
    """List the models available to a Domo AI service."""
    return auth.get(f"/ai/v1/settings/services/{service}/models")


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_services_get_default_model(
    service: Annotated[AIService, "AI service: sql (Text to SQL), generation, beastmode, summarization, forecasting, image (Image to Text)"],
) -> Any:
    """Get the default model configured for a Domo AI service."""
    return auth.get(f"/ai/v1/settings/services/{service}/models/default")


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_services_run(
    service: Annotated[AIRunService, "AI service to run"],
    body: Annotated[
        dict[str, Any],
        (
            "Request body. All services accept optional model (str model ID) and "
            "promptTemplate ({template: str}); all but generation accept system (str). "
            "Required by service — "
            "sql: input (natural language question), dataSourceSchemas (list of "
            "{dataSourceName, columns: [{name, type}]}); "
            "generation: input (prompt); "
            "beastmode: input (natural language request), dataSourceSchema "
            "({dataSourceName, columns: [{name, type}]}); "
            "summarization: input (text to summarize); "
            "image: input (instructions), image ({mediaType, type: 'base64', data})"
        ),
    ],
) -> Any:
    """Run a Domo AI service: generate SQL or a Beast Mode expression from natural
    language, generate or summarize text, or extract text from an image. Consumes
    AI credits. To run a forecast query, use datasets_query with SQL."""
    return auth.post(_AI_RUN_PATHS[service], body=body)


# ---------------------------------------------------------------------------
# AI Service Layer — General
# ---------------------------------------------------------------------------

@domo_tool(toolset="ai_data_science", read_only=True)
def ai_get_settings() -> Any:
    """Get general AI service settings for the instance."""
    return auth.get("/ai/v1/settings/general")


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_get_session(
    session_id: Annotated[str, "AI session ID (UUID)"],
) -> Any:
    """Get an AI chat session by ID."""
    return auth.get(f"/ai/v1/sessions/{session_id}")


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_get_session_context(
    session_id: Annotated[str, "AI session ID (UUID)"],
) -> Any:
    """Get the context (history and state) of an AI chat session."""
    return auth.get(f"/ai/v1/sessions/{session_id}/context")


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_ask_chat(
    body: Annotated[
        dict[str, Any],
        (
            "Chat request body. Required: input (str user message). "
            "Optional: sessionId (str UUID), agentType (str e.g. 'REACT'), "
            "aiAssistantContext ({dataSourceIds, cardIds, pageIds, filters, ignorableDataSourceIds})"
        ),
    ],
) -> Any:
    """Send a message to the Domo AI assistant (streaming endpoint)."""
    return auth.post(
        "/ai/v1/assistant/toolkits/DOMO_BASIC_ASSISTANT/execute/streaming",
        body=body,
    )


# ---------------------------------------------------------------------------
# Jupyter Workspaces — File Shares
# ---------------------------------------------------------------------------

@domo_tool(toolset="ai_data_science", read_only=True)
def ai_jupyter_list_file_shares() -> Any:
    """List all Jupyter file shares."""
    return auth.get("/fileshare/v1/shares")


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_jupyter_get_file_share_perms(
    share_id: Annotated[str, "File share ID"],
) -> Any:
    """Get permissions for a Jupyter file share."""
    return auth.get(f"/fileshare/v1/shares/{share_id}/permissions")


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_jupyter_create_file_share(
    name: Annotated[str, "File share name"],
    description: Annotated[str | None, "File share description"] = None,
    default_mount_point: Annotated[str | None, "Default mount point path"] = None,
) -> Any:
    """Create a new Jupyter file share."""
    body: dict[str, Any] = {"name": name}
    if description is not None:
        body["description"] = description
    if default_mount_point is not None:
        body["defaultMountPoint"] = default_mount_point
    return auth.post("/fileshare/v1/shares", body=body)


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_jupyter_update_file_share(
    share_id: Annotated[str, "File share ID"],
    body: Annotated[
        dict[str, Any],
        (
            "File share update object. Keys: name (str), description (str), "
            "defaultMountPoint (str), fileshareType (str e.g. 'SHARED'), "
            "lifecycleOwner (str user ID), lifecycleOwnerType (str), permissionLevel"
        ),
    ],
) -> Any:
    """Update a Jupyter file share."""
    return auth.put(f"/fileshare/v1/shares/{share_id}", body=body)


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_jupyter_update_file_share_perms(
    share_id: Annotated[str, "File share ID"],
    share: Annotated[
        list[dict[str, Any]] | None,
        "Permissions to add: list of {entityId (int), permissionLevel (str e.g. 'ADMIN'), entityType (str e.g. 'USER')}",
    ] = None,
    unshare: Annotated[
        list[dict[str, Any]] | None,
        "Permissions to remove: list of {entityId (int), entityType (str)}",
    ] = None,
) -> Any:
    """Update permissions on a Jupyter file share."""
    body: dict[str, Any] = {}
    if share is not None:
        body["share"] = share
    if unshare is not None:
        body["unshare"] = unshare
    return auth.post(f"/fileshare/v1/shares/{share_id}/permissions", body=body)


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_jupyter_delete_file_share(
    share_id: Annotated[str, "File share ID to delete"],
) -> Any:
    """Delete a Jupyter file share."""
    return auth.delete(f"/fileshare/v1/shares/{share_id}")


# ---------------------------------------------------------------------------
# Jupyter Workspaces
# ---------------------------------------------------------------------------

@domo_tool(toolset="ai_data_science", read_only=True)
def ai_jupyter_list_workspaces(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: filters (list of {type, values} — type options: 'OWNER'), "
            "limit (int), offset (int), sortFieldMap (dict e.g. {'LAST_RUN': 'DESC'}), "
            "searchFieldMap (dict)"
        ),
    ],
) -> Any:
    """List or search Jupyter workspaces."""
    return auth.post_read("/datascience/v1/search/workspaces", body=body)


@domo_tool(toolset="ai_data_science", read_only=True)
def ai_jupyter_get_workspace(
    workspace_id: Annotated[str, "Jupyter workspace ID"],
) -> Any:
    """Get a Jupyter workspace by ID."""
    return auth.get(f"/datascience/v1/workspaces/{workspace_id}")


@domo_tool(toolset="ai_data_science", read_only=False)
def ai_jupyter_update_workspace_owner(
    workspace_id: Annotated[str, "Jupyter workspace ID"],
    new_owner_id: Annotated[int, "New owner user ID"],
) -> Any:
    """Transfer ownership of a Jupyter workspace."""
    return auth.put(
        f"/datascience/v1/workspaces/{workspace_id}/ownership",
        body={"newOwnerId": new_owner_id},
    )
