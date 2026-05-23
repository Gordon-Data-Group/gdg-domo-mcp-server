"""Sandbox tools — environment promotion, repositories, commit requests.

API reference: api-definitions-md/31-sandbox.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def sandbox_list_repositories(
    body: Annotated[
        dict[str, Any] | None,
        "Search body. Keys: query ({offset, limit, fieldSearchMap, sort, order, filters, dateFilters}), shared (bool)",
    ] = None,
) -> Any:
    """List sandbox repositories."""
    return auth.post(
        "/version/v1/repositories/search",
        body=body or {"query": {"offset": 0, "limit": 50, "fieldSearchMap": {}, "sort": "started", "order": "desc", "filters": {}, "dateFilters": {}}, "shared": True},
    )


@mcp.tool()
def sandbox_list_promotion_history(
    body: Annotated[
        dict[str, Any] | None,
        "Search body. Keys: offset (int), limit (int), filters ({repositoryName, commitName, status, userId}), fieldSearchMap, sort, order, searchDistinct, dateFilters",
    ] = None,
) -> Any:
    """List sandbox promotion history."""
    return auth.post(
        "/version/v1/promotions/search",
        body=body or {"offset": 0, "limit": 500, "filters": {}, "fieldSearchMap": {}, "sort": "completed", "order": "desc", "searchDistinct": False, "dateFilters": {}},
    )


@mcp.tool()
def sandbox_list_commit_history(
    body: Annotated[
        dict[str, Any] | None,
        "Search body. Keys: offset (int), limit (int), filters ({repositoryName, commitName, status}), fieldSearchMap, sort, order, searchDistinct, dateFilters",
    ] = None,
) -> Any:
    """List sandbox commit request history."""
    return auth.post(
        "/version/v1/commitRequests/search",
        body=body or {"offset": 0, "limit": 500, "filters": {}, "fieldSearchMap": {}, "sort": "completed", "order": "desc", "searchDistinct": False, "dateFilters": {}},
    )


@mcp.tool()
def sandbox_list_instances(
    limit: Annotated[int | None, "Max instances to return"] = None,
) -> Any:
    """List sandbox instance authorizations."""
    return auth.get("/version/v1/authorizations", limit=limit)


@mcp.tool()
def sandbox_get_repository(
    repository_id: Annotated[str, "Repository ID"],
) -> Any:
    """Get a sandbox repository by ID."""
    return auth.get(f"/version/v1/repositories/{repository_id}")


@mcp.tool()
def sandbox_get_repository_commits(
    repository_id: Annotated[str, "Repository ID"],
) -> Any:
    """Get commits for a sandbox repository."""
    return auth.get(f"/version/v1/repositories/{repository_id}/commits")


@mcp.tool()
def sandbox_get_repository_commit_reqs(
    repository_id: Annotated[str, "Repository ID"],
) -> Any:
    """Get commit requests for a sandbox repository."""
    return auth.get(f"/version/v1/repositories/{repository_id}/commitRequests")


@mcp.tool()
def sandbox_get_repository_permissions(
    repository_id: Annotated[str, "Repository ID"],
) -> Any:
    """Get user/group permissions for a sandbox repository."""
    return auth.get(f"/version/v1/repositories/{repository_id}/permissions")


@mcp.tool()
def sandbox_get_instance_access(
    repository_id: Annotated[str, "Repository ID"],
) -> Any:
    """Get instance access list for a sandbox repository."""
    return auth.get(f"/version/v1/repositories/{repository_id}/access")


@mcp.tool()
def sandbox_get_settings() -> Any:
    """Get sandbox settings for the instance."""
    return auth.get("/version/v1/settings")


@mcp.tool()
def sandbox_promote_and_link(
    repository_id: Annotated[str, "Repository ID"],
    deployment_id: Annotated[str, "Deployment ID"],
    body: Annotated[
        dict[str, Any],
        "Promotion body. Keys: commitId (str UUID), mapping (list of {mappingId, deployObjectId, repositoryObjectId, contentType, link}), pusherEventId (str), approvalId (str), seedingRepoName (str)",
    ],
) -> Any:
    """Promote and link a sandbox commit to a deployment."""
    return auth.post(
        f"/version/v1/repositories/{repository_id}/deployments/{deployment_id}/promoteAndSeed",
        body=body,
    )


@mcp.tool()
def sandbox_create_commit(
    repository_id: Annotated[str, "Repository ID"],
    summary: Annotated[str, "Commit summary message"],
    hidden: Annotated[bool | None, "Hide the commit"] = None,
    pusher_event_id: Annotated[str | None, "Pusher event ID"] = None,
) -> Any:
    """Create a commit request for a sandbox repository."""
    body: dict[str, Any] = {"summary": summary}
    if hidden is not None:
        body["hidden"] = hidden
    if pusher_event_id is not None:
        body["pusherEventId"] = pusher_event_id
    return auth.post(f"/version/v1/repositories/{repository_id}/commitRequests", body=body)


@mcp.tool()
def sandbox_update_repository_perms(
    repository_id: Annotated[str, "Repository ID"],
    permission_updates: Annotated[
        list[dict[str, Any]],
        "Permission updates. Each: userId (str), groupId (str), permission (str e.g. 'NONE')",
    ],
) -> Any:
    """Update user/group permissions for a sandbox repository."""
    return auth.post(
        f"/version/v1/repositories/{repository_id}/permissions",
        body={"repositoryPermissionUpdates": permission_updates},
    )


@mcp.tool()
def sandbox_update_instance_access(
    repository_id: Annotated[str, "Repository ID"],
    domains: Annotated[list[str], "List of allowed domains (e.g. ['sub1.domain.tld'])"],
) -> Any:
    """Update the instance access list for a sandbox repository."""
    return auth.post(f"/version/v1/repositories{repository_id}/access", body=domains)


@mcp.tool()
def sandbox_update_instance_alias(
    aliased_domain: Annotated[str, "Full domain to alias (e.g. 'test.domo.com')"],
    alias: Annotated[str, "Alias name (e.g. 'test')"],
) -> Any:
    """Set an alias for a sandbox instance domain."""
    return auth.post(
        "/version/v1/authorizations/aliases",
        body={"aliasedDomain": aliased_domain, "alias": alias},
    )
