# Scheduled Reports

### List Scheduled Reports
`GET {{instanceUrl}}/api/content/v1/reportschedules`
- Query: `filter`, `isAscending`, `orderBy`

### List Scheduled Report Resources
`GET {{instanceUrl}}/api/content/v1/reportschedules/resources`
- Query: `limit`, `skip`

### Get Scheduled Report
`GET {{instanceUrl}}/api/content/v1/reportschedules/:id`
- Path: `:id`

### Get Scheduled Report History
`GET {{instanceUrl}}/api/content/v1/reportschedules/:id/history`
- Path: `:id`
- Query: `limit`, `skip`

### Get Scheduled Reports for Resource
`GET {{instanceUrl}}/api/content/v1/reportschedules/resources/:resourceType/:resourceId`
- Path: `:resourceType`, `:resourceId`
- Query: `skip`, `limit`, `showAll`

### Get View
`GET {{instanceUrl}}/api/content/v2/views/:id`
- Path: `:id`

### Search Scheduled Report History
`POST {{instanceUrl}}/api/content/v1/reportschedules/history/search`
- Query: `limit`, `skip`
- Body:
  ```json
  {
      "includeTypeClause": false,
      "isAutomated": false,
      "includeTitleClause": false,
      "includeStatusClause": true,
      "includeScheduleIdClause": true,
      "scheduleId": "120",
      "status": "success" //success or failure
  }
  ```

### Send Scheduled Report
`POST {{instanceUrl}}/api/content/v1/reportschedules/:id/sendnow`
- Path: `:id`
- Body: `[{"type":"USER","value":"123456"}]`

### Create Scheduled Report
`POST {{instanceUrl}}/api/content/v1/reportschedules`
- Body:
  ```json
  {
    "subject": "<string>",
    "attachmentInclude": true,
    "schedule": {
      "frequency": "WEEKLY",
      "enabled": true,
      "daysToRun": "1",
      "hourOfDay": "11",
      "minOfHour": "11",
      "expirationDate": 123456789000,
      "startDate": 123456789000,
      "additionalRecipients": [
        {
          "type": "USER",
          "value": "123456",
          "email": "test@email.com"
        },
        {
          "type": "EMAIL",
          "value": "email@domain.tld",
          "email": "email@domain.tld"
        }
      ]
    },
    "viewId": 123456
  }
  ```

### Create View
`POST {{instanceUrl}}/api/content/v2/views`
- Body:
  ```json
  {
    "name": "<string>",
    "resourceType": "CARD",
    "resourceId": 123456,
    "type": "VIEW",
    "purpose": "REPORT",
    "filterGroupIds": [],
    "filters": [],
    "functionOverrides": {},
    "chartState": {
      "chartType": "badge_basic_table",
      "overrides": {
        "hide_series": "none",
        "series_filter": "none",
        "row_filter": "none",
        "range_filter_y": "none",
        "range_filter_x": "none",
        "range_filter_cat_x": "none",
        "range_filter_time": "none",
        "collapsed_filters": "none",
        "column_sort": "[{\"column\":\"Date\",\"sort\":\"asc\"}]"
      }
    },
    "overrideDateRange": true,
    "overrideSlicers": true,
    "segmentIds": []
  }
  ```

### Update Scheduled Report
`PUT {{instanceUrl}}/api/content/v1/reportschedules/:id`
- Path: `:id`
- Body:
  ```json
  {
    "id": 123,
    "title": "<string>",
    "ownerId": 123456,
    "owner": false,
    "schedule": {
      "frequency": "WEEKLY",
      "ownerId": 123456,
      "daysToRun": "1",
      "hourOfDay": 11,
      "minOfHour": 11,
      "expirationDate": 1234567890000,
      "timezone": "America/New_York",
      "additionalRecipients": [
        {
          "type": "USER",
          "value": "123456"
        },
        {
          "type": "EMAIL",
          "value": "email@domain.tld"
        }
      ],
      "nextRunDate": 1234567890000,
      "startDate": 1234567890000,
      "unsubscribedRecipients": [],
      "enabled": true,
      "embedReport": false
    },
    "subject": "<string>",
    "viewId": 123456,
    "active": true,
    "attachmentInclude": true
  }
  ```

### Enable/Disable Scheduled Report
`PUT {{instanceUrl}}/api/content/v1/reportschedules/:id/enabled`
- Path: `:id`
- Body: `false`

### Update View
`PUT {{instanceUrl}}/api/content/v2/views/:id`
- Path: `:id`
- Body:
  ```json
  {
    "id": 123456,
    "name": "<string>",
    "type": "VIEW",
    "resourceType": "CARD",
    "resourcePrefix": null,
    "resourceId": 123456,
    "locked": false,
    "active": true,
    "ownerId": 123456,
    "description": null,
    "filters": [
      {
        "column": "Column 1",
        "operand": "IN",
        "values": [
          "Lost"
        ],
        "dataType": "string",
        "filterType": "LEGACY",
        "affectedCardUrns": [],
        "label": "<string>",
        "dataSourceId": "00000000-0000-0000-0000-000000000000",
        "sourceCardURN": ""
      }
    ],
    "created": 1234567890000,
    "modified": 1234567890000,
    "filterGroupIds": [],
    "chartStates": [],
    "chartType": "badge_basic_table",
    "chartOverrides": [
      {
        "key": "row_filter",
        "value": "none"
      }
    ],
    "rowFilterOverride": "none",
    "filterGroups": [],
    "purpose": "REPORT",
    "dateRangeFilter": null,
    "overrideDateRange": true,
    "backgroundId": null,
    "fitToFrame": false,
    "darkMode": false,
    "segmentIds": [],
    "functionOverrides": {},
    "dataControlFilters": [],
    "overrideSlicers": true,
    "chartState": {
      "chartType": "badge_basic_table",
      "overrides": {
        "hide_series": "none",
        "series_filter": "none",
        "row_filter": "none",
        "range_filter_y": "none",
        "range_filter_x": "none",
        "range_filter_cat_x": "none",
        "range_filter_time": "none",
        "collapsed_filters": "none",
        "column_sort": "[{\"column\":\"Column 1\",\"sort\":\"asc\"}]"
      }
    }
  }
  ```

### Delete Scheduled Report
`DELETE {{instanceUrl}}/api/content/v1/reportschedules/:id`
- Path: `:id`

### Delete Unsubscribe (Resubscribe Signed In/Token User)
`DELETE {{instanceUrl}}/api/content/v1/reportschedules/:id/unsubscribe/recipient`
- Path: `:id`

### Unsubscribe (Signed In/Token User)
`POST {{instanceUrl}}/api/content/v1/reportschedules/:id/unsubscribe`
- Path: `:id`
