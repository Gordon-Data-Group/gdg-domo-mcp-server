"""Alerts tools — alert creation, evaluation, subscriptions, sharing.

API reference: api-definitions-md/05-alerts.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="alerts", read_only=True)
def alerts_list(
    all: Annotated[bool | None, "Return all alerts, not just the current user's"] = None,
    fields: Annotated[str | None, "Comma-separated fields to include in the response"] = None,
    limit: Annotated[int | None, "Max alerts to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """List alerts in the instance."""
    return auth.get("/social/v4/alerts", all=all, fields=fields, limit=limit, offset=offset)


@domo_tool(toolset="alerts", read_only=True)
def alerts_list_immediate() -> Any:
    """List alerts configured to trigger immediately (no schedule delay)."""
    return auth.get("/messaging/v3/subscriptions/schedule/primary/immediate")


@domo_tool(toolset="alerts", read_only=True)
def alerts_list_immediate_preferences() -> Any:
    """Get the current user's notification preferences for immediately-triggered alerts."""
    return auth.get("/messaging/v3/preferences/immediate/user/current/alert_triggered")


@domo_tool(toolset="alerts", read_only=True)
def alerts_search(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: count (int), offset (int), query (str), "
            "combineResults (bool), filters (list), "
            "sort ({fieldSorts: [{enum, field, sortOrder, label, order}]}), "
            "facetValuesToInclude (list e.g. ['TYPE']), facetValueLimit (int), "
            "facetValueOffset (int), includePhonetic (bool), "
            "queryProfile (str e.g. 'GLOBAL'), state (str), topic, savedSearchId, "
            "entityList (e.g. [['alert']])"
        ),
    ],
) -> Any:
    """Search alerts using the global search API."""
    return auth.post("/search/v1/query", body=body)


@domo_tool(toolset="alerts", read_only=True)
def alerts_get_bulk(
    alert_ids: Annotated[list[str], "List of alert IDs to fetch"],
    all: Annotated[bool | None, "Include alerts the current user does not own"] = None,
    subscriber_id: Annotated[str | None, "Filter by subscriber ID"] = None,
    fields: Annotated[str | None, "Comma-separated fields to include"] = None,
    limit: Annotated[int | None, "Max alerts to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
) -> Any:
    """Fetch multiple alerts by ID in a single request."""
    return auth.post(
        "/social/v4/alerts/ids",
        body=alert_ids,
        all=all,
        subscriberId=subscriber_id,
        fields=fields,
        limit=limit,
        offset=offset,
    )


@domo_tool(toolset="alerts", read_only=True)
def alerts_get(
    alert_id: Annotated[str, "Alert ID"],
) -> Any:
    """Get a single alert by ID."""
    return auth.get(f"/social/v4/alerts/{alert_id}")


@domo_tool(toolset="alerts", read_only=True)
def alerts_get_action(
    alert_id: Annotated[str, "Alert ID"],
    action_id: Annotated[str, "Action ID"],
) -> Any:
    """Get a specific action associated with an alert."""
    return auth.get(f"/social/v4/alerts/{alert_id}/actions/{action_id}")


@domo_tool(toolset="alerts", read_only=True)
def alerts_get_evaluations(
    alert_id: Annotated[str, "Alert ID"],
) -> Any:
    """Get the evaluation history for an alert."""
    return auth.get(f"/social/v4/alerts/{alert_id}/evaluations")


@domo_tool(toolset="alerts", read_only=False)
def alerts_create(
    body: Annotated[
        dict[str, Any],
        (
            "Alert definition. Required keys: name (str), type (str e.g. 'SUMMARY_NUMBER'), "
            "owner (int user ID), resourceType (str e.g. 'CARD' or 'DATASET'), "
            "resourceId (str). Optional: active (bool), enabled (bool), "
            "triggerFrequency (str), configurations (list of {name, value}), "
            "filterGroups (list), filters (list), subscriptions (list of {subscriberId, type}), "
            "category (str e.g. 'DATA'), contextual (bool)"
        ),
    ],
) -> Any:
    """Create a new alert."""
    return auth.post("/social/v4/alerts", body=body)


@domo_tool(toolset="alerts", read_only=False)
def alerts_share(
    alert_id: Annotated[str, "Alert ID to share"],
    alert_subscriptions: Annotated[
        list[dict[str, Any]],
        "List of subscribers, each with 'subscriberId' (int) and 'type' (e.g. 'USER')",
    ],
    user_message: Annotated[str | None, "Message to include with the share notification"] = None,
    send_email: Annotated[bool | None, "Send an email notification to new subscribers"] = None,
    meta_data: Annotated[dict[str, Any] | None, "Additional metadata for the share event"] = None,
) -> Any:
    """Share an alert with users or groups."""
    body: dict[str, Any] = {"alertSubscriptions": alert_subscriptions}
    if user_message is not None:
        body["userMessage"] = user_message
    if send_email is not None:
        body["sendEmail"] = send_email
    if meta_data is not None:
        body["metaData"] = meta_data
    return auth.post(f"/social/v4/alerts/{alert_id}/share", body=body)


@domo_tool(toolset="alerts", read_only=False)
def alerts_update(
    alert_id: Annotated[str, "Alert ID"],
    body: Annotated[
        dict[str, Any],
        "Partial alert object to patch (e.g. {id: int, owner: int})",
    ],
) -> Any:
    """Partially update an alert's metadata (e.g. owner)."""
    return auth.patch(f"/social/v4/alerts/{alert_id}", body=body)


@domo_tool(toolset="alerts", read_only=False)
def alerts_update_rules(
    alert_id: Annotated[str, "Alert ID"],
    body: Annotated[
        dict[str, Any],
        (
            "Full alert rule definition. Keys: type (str e.g. 'ANY_ROW'), name (str), "
            "resourceType (str e.g. 'DATASET'), resourceId (str), owner (int), "
            "configurations (list of {name, value, order?}), "
            "filterGroups (list of {filterGroupId})"
        ),
    ],
) -> Any:
    """Replace the trigger rules for an alert."""
    return auth.put(f"/social/v4/alerts/{alert_id}", body=body)


@domo_tool(toolset="alerts", read_only=False)
def alerts_update_message_template(
    alert_id: Annotated[str, "Alert ID"],
    body: Annotated[str, "HTML body of the message template, e.g. '<p><span class=\"INAF rule\">Rule text</span> for card <span class=\"INAF cardName\">Name</span>. It was <span class=\"INAF previousValue\">[Previous alert value]</span>, now it&#x27;s <span class=\"INAF currentValue\">[Current alert value]</span>.</p>'"],
    header: Annotated[str, "Header text (use empty string for none)"] = "",
    footer: Annotated[str, "Footer text (use empty string for none)"] = "",
    formulas: Annotated[dict[str, Any], "Formula definitions referenced in the template (use empty dict for none)"] = {},
) -> Any:
    """Update the message template for an alert notification."""
    return auth.put(
        f"/social/v4/alerts/{alert_id}/message-template",
        body={"body": body, "header": header, "footer": footer, "formulas": formulas},
    )


@domo_tool(toolset="alerts", read_only=False)
def alerts_delete(
    alert_id: Annotated[str, "Alert ID to delete"],
) -> Any:
    """Delete an alert."""
    return auth.delete(f"/social/v4/alerts/{alert_id}")


@domo_tool(toolset="alerts", read_only=False)
def alerts_unshare(
    alert_id: Annotated[str, "Alert ID"],
    subscriber_id: Annotated[str | None, "Subscriber ID to remove"] = None,
    type: Annotated[str | None, "Subscriber type ('USER' or 'GROUP')"] = None,
) -> Any:
    """Remove a subscriber from an alert."""
    return auth.delete(
        f"/social/v4/alerts/{alert_id}/subscriptions",
        subscriberId=subscriber_id,
        type=type,
    )
