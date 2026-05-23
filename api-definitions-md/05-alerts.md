# Alerts

### List Alerts
`GET {{instanceUrl}}/api/social/v4/alerts`
- Query: `all`, `fields`, `limit`, `offset`

### List Immediate Alerts
`GET {{instanceUrl}}/api/messaging/v3/subscriptions/schedule/primary/immediate`

### List Alert Triggered Preferences
`GET {{instanceUrl}}/api/messaging/v3/preferences/immediate/user/current/alert_triggered`

### Search Alerts
`POST {{instanceUrl}}/api/search/v1/query`
- Body:
  ```json
  {
    "count": 1000,
    "offset": 0,
    "combineResults": false,
    "query": "*",
    "filters": [],
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
    "facetValuesToInclude": [
      "TYPE"
    ],
    "facetValueLimit": 0,
    "facetValueOffset": 0,
    "includePhonetic": true,
    "queryProfile": "GLOBAL",
    "state": "list",
    "topic": null,
    "savedSearchId": null,
    "entityList": [
      [
        "alert"
      ]
    ]
  }
  ```

### Get Alerts
`POST {{instanceUrl}}/api/social/v4/alerts/ids`
- Query: `all`, `subscriberId`, `fields`, `limit`, `offset`
- Body: `["123","123"]`

### Get Alert
`GET {{instanceUrl}}/api/social/v4/alerts/:id`
- Path: `:id`

### Get Alert Action
`GET {{instanceUrl}}/api/social/v4/alerts/:alertId/actions/:actionId`
- Path: `:alertId`, `:actionId`

### Get Evaluations for Alert
`GET {{instanceUrl}}/api/social/v4/alerts/:id/evaluations`
- Path: `:id`

### Create Alert
`POST {{instanceUrl}}/api/social/v4/alerts`
- Body:
  ```json
  {
    "name": "<string>",
    "type": "SUMMARY_NUMBER",
    "owner": 123456,
    "active": true,
    "enabled": true,
    "resourceType": "CARD",
    "resourceId": "1234",
    "resourceName": "<string>",
    "triggered": false,
    "triggerFrequency": "Rarely",
    "configurations": [
      {
        "name": "OPERATION",
        "value": "CHANGES_BY"
      },
      {
        "name": "VALUE",
        "value": "100000"
      },
      {
        "name": "NOTIFY_TRIGGER",
        "value": "true"
      }
    ],
    "filterGroups": [
      {
        "name": "All Rows",
        "filterGroupId": 12345,
        "dataSourceId": "00000000-0000-0000-0000-000000000000",
        "type": "open",
        "dataSourcePermissions": false,
        "order": 0
      },
      {
        "name": "<string>",
        "filterGroupId": 23456,
        "dataSourceId": "00000000-0000-0000-0000-000000000000",
        "type": "user",
        "dataSourcePermissions": false,
        "parameters": [
          {
            "name": "dynamicPlaceholder",
            "value": "domo.policy.managed_employee_id",
            "values": [
              "domo.policy.managed_employee_id"
            ],
            "type": "DYNAMIC",
            "operator": "EQUALS",
            "not": false,
            "ignoreCase": false
          }
        ],
        "order": 0
      }
    ],
    "contextual": false,
    "filters": [
      {
        "column": "Column 1",
        "operand": "IN",
        "values": [
          "<value>"
        ],
        "dataSourceId": "00000000-0000-0000-0000-000000000000",
        "dataType": "string",
        "label": "Column 1 Label"
      }
    ],
    "subscriptions": [
      {
        "id": 123,
        "subscriberId": "1234",
        "type": "USER",
        "subscribedBy": 1234
      },
      {
        "id": 817,
        "subscriberId": "1907294812",
        "type": "GROUP",
        "subscribedBy": 466826668,
        "mutedSubscriberIds": [
          466826668
        ],
        "currentUserMember": false
      }
    ],
    "createdAt": "2025-01-01T12:00:00Z",
    "createdBy": 123456,
    "modifiedAt": "2025-01-01T12:00:00Z",
    "modifiedBy": 123456,
    "rule": "<string>",
    "filterRules": [
      "<string>"
    ],
    "category": "DATA",
    "currentUserSubscribed": false
  }
  ```

### Share Alert
`POST {{instanceUrl}}/api/social/v4/alerts/:id/share`
- Path: `:id`
- Body: `{"userMessage":"<string>","alertSubscriptions":[{"subscriberId":123456,"type":"USER"}],"sendEmail":true,"metaData":{}}`

### Update Alert
`PATCH {{instanceUrl}}/api/social/v4/alerts/:id`
- Path: `:id`
- Body: `{"id":123,"owner":123456}`

### Update Alert Rules
`PUT {{instanceUrl}}/api/social/v4/alerts/:id`
- Path: `:id`
- Body:
  ```json
  {
    "configurations": [
      {
        "name": "ANY_ROW_PRIMARY_KEYS",
        "value": "Column 1,Column 2,Column 3"
      },
      {
        "name": "OPERATION",
        "value": "ROWS_ADDED"
      },
      {
        "name": "COLUMN_ID",
        "value": "Column 2",
        "order": 0
      },
      {
        "name": "OPERATION",
        "value": "IN",
        "order": 0
      },
      {
        "name": "VALUE",
        "value": "<string>",
        "order": 0
      },
      {
        "name": "NOTIFY_REPEATABLE_TRIGGER",
        "value": true
      },
      {
        "name": "NOTIFY_TRIGGER",
        "value": true
      }
    ],
    "type": "ANY_ROW",
    "name": "<string>",
    "resourceType": "DATASET",
    "resourceId": "00000000-0000-0000-0000-000000000000",
    "filterGroups": [
      {
        "filterGroupId": 123456
      }
    ],
    "owner": 123456
  }
  ```

### Update Alert Message
`PUT {{instanceUrl}}/api/social/v4/alerts/:id/message-template`
- Path: `:id`
- Body:
  ```json
  {
    "body": "<p><span class=\"INAF rule\"></span>blah blah<span class=\"INAF cardName\">blah blah</span>blah blah<span class=\"INAF previousValue\">[Previous alert value]</span>blah blah<span class=\"INAF currentValue\">[Current alert value]</span>.</p>",
    "footer": "",
    "header": "",
    "formulas": {}
  }
  ```

### Delete Alert
`DELETE {{instanceUrl}}/api/social/v4/alerts/:id`
- Path: `:id`

### Unshare Alert
`DELETE {{instanceUrl}}/api/social/v4/alerts/:id/subscriptions`
- Path: `:id`
- Query: `subscriberId`, `type`
