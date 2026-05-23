# DataSets and Streams

### Search DataSets
`POST {{instanceUrl}}/api/data/ui/v3/datasources/search`
- Body:
  ```json
  {
    "entities": [
      "DATASET"
    ],
    "filters": [
      {
        "field": "name_sort",
        "filterType": "wildcard",
        "query": "*"
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

### List DataSets
`GET {{instanceUrl}}/api/data/v3/datasources`
- Query: `limit`, `offset`, `part`, `includeHidden`, `orderBy`, `ownerId`, `displayType`, `type`, `dataProviderType`, `nameLike`, `createdSince`

### List Tags
`GET {{instanceUrl}}/api/data/ui/v3/datasources/search/tags/all`

### Get DataSets
`POST {{instanceUrl}}/api/data/v3/datasources/bulk`
- Query: `includePrivate`, `includeAllDetails`
- Body: `["00000000-0000-0000-0000-000000000000","00000000-0000-0000-0000-000000000000"]`

### Get DataSets Owned by User/Group
`POST {{instanceUrl}}/api/data/ui/v3/datasources/ownedBy`
- Body: `[{"id":1234,"type":"USER"}]`

### Get DataSet
`GET {{instanceUrl}}/api/data/v3/datasources/:id`
- Path: `:id`
- Query: `includeAllDetails`, `part`

### Get Stream
`GET {{instanceUrl}}/api/data/v1/streams/:id`
- Path: `:id`
- Query: `fields`

### Get Stream Executions
`GET {{instanceUrl}}/api/data/v1/streams/:id/executions`
- Path: `:id`

### Get Stream Execution
`GET {{instanceUrl}}/api/data/v1/streams/:streamId/executions/:executionId`
- Path: `:streamId`, `:executionId`

### Get Saved Datacenter Filters
`GET {{instanceUrl}}/api/search/v1/saved`
- Query: `queryProfile`

### Get Lineage
`GET {{instanceUrl}}/api/data/v1/lineage/DATA_SOURCE/:id`
- Path: `:id`
- Query: `traverseUp`, `traverseDown`, `requestEntities`, `maxDepth`

### Get Impact Counts
`GET {{instanceUrl}}/api/data/v1/impacts/DATA_SOURCE/:id`
- Path: `:id`

### Get Schema
`GET {{instanceUrl}}/api/query/v1/datasources/:id/schema/indexed`
- Path: `:id`
- Query: `includeHidden`

### Get Wrangle (Column Tags, Descriptions, and Order)
`GET {{instanceUrl}}/api/query/v1/datasources/:id/wrangle`
- Path: `:id`

### Query DataSet
`POST {{instanceUrl}}/api/query/v1/execute/:id`
- Path: `:id`
- Body:
  ```json
  {
      "querySource": "data_table",
      "useCache": true,
      "query": {
          "columns": [
              {
                  "exprType": "COLUMN",
                  "column": "Column 1"
              },
              {
                  "exprType": "COLUMN",
                  "column": "Column 2"
              }
          ],
          "limit": {
              "limit": 10000,
              "offset": 0
          },
          "orderByColumns": [
              {
                  "expression": {
                      "exprType": "COLUMN",
                      "column": "Column 1"
                  },
                  "order": "ASCENDING"
              }
          ],
          "groupByColumns": [
              {
                  "exprType": "COLUMN",
                  "column": "Column 1"
              }
          ],
          "where": {
              "not": false,
              "exprType": "IN",
              "leftExpr": {
                  "exprType": "COLUMN",
                  "column": "Column 1"
              },
              "selectSet": [
                  {
                      "exprType": "STRING_VALUE",
                      "value": "<string>"
                  }
              ]
          },
          "having": null
      },
      "context": {
          "calendar": "StandardCalendar",
          "features": {
              "PerformTimeZoneConversion": true,
              "AllowNullValues": true,
              "TreatNumbersAsStrings": true
          }
      },
      // Used for Views Explorer, not the regular Data table
      "viewTemplate": null,
      "tableAliases": null
  }
  ```

### Query DataSet with SQL
`POST {{instanceUrl}}/api/query/v1/execute/:id`
- Path: `:id`
- Body: `{"sql":"SELECT * FROM your_table WHERE column = 'value'"}`

### Query Preview (Views Explorer)
`POST {{instanceUrl}}/api/query/v1/views/query-preview`
- Body:
  ```json
  {
    "querySource": "judoTable",
    "schema": {
      "name": "<string>",
      "tables": [
        {
          "columns": []
        }
      ],
      "viewTemplate": {
        "version": "jsql",
        "fromItemInfo": {
          "mapping": {
            "columnInfo": {}
          },
          "where": {
            "columnInfo": {}
          },
          "having": {
            "columnInfo": {}
          },
          "calculated": {
            "columnInfo": {}
          },
          "remapped": {
            "columnInfo": {}
          }
        },
        "select": {
          "@type": "SELECT",
          "selectBody": {
            "@type": "PLAIN_SELECT",
            "fromItem": {
              "@type": "TABLE",
              "name": "00000000-0000-0000-0000-000000000000",
              "alias": {
                "name": "base"
              }
            },
            "groupBy": null,
            "where": {},
            "joins": [],
            "orderByElements": [],
            "selectItems": []
          }
        }
      },
      "tableAliases": {
        "<dataset_name>": "00000000-0000-0000-0000-000000000000"
      }
    },
    "useCache": true,
    "query": {
      "columns": [],
      "limit": {
        "limit": 10000,
        "offset": 0
      },
      "orderByColumns": null,
      "groupByColumns": null,
      "where": null,
      "having": null
    },
    "context": {
      "calendar": "StandardCalendar",
      "features": {
        "PerformTimeZoneConversion": true,
        "AllowNullValues": true,
        "TreatNumbersAsStrings": true
      }
    },
    "viewTemplate": {
      "version": "jsql",
      "fromItemInfo": {
        "mapping": {
          "columnInfo": {}
        },
        "where": {
          "columnInfo": {}
        },
        "having": {
          "columnInfo": {}
        },
        "calculated": {
          "columnInfo": {}
        },
        "remapped": {
          "columnInfo": {}
        }
      },
      "select": {
        "@type": "SELECT",
        "selectBody": {
          "@type": "PLAIN_SELECT",
          "fromItem": {
            "@type": "TABLE",
            "name": "00000000-0000-0000-0000-000000000000",
            "alias": {
              "name": "base"
            }
          },
          "groupBy": null,
          "where": {},
          "joins": [],
          "orderByElements": [],
          "selectItems": []
        }
      }
    },
    "tableAliases": {
      "<dataset_name>": "00000000-0000-0000-0000-000000000000"
    }
  }
  ```

### Create Stream and DataSet
`POST {{instanceUrl}}/api/data/v1/streams`
- Body:
  ```json
  {
    "updateMethod": "REPLACE",
    "transport": {
      "type": "CONNECTOR",
      "description": "com.domo.connector.json.customparsing",
      "version": "4"
    },
    "dataProvider": {
      "id": 1234,
      "key": "json5"
    },
    "account": {
      "id": 1234
    },
    "accounts": [],
    "accountTemplate": null,
    "dataSource": {
      "name": "<string>",
      "description": "<string>"
    },
    "scheduleExpression": null,
    "scheduleStartDate": null,
    "advancedScheduleJson": "{\"type\":\"MANUAL\",\"timezone\":\"UTC\"}",
    "scheduleRetryExpression": "15 minutes",
    "scheduleRetryCount": 3,
    "scheduleState": "MANUAL",
    "scheduleAssertion": false,
    "inactiveScheduleCode": null,
    "configuration": [
      {
        "category": "METADATA",
        "name": "retry.retryNumber",
        "type": "string",
        "value": "0"
      }
    ]
  }
  ```

### Create View (Views Explorer)
`POST {{instanceUrl}}/api/query/v1/views`
- Body:
  ```json
  {
      "lastModified": "1735689600000",
      "dataSourceName": "<string>",
      "dataSourceDescription": "",
      "dataProviderType": "dataset-view",
      "cloudId": "domo",
      "responsibleUserId": 1234,
      "trigger": {
          "dataSource": "00000000-0000-0000-0000-000000000000"
      },
      "schema": {
          "tables": [
              {
                  "columns": [
                      {
                          "name": "Column 1",
                          "id": "Column 1",
                          "type": "STRING",
                          "visible": true,
                          "order": 0,
                          "referenceDataSourceId": "00000000-0000-0000-0000-000000000000",
                          "aggregated": false
                      }
                  ]
              }
          ],
          "viewTemplate": {
              "version": "jsql",
              "fromItemInfo": {
                  "mapping": {
                      "columnInfo": {
                          "Column 1": {
                              "formattedExpression": "`base`.`Column 1`",
                              "type": "STRING",
                              "aggregated": false
                      }
                  },
                  "where": {
                      "columnInfo": {}
                  },
                  "having": {
                      "columnInfo": {}
                  },
                  "calculated": {
                      "columnInfo": {}
                  },
                  "remapped": {
                      "columnInfo": {}
                  }
              },
              "select": {
                  "@type": "SELECT",
                  "selectBody": {
                      "@type": "PLAIN_SELECT",
                      "fromItem": {
                          "@type": "TABLE",
                          "name": "00000000-0000-0000-0000-000000000000",
                          "alias": {
                              "name": "base"
                          }
                      },
                      "groupBy": null,
                      "joins": [],
                      "orderByElements": [
                          {
                              "asc": true,
                              "ascDescPresent": true,
                              "expression": {
                                  "@type": "COLUMN",
                                  "columnName": "Column 1",
                                  "table": {
                                      "@type": "TABLE",
                                      "name": "mapping"
                                  },
                                  "type": {
                                      "dataType": "STRING"
                                  }
                              }
                          }
                      ],
                      "selectItems": [
                          {
                              "@type": "SELECT_EXPRESSION_ITEM",
                              "expression": {
                                  "@type": "COLUMN",
                                  "columnName": "Column 1",
                                  "table": {
                                      "@type": "TABLE",
                                      "name": "mapping"
                                  },
                                  "type": {
                                      "dataType": "STRING"
                                  }
                              }
                          }
                      ]
                  }
              }
          },
          "tableAliases": {
              "<string>": "00000000-0000-0000-0000-000000000000"
          }
      }
  }
  ```

### Bulk Add Tags
`POST {{instanceUrl}}/api/data/v1/ui/bulk/tag`
- Body: `{"bulkItems":{"ids":["00000000-0000-0000-0000-000000000000"],"type":"DATA_SOURCE"},"tags":["Tag 1"]}`

### Run Stream/DataSet
`POST {{instanceUrl}}/api/data/v1/streams/:id/executions`
- Path: `:id`

### Defrost (Unvault) DataSet
`POST {{instanceUrl}}/api/data/ui/v3/datasources/:id/defrost`
- Path: `:id`

### Share DataSet
`POST {{instanceUrl}}/api/data/v3/datasources/:id/share`
- Path: `:id`
- Body: `{"permissions":[{"type":"GROUP","id":"1234","accessLevel":"CAN_SHARE"}],"sendEmail":false}`

### Append to Webhook DataSet
`POST {{instanceUrl}}/api/iot/v1/webhook/data/:id`
- Path: `:id`

### Wrangle (Update Column Tags, Descriptions, and Order)
`POST {{instanceUrl}}/api/query/v1/datasources/:id/wrangle`
- Path: `:id`
- Body: `{"columns":[{"name":"Column 1","id":"Column 1","type":"LONG","visible":true,"order":0,"referenceDataSourceId":"00000000-0000-0000-0000-000000000000","invalid":false,"newName":"Column 1"}]}`

### Update Stream
`PUT {{instanceUrl}}/api/data/v1/streams/:id`
- Path: `:id`
- Body:
  ```json
  {
    "id": 1234,
    "valid": true,
    "updateMethod": "REPLACE",
    "dataProvider": {
      "id": 1234,
      "key": "json5"
    },
    "account": {
      "id": 123
    },
    "accounts": [],
    "accountTemplate": null,
    "dataSource": {
      "id": "00000000-0000-0000-0000-000000000000",
      "name": "<string>",
      "description": "<string>"
    },
    "schemaDefinition": {
      "columns": [
        {
          "type": "STRING",
          "name": "Column 1",
          "id": "Column 1",
          "visible": true,
          "metadata": {
            "colLabel": "Column 1",
            "colFormat": "",
            "isEncrypted": false
          }
        }
      ]
    },
    "scheduleExpression": "0 28 23 * * ?",
    "scheduleStartDate": null,
    "advancedScheduleJson": "{\"type\":\"DAY\",\"at\":\"11:28 PM\",\"timezone\":\"UTC\"}",
    "scheduleRetryExpression": null,
    "scheduleRetryCount": 0,
    "scheduleState": "ACTIVE",
    "scheduleAssertion": false,
    "inactiveScheduleCode": null,
    "configuration": [
      {
        "category": "METADATA",
        "name": "report",
        "type": "string",
        "value": "BalanceSheet"
      }
    ]
  }
  ```

### Update Name and Description
`PUT {{instanceUrl}}/api/data/v3/datasources/:id/properties`
- Path: `:id`
- Body: `{"dataSourceName":"<string>","dataSourceDescription":"<string>"}`

### Update Owner
`PUT {{instanceUrl}}/api/data/v2/datasources/:id/responsibleUsers`
- Path: `:id`
- Body: `{"responsibleUserId":"1234"}`

### Bulk Update Owners (v2/datasources)
`PUT {{instanceUrl}}/api/data/v2/datasources/responsible-user/:userId`
- Path: `:userId`
- Body: `["00000000-0000-0000-0000-000000000000"]`

### Bulk Update Owners (v1/ui)
`POST {{instanceUrl}}/api/data/v1/ui/bulk/reassign`
- Body: `{ "type": "DATA_SOURCE", "ids": [ "00000000-0000-0000-0000-000000000000", "11111111-1111-1111-1111-111111111111" ], // groupId or userId "groupId": 1234 }`

### Bulk Delete DataSets
`POST {{instanceUrl}}/api/data/v1/ui/bulk/delete`
- Body: `{"type":"DATA_SOURCE","ids":["00000000-0000-0000-0000-000000000000","11111111-1111-1111-1111-111111111111"]}`

### Update Tags
`POST {{instanceUrl}}/api/data/ui/v3/datasources/:id/tags`
- Path: `:id`
- Body: `["<string>"]`

### Sync Cloud Amplifier DataSet
`PUT {{instanceUrl}}/api/query/v1/byos/accounts/:cloudId/polling/refresh`
- Path: `:cloudId`

### Delete DataSet
`DELETE {{instanceUrl}}/api/data/v3/datasources/:id`
- Path: `:id`
- Query: `deleteMethod`

### Delete Check
`POST {{instanceUrl}}/api/data/v1/ui/bulk/delete/check`
- Body: `{"type":"DATA_SOURCE","ids":["00000000-0000-0000-0000-000000000000"]}`

### Abort Stream
`PUT {{instanceUrl}}/api/data/v1/streams/:streamId/executions/:executionId`
- Path: `:streamId`, `:executionId`
- Body: `{"category":"CONNECTOR","message":"<string>"}`

## AI Readiness/Data Dictionary

### Get Data Dictionary
`GET {{instanceUrl}}/api/ai/readiness/v1/data-dictionary/dataset/:id`
- Path: `:id`

### Create Data Dictionary
`POST {{instanceUrl}}/api/ai/readiness/v1/data-dictionary/dataset/:datasetId`
- Path: `:datasetId`
- Body:
  ```json
  {
    "id": "00000000-0000-0000-0000-000000000000",
    "datasetId": "00000000-0000-0000-0000-000000000000",
    "name": "<string>",
    "description": "<string>",
    "unitOfAnalysis": "",
    "columns": [
      {
        "name": "Column 1",
        "description": "<string>",
        "synonyms": [],
        "subType": {
          "type": null,
          "defaultAggregation": null
        },
        "agentEnabled": true,
        "beastmodeId": null
      },
      {
        "name": "Column 2",
        "description": "<string>",
        "synonyms": [],
        "subType": {
          "type": null,
          "defaultAggregation": null
        },
        "agentEnabled": true,
        "beastmodeId": null
      }
    ]
  }
  ```

### Update Data Dictionary
`PUT {{instanceUrl}}/api/ai/readiness/v1/data-dictionary/dataset/:id`
- Path: `:id`
- Body:
  ```json
  {
      "id": "00000000-0000-0000-0000-000000000000",
      "datasetId": "00000000-0000-0000-0000-000000000000",
      "name": "<string>",
      "description": "<string>",
      "columns": [
          {
              "columnId": "00000000-0000-0000-0000-000000000000",
              "name": "Column 1",
              "description": "<string>",
              "synonyms": [],
              "subType": {
                  "type": null,
                  "defaultAggregation": null
              },
              "agentEnabled": true
          },
          {
              //columnId can be excluded to create/add
              "name": "Column 2",
              "description": "<string>",
              "synonyms": [],
              "subType": {
                  "type": null,
                  "defaultAggregation": null
              },
              "agentEnabled": true
          }
      ]
  }
  ```

## Data Repair

### List Data Versions (v3)
`GET {{instanceUrl}}/api/data/v3/datasources/:datasetId/dataversions/details`
- Path: `:datasetId`

### List Data Versions (v2)
`GET {{instanceUrl}}/api/data/v2/datasources/:datasetId/dataversions`
- Path: `:datasetId`

### Get Data Version
`GET {{instanceUrl}}/api/data/v2/datasources/:datasetId/dataversions/:versionId`
- Path: `:datasetId`, `:versionId`
- Query: `excludeAppendedData`, `rowLimit`

### Insert Data Version
`POST {{instanceUrl}}/api/data/v3/datasources/:datasetId/dataversions`
- Path: `:datasetId`
- Query: `repairDataVersionId`, `repairAction`

### Bulk Delete Data Versions
`DELETE {{instanceUrl}}/api/data/v2/datasources/:datasetId/dataversions`
- Path: `:datasetId`
- Body: `[1,2,3,4]`

## PDP/Column PDP

### Get Column PDP Policies
`GET {{instanceUrl}}/api/query/v2/data-control/:datasetId/policy-group`
- Path: `:datasetId`

### Get Column PDP Policy Mapping
`GET {{instanceUrl}}/api/query/v2/data-control/:datasetId/column-policy-mapping`
- Path: `:datasetId`

### Create Column PDP Policy
`POST {{instanceUrl}}/api/query/v2/data-control/:datasetId/policy-group`
- Path: `:datasetId`
- Body:
  ```json
  {
      "name": "<string>",
      "filterGroupId": null,
      "dataSourceId": "00000000-0000-0000-0000-000000000000",
      "type": "user",
      "columnPolicies": [
          {
              "uuid": "00000000-0000-0000-0000-000000000000",
              "values": [
                  "hash",
                  "md5"
              ],
              "dataSourcePermissions": true,
              "policyOrder": 0,
              "defaultPolicy": true
          },
          {
              "uuid": "00000000-0000-0000-0000-000000000000",
              "values": [
                  "visible"
              ],
              "dataSourcePermissions": false,
              "groupIds": [], //as integers
              "policyOrder": 1,
              "defaultPolicy": false
          }
      ],
      "isNew": true
  }
  ```

### Create Column PDP Policy Mapping
`POST {{instanceUrl}}/api/query/v2/data-control/:datasetId/column-policy-mapping`
- Path: `:datasetId`
- Body: `{"id":null,"filterGroupId":12345,"dataSourceId":"00000000-0000-0000-0000-000000000000","columnName":"<string>"}`

### Update Column PDP Policy
`PUT {{instanceUrl}}/api/query/v2/data-control/:datasetId/policy-group/:policyId`
- Path: `:datasetId`, `:policyId`
- Body:
  ```json
  {
    "name": "<string>",
    "filterGroupId": 12345,
    "dataSourceId": "00000000-0000-0000-0000-000000000000",
    "type": "user",
    "columnPolicies": [
      {
        "uuid": "00000000-0000-0000-0000-000000000000",
        "policyOrder": 0,
        "values": [
          "hash",
          "md5"
        ],
        "dataSourcePermissions": true,
        "policyId": 6,
        "defaultPolicy": true
      }
    ]
  }
  ```

### Update Column PDP Policy Mapping
`PUT {{instanceUrl}}/api/query/v2/data-control/:datasetId/column-policy-mapping/:columnPdpPolicyMappingId`
- Path: `:datasetId`, `:columnPdpPolicyMappingId`
- Body: `{"id":1,"filterGroupId":12345,"policyName":"<string>","dataSourceId":"00000000-0000-0000-0000-000000000000","columnName":"<string>"}`

### Delete Column PDP Policy
`DELETE {{instanceUrl}}/api/query/v2/data-control/:datasetId/policy-group/:policyId`
- Path: `:datasetId`, `:policyId`

### Delete Column PDP Policy Mapping
`DELETE {{instanceUrl}}/api/query/v2/data-control/:datasetId/column-policy-mapping/:columnPdpPolicyMappingId`
- Path: `:datasetId`, `:columnPdpPolicyMappingId`

## PDP/Row PDP

### Get Row PDP Policies
`GET {{instanceUrl}}/api/query/v1/data-control/:datasetId/filter-groups`
- Path: `:datasetId`
- Query: `options`

### Create Row PDP Policy
`POST {{instanceUrl}}/api/query/v1/data-control/:datasetId/filter-groups`
- Path: `:datasetId`
- Body:
  ```json
  {
    "name": "<string>",
    "dataSourceId": "00000000-0000-0000-0000-000000000000",
    "userIds": [],
    "virtualUserIds": [],
    "groupIds": [],
    "dataSourcePermissions": false,
    "parameters": [
      {
        "type": "DYNAMIC",
        "name": "Column 1",
        "values": [
          "domo.policy.managed_employee_id"
        ],
        "operator": "EQUALS",
        "ignoreCase": false
      }
    ]
  }
  ```

### Update Row PDP Policy
`PUT {{instanceUrl}}/api/query/v1/data-control/:datasetId/filter-groups/:policyId`
- Path: `:datasetId`, `:policyId`
- Body:
  ```json
  {
    "name": "<string>",
    "filterGroupId": 12345,
    "dataSourceId": "00000000-0000-0000-0000-000000000000",
    "type": "user",
    "policySetId": 1234,
    "userIds": [],
    "dataSourcePermissions": false,
    "parameters": [
      {
        "name": "Column 1",
        "operator": "EQUALS",
        "type": "COLUMN",
        "values": [
          "<string>"
        ],
        "ignoreCase": false
      },
      {
        "name": "Column 2",
        "operator": "EQUALS",
        "type": "COLUMN",
        "values": [
          "<string>"
        ],
        "ignoreCase": false
      }
    ],
    "order": 0
  }
  ```

### Delete Row PDP Policy
`DELETE {{instanceUrl}}/api/query/v1/data-control/:datasetId/filter-groups/:policyId`
- Path: `:datasetId`, `:policyId`

## PDP

### Get DataSet PDP Status
`GET {{instanceUrl}}/api/query/v2/data-control/:datasetId`
- Path: `:datasetId`

### Get DataSet PDP Impacted Resources
`GET {{instanceUrl}}/api/data/v3/datasources/:datasetId/impacted-resources`
- Path: `:datasetId`

### Enable/Disable PDP on DataSet
`PUT {{instanceUrl}}/api/query/v1/data-control/:datasetId`
- Path: `:datasetId`
- Body: `{"enabled":true,"secured":false,"external":false,"enabledColumn":true}`

## Uploads

### Create New Upload
`POST {{instanceUrl}}/api/data/v3/datasources/:datasetId/uploads`
- Path: `:datasetId`
- Body: `{"action":"APPEND","message":"Uploading","appendId":"latest"}`

### Upload Data
`PUT {{instanceUrl}}/api/data/v3/datasources/:datasetId/uploads/:uploadId/parts/:partNumber`
- Path: `:datasetId`, `:uploadId`, `:partNumber`
- Body: `text,formatted,as,csv`

### Commit Upload
`PUT {{instanceUrl}}/api/data/v3/datasources/:datasetId/uploads/:uploadId/commit`
- Path: `:datasetId`, `:uploadId`
- Body: `{"index":true,"appendId":"latest","message":"it worked"}`

## Webforms

### Get Webform Data
`GET {{instanceUrl}}/api/data/v2/webforms/:datasetId/grid`
- Path: `:datasetId`

### Update Webform Data
`PUT {{instanceUrl}}/api/data/v2/webforms/:streamId`
- Path: `:streamId`
- Body:
  ```json
  {
    "rows": [
      [
        "<string>",
        1234,
        "<date>"
      ],
      [
        "<string>",
        1234,
        "<date>"
      ]
    ],
    "columns": [
      {
        "name": "Column 1",
        "type": "STRING"
      },
      {
        "name": "Column 2",
        "type": "LONG",
        "displayType": "NUMBER"
      },
      {
        "name": "Column 3",
        "type": "DATE"
      }
    ],
    "name": "<dataset_name>",
    "cloudId": null
  }
  ```
