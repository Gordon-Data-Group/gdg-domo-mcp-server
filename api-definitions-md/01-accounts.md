# Accounts

### List Accounts
`GET {{instanceUrl}}/api/data/v1/accounts`

### Search Accounts
`POST {{instanceUrl}}/api/search/v1/query`
- Body:
  ```json
  {
    "count": 100,
    "offset": 0,
    "combineResults": false,
    "query": "**",
    "filters": [],
    "facetValuesToInclude": [
      "DATAPROVIDERNAME",
      "OWNED_BY_ID",
      "VALID",
      "USED",
      "LAST_MODIFIED_DATE"
    ],
    "queryProfile": "GLOBAL",
    "entityList": [
      [
        "account"
      ]
    ],
    "sort": {
      "fieldSorts": [
        {
          "field": "display_name_sort",
          "sortOrder": "ASC"
        }
      ]
    }
  }
  ```

### List OAuth Configurations
`GET {{instanceUrl}}/api/data/v1/accounts/templates/user/extended`

### List Providers with Accounts
`GET {{instanceUrl}}/api/data/v2/datasources/providers`

### List Providers
`GET {{instanceUrl}}/api/data/v1/providers`
- Query: `fields`, `filter`, `includeFederated`

### Get Accounts for Provider
`GET {{instanceUrl}}/api/data/v1/accounts/provider/:provider`
- Path: `:provider`

### Get Account
`GET {{instanceUrl}}/api/data/v1/accounts/:id`
- Path: `:id`

### Get Account Credentials
`GET {{instanceUrl}}/api/data/v1/providers/:provider/account/:id`
- Path: `:provider`, `:id`
- Query: `unmask`

### Get Provider
`GET {{instanceUrl}}/api/data/v1/providers/:provider`
- Path: `:provider`
- Query: `fields`, `country`, `language`

### Get Provider Image
`GET {{instanceUrl}}/api/data/v1/providers/:provider/images/96.png`
- Path: `:provider`

### Get Appstore Connector
`GET {{instanceUrl}}/api/connectors/appstore/v2/details/connector/:connector`
- Path: `:connector`
- Query: `fields`, `country`, `language`

### Get DataSets Used by Account
`GET {{instanceUrl}}/api/data/v2/datasources/account/:id`
- Path: `:id`

### Get DataSets Used by Accounts
`POST {{instanceUrl}}/api/data/v2/datasources/accounts`
- Body: `[123,234]`

### Validate Account Credentials
`POST {{instanceUrl}}/api/data/v1/accounts/validators`
- Body: `{"dataProviderKey":"<string>","credentials":{"authentication":"apiKey","apiType":"header","name":"<string>","apiKey":"<string>"},"accountId":null}`

### Create Account
`POST {{instanceUrl}}/api/data/v1/accounts`
- Body: `{"name":"<string>","displayName":"<string>","dataProviderType":"<string>","configurations":{"authentication":"apiKey","apiType":"header","name":"<string>","apiKey":"<string>"}}`

### Update Account Name
`PUT {{instanceUrl}}/api/data/v1/accounts/:id/name`
- Path: `:id`
- Body: `Raw text name`

### Update Account Credentials
`PUT {{instanceUrl}}/api/data/v1/providers/:providerId/account/:id`
- Path: `:providerId`, `:id`
- Body: `{"<property>":"<value>"}`

### Update Account Access
`PUT {{instanceUrl}}/api/data/v2/accounts/share/:id`
- Path: `:id`
- Body: `{ "type": "GROUP", //USER or GROUP "id": 12345, "accessLevel": "OWNER" //NONE, CAN_VIEW, CAN_SHARE, CAN_EDIT, or OWNER }`

### Delete Account
`DELETE {{instanceUrl}}/api/data/v1/accounts/:id`
- Path: `:id`
