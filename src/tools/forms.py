"""Forms tools — form instances and submissions.

API reference: api-definitions-md/22-forms.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="forms", read_only=True)
def forms_search(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: count (int), offset (int), filters (list), "
            "useEntities (bool), combineResults (bool), facetValueLimit (int), "
            "entityList (e.g. [['form']]), sort ({isRelevance, fieldSorts}), "
            "query (str), hideSearchObjects (bool), state (str)"
        ),
    ],
) -> Any:
    """Search forms using the global search API."""
    return auth.post("/search/v1/query", body=body)


@domo_tool(toolset="forms", read_only=True)
def forms_get(
    form_id: Annotated[str, "Form ID"],
) -> Any:
    """Get a form by ID."""
    return auth.get(f"/forms/v1/{form_id}")


@domo_tool(toolset="forms", read_only=False)
def forms_create_instance(
    body: Annotated[
        dict[str, Any],
        (
            "Form instance. Keys: formId (str UUID), "
            "fieldConfiguration (dict keyed by field UUID), "
            "submitConfiguration ({type, name})"
        ),
    ],
) -> Any:
    """Create a form instance."""
    return auth.post("/forms/v1/instances", body=body)


@domo_tool(toolset="forms", read_only=False)
def forms_create_submission(
    instance_id: Annotated[str, "Form instance ID"],
    fields: Annotated[
        list[dict[str, Any]],
        "List of field submissions, each with id, label, fieldType, dataType, value, etc.",
    ],
) -> Any:
    """Submit a form instance."""
    return auth.post(f"/forms/v1/instances/{instance_id}/submission", body=fields)


@domo_tool(toolset="forms", read_only=False)
def forms_update_instance(
    instance_id: Annotated[str, "Form instance ID"],
    body: Annotated[
        dict[str, Any],
        "Instance update. Keys: formInstanceId (str), formId (str), fieldConfiguration (dict), submitConfiguration ({type, id, name})",
    ],
) -> Any:
    """Update a form instance configuration."""
    return auth.put(f"/forms/v1/instances/{instance_id}", body=body)


@domo_tool(toolset="forms", read_only=False)
def forms_update_fields(
    form_id: Annotated[str, "Form ID"],
    body: Annotated[
        dict[str, Any],
        "Field hydration map keyed by field UUID, each with options and value objects",
    ],
) -> Any:
    """Update (hydrate) form field configurations."""
    return auth.post(f"/forms/v1/{form_id}/hydration", body=body)
