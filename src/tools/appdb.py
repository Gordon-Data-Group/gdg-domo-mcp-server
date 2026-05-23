"""AppDB tools — NoSQL document store (datastores, collections, documents).

API reference: api-definitions-md/06-appdb.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.app import mcp
from src import auth


@mcp.tool()
def appdb_search_collections(
    body: Annotated[
        dict[str, Any],
        (
            "Search filter. Keys: collectionFilteringList (list of {filterType, typedValue, comparingCriteria}), "
            "sortBy (str e.g. 'createdOn'), direction (str e.g. 'desc'), pageSize (int), pageNumber (int)"
        ),
    ],
) -> Any:
    """Search AppDB collections with filters and sorting."""
    return auth.post("/datastores/v1/collections/query", body=body)


@mcp.tool()
def appdb_query_documents(
    collection_id: Annotated[str, "Collection ID"],
    body: Annotated[dict[str, Any], "MongoDB-style query filter (e.g. {'$or': [...]})"],
    limit: Annotated[int | None, "Max documents to return"] = None,
    offset: Annotated[int | None, "Pagination offset"] = None,
    count: Annotated[str | None, "Field to count"] = None,
    avg: Annotated[str | None, "Field to average"] = None,
    sum: Annotated[str | None, "Field to sum"] = None,
    max: Annotated[str | None, "Field to find max of"] = None,
    min: Annotated[str | None, "Field to find min of"] = None,
    orderby: Annotated[str | None, "Field to order results by"] = None,
    groupby: Annotated[str | None, "Field to group results by"] = None,
) -> Any:
    """Query documents in a collection using a MongoDB-style filter."""
    return auth.post(
        f"/datastores/v2/collections/{collection_id}/documents/query",
        body=body,
        limit=limit,
        offset=offset,
        count=count,
        avg=avg,
        sum=sum,
        max=max,
        min=min,
        orderby=orderby,
        groupby=groupby,
    )


@mcp.tool()
def appdb_list_datastores() -> Any:
    """List all AppDB datastores."""
    return auth.get("/datastores/v1")


@mcp.tool()
def appdb_list_collections() -> Any:
    """List all AppDB collections."""
    return auth.get("/datastores/v1/collections")


@mcp.tool()
def appdb_get_datastore(
    datastore_id: Annotated[str, "Datastore ID"],
) -> Any:
    """Get an AppDB datastore by ID."""
    return auth.get(f"/datastores/v1/{datastore_id}")


@mcp.tool()
def appdb_get_datastore_collections(
    datastore_id: Annotated[str, "Datastore ID"],
) -> Any:
    """Get all collections in an AppDB datastore."""
    return auth.get(f"/datastores/v1/{datastore_id}/collections")


@mcp.tool()
def appdb_get_collection(
    collection_id: Annotated[str, "Collection ID"],
) -> Any:
    """Get an AppDB collection by ID."""
    return auth.get(f"/datastores/v1/collections/{collection_id}")


@mcp.tool()
def appdb_get_documents(
    collection_id: Annotated[str, "Collection ID"],
) -> Any:
    """Get all documents in an AppDB collection."""
    return auth.get(f"/datastores/v1/collections/{collection_id}/documents")


@mcp.tool()
def appdb_get_collection_permissions(
    collection_id: Annotated[str, "Collection ID"],
) -> Any:
    """Get the permissions for an AppDB collection."""
    return auth.get(f"/datastores/v1/collections/{collection_id}/permission")


@mcp.tool()
def appdb_create_datastore(
    name: Annotated[str, "Datastore name"],
) -> Any:
    """Create a new AppDB datastore."""
    return auth.post("/datastores/v1", body={"name": name})


@mcp.tool()
def appdb_create_collection_in_datastore(
    datastore_id: Annotated[str, "Datastore ID"],
    body: Annotated[
        dict[str, Any],
        (
            "Collection definition. Keys: name (str), "
            "schema ({columns: [{name, type}]}), syncEnabled (bool)"
        ),
    ],
) -> Any:
    """Create a new collection in an existing datastore."""
    return auth.post(f"/datastores/v1/{datastore_id}/collections/", body=body)


@mcp.tool()
def appdb_create_collection(
    body: Annotated[
        dict[str, Any],
        (
            "Collection definition (creates datastore automatically). Keys: name (str), "
            "schema ({columns: [{name, type}]}), syncEnabled (bool)"
        ),
    ],
) -> Any:
    """Create a new AppDB collection (and a datastore if needed)."""
    return auth.post("/datastores/v1/collections", body=body)


@mcp.tool()
def appdb_create_document(
    collection_id: Annotated[str, "Collection ID"],
    content: Annotated[dict[str, Any], "Document content as key-value pairs matching the collection schema"],
) -> Any:
    """Create a single document in an AppDB collection."""
    return auth.post(
        f"/datastores/v1/collections/{collection_id}/documents",
        body={"content": content},
    )


@mcp.tool()
def appdb_create_documents(
    collection_id: Annotated[str, "Collection ID"],
    documents: Annotated[list[dict[str, Any]], "List of documents, each with a 'content' key"],
) -> Any:
    """Create multiple documents in an AppDB collection."""
    return auth.post(
        f"/datastores/v1/collections/{collection_id}/documents/bulk",
        body=documents,
    )


@mcp.tool()
def appdb_update_collection(
    collection_id: Annotated[str, "Collection ID"],
    body: Annotated[
        dict[str, Any],
        "Collection update. Keys: id (str), owner (int), schema ({columns: [{name, type}]}), syncEnabled (bool)",
    ],
) -> Any:
    """Update an AppDB collection's schema or settings."""
    return auth.put(f"/datastores/v1/collections/{collection_id}", body=body)


@mcp.tool()
def appdb_update_collection_permissions(
    collection_id: Annotated[str, "Collection ID"],
    entity_type: Annotated[str, "Entity type (e.g. 'USER' or 'GROUP')"],
    entity_id: Annotated[str, "Entity ID"],
    overwrite: Annotated[bool | None, "Overwrite existing permissions"] = None,
    permissions: Annotated[str | None, "Comma-separated permission names"] = None,
) -> Any:
    """Update permissions for an entity on an AppDB collection."""
    return auth.put(
        f"/datastores/v1/collections/{collection_id}/permission/{entity_type}/{entity_id}",
        overwrite=overwrite,
        permissions=permissions,
    )


@mcp.tool()
def appdb_update_document(
    collection_id: Annotated[str, "Collection ID"],
    document_id: Annotated[str, "Document ID"],
    content: Annotated[dict[str, Any], "New document content as key-value pairs"],
) -> Any:
    """Update a document in an AppDB collection."""
    return auth.put(
        f"/datastores/v2/collections/{collection_id}/documents/{document_id}",
        body={"content": content},
    )


@mcp.tool()
def appdb_upsert_documents(
    collection_id: Annotated[str, "Collection ID"],
    documents: Annotated[
        list[dict[str, Any]],
        "List of documents. Each with 'content' dict; include 'id' to update, omit to create.",
    ],
) -> Any:
    """Upsert multiple documents in an AppDB collection."""
    return auth.put(
        f"/datastores/v2/collections/{collection_id}/documents/bulk",
        body=documents,
    )


@mcp.tool()
def appdb_delete_datastore(
    datastore_id: Annotated[str, "Datastore ID to delete"],
) -> Any:
    """Delete an AppDB datastore."""
    return auth.delete(f"/datastores/v1/{datastore_id}")


@mcp.tool()
def appdb_delete_collection(
    collection_id: Annotated[str, "Collection ID to delete"],
) -> Any:
    """Delete an AppDB collection."""
    return auth.delete(f"/datastores/v1/collections/{collection_id}")


@mcp.tool()
def appdb_remove_collection_access(
    collection_id: Annotated[str, "Collection ID"],
    entity_type: Annotated[str, "Entity type (e.g. 'USER' or 'GROUP')"],
    entity_id: Annotated[str, "Entity ID to remove"],
) -> Any:
    """Remove an entity's access from an AppDB collection."""
    return auth.delete(
        f"/datastores/v1/collections/{collection_id}/permission/{entity_type}/{entity_id}"
    )


@mcp.tool()
def appdb_delete_document(
    collection_id: Annotated[str, "Collection ID"],
    document_id: Annotated[str, "Document ID to delete"],
) -> Any:
    """Delete a single document from an AppDB collection."""
    return auth.delete(
        f"/datastores/v2/collections/{collection_id}/documents/{document_id}"
    )


@mcp.tool()
def appdb_delete_documents(
    collection_id: Annotated[str, "Collection ID"],
    ids: Annotated[str, "Comma-separated document IDs to delete"],
) -> Any:
    """Delete multiple documents from an AppDB collection by ID."""
    return auth.delete(
        f"/datastores/v2/collections/{collection_id}/documents/bulk",
        ids=ids,
    )
