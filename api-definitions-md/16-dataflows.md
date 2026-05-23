# DataFlows

### Search DataFlows
`POST {{instanceUrl}}/api/search/v1/query`
- Body:
  ```json
  {
    "entities": [
      "DATAFLOW"
    ],
    "filters": [
      {
        "field": "name_sort",
        "filterType": "wildcard",
        "query": "*<query>*"
      }
    ],
    "combineResults": true,
    "query": "*",
    "count": 100,
    "offset": 0,
    "sort": {
      "isRelevance": false,
      "fieldSorts": [
        {
          "field": "create_date",
          "sortOrder": "DESC"
        }
      ]
    }
  }
  ```

### List DataFlows
`GET {{instanceUrl}}/api/dataprocessing/v2/dataflows`
- Query: `limit`, `offset`, `orderBy`

### List DataFlow Versions
`GET {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/versions`
- Path: `:id`

### Get DataFlow
`GET {{instanceUrl}}/api/dataprocessing/v2/dataflows/:id`
- Path: `:id`

### Get DataFlow Version
`GET {{instanceUrl}}/api/dataprocessing/v2/dataflows/:dataflowId/versions/:versionId`
- Path: `:dataflowId`, `:versionId`

### Get DataFlow Version by Version Number
`GET {{instanceUrl}}/api/dataprocessing/v3/dataflows/:dataflowId/versions/:versionNumber`
- Path: `:dataflowId`, `:versionNumber`

### Get DataFlow Executions
`GET {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/executions`
- Path: `:id`
- Query: `limit`, `offset`

### Get DataFlow Execution
`GET {{instanceUrl}}/api/dataprocessing/v1/dataflows/:dataflowId/executions/:executionId`
- Path: `:dataflowId`, `:executionId`

### Get Tags
`GET {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/subscription`
- Path: `:id`

### Get Saved Datacenter Filters
`GET {{instanceUrl}}/api/search/v1/saved`
- Query: `queryProfile`

### Get Timezones (General)
`GET {{instanceUrl}}/api/dataprocessing/v1/dataflows/timezones`

### Get SQL Functions (General)
`GET {{instanceUrl}}/api/dataprocessing/v1/expression-docs`

### Count DataFlows by Type
`GET {{instanceUrl}}/api/dataprocessing/v2/dataflows/filters/dataflowType`

### Run DataFlow
`POST {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/executions`
- Path: `:id`
- Query: `activationTypeOverride`, `createPendingExecution`

### Bulk Run DataFlows
`POST {{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/execute`
- Body: `{"dataFlowIds":[1234,2345]}`

### Run Preview
`POST {{instanceUrl}}/api/dataprocessing/v1/dataflows/previews/run`
- Body: `{"databaseType":"MAGIC","engineProperties":{"kettle.mode":"STRICT"},"actions":[],"settings":{"zoneId":"UTC"}}`

### Create DataFlow
`POST {{instanceUrl}}/api/dataprocessing/v1/dataflows`
- Body:
  ```json
  {
    "name": "<string>",
    "actions": [
      {
        "type": "LoadFromVault",
        "id": "00000000-0000-0000-0000-000000000000",
        "name": "<string>",
        "settings": {},
        "gui": {
          "x": 123,
          "y": 123,
          "color": 3238043,
          "colorSource": null,
          "sampleJson": null
        },
        "dataSourceId": "00000000-0000-0000-0000-000000000000",
        "executeFlowWhenUpdated": false,
        "pseudoDataSource": false,
        "truncateTextColumns": false,
        "truncateRows": false,
        "onlyLoadNewVersions": false,
        "recentVersionCutoffMs": 0,
        "versionWindow": {
          "type": "NEW"
        }
      }
    ],
    "engineProperties": {
      "kettle.mode": "STRICT"
    },
    "gui": {
      "version": "1.0",
      "canvases": {
        "default": {
          "canvasSettings": {
            "coarserGrid": true,
            "backgroundVariant": "Lines"
          },
          "elements": [
            {
              "type": "Tile",
              "id": "00000000-0000-0000-0000-000000000000",
              "x": 123,
              "y": 123,
              "color": 3238043,
              "colorSource": null,
              "sampleJson": null
            },
            {
              "type": "Tile",
              "id": "00000000-0000-0000-0000-000000000000",
              "x": 123,
              "y": 123,
              "color": null,
              "colorSource": null,
              "sampleJson": null
            }
          ]
        }
      }
    },
    "inputs": [],
    "outputs": [],
    "useLegacyTriggerBehavior": false,
    "passwordProtected": false,
    "abandoned": false,
    "neverAbandon": false,
    "settings": {
      "zoneId": "UTC"
    },
    "triggerSettings": {
      "triggers": [
        {
          "title": "<string>",
          "triggerEvents": [
            {
              "datasetId": "00000000-0000-0000-0000-000000000000",
              "triggerOnDataChanged": false,
              "type": "DATASET_UPDATED"
            }
          ],
          "triggerConditions": [],
          "triggerId": 1
        }
      ],
      "zoneId": "UTC",
      "locale": "en_US"
    },
    "paused": false,
    "enabled": true,
    "restricted": false,
    "container": false,
    "databaseType": "MAGIC",
    "triggeredByInput": false,
    "draft": false,
    "editable": true,
    "magic": true,
    "subsetProcessing": false
  }
  ```

### Add Tag
`POST {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/tags`
- Path: `:id`
- Body: `{"tag":"string"}`

### Bulk Add Tags
`PUT {{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/tag`
- Body: `{"dataFlowIds":[1234,2345],"tagNames":["tag1","tag2"]}`

### Update DataFlow
`PUT {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id`
- Path: `:id`
- Body:
  ```json
  {
    "id": 1234,
    "name": "<string>",
    "dapDataFlowId": "00000000-0000-0000-0000-000000000000",
    "responsibleUserId": 123456,
    "runState": "ENABLED",
    "gui": {
      "version": "1.0",
      "canvases": {
        "default": {
          "canvasSettings": {
            "coarserGrid": true,
            "backgroundVariant": "Lines"
          },
          "elements": [
            {
              "type": "Tile",
              "id": "00000000-0000-0000-0000-000000000000",
              "x": 123,
              "y": 123,
              "color": 3238043,
              "colorSource": null,
              "sampleJson": null
            },
            {
              "type": "Tile",
              "id": "00000000-0000-0000-0000-000000000000",
              "x": 123,
              "y": 123,
              "color": null,
              "colorSource": null,
              "sampleJson": null
            }
          ]
        }
      }
    },
    "actions": [
      {
        "type": "LoadFromVault",
        "id": "00000000-0000-0000-0000-000000000000",
        "name": "<string>",
        "settings": {},
        "gui": {
          "x": 123,
          "y": 123,
          "color": 3238043,
          "colorSource": null,
          "sampleJson": null
        },
        "dataSourceId": "00000000-0000-0000-0000-000000000000",
        "executeFlowWhenUpdated": false,
        "pseudoDataSource": false,
        "truncateTextColumns": false,
        "truncateRows": false,
        "onlyLoadNewVersions": true,
        "recentVersionCutoffMs": 0,
        "versionWindow": {
          "type": "NEW"
        }
      },
      {
        "type": "ExpressionEvaluator",
        "id": "00000000-0000-0000-0000-000000000000",
        "name": "<string>",
        "dependsOn": [
          "00000000-0000-0000-0000-000000000000"
        ],
        "settings": {},
        "gui": {
          "x": 123,
          "y": 123,
          "color": null,
          "colorSource": null,
          "sampleJson": null
        },
        "expressions": [
          {
            "expression": "<sql>",
            "fieldName": "<string>",
            "settings": {}
          }
        ],
        "columnSettings": {
          "<field1>": {}
        }
      }
    ],
    "engineProperties": {
      "kettle.mode": "STRICT"
    },
    "inputs": [
      {
        "dataSourceId": "00000000-0000-0000-0000-000000000000",
        "executeFlowWhenUpdated": false,
        "dataSourceName": "<string>",
        "onlyLoadNewVersions": false,
        "recentVersionCutoffMs": 0
      }
    ],
    "outputs": [
      {
        "onboardFlowId": null,
        "dataSourceId": "00000000-0000-0000-0000-000000000000",
        "dataSourceName": "<string>",
        "versionChainType": "UPSERT"
      }
    ],
    "hydrationState": "DEHYDRATED",
    "useLegacyTriggerBehavior": false,
    "passwordProtected": false,
    "deleted": false,
    "abandoned": false,
    "neverAbandon": false,
    "settings": {},
    "triggerSettings": {
      "triggers": [
        {
          "title": "<string>",
          "triggerEvents": [
            {
              "datasetId": "00000000-0000-0000-0000-000000000000",
              "triggerOnDataChanged": false,
              "type": "DATASET_UPDATED"
            }
          ],
          "triggerConditions": [],
          "triggerId": 1
        }
      ],
      "zoneId": "UTC",
      "locale": "en_US"
    },
    "paused": false,
    "enabled": true,
    "draft": false,
    "triggeredByInput": false,
    "onboardFlowVersion": {
      "id": 12345,
      "timeStamp": 1742241147000,
      "authorId": 123456,
      "description": "<string>",
      "numInputs": 1,
      "numOutputs": 1,
      "executionCount": 1,
      "executionSuccessCount": 1,
      "versionNumber": 1
    },
    "numInputs": 1,
    "numOutputs": 1,
    "magic": true,
    "restricted": false,
    "subsetProcessing": true,
    "container": false,
    "databaseType": "MAGIC",
    "editable": true
  }
  ```

### Update Owner, Name, and Description
`PUT {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/patch`
- Path: `:id`
- Body: `{"databaseType":"<string>","description":"<string>","enabled":true,"name":"<string>","password":"<string>","responsibleUserId":1234,"restore":true,"restoreFlow":true,"useLegacyTriggerBehavior":true}`

### Bulk Update Owner
`PUT {{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/patch`
- Body: `{"dataFlowIds":[1234,2345],"responsibleUserId":1234,"restore":true,"enabled":true}`

### Update Tags
`POST {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/tags`
- Path: `:id`
- Body: `{"flowId":1234,"tags":["tag1"]}`

### Delete DataFlow
`DELETE {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id`
- Path: `:id`

### Bulk Delete DataFlows
`PUT {{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/delete`
- Body: `{"dataFlowIds":[0]}`

### Remove All Tags
`DELETE {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/tags`
- Path: `:id`

### Remove Tag
`DELETE {{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/tags/:tag`
- Path: `:id`, `:tag`

### Bulk Remove Tags
`PUT {{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/tag/delete`
- Body: `{"dataFlowIds":[1234,2345],"tagNames":["tag1","tag2"]}`
