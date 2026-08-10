"""Reports tools — slideshow publication reports.

API reference: api-definitions-md/29-reports-slideshow-publications-.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="reports", read_only=True)
def reports_list() -> Any:
    """List all slideshow publication reports."""
    return auth.get("/content/v1/reports")


@domo_tool(toolset="reports", read_only=False)
def reports_create(
    body: Annotated[
        dict[str, Any],
        (
            "Report definition. Keys: title (str), type (str e.g. 'slideshow'), "
            "properties ({isShared, tokenId, isAccessCodeRequired, accessCode}), "
            "cardIds (list of str)"
        ),
    ],
) -> Any:
    """Create a new slideshow publication report."""
    return auth.post("/content/v1/reports", body=body)


@domo_tool(toolset="reports", read_only=False)
def reports_update(
    report_id: Annotated[str, "Report ID"],
    body: Annotated[
        dict[str, Any],
        (
            "Full report object. Keys: id (int), ownerId (int), title (str), "
            "created, updated, subject, schedule, "
            "properties ({isShared, tokenId, isAccessCodeRequired, accessCode}), "
            "cardIds (list)"
        ),
    ],
) -> Any:
    """Update a slideshow publication report."""
    return auth.put(f"/content/v1/reports/{report_id}", body=body)


@domo_tool(toolset="reports", read_only=False)
def reports_delete(
    report_id: Annotated[str, "Report ID to delete"],
) -> Any:
    """Delete a slideshow publication report."""
    return auth.delete(f"/content/v1/reports/{report_id}")
