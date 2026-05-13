"""Domo Everywhere tools — publications and subscriber management.

API reference: api-definitions-md/18-domo-everywhere.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def domo_everywhere_list_publications() -> Any:
    """List all Domo Everywhere publications."""
    return auth.get("/publish/v2/publications")


@mcp.tool()
def domo_everywhere_list_publication_summaries(
    public: Annotated[bool | None, "Filter to public publications"] = None,
    limit: Annotated[int | None, "Max results to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    search_term: Annotated[str | None, "Search term"] = None,
    sort: Annotated[str | None, "Sort field"] = None,
) -> Any:
    """List publication summaries with optional filters."""
    return auth.get(
        "/publish/v2/publications/summaries",
        public=public,
        limit=limit,
        offset=offset,
        searchTerm=search_term,
        sort=sort,
    )


@mcp.tool()
def domo_everywhere_get_publication(
    publication_id: Annotated[str, "Publication ID"],
) -> Any:
    """Get a Domo Everywhere publication by ID."""
    return auth.get(f"/publish/v2/publications/{publication_id}")


@mcp.tool()
def domo_everywhere_get_publication_summary(
    publication_id: Annotated[str, "Publication ID"],
) -> Any:
    """Get the summary for a specific publication."""
    return auth.get(f"/publish/v2/publications/summaries/{publication_id}")


@mcp.tool()
def domo_everywhere_get_publication_status() -> Any:
    """Get the status of Domo Everywhere publications."""
    return auth.get("/publish/v2/publications/status")


@mcp.tool()
def domo_everywhere_list_subscription_summaries(
    search_term: Annotated[str | None, "Search term"] = None,
    limit: Annotated[int | None, "Max results to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List subscription summaries."""
    return auth.get(
        "/publish/v2/subscriptions/summaries",
        searchTerm=search_term,
        limit=limit,
        offset=offset,
    )


@mcp.tool()
def domo_everywhere_list_auto_subscriptions() -> Any:
    """List automatic subscriptions."""
    return auth.get("/publish/v2/automatic-subscriptions")


@mcp.tool()
def domo_everywhere_list_auto_sub_shares() -> Any:
    """List automatic subscription shares."""
    return auth.get("/publish/v2/automatic-subscriptions/shares/v1")


@mcp.tool()
def domo_everywhere_list_invites(
    search_term: Annotated[str | None, "Search term"] = None,
    limit: Annotated[int | None, "Max results to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List subscription invites."""
    return auth.get(
        "/publish/v2/subscriptions/invites",
        searchTerm=search_term,
        limit=limit,
        offset=offset,
    )


@mcp.tool()
def domo_everywhere_count_summaries(
    search_term: Annotated[str | None, "Search term"] = None,
) -> Any:
    """Count subscription summaries."""
    return auth.get("/publish/v2/subscriptions/summaries/counts", searchTerm=search_term)


@mcp.tool()
def domo_everywhere_count_invites(
    search_term: Annotated[str | None, "Search term"] = None,
) -> Any:
    """Count subscription invites."""
    return auth.get("/publish/v2/subscriptions/invites/counts", searchTerm=search_term)


@mcp.tool()
def domo_everywhere_get_subscription_share(
    subscription_id: Annotated[str, "Subscription ID"],
) -> Any:
    """Get the share details for a subscription."""
    return auth.get(f"/publish/v2/subscriptions/{subscription_id}/share")


@mcp.tool()
def domo_everywhere_update_subscription(
    subscription_id: Annotated[str, "Subscription ID"],
    body: Annotated[
        dict[str, Any],
        "Subscription update. Keys: publicationId (str UUID), domain (str), customerId (str), userId (int), userIds (list of int), groupIds (list of int)",
    ],
) -> Any:
    """Update a subscription's configuration."""
    return auth.put(f"/publish/v2/subscriptions/{subscription_id}", body=body)
