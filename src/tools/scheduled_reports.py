"""Scheduled Reports tools — report schedule CRUD, send-now, view management.

API reference: api-definitions-md/32-scheduled-reports.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="scheduled_reports", read_only=True)
def scheduled_reports_list(
    filter: Annotated[str | None, "Filter term"] = None,
    is_ascending: Annotated[bool | None, "Sort ascending"] = None,
    order_by: Annotated[str | None, "Sort field"] = None,
) -> Any:
    """List scheduled reports."""
    return auth.get(
        "/content/v1/reportschedules",
        filter=filter,
        isAscending=is_ascending,
        orderBy=order_by,
    )


@domo_tool(toolset="scheduled_reports", read_only=True)
def scheduled_reports_list_resources(
    limit: Annotated[int | None, "Max results to return"] = None,
    skip: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List resources available for scheduled reports."""
    return auth.get("/content/v1/reportschedules/resources", limit=limit, skip=skip)


@domo_tool(toolset="scheduled_reports", read_only=True)
def scheduled_reports_get(
    report_id: Annotated[str, "Scheduled report ID"],
) -> Any:
    """Get a scheduled report by ID."""
    return auth.get(f"/content/v1/reportschedules/{report_id}")


@domo_tool(toolset="scheduled_reports", read_only=True)
def scheduled_reports_get_history(
    report_id: Annotated[str, "Scheduled report ID"],
    limit: Annotated[int | None, "Max results to return"] = None,
    skip: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """Get the send history for a scheduled report."""
    return auth.get(
        f"/content/v1/reportschedules/{report_id}/history",
        limit=limit,
        skip=skip,
    )


@domo_tool(toolset="scheduled_reports", read_only=True)
def scheduled_reports_get_for_resource(
    resource_type: Annotated[str, "Resource type (e.g. 'CARD')"],
    resource_id: Annotated[str, "Resource ID"],
    skip: Annotated[int | None, "Pagination offset"] = None,
    limit: Annotated[int | None, "Max results to return"] = None,
    show_all: Annotated[bool | None, "Show all schedules including inactive"] = None,
) -> Any:
    """Get scheduled reports for a specific resource."""
    return auth.get(
        f"/content/v1/reportschedules/resources/{resource_type}/{resource_id}",
        skip=skip,
        limit=limit,
        showAll=show_all,
    )


@domo_tool(toolset="scheduled_reports", read_only=True)
def scheduled_reports_get_view(
    view_id: Annotated[str, "View ID"],
) -> Any:
    """Get a view by ID."""
    return auth.get(f"/content/v2/views/{view_id}")


@domo_tool(toolset="scheduled_reports", read_only=True)
def scheduled_reports_search_history(
    body: Annotated[
        dict[str, Any],
        "Search body. Keys: includeTypeClause (bool), isAutomated (bool), includeTitleClause (bool), includeStatusClause (bool), includeScheduleIdClause (bool), scheduleId (str), status (str e.g. 'success')",
    ],
    limit: Annotated[int | None, "Max results to return"] = None,
    skip: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """Search scheduled report history."""
    return auth.post(
        "/content/v1/reportschedules/history/search",
        body=body,
        limit=limit,
        skip=skip,
    )


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_send_now(
    report_id: Annotated[str, "Scheduled report ID"],
    recipients: Annotated[
        list[dict[str, Any]],
        "List of recipients, each with 'type' (str) and 'value' (str user/email ID)",
    ],
) -> Any:
    """Send a scheduled report immediately."""
    return auth.post(f"/content/v1/reportschedules/{report_id}/sendnow", body=recipients)


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_create(
    body: Annotated[
        dict[str, Any],
        "Report definition. Keys: subject (str), attachmentInclude (bool), schedule ({frequency, enabled, daysToRun, hourOfDay, minOfHour, expirationDate, startDate, additionalRecipients}), viewId (int)",
    ],
) -> Any:
    """Create a new scheduled report."""
    return auth.post("/content/v1/reportschedules", body=body)


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_create_view(
    body: Annotated[
        dict[str, Any],
        "View definition. Keys: name (str), resourceType (str), resourceId (int), type (str), purpose (str), filterGroupIds (list), filters (list), functionOverrides (dict), chartState ({chartType, overrides}), overrideDateRange (bool), overrideSlicers (bool), segmentIds (list)",
    ],
) -> Any:
    """Create a new view for use with scheduled reports."""
    return auth.post("/content/v2/views", body=body)


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_update(
    report_id: Annotated[str, "Scheduled report ID"],
    body: Annotated[dict[str, Any], "Full scheduled report object to replace"],
) -> Any:
    """Update a scheduled report."""
    return auth.put(f"/content/v1/reportschedules/{report_id}", body=body)


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_enable_disable(
    report_id: Annotated[str, "Scheduled report ID"],
    enabled: Annotated[bool, "True to enable, False to disable"],
) -> Any:
    """Enable or disable a scheduled report."""
    return auth.put(f"/content/v1/reportschedules/{report_id}/enabled", body=enabled)


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_update_view(
    view_id: Annotated[str, "View ID"],
    body: Annotated[dict[str, Any], "Full view object to replace"],
) -> Any:
    """Update a view."""
    return auth.put(f"/content/v2/views/{view_id}", body=body)


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_delete(
    report_id: Annotated[str, "Scheduled report ID to delete"],
) -> Any:
    """Delete a scheduled report."""
    return auth.delete(f"/content/v1/reportschedules/{report_id}")


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_resubscribe(
    report_id: Annotated[str, "Scheduled report ID"],
) -> Any:
    """Resubscribe the current user to a scheduled report."""
    return auth.delete(f"/content/v1/reportschedules/{report_id}/unsubscribe/recipient")


@domo_tool(toolset="scheduled_reports", read_only=False)
def scheduled_reports_unsubscribe(
    report_id: Annotated[str, "Scheduled report ID"],
) -> Any:
    """Unsubscribe the current user from a scheduled report."""
    return auth.post(f"/content/v1/reportschedules/{report_id}/unsubscribe")
