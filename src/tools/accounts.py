"""Accounts tools — data connectors, providers, OAuth configs, account credentials.

API reference: api-definitions-md/01-accounts.md
"""
from __future__ import annotations

from typing import Annotated, Any

from src.toolsets import domo_tool
from src import auth


@domo_tool(toolset="accounts", read_only=True)
def accounts_list() -> Any:
    """List all data accounts in the Domo instance."""
    return auth.get("/data/v1/accounts")


@domo_tool(toolset="accounts", read_only=True)
def accounts_search(
    body: Annotated[
        dict[str, Any],
        (
            "Search body. Keys: count (int), offset (int), query (str), "
            "combineResults (bool), filters (list), "
            "facetValuesToInclude (list e.g. ['DATAPROVIDERNAME','OWNED_BY_ID','VALID','USED','LAST_MODIFIED_DATE']), "
            "queryProfile (str e.g. 'GLOBAL'), "
            "entityList (e.g. [['account']]), "
            "sort ({fieldSorts: [{field, sortOrder}]})"
        ),
    ],
) -> Any:
    """Search accounts using the global search API."""
    return auth.post("/search/v1/query", body=body)


@domo_tool(toolset="accounts", read_only=True)
def accounts_list_oauth_configs() -> Any:
    """List OAuth configurations available for user-level account templates."""
    return auth.get("/data/v1/accounts/templates/user/extended")


@domo_tool(toolset="accounts", read_only=True)
def accounts_list_providers_with_accounts() -> Any:
    """List data providers that have at least one account configured."""
    return auth.get("/data/v2/datasources/providers")


@domo_tool(toolset="accounts", read_only=True)
def accounts_list_providers(
    fields: Annotated[str | None, "Comma-separated fields to include in the response"] = None,
    filter: Annotated[str | None, "Filter string to narrow results"] = None,
    include_federated: Annotated[bool | None, "Include federated providers"] = None,
) -> Any:
    """List all data providers."""
    return auth.get(
        "/data/v1/providers",
        fields=fields,
        filter=filter,
        includeFederated=include_federated,
    )


@domo_tool(toolset="accounts", read_only=True)
def accounts_get_by_provider(
    provider: Annotated[str, "Provider key (e.g. 'salesforce')"],
) -> Any:
    """Get all accounts for a specific provider."""
    return auth.get(f"/data/v1/accounts/provider/{provider}")


@domo_tool(toolset="accounts", read_only=True)
def accounts_get(
    account_id: Annotated[str, "Account ID"],
) -> Any:
    """Get a single account by ID."""
    return auth.get(f"/data/v1/accounts/{account_id}")


@domo_tool(toolset="accounts", read_only=True)
def accounts_get_credentials(
    provider: Annotated[str, "Provider key"],
    account_id: Annotated[str, "Account ID"],
    unmask: Annotated[bool | None, "Return unmasked credential values"] = None,
) -> Any:
    """Get the credentials stored for an account."""
    return auth.get(f"/data/v1/providers/{provider}/account/{account_id}", unmask=unmask)


@domo_tool(toolset="accounts", read_only=True)
def accounts_get_provider(
    provider: Annotated[str, "Provider key"],
    fields: Annotated[str | None, "Comma-separated fields to include"] = None,
    country: Annotated[str | None, "Country code for localized provider info"] = None,
    language: Annotated[str | None, "Language code for localized provider info"] = None,
) -> Any:
    """Get details for a specific data provider."""
    return auth.get(
        f"/data/v1/providers/{provider}",
        fields=fields,
        country=country,
        language=language,
    )


@domo_tool(toolset="accounts", read_only=True)
def accounts_get_provider_image(
    provider: Annotated[str, "Provider key"],
) -> Any:
    """Get the 96px PNG logo image for a provider."""
    return auth.get(f"/data/v1/providers/{provider}/images/96.png")


@domo_tool(toolset="accounts", read_only=True)
def accounts_get_appstore_connector(
    connector: Annotated[str, "Connector ID from the Domo Appstore"],
    fields: Annotated[str | None, "Comma-separated fields to include"] = None,
    country: Annotated[str | None, "Country code for localized info"] = None,
    language: Annotated[str | None, "Language code for localized info"] = None,
) -> Any:
    """Get details for an Appstore connector."""
    return auth.get(
        f"/connectors/appstore/v2/details/connector/{connector}",
        fields=fields,
        country=country,
        language=language,
    )


@domo_tool(toolset="accounts", read_only=True)
def accounts_get_datasets_used(
    account_id: Annotated[str, "Account ID"],
) -> Any:
    """Get datasets powered by a specific account."""
    return auth.get(f"/data/v2/datasources/account/{account_id}")


@domo_tool(toolset="accounts", read_only=True)
def accounts_get_datasets_used_bulk(
    account_ids: Annotated[list[int], "List of account IDs to look up"],
) -> Any:
    """Get datasets used by multiple accounts in a single request."""
    return auth.post("/data/v2/datasources/accounts", body=account_ids)


@domo_tool(toolset="accounts", read_only=True)
def accounts_validate_credentials(
    data_provider_key: Annotated[str, "Provider key to validate against"],
    credentials: Annotated[
        dict[str, Any],
        "Credential object (e.g. {authentication, apiType, name, apiKey})",
    ],
    account_id: Annotated[str | None, "Existing account ID to re-validate; omit for new credentials"] = None,
) -> Any:
    """Validate account credentials against a provider without saving them."""
    body: dict[str, Any] = {
        "dataProviderKey": data_provider_key,
        "credentials": credentials,
        "accountId": account_id,
    }
    return auth.post("/data/v1/accounts/validators", body=body)


@domo_tool(toolset="accounts", read_only=False)
def accounts_create(
    name: Annotated[str, "Internal account name"],
    display_name: Annotated[str, "Human-readable display name"],
    data_provider_type: Annotated[str, "Provider type key"],
    configurations: Annotated[
        dict[str, Any],
        "Credential/configuration object (e.g. {authentication, apiType, name, apiKey})",
    ],
) -> Any:
    """Create a new data account."""
    body: dict[str, Any] = {
        "name": name,
        "displayName": display_name,
        "dataProviderType": data_provider_type,
        "configurations": configurations,
    }
    return auth.post("/data/v1/accounts", body=body)


@domo_tool(toolset="accounts", read_only=False)
def accounts_update_name(
    account_id: Annotated[str, "Account ID"],
    name: Annotated[str, "New display name for the account"],
) -> Any:
    """Rename an account."""
    return auth.put_text(f"/data/v1/accounts/{account_id}/name", text=name, content_type="text/plain")


@domo_tool(toolset="accounts", read_only=False)
def accounts_update_credentials(
    provider_id: Annotated[str, "Provider key"],
    account_id: Annotated[str, "Account ID"],
    credentials: Annotated[dict[str, Any], "Map of credential property names to their new values"],
) -> Any:
    """Update the credentials stored for an account."""
    return auth.put(f"/data/v1/providers/{provider_id}/account/{account_id}", body=credentials)


@domo_tool(toolset="accounts", read_only=False)
def accounts_update_access(
    account_id: Annotated[str, "Account ID"],
    type: Annotated[str, "Principal type: 'USER' or 'GROUP'"],
    id: Annotated[int, "User or group ID"],
    access_level: Annotated[
        str,
        "Access level: 'NONE', 'CAN_VIEW', 'CAN_SHARE', 'CAN_EDIT', or 'OWNER'",
    ],
) -> Any:
    """Set access permissions for a user or group on an account."""
    return auth.put(
        f"/data/v2/accounts/share/{account_id}",
        body={"type": type, "id": id, "accessLevel": access_level},
    )


@domo_tool(toolset="accounts", read_only=False)
def accounts_delete(
    account_id: Annotated[str, "Account ID to delete"],
) -> Any:
    """Delete a data account."""
    return auth.delete(f"/data/v1/accounts/{account_id}")
