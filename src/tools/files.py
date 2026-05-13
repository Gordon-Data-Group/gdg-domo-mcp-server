"""Files tools — binary file upload/management and file cards.

API reference: api-definitions-md/20-files.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def files_get_revision(
    file_id: Annotated[str, "File ID"],
    revision_id: Annotated[str, "Revision ID"],
    file_name: Annotated[str | None, "File name for the download"] = None,
) -> Any:
    """Get a specific revision of a file."""
    return auth.get(
        f"/data/v1/data-files/{file_id}/revisions/{revision_id}",
        fileName=file_name,
    )


@mcp.tool()
def files_get_revision_details(
    file_id: Annotated[str, "File ID"],
    revision_id: Annotated[str, "Revision ID"],
) -> Any:
    """Get details about a specific file revision."""
    return auth.get(f"/data/v1/data-files/{file_id}/revisions/{revision_id}/details")


@mcp.tool()
def files_get_details(
    file_id: Annotated[str, "File ID"],
    expand: Annotated[str | None, "Comma-separated fields to expand"] = None,
) -> Any:
    """Get details about a file."""
    return auth.get(f"/data/v1/data-files/{file_id}/details", expand=expand)


@mcp.tool()
def files_create(
    name: Annotated[str | None, "File name"] = None,
    public: Annotated[bool | None, "Make the file publicly accessible"] = None,
) -> Any:
    """Create a new file entry."""
    return auth.post("/data/v1/data-files", name=name, public=public)


@mcp.tool()
def files_create_card(
    body: Annotated[
        dict[str, Any],
        (
            "Card definition. Keys: type (str e.g. 'document'), description (str), "
            "metadata ({title, documentId, usingSampleData, kpiType, description})"
        ),
    ],
    page_id: Annotated[str | None, "Page ID to add the card to"] = None,
) -> Any:
    """Create a file (document) card on a page."""
    return auth.post("/content/v1/cards", body=body, pageId=page_id)


@mcp.tool()
def files_update(
    file_id: Annotated[str, "File ID"],
    public: Annotated[bool | None, "Make the file publicly accessible"] = None,
    description: Annotated[str | None, "File description"] = None,
) -> Any:
    """Update a file's metadata."""
    return auth.put(f"/data/v1/data-files/{file_id}", public=public, description=description)


@mcp.tool()
def files_update_card(
    card_id: Annotated[str, "Card ID"],
    body: Annotated[
        dict[str, Any],
        "Card update. Keys: metadata ({documentId, revisionId, title, kpiType, usingSampleData})",
    ],
) -> Any:
    """Update a file card's metadata."""
    return auth.put(f"/content/v1/cards/{card_id}", body=body)
