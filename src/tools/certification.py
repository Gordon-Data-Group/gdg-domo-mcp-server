"""Certification tools — content certification workflows (GraphQL).

API reference: api-definitions-md/13-certification.md
Note: most operations POST to /synapse/approval/graphql with a GraphQL body.
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth

_GQL = "/synapse/approval/graphql"

_LIST_QUERY = (
    "query getWorkflowConnection($type: String!, $after: ID, $view: View, $timePeriod: TimePeriod, "
    "$orderBy: OrderBy, $reverseSort: Boolean, $searchTerm: String, $first: Int, $templateId: ID) {\n"
    "  workflowConnection(type: $type, after: $after, view: $view, timePeriod: $timePeriod, "
    "orderBy: $orderBy, reverseSort: $reverseSort, searchTerm: $searchTerm, first: $first, "
    "templateId: $templateId) {\n    edges {\n      cursor\n      node {\n"
    "        certificationRequest { id type status entityType entityId entityTitle modifiedTime createdTime }\n"
    "        approval { id title status modifiedTime submittedTime }\n      }\n    }\n"
    "    pageInfo { hasNextPage hasPreviousPage startCursor endCursor }\n  }\n}"
)

_LIST_TEMPLATES_QUERY = (
    "query getCertifiedTemplates($type: String, $includeUnpublished: Boolean) {\n"
    "  templates(type: $type, includeUnpublished: $includeUnpublished) {\n"
    "    type id title description isPublic isPublished providerName fieldCount useCount\n"
    "    owner { id displayName avatarKey isCurrentUser title }\n  }\n}"
)

_LIST_CERTIFIED_ENTITIES_QUERY = (
    "query getCertifiedEntities($type: String!, $first: Int, $after: ID, $searchTerm: String, "
    "$stateFilter: CertifyState) {\n  certifyEntitiesConnection(type: $type, first: $first, "
    "after: $after, searchTerm: $searchTerm, stateFilter: $stateFilter) {\n    edges {\n"
    "      cursor\n      node {\n        id title entityType description processType\n"
    "        lastUpdated views dateCertified certifyState certifyApprovalId provider\n"
    "        ownerEx { id type displayName }\n      }\n    }\n"
    "    pageInfo { hasNextPage endCursor startCursor }\n  }\n}"
)

_GET_CERT_QUERY = (
    "query getCertificationDetails($id: ID!) {\n  certification(id: $id) {\n    id\n"
    "    request { id type status entityType entityId entityTitle modifiedTime createdTime\n"
    "      requestor { id displayName title avatarKey isCurrentUser } }\n"
    "    approval { id version type title status providerName templateTitle modifiedTime\n"
    "      submitter { id displayName title avatarKey isCurrentUser }\n"
    "      chain { approver { id type displayName } status time type key }\n"
    "      fields { data name type key }\n    }\n  }\n}"
)

_GET_TEMPLATE_QUERY = (
    "query getCertifiedTemplate($templateId: ID, $type: CertifyType!, $id: ID, $title: String) {\n"
    "  companyName\n  template: certifyTemplate(templateId: $templateId, type: $type, id: $id, title: $title) {\n"
    "    id type title titleName titleData titlePlaceholder instructions description providerName\n"
    "    isPublic chainIsLocked\n    owner { id displayName avatarKey }\n"
    "    fields { key type name data placeholder required disabled }\n"
    "    approvers {\n      type key\n      ... on ApproverPerson { approverId userDetails { id displayName title avatarKey } }\n"
    "      ... on ApproverGroup { approverId groupDetails { id displayName userCount isDeleted } }\n"
    "      ... on ApproverPlaceholder { placeholderText }\n    }\n  }\n}"
)

_GET_ID_FROM_APPROVAL_QUERY = (
    "query getCertificationIdFromApprovalId($id: ID!) {\n"
    "  certificationId: certificationByApprovalId(id: $id) { id }\n}"
)

_CHECK_ENTITY_ACCESS_QUERY = (
    "query checkEntityAccess($entityId: ID!, $entityType: CertifyType!, $approvers: [ApproverInput!]!) {\n"
    "  isEntityAccessGranted(entityId: $entityId, entityType: $entityType, approvers: $approvers) {\n"
    "    deniedUsers { type id displayName }\n    deniedGroups { id type displayName }\n  }\n}"
)

_WAITING_ON_ME_QUERY = (
    "query getWaitingOnMeCount($type: String = \"CC\") {\n  count: waitingOnMeCount(type: $type)\n}"
)

_NEW_APPROVAL_MUTATION = (
    "mutation newApproval($request: ApprovalRequest!, $adminCertified: Boolean) {\n"
    "  approval: submitRequest(request: $request, adminCertified: $adminCertified) {\n"
    "    id type submittedTime modifiedTime status title providerName templateTitle version\n"
    "    submitter { id displayName }\n    observers { id type displayName }\n"
    "    history { actor { type id displayName } status time }\n"
    "    fields { data name type key }\n"
    "    pendingApprover: pendingApproverEx { id type displayName }\n"
    "    chain { approver { id type displayName } status time type key }\n  }\n}"
)

_REMOVE_MUTATION = (
    "mutation remove($type: CertifyType!, $id: ID!) {\n  removeCertification(type: $type, id: $id)\n}"
)


@mcp.tool()
def certification_list(
    type: Annotated[str | None, "Certification type (e.g. 'CC')"] = None,
    view: Annotated[str | None, "View filter: 'WAITING' or 'SUBMITTED'"] = None,
    time_period: Annotated[str | None, "Time period: 'ACTIVE' or 'PAST'"] = None,
    first: Annotated[int | None, "Max results"] = None,
    after: Annotated[str | None, "Cursor for pagination"] = None,
    order_by: Annotated[str | None, "Sort field (e.g. 'DATE')"] = None,
    reverse_sort: Annotated[bool | None, "Reverse sort order"] = None,
    search_term: Annotated[str | None, "Search term"] = None,
    template_id: Annotated[str | None, "Filter by template ID"] = None,
) -> Any:
    """List certification requests."""
    return auth.post(_GQL, body=[{
        "operationName": "getWorkflowConnection",
        "query": _LIST_QUERY,
        "variables": {
            "type": type or "CC",
            "view": view,
            "timePeriod": time_period,
            "first": first,
            "after": after,
            "orderBy": order_by,
            "reverseSort": reverse_sort or False,
            "searchTerm": search_term or "",
            "templateId": template_id,
        },
    }])


@mcp.tool()
def certification_list_templates(
    type: Annotated[str | None, "Certification type (e.g. 'CC:CARD' or 'CC:DSET')"] = None,
    include_unpublished: Annotated[bool | None, "Include unpublished templates"] = None,
) -> Any:
    """List certification templates."""
    return auth.post(_GQL, body=[{
        "operationName": "getCertifiedTemplates",
        "query": _LIST_TEMPLATES_QUERY,
        "variables": {"type": type, "includeUnpublished": include_unpublished or False},
    }])


@mcp.tool()
def certification_list_certified_entities(
    type: Annotated[str, "Entity type: 'CC:CARD' or 'CC:DSET'"],
    first: Annotated[int | None, "Max results"] = None,
    after: Annotated[str | None, "Cursor for pagination"] = None,
    search_term: Annotated[str | None, "Search term"] = None,
    state_filter: Annotated[str | None, "State filter: PENDING, EXPIRED, CERTIFIED, or REQUESTED"] = None,
) -> Any:
    """List certified entities (cards or datasets)."""
    return auth.post(_GQL, body={
        "operationName": "getCertifiedEntities",
        "query": _LIST_CERTIFIED_ENTITIES_QUERY,
        "variables": {
            "type": type,
            "first": first,
            "after": after,
            "searchTerm": search_term or "",
            "stateFilter": state_filter,
        },
    })


@mcp.tool()
def certification_get(
    certification_id: Annotated[str, "Certification ID (UUID)"],
) -> Any:
    """Get a certification request by ID."""
    return auth.post(_GQL, body=[{
        "operationName": "getCertificationDetails",
        "query": _GET_CERT_QUERY,
        "variables": {"id": certification_id},
    }])


@mcp.tool()
def certification_get_template(
    type: Annotated[str, "Certification type: 'CARD' or 'DATASET'"],
    template_id: Annotated[str | None, "Template ID (UUID)"] = None,
    entity_id: Annotated[int | None, "Card or dataset ID"] = None,
    title: Annotated[str | None, "Entity title"] = None,
) -> Any:
    """Get a certification template."""
    return auth.post(_GQL, body=[{
        "operationName": "getCertifiedTemplate",
        "query": _GET_TEMPLATE_QUERY,
        "variables": {"type": type, "templateId": template_id, "id": entity_id, "title": title},
    }])


@mcp.tool()
def certification_get_id_from_approval(
    approval_id: Annotated[str, "Approval ID (UUID)"],
) -> Any:
    """Get the certification ID corresponding to an approval ID."""
    return auth.post(_GQL, body=[{
        "operationName": "getCertificationIdFromApprovalId",
        "query": _GET_ID_FROM_APPROVAL_QUERY,
        "variables": {"id": approval_id},
    }])


@mcp.tool()
def certification_get_entity_access(
    entity_type: Annotated[str, "Entity type: 'CARD' or 'DATASET'"],
    entity_id: Annotated[int, "Card or dataset ID"],
    approvers: Annotated[list[dict[str, Any]], "List of approver objects with type, id, approverId, etc."],
) -> Any:
    """Check whether approvers have access to a certifiable entity."""
    return auth.post(_GQL, body=[{
        "operationName": "checkEntityAccess",
        "query": _CHECK_ENTITY_ACCESS_QUERY,
        "variables": {"entityType": entity_type, "entityId": entity_id, "approvers": approvers},
    }])


@mcp.tool()
def certification_get_waiting_on_me_count(
    type: Annotated[str | None, "Certification type (default 'CC')"] = None,
) -> Any:
    """Get the count of certifications waiting on the current user."""
    return auth.post(_GQL, body=[{
        "operationName": "getWaitingOnMeCount",
        "query": _WAITING_ON_ME_QUERY,
        "variables": {"type": type or "CC"},
    }])


@mcp.tool()
def certification_get_expire_on_edit(
    type: Annotated[str, "Property type key (e.g. 'certification.expireOnEdit')"],
) -> Any:
    """Get the 'expire on edit' certification property setting."""
    return auth.get(f"/customer/v1/properties/{type}")


@mcp.tool()
def certification_create(
    request: Annotated[
        dict[str, Any],
        "Approval request. Keys: templateId (str), title (str), fields (list), approvers (list), attachments (list)",
    ],
    admin_certified: Annotated[bool | None, "Mark as admin-certified"] = None,
) -> Any:
    """Create (submit) a new certification request."""
    return auth.post(_GQL, body=[{
        "operationName": "newApproval",
        "query": _NEW_APPROVAL_MUTATION,
        "variables": {"request": request, "adminCertified": admin_certified},
    }])


@mcp.tool()
def certification_remove(
    type: Annotated[str, "Entity type: 'CARD' or 'DATASET'"],
    entity_id: Annotated[str, "Card or dataset ID"],
) -> Any:
    """Remove certification from an entity."""
    return auth.post(_GQL, body=[{
        "operationName": "remove",
        "query": _REMOVE_MUTATION,
        "variables": {"type": type, "id": entity_id},
    }])
