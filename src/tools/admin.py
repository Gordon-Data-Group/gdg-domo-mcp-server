"""Admin tools — activity logs, access tokens, sessions, company settings, OAuth clients.

API reference: api-definitions-md/03-admin.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


# ---------------------------------------------------------------------------
# Access Tokens
# ---------------------------------------------------------------------------

@domo_tool(toolset="admin", read_only=True)
def admin_list_access_tokens() -> Any:
    """List all access tokens in the instance."""
    return auth.get("/data/v1/accesstokens")


@domo_tool(toolset="admin", read_only=False)
def admin_delete_access_token(
    token_id: Annotated[str, "Access token ID to revoke"],
) -> Any:
    """Revoke and delete an access token."""
    return auth.delete(f"/data/v1/accesstokens/{token_id}")


# ---------------------------------------------------------------------------
# Activity Log
# ---------------------------------------------------------------------------

@domo_tool(toolset="admin", read_only=True)
def admin_list_activity_log_types() -> Any:
    """List all auditable object types for the activity log."""
    return auth.get("/audit/v1/user-audits/objectTypes")


@domo_tool(toolset="admin", read_only=True)
def admin_get_activity_log(
    start: Annotated[str | None, "Start datetime for the log range (ISO 8601 or epoch ms)"] = None,
    end: Annotated[str | None, "End datetime for the log range (ISO 8601 or epoch ms)"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    limit: Annotated[int | None, "Max events to return"] = None,
    object_type: Annotated[str | None, "Filter by object type (from admin_list_activity_log_types)"] = None,
) -> Any:
    """Get activity log events with optional date range and type filters."""
    return auth.get(
        "/audit/v1/user-audits",
        start=start,
        end=end,
        offset=offset,
        limit=limit,
        objectType=object_type,
    )


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------

@domo_tool(toolset="admin", read_only=True)
def admin_get_customer_stats() -> Any:
    """Get aggregate usage statistics for the Domo instance."""
    return auth.get("/query/v1/datasources/customer-stats")


@domo_tool(toolset="admin", read_only=True)
def admin_list_timezones() -> Any:
    """List all timezone options available for dataflows and scheduling."""
    return auth.get("/dataprocessing/v1/dataflows/timezones")


@domo_tool(toolset="admin", read_only=True)
def admin_get_locale(
    ignore_cache: Annotated[bool | None, "Bypass cache and fetch fresh locale data"] = None,
) -> Any:
    """Get the locale configuration for the Domo instance."""
    return auth.get("/content/v1/customer-states/locale", ignoreCache=ignore_cache)


@domo_tool(toolset="admin", read_only=True)
def admin_get_customer_state(
    customer_state: Annotated[str, "Customer state key to retrieve (e.g. 'domo.policy.multifactor.maxCodeAttempts')"],
    ignore_cache: Annotated[bool | None, "Bypass cache and fetch fresh state data"] = None,
) -> Any:
    """Get a specific customer state value by key."""
    return auth.get(
        f"/content/v1/customer-states/{customer_state}",
        ignoreCache=ignore_cache,
    )


@domo_tool(toolset="admin", read_only=True)
def admin_get_licenses() -> Any:
    """Get current license counts and limits for the Domo instance."""
    return auth.get("/content/v1/licenses/total/current")


@domo_tool(toolset="admin", read_only=True)
def admin_get_jupyter_settings() -> Any:
    """Get Jupyter notebook settings for the instance."""
    return auth.get("/datascience/v1/settings")


@domo_tool(toolset="admin", read_only=True)
def admin_get_credits_summary() -> Any:
    """Get the current credit usage summary for the instance's contract period."""
    return auth.get("/metrics/v1/usage/credits/contract/current/summary")


@domo_tool(toolset="admin", read_only=True)
def admin_get_default_landing_page() -> Any:
    """Get the default landing page configured for the instance."""
    return auth.get("/content/v1/landings/customer")


@domo_tool(toolset="admin", read_only=False)
def admin_update_customer_state(
    customer_state: Annotated[str, "Customer state key to update"],
    name: Annotated[str, "State name"],
    value: Annotated[str, "New state value"],
) -> Any:
    """Update a customer state value."""
    return auth.put(
        f"/content/v1/customer-states/{customer_state}",
        body={"name": name, "value": value},
    )


@domo_tool(toolset="admin", read_only=False)
def admin_update_property(
    property: Annotated[str, "Property key to update"],
    body: Annotated[
        dict[str, Any],
        (
            "Property update object. Keys: keyspace (str), issuer (str), entityId (str), "
            "key (str), value (str), values (list of str)"
        ),
    ],
) -> Any:
    """Update a customer property value."""
    return auth.put(f"/customer/v1/properties/{property}", body=body)


# ---------------------------------------------------------------------------
# OAuth API Clients
# ---------------------------------------------------------------------------

@domo_tool(toolset="admin", read_only=True)
def admin_list_oauth_clients() -> Any:
    """List all OAuth API client (developer token) configurations."""
    return auth.get("/identity/v1/developer-tokens")


# ---------------------------------------------------------------------------
# Session Management
# ---------------------------------------------------------------------------

@domo_tool(toolset="admin", read_only=False)
def admin_delete_session(
    session_id: Annotated[str, "Session ID to terminate"],
) -> Any:
    """Terminate an active user session."""
    return auth.delete(f"/sessions/v1/admin/{session_id}")
