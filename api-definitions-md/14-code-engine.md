# Code Engine

### Search Packages
`POST {{instanceUrl}}/api/search/v1/query`
- Body:
  ```json
  {
    "query": "*",
    "entityList": [
      [
        "package"
      ]
    ],
    "count": 100,
    "offset": 0,
    "sort": {
      "isRelevance": true,
      "fieldSorts": [
        {
          "field": "lastModified",
          "sortOrder": "DESC"
        }
      ]
    },
    "filters": [
      {
        "facetType": "user",
        "filterType": "term",
        "field": "owned_by_id",
        "value": "1234:USER"
      }
    ],
    "useEntities": true,
    "combineResults": true,
    "facetValueLimit": 1000,
    "hideSearchObjects": false,
    "state": "facet"
  }
  ```

### Get Package
`GET {{instanceUrl}}/api/codeengine/v2/packages/:id`
- Path: `:id`
- Query: `parts`

### Get Package Version
`GET {{instanceUrl}}/api/codeengine/v2/packages/:id/versions/:version`
- Path: `:id`, `:version`
- Query: `parts`

### Get Package Permissions
`GET {{instanceUrl}}/api/codeengine/v2/packages/:id/permissions`
- Path: `:id`

### Run Function
`POST {{instanceUrl}}/api/codeengine/v2/packages/:id/versions/:version/functions/:function`
- Path: `:id`, `:version`, `:function`
- Body: `{"inputVariables":{"<variable1>":"<input>"},"settings":{"getLogs":true}}`

### Create Package Release (Deploy)
`POST {{instanceUrl}}/api/codeengine/v2/packages/:id/versions/:version/release`
- Path: `:id`, `:version`

### Update Package
`POST {{instanceUrl}}/api/codeengine/v2/packages`
- Body:
  ```json
  {
    "name": "<string>",
    "version": "1.0.0",
    "code": "<javascript_or_python_code>",
    "environment": "LAMBDA",
    "id": "00000000-0000-0000-0000-000000000000",
    "language": "JAVASCRIPT",
    "manifest": {
      "functions": [
        {
          "editorStartIndex": 1234,
          "displayName": "<function_name>",
          "output": null,
          "name": "<function_name>",
          "variables": [],
          "description": "",
          "inputs": [
            {
              "defaultValues": null,
              "isList": false,
              "name": "<input_name>",
              "type": "text",
              "value": null,
              "displayName": "<input_name>",
              "nullable": true,
              "children": []
            }
          ]
        }
      ],
      "configuration": {
        "accountsMapping": [
          {
            "accountId": 123,
            "alias": "123"
          },
          {
            "accountId": 234,
            "alias": "234"
          }
        ]
      }
    }
  }
  ```

### Update Package Owner
`PUT {{instanceUrl}}/api/codeengine/v2/packages/:id`
- Path: `:id`
- Body: `{"owner":123456}`

### Update Package Permissions
`POST {{instanceUrl}}/api/codeengine/v2/packages/:id/permissions`
- Path: `:id`
- Body:
  ```json
  [
    {
      "id": "123456",
      "permissions": [
        "ADMIN",
        "DELETE",
        "READ",
        "WRITE",
        "SHARE",
        "READ_CONTENT",
        "UPDATE_CONTENT"
      ],
      "name": "<string>",
      "type": "USER"
    },
    {
      "id": "234567",
      "name": "<string>",
      "type": "USER",
      "permissions": [
        "ADMIN"
      ]
    }
  ]
  ```
