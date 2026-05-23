# Functions (Beast Modes and Variables)

### List Functions
`POST {{instanceUrl}}/api/query/v1/functions/search`
- Body: `{"name":"","filters":[{"field":"dataset","idList":["00000000-0000-0000-0000-000000000000"]},{"field":"notvariable"}],"sort":{"field":"name","ascending":true},"limit":5000,"offset":0}`

### Get Functions
`POST {{instanceUrl}}/api/query/v1/functions/list/id`
- Body: `{"ids":["1234","2345"]}`

### Get Function
`GET {{instanceUrl}}/api/query/v1/functions/template/:id`
- Path: `:id`
- Query: `hidden`

### Get Cards Function is Used On
`GET {{instanceUrl}}/api/content/v2/cards/formulausage`
- Query: `datasourceId`, `formulaId`

### Create Function
`POST {{instanceUrl}}/api/query/v1/functions/template`
- Query: `strict`
- Body:
  ```json
  {
    "name": "Test",
    "owner": 466826668,
    "locked": false,
    "global": false,
    "expression": "'test'",
    "checkSum": null,
    "links": [
      {
        "resource": {
          "type": "DATA_SOURCE",
          "id": "6ecd2cbb-db04-4cdc-b418-f8d705624cc6"
        },
        "visible": true,
        "active": false,
        "valid": "INCOMPATIBLE_LINK"
      }
    ],
    "aggregated": false,
    "analytic": false,
    "nonAggregatedColumns": [],
    "dataType": "STRING",
    "status": "VALID",
    "cacheWindow": "non_dynamic",
    "columnPositions": [],
    "functions": [],
    "functionTemplateDependencies": [],
    "archived": false,
    "hidden": false,
    "variable": false
  }
  ```

### Bulk Create Functions
`POST {{instanceUrl}}/api/query/v1/functions/bulk/template`
- Body:
  ```json
  {
    "create": [
      {
        "name": "<string>",
        "owner": 123456,
        "locked": false,
        "global": false,
        "expression": "<sql>",
        "checkSum": "<string>",
        "links": [
          {
            "resource": {
              "type": "CARD",
              "id": "<card_id>"
            },
            "visible": false,
            "active": true,
            "valid": "VALID"
          },
          {
            "resource": {
              "type": "DATA_SOURCE",
              "id": "<dataset_id>"
            },
            "visible": true,
            "active": false,
            "valid": "INCOMPATIBLE_LINK"
          }
        ],
        "aggregated": false,
        "analytic": false,
        "nonAggregatedColumns": [],
        "dataType": "STRING",
        "status": "VALID",
        "cacheWindow": "non_dynamic",
        "columnPositions": [
          {
            "columnName": "`Column 1`",
            "columnPosition": 14
          }
        ],
        "functions": [],
        "functionTemplateDependencies": [],
        "archived": false,
        "hidden": false,
        "variable": false
      }
    ],
    "links": {},
    "strict": false,
    "replaceLinks": true,
    "copyDependencies": true
  }
  ```

### Update Function
`PUT {{instanceUrl}}/api/query/v1/functions/template/:id`
- Path: `:id`
- Query: `strict`
- Body: `{"expression":"<sql>","id":1234,"name":"<string>","status":"VALID","persistedOnDataSource":true,"archived":false,"certification":{"state":"NOT_CERTIFIED"}}`

### Bulk Update Functions
`POST {{instanceUrl}}/api/query/v1/functions/bulk/template`
- Body:
  ```json
  {
    "update": [
      {
        "id": 1234,
        "name": "<string>",
        "owner": 1234,
        "lastModified": 1735689600000,
        "created": 1735689600000,
        "global": false,
        "locked": false,
        "certificationStatus": "PENDING",
        "legacyId": "calculation_00000000-0000-0000-0000-000000000000",
        "status": "VALID",
        "dataType": "STRING",
        "links": [],
        "archived": false,
        "activeLinks": {},
        "certification": {},
        "checked": true,
        "selected": true,
        "showCheckbox": true
      },
      {
        "id": 2345,
        "locked": true
      }
    ]
  }
  ```

### Lock Function
`PUT {{instanceUrl}}/api/query/v1/functions/template/:id`
- Path: `:id`
- Body: `{"locked":true}`

### Delete Function
`DELETE {{instanceUrl}}/api/query/v1/functions/template/:id`
- Path: `:id`

### Bulk Delete Functions
`POST {{instanceUrl}}/api/query/v1/functions/bulk/template`
- Body: `{"delete":[1234,2345]}`
