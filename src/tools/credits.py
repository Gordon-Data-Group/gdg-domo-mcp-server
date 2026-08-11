"""Credits tools — credit usage reporting and contract details.

API reference: api-definitions-md/15-credits.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="credits", read_only=True)
def credits_get_usage_report(
    start_date: Annotated[str | None, "Start date for the report (YYYY-MM-DD). Required in practice — API returns 400 without it."] = None,
    end_date: Annotated[str | None, "End date for the report (YYYY-MM-DD). Required in practice — API returns 400 without it."] = None,
) -> Any:
    """Get the credit usage report broken down by month. Note: start_date and end_date are required by the API even though marked optional."""
    return auth.get(
        "/metrics/v1/usage/credits/reports/usage",
        startDate=start_date,
        endDate=end_date,
    )


@domo_tool(toolset="credits", read_only=True)
def credits_get_subscription_details() -> Any:
    """Get subscription page and contract details for the instance."""
    return auth.get("/metrics/v1/usage/credits/reports/subscription")


@domo_tool(toolset="credits", read_only=True)
def credits_get_balance() -> Any:
    """Get credit balance and statements for the instance."""
    return auth.get("/metrics/v1/usage/credits/reports/balance")
