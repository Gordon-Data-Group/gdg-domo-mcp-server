"""Toolkit tools — scheduled job execution and triggers.

API reference: api-definitions-md/34-toolkit.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def toolkit_list_applications() -> Any:
    """List all Toolkit applications."""
    return auth.get("/executor/v1/applications")


@mcp.tool()
def toolkit_get_jobs(
    application_id: Annotated[str, "Application ID"],
    limit: Annotated[int | None, "Max jobs to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """Get jobs for a Toolkit application."""
    return auth.get(
        f"/executor/v2/applications/{application_id}/jobs",
        limit=limit,
        offset=offset,
    )


@mcp.tool()
def toolkit_get_job(
    application_id: Annotated[str, "Application ID"],
    job_id: Annotated[str, "Job ID"],
) -> Any:
    """Get a specific Toolkit job."""
    return auth.get(f"/executor/v1/applications/{application_id}/jobs/{job_id}")


@mcp.tool()
def toolkit_run_job(
    application_id: Annotated[str, "Application ID"],
    job_id: Annotated[str, "Job ID"],
) -> Any:
    """Run a Toolkit job."""
    return auth.post(
        f"/executor/v1/applications/{application_id}/jobs/{job_id}/executions",
        body={},
    )


@mcp.tool()
def toolkit_share_job(
    application_id: Annotated[str, "Application ID"],
    job_id: Annotated[str, "Job ID"],
    owner_user_id: Annotated[int, "Owner user ID"],
    grant_user_ids: Annotated[list[int] | None, "User IDs to grant access to"] = None,
    revoke_user_ids: Annotated[list[int] | None, "User IDs to revoke access from"] = None,
    grant_group_ids: Annotated[list[int] | None, "Group IDs to grant access to"] = None,
    revoke_group_ids: Annotated[list[int] | None, "Group IDs to revoke access from"] = None,
) -> Any:
    """Share or unshare a Toolkit job."""
    return auth.put(
        f"/executor/v1/applications/{application_id}/jobs/{job_id}/share",
        body={
            "ownerUserId": owner_user_id,
            "grantUserIds": grant_user_ids or [],
            "revokeUserIds": revoke_user_ids or [],
            "grantGroupIds": grant_group_ids or [],
            "revokeGroupIds": revoke_group_ids or [],
        },
    )


@mcp.tool()
def toolkit_create_trigger(
    app_id: Annotated[str, "Application ID"],
    job_id: Annotated[str, "Job ID"],
    event_entity: Annotated[str, "Dataset UUID to trigger on"],
    event_type: Annotated[str | None, "Event type (e.g. 'datasetUpdated')"] = None,
) -> Any:
    """Create a trigger for a Toolkit job."""
    body: dict[str, Any] = {"eventEntity": event_entity}
    if event_type is not None:
        body["eventType"] = event_type
    return auth.post(f"/executor/v1/applications/{app_id}/jobs/{job_id}/triggers", body=body)


@mcp.tool()
def toolkit_update_job(
    app_id: Annotated[str, "Application ID"],
    job_id: Annotated[str, "Job ID"],
    body: Annotated[
        dict[str, Any],
        "Full job object. Keys: jobId, applicationId, customerId, jobName, jobDescription, userId, executionTimeout, jobStatus, executionPayload, executionResponse, accounts, executionClass, created, updated, triggers, compressPayload",
    ],
) -> Any:
    """Update a Toolkit job."""
    return auth.put(f"/executor/v1/applications/{app_id}/jobs/{job_id}", body=body)


@mcp.tool()
def toolkit_delete_job(
    app_id: Annotated[str, "Application ID"],
    job_id: Annotated[str, "Job ID to delete"],
) -> Any:
    """Delete a Toolkit job."""
    return auth.delete(f"/executor/v1/applications/{app_id}/jobs/{job_id}")
