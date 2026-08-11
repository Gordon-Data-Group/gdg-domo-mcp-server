"""Approvals tools — approval workflow templates and requests (GraphQL).

API reference: api-definitions-md/07-approvals.md
Note: all operations POST to /synapse/approval/graphql with a GraphQL body.
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth

_GQL = "/synapse/approval/graphql"

_SEARCH_TEMPLATES_QUERY = (
    "\nquery getApprovalTemplatesConnection(\n  $first: Int\n  $after: ID\n  $orderBy: OrderBy\n"
    "  $reverseSort: Boolean\n  $query: TemplateQueryRequest!\n) {\n  templateConnection(\n"
    "    first: $first\n    after: $after\n    orderBy: $orderBy\n    reverseSort: $reverseSort\n"
    "    query: $query\n  ) {\n    edges {\n      cursor\n      node {\n        id\n        datasetId\n"
    "        title\n        isPublic\n        providerName\n        description\n        observers {\n"
    "          id\n          type\n          displayName\n          avatarKey\n          title\n"
    "          ... on Group {\n            userCount\n          }\n        }\n        owner {\n"
    "          id\n          displayName\n          avatarKey\n          isCurrentUser\n          title\n"
    "        }\n        fieldCount\n        useCount\n        categories {\n          id\n          name\n"
    "        }\n      }\n    }\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n"
    "      startCursor\n      endCursor\n    }\n  }\n}"
)

_SEARCH_APPROVALS_QUERY = (
    "query getFilteredRequests($query: QueryRequest!, $after: ID, $reverseSort: Boolean) {\n"
    "  workflowSearch(\n    query: $query\n    type: \"AC\"\n    after: $after\n    reverseSort: $reverseSort\n"
    "  ) {\n    edges {\n      cursor\n      node {\n        approval {\n          id\n          title\n"
    "          templateID\n          templateTitle\n          status\n          modifiedTime\n          version\n"
    "          providerName\n          approvalChainIdx\n          pendingApprover: pendingApproverEx {\n"
    "            id\n            type\n            displayName\n            ... on User {\n              title\n"
    "              avatarKey\n            }\n            ... on Group {\n              isDeleted\n            }\n"
    "          }\n          submitter {\n            id\n            type\n            displayName\n"
    "            avatarKey\n            isCurrentUser\n          }\n        }\n      }\n    }\n"
    "    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n    }\n  }\n}"
)

_LIST_TEMPLATES_QUERY = (
    "query listTemplates {\n  templates {\n    id\n    title\n    titleName\n    titlePlaceholder\n"
    "    acknowledgment\n    instructions\n    description\n    providerName\n    isPublic\n"
    "    chainIsLocked\n    type\n    isPublished\n    observers {\n      id\n      type\n"
    "      displayName\n      avatarKey\n      title\n      ... on Group {\n        userCount\n      }\n"
    "    }\n    categories {\n      id\n      name\n    }\n    owner {\n      id\n      displayName\n"
    "      avatarKey\n    }\n  }\n}"
)

_GET_TEMPLATE_QUERY = (
    "query getTemplateForEdit($id: ID!) {\n  template(id: $id) {\n    id\n    title\n    titleName\n"
    "    titlePlaceholder\n    acknowledgment\n    instructions\n    description\n    providerName\n"
    "    isPublic\n    chainIsLocked\n    type\n    isPublished\n    observers {\n      id\n      type\n"
    "      displayName\n      avatarKey\n      title\n    }\n    categories {\n      id\n      name\n    }\n"
    "    owner {\n      id\n      displayName\n      avatarKey\n    }\n    fields {\n      key\n      type\n"
    "      name\n      data\n      placeholder\n      required\n      isPrivate\n    }\n    approvers {\n"
    "      type\n      key\n      ... on ApproverPerson {\n        approverId\n        userDetails {\n"
    "          id\n          displayName\n          title\n          avatarKey\n        }\n      }\n"
    "      ... on ApproverGroup {\n        approverId\n        groupDetails {\n          id\n"
    "          displayName\n          userCount\n          isDeleted\n        }\n      }\n"
    "      ... on ApproverPlaceholder {\n        placeholderText\n      }\n    }\n  }\n  categories {\n"
    "    id\n    name\n  }\n}"
)

_GET_APPROVAL_QUERY = (
    "query getApprovalForDetails($id: ID!) {\n  request: approval(id: $id) {\n    id\n    title\n"
    "    status\n    templateID\n    templateTitle\n    modifiedTime\n    submittedTime\n    version\n"
    "    providerName\n    approvalChainIdx\n    submitter { id displayName title avatarKey isCurrentUser type }\n"
    "    pendingApprover: pendingApproverEx { id type displayName }\n    chain {\n      approver { id type displayName }\n"
    "      status\n      time\n      type\n      key\n    }\n    fields { data name type key }\n    history {\n"
    "      actor { type id displayName }\n      status\n      time\n    }\n  }\n}"
)

_SAVE_TEMPLATE_MUTATION = (
    "mutation saveTemplate($template: TemplateInput!) {\n  template: saveTemplate(template: $template) {\n"
    "    id\n    title\n    titleName\n    titlePlaceholder\n    acknowledgment\n    instructions\n"
    "    description\n    providerName\n    isPublic\n    chainIsLocked\n    owner { id displayName avatarKey }\n"
    "    fields { key type name placeholder required isLocked }\n    approvers {\n      type\n      key\n"
    "      ... on ApproverPerson { approverId userDetails { id displayName title avatarKey } }\n"
    "      ... on ApproverGroup { approverId groupDetails { id displayName userCount isDeleted } }\n"
    "      ... on ApproverPlaceholder { placeholderText }\n    }\n  }\n}"
)


@domo_tool(toolset="approvals", read_only=True)
def approvals_search_templates(
    first: Annotated[int | None, "Max templates to return"] = None,
    after: Annotated[str | None, "Cursor for pagination"] = None,
    order_by: Annotated[str | None, "Sort field (e.g. 'TEMPLATE')"] = None,
    reverse_sort: Annotated[bool | None, "Reverse sort order"] = None,
    query: Annotated[
        dict[str, Any] | None,
        "Template query filter. Keys: type, searchTerm, category (list), ownerId, publishedOnly",
    ] = None,
) -> Any:
    """Search approval templates with filters."""
    variables: dict[str, Any] = {
        "query": query or {"type": "AC", "searchTerm": "", "category": [], "ownerId": None, "publishedOnly": False},
    }
    if first is not None:
        variables["first"] = first
    if after is not None:
        variables["after"] = after
    if order_by is not None:
        variables["orderBy"] = order_by
    if reverse_sort is not None:
        variables["reverseSort"] = reverse_sort
    return auth.post(_GQL, body={
        "operationName": "getApprovalTemplatesConnection",
        "query": _SEARCH_TEMPLATES_QUERY,
        "variables": variables,
    })


@domo_tool(toolset="approvals", read_only=True)
def approvals_search(
    query: Annotated[
        dict[str, Any] | None,
        "Approval filter. Keys: active, submitterId, approverId, templateId, title, lastModifiedBefore",
    ] = None,
    after: Annotated[str | None, "Cursor for pagination"] = None,
    reverse_sort: Annotated[bool | None, "Reverse sort order"] = None,
) -> Any:
    """Search approval requests with filters."""
    return auth.post(_GQL, body={
        "operationName": "getFilteredRequests",
        "query": _SEARCH_APPROVALS_QUERY,
        "variables": {
            "query": query or {},
            "after": after,
            "reverseSort": reverse_sort or False,
        },
    })


@domo_tool(toolset="approvals", read_only=True)
def approvals_list_templates() -> Any:
    """List all approval templates."""
    return auth.post(_GQL, body={
        "operationName": "listTemplates",
        "query": _LIST_TEMPLATES_QUERY,
    })


@domo_tool(toolset="approvals", read_only=True)
def approvals_get_template(
    template_id: Annotated[str, "Template ID (UUID)"],
) -> Any:
    """Get an approval template by ID."""
    return auth.post(_GQL, body=[{
        "operationName": "getTemplateForEdit",
        "query": _GET_TEMPLATE_QUERY,
        "variables": {"id": template_id},
    }])


@domo_tool(toolset="approvals", read_only=True)
def approvals_get(
    approval_id: Annotated[str, "Approval request ID (UUID)"],
) -> Any:
    """Get an approval request by ID."""
    return auth.post(_GQL, body={
        "operationName": "getApprovalForDetails",
        "query": _GET_APPROVAL_QUERY,
        "variables": {"id": approval_id},
    })


@domo_tool(toolset="approvals", read_only=False)
def approvals_replace_approver(
    body: Annotated[
        dict[str, Any],
        "GraphQL mutation body with operationName, query, and variables for replacing an approver",
    ],
) -> Any:
    """Replace an approver in an approval workflow (GraphQL mutation)."""
    return auth.post(_GQL, body=body)


@domo_tool(toolset="approvals", read_only=False)
def approvals_update_template(
    template: Annotated[
        dict[str, Any],
        (
            "Template definition. Keys: id (str UUID), title (str), description (str), "
            "acknowledgment, fields (list), approvers (list), observers (list), "
            "isPublic (bool), providerName (str), chainIsLocked (bool), "
            "categories ({id}), ownerId (int)"
        ),
    ],
) -> Any:
    """Save (create or update) an approval template."""
    return auth.post(_GQL, body=[{
        "operationName": "saveTemplate",
        "query": _SAVE_TEMPLATE_MUTATION,
        "variables": {"template": template},
    }])
