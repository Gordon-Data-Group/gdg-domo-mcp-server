# Cards

### List/Search Cards
`POST {{instanceUrl}}/api/search/v1/query`
- Body:
  ```json
  {
    "count": 10000,
    "offset": 0,
    "combineResults": false,
    "query": "*",
    "filters": [
      {
        "name": "OWNED_BY_ID",
        "field": "owned_by_id",
        "facetType": "user",
        "value": "<user_id>:USER",
        "filterType": "term",
        "count": 123,
        "displayValue": "<user_name>",
        "translatedDisplayValue": "Owned by: <user_name>",
        "translatedPlaceHolderText": "Search people"
      }
    ],
    "sort": {
      "fieldSorts": [
        {
          "enum": "CREATED_DESCENDING",
          "field": "createDate",
          "sortOrder": "DESC",
          "label": "Created (Newest)",
          "order": 1
        }
      ]
    },
    "facetValuesToInclude": [],
    "facetValueLimit": 0,
    "facetValueOffset": 0,
    "includePhonetic": true,
    "queryProfile": "GLOBAL",
    "state": "list",
    "topic": null,
    "savedSearchId": null,
    "entityList": [
      [
        "card"
      ]
    ]
  }
  ```

### List Cards (Admin Summary)
`POST {{instanceUrl}}/api/content/v2/cards/adminsummary`
- Query: `limit`, `skip`
- Body:
  ```json
  {
    "ascending": true,
    "orderBy": "cardTitle",
    "includeCardTypeClause": true,
    "cardTypes": [
      "kpi",
      "badge"
    ],
    "includeCardOwnerClause": true,
    "addCardWithNoOwner": true,
    "cardOwners": [
      {
        "id": 123456,
        "type": "USER"
      }
    ],
    "includeCardTitleClause": true,
    "cardTitleSearchText": "test",
    "includePageTitleClause": true,
    "notOnPage": false,
    "pageIds": [
      123456
    ],
    "includeLastModifiedDateClause": true,
    "lastModifiedDateOperand": "BETWEEN",
    "lastModifiedStartDate": "2025-04-01",
    "lastModifiedEndDate": "2025-04-02"
  }
  ```

### Get Cards
`GET {{instanceUrl}}/api/content/v1/cards`
- Query: `urns`, `parts`, `includeFiltered`

### Get Notebook Card
`GET {{instanceUrl}}/api/content/v1/cards/notebook/:id`
- Path: `:id`

### Get Linked Cards
`GET {{instanceUrl}}/api/content/v1/cards/:id/link`
- Path: `:id`

### Get Cards Views
`PUT {{instanceUrl}}/api/content/v1/analytics/views/cards/counts`
- Body: `{"urns":[12345]}`

### Get Card Access
`GET {{instanceUrl}}/api/content/v1/share/accesslist/badge/:id`
- Path: `:id`
- Query: `expandUsers`

### Get Card DataSet Schema
`GET {{instanceUrl}}/api/content/v1/cards/:id/details`
- Path: `:id`

### Get Cards for DataSet
`GET {{instanceUrl}}/api/content/v1/datasources/:id/cards`
- Path: `:id`
- Query: `drill`

### Get Cards Min/Max Dates
`GET {{instanceUrl}}/api/content/v1/cards/minmaxdates`
- Query: `urns`

### Get Cards User has Access To
`GET {{instanceUrl}}/api/content/v1/access/users/:id/cards`
- Path: `:id`
- Query: `limit`, `offset`

### Get Chart Type Settings (General)
`GET {{instanceUrl}}/api/content/v1/cards/kpi/:chartType/options`
- Path: `:chartType`

### Get Color Palette (General)
`GET {{instanceUrl}}/api/content/v1/cards/kpi/palette`

### Validate Move to New DataSet
`GET {{instanceUrl}}/api/content/v1/cards/kpi/:cardId/comparemove/:datasetId`
- Path: `:cardId`, `:datasetId`

### Get Card Details for Update
`PUT {{instanceUrl}}/api/content/v3/cards/kpi/definition`
- Body: `{"dynamicText":true,"variables":true,"urn":"123456"}`

### Render Card (Data)
`PUT {{instanceUrl}}/api/content/v1/cards/kpi/:id/render`
- Path: `:id`
- Query: `parts`
- Body: `{"queryOverrides":{"filters":[],"overrideSlicers":false,"segments":[],"functionOverrides":{},"overrideDateRange":false},"width":960,"height":400,"scale":1,"treatLongsAsStrings":false}`

### Create Card
`PUT {{instanceUrl}}/api/content/v3/cards/kpi`
- Query: `pageId`, `parentUrn`
- Body:
  ```json
  {
    "definition": {
      "subscriptions": {
        "big_number": {
          "name": "big_number",
          "columns": [
            {
              "formulaId": "calculation_00000000-0000-0000-0000-000000000000",
              "alias": "<string>",
              "format": {
                "type": "number",
                "format": "###,##0",
                "percentMultiplied": false
              }
            }
          ],
          "filters": [],
          "orderBy": [],
          "groupBy": [],
          "fiscal": false,
          "projection": false,
          "distinct": false,
          "limit": 1
        },
        "main": {
          "name": "main",
          "columns": [
            {
              "column": "Column 1",
              "mapping": "VALUE"
            },
            {
              "formulaId": "calculation_00000000-0000-0000-0000-000000000000",
              "mapping": "VALUE",
              "format": {
                "tableColumn": {
                  "hideTotal": true
                }
              }
            }
          ],
          "filters": [
            {
              "column": "Column 1",
              "values": [],
              "filterType": "LEGACY",
              "operand": "IN",
              "dataType": "string"
            }
          ],
          "orderBy": [
            {
              "formulaId": "calculation_00000000-0000-0000-0000-000000000000",
              "order": "DESCENDING"
            }
          ],
          "groupBy": [
            {
              "column": "Column 1"
            },
            {
              "formulaId": "calculation_00000000-0000-0000-0000-000000000000"
            }
          ],
          "fiscal": false,
          "projection": false,
          "distinct": false
        }
      },
      "formulas": {
        "dsUpdated": [],
        "dsDeleted": [],
        "card": []
      },
      "annotations": {
        "new": [],
        "modified": [],
        "deleted": []
      },
      "conditionalFormats": {
        "card": [
          {
            "condition": {
              "column": "calculation_00000000-0000-0000-0000-000000000000",
              "values": [],
              "dataSourceId": "50a665ab-abfb-4721-a1e7-03fe13d36f8e",
              "filterType": "LEGACY",
              "operand": "IN"
            },
            "format": {
              "color": "#80C25DFF",
              "textColor": "#ffffff",
              "textStyle": "PLAIN",
              "applyToRow": false
            }
          }
        ],
        "datasource": []
      },
      "dynamicTitle": {
        "text": [
          {
            "text": "<string>",
            "type": "TEXT"
          },
          {
            "columns": [
              "calculation_<legacy_function_id>"
            ],
            "type": "FILTER"
          },
          {
            "text": " ",
            "type": "TEXT"
          },
          {
            "columns": [
              "Column 1",
              "calculation_<legacy_function_id>"
            ],
            "type": "FILTER"
          },
          {
            "text": " ",
            "type": "TEXT"
          },
          {
            "defaultText": "<string>",
            "columns": [
              "Column 2"
            ],
            "type": "FILTER"
          },
          {
            "text": " <string> ",
            "type": "TEXT"
          },
          {
            "type": "DATE_RANGE_FILTER_DATE_TIME_RANGE"
          }
        ]
      },
      "dynamicDescription": {
        "text": [
          {
            "text": " \n ",
            "type": "TEXT"
          },
          {
            "prefix": "<string>",
            "suffix": "<string>",
            "variables": [
              12345
            ],
            "type": "VARIABLE_VALUE"
          }
        ],
        "displayOnCardDetails": true
      },
      "charts": {
        "main": {
          "component": "main",
          "chartType": "badge_basic_table",
          "overrides": {
            "padding": "Medium",
            "header_row_fill_color": "<hex>",
            "total_row": "true",
            "hide_columns": "2,3",
            "total_row_fill_color": "<hex>",
            "total_row_position": "Before",
            "hide_alternate_row_colors": "false",
            "attr_header_row": "Bold",
            "header_row": "Left",
            "attr_total_row": "Bold"
          },
          "goal": null
        }
      },
      "allowTableDrill": false,
      "segments": {
        "active": [],
        "definitions": []
      },
      "controls": [
        {
          "id": 123,
          "function": {
            "id": 123
          },
          "entityType": "CARD",
          "entityId": "1234",
          "type": "RADIOS",
          "dataType": "STRING",
          "values": [
            {
              "expression": {
                "exprType": "STRING_VALUE",
                "value": "Yes"
              }
            },
            {
              "expression": {
                "exprType": "STRING_VALUE",
                "value": "No"
              }
            }
          ],
          "format": {
            "type": "default"
          },
          "name": "<string>",
          "description": "<string>",
          "controlType": "VARIABLE"
        },
        {
          "type": "string",
          "displayType": "multiple_select",
          "name": "<string>",
          "column": "Column 1",
          "operator": "IN",
          "values": [],
          "collapsed": false,
          "controlType": "SLICER"
        },
        {
          "dataSourceId": "00000000-0000-0000-0000-000000000000",
          "column": "calculation_00000000-0000-0000-0000-000000000000",
          "name": "Beast Mode 1",
          "columnDisplayName": "<string>",
          "operator": "IN",
          "values": [],
          "type": "string",
          "collapsed": false,
          "displayType": "multiple_select",
          "controlType": "SLICER"
        }
      ]
    },
    "dataProvider": {
      "dataSourceId": "00000000-0000-0000-0000-000000000000"
    },
    "variables": true
  }
  ```

### Share Access
`POST {{instanceUrl}}/api/content/v1/share`
- Query: `sendEmail`
- Body: `{"resources":[{"type":"badge","id":"12345"},{"type":"badge","id":"23456"}],"recipients":[{"type":"user","id":"12345"}],"message":"<string>"}`

### Create Card Change in History
`POST {{instanceUrl}}/api/kpis/:id/history`
- Path: `:id`
- Body: `{"changes":{"kpi":{"title":true,"description":true,"aggregationChanged":true,"dimensionsChanged":true,"orderingChanged":true,"filtersChanged":true},"data":{},"initial":true},"comment":"<string>"}`

### Update Card
`PUT {{instanceUrl}}/api/content/v3/cards/kpi/:id`
- Path: `:id`
- Body:
  ```json
  {
    "definition": {
      "subscriptions": {
        "big_number": {
          "name": "big_number",
          "columns": [
            {
              "formulaId": "calculation_00000000-0000-0000-0000-000000000000",
              "alias": "<string>",
              "format": {
                "type": "number",
                "format": "###,##0",
                "percentMultiplied": false
              }
            }
          ],
          "filters": [],
          "orderBy": [],
          "groupBy": [],
          "fiscal": false,
          "projection": false,
          "distinct": false,
          "limit": 1
        },
        "main": {
          "name": "main",
          "columns": [
            {
              "column": "Column 1",
              "mapping": "VALUE"
            },
            {
              "formulaId": "calculation_00000000-0000-0000-0000-000000000000",
              "mapping": "VALUE",
              "format": {
                "tableColumn": {
                  "hideTotal": true
                }
              }
            }
          ],
          "filters": [
            {
              "column": "Column 1",
              "values": [
                "<string>"
              ],
              "filterType": "LEGACY",
              "operand": "IN",
              "dataType": "string"
            }
          ],
          "orderBy": [
            {
              "formulaId": "calculation_00000000-0000-0000-0000-000000000000",
              "order": "DESCENDING"
            }
          ],
          "groupBy": [
            {
              "column": "Column 1"
            },
            {
              "formulaId": "calculation_00000000-0000-0000-0000-000000000000"
            }
          ],
          "fiscal": false,
          "projection": false,
          "distinct": false
        }
      },
      "formulas": {
        "dsUpdated": [],
        "dsDeleted": [],
        "card": []
      },
      "annotations": {
        "new": [],
        "modified": [],
        "deleted": []
      },
      "conditionalFormats": {
        "card": [],
        "datasource": []
      },
      "dynamicTitle": {
        "text": [
          {
            "text": "<string>",
            "type": "TEXT"
          },
          {
            "columns": [
              "calculation_<legacy_function_id>"
            ],
            "type": "FILTER"
          },
          {
            "text": " ",
            "type": "TEXT"
          },
          {
            "columns": [
              "Column 1",
              "calculation_00000000-0000-0000-0000-000000000000"
            ],
            "type": "FILTER"
          },
          {
            "text": " ",
            "type": "TEXT"
          },
          {
            "defaultText": "<string>",
            "columns": [
              "Column 2"
            ],
            "type": "FILTER"
          },
          {
            "text": " <string> ",
            "type": "TEXT"
          },
          {
            "type": "DATE_RANGE_FILTER_DATE_TIME_RANGE"
          }
        ]
      },
      "dynamicDescription": {
        "text": [
          {
            "text": " \n ",
            "type": "TEXT"
          },
          {
            "prefix": "<string>",
            "suffix": "<string>",
            "variables": [
              12345
            ],
            "type": "VARIABLE_VALUE"
          }
        ],
        "displayOnCardDetails": true
      },
      "charts": {
        "main": {
          "component": "main",
          "chartType": "badge_basic_table",
          "overrides": {},
          "goal": null
        }
      },
      "allowTableDrill": false,
      "segments": {
        "active": [],
        "definitions": []
      },
      "modified": 1738968629000,
      "controls": [
        {
          "id": 123,
          "function": {
            "id": 1234
          },
          "entityType": "CARD",
          "entityId": "<card_id>",
          "type": "RADIOS",
          "dataType": "STRING",
          "values": [
            {
              "expression": {
                "exprType": "STRING_VALUE",
                "value": "Yes"
              }
            },
            {
              "expression": {
                "exprType": "STRING_VALUE",
                "value": "No"
              }
            }
          ],
          "format": {
            "type": "default"
          },
          "name": "<string>",
          "description": "<string>",
          "controlType": "VARIABLE"
        },
        {
          "type": "string",
          "displayType": "multiple_select",
          "name": "<string>",
          "column": "Column 1",
          "operator": "IN",
          "values": [],
          "collapsed": false,
          "controlType": "SLICER"
        }
      ]
    },
    "dataProvider": {
      "dataSourceId": "00000000-0000-0000-0000-000000000000"
    },
    "variables": true
  }
  ```

### Lock/Unlock Card
`PUT {{instanceUrl}}/api/content/v1/cards/:id`
- Path: `:id`
- Body: `{"locked":true}`

### Bulk Add Cards to Pages (Does Not Remove)
`PUT {{instanceUrl}}/api/content/v1/cards/bulk/pages`
- Body: `{"cardIds":["123","234"],"destinationPageIds":[123456]}`

### Move Card (Update Pages)
`PUT {{instanceUrl}}/api/content/v1/cards/:id/pages`
- Path: `:id`
- Body: `[123456,234567]`

### Increment Views
`PUT {{instanceUrl}}/api/content/v1/analytics/views/cards/increment`
- Body: `{"urns":["1234","2345"],"context":"AUTHENTICATED"}`

### Update Owners
`POST {{instanceUrl}}/api/content/v1/cards/owners/:action`
- Path: `:action`
- Body: `{"cardIds":[123456],"cardOwners":[{"id":"1234","type":"USER"}]}`

### Remove Card from Page
`POST {{instanceUrl}}/api/kpis/:id/remove`
- Path: `:id`
- Query: `pageid`

### Remove Access to Cards
`DELETE {{instanceUrl}}/api/content/v1/share/bulk/badge/:type/:id`
- Path: `:type`, `:id`
- Query: `resourceIds`

### Delete Cards
`DELETE {{instanceUrl}}/api/content/v1/cards/bulk`
- Query: `cardIds`

### Delete Drill Path
`DELETE {{instanceUrl}}/api/kpis/:cardId/drillPath/:drillNumber/drillView/:drillPathId`
- Path: `:cardId`, `:drillNumber`, `:drillPathId`

## Problems (Issues)

### Get Card Problems
`GET {{instanceUrl}}/api/content/v1/cards`
- Query: `urns`, `parts`

### Create Problem
`POST {{instanceUrl}}/api/content/v1/badges/:cardId/problems`
- Path: `:cardId`
- Body: `raw message text`

### Resolve Problem
`PUT {{instanceUrl}}/api/content/v1/badges/:cardId/problems/:problemId/states`
- Path: `:cardId`, `:problemId`
- Body: `{"state":"RESOLVED"}`
