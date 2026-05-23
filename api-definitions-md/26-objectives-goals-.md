# Objectives (Goals)

### List Objectives
`GET {{instanceUrl}}/api/social/v1/objectives/search`
- Query: `filterKeyResults`, `periodId`, `query`

### List Personal Objectives
`GET {{instanceUrl}}/api/social/v2/objectives/profile`
- Query: `filterKeyResults`, `includeSampleGoal`, `ownerId`, `periodId`, `type`

### List Team Objectives
`GET {{instanceUrl}}/api/social/v2/objectives/teams-profile`
- Query: `filterKeyResults`, `ownerId`, `periodId`

### List Periods
`GET {{instanceUrl}}/api/social/v1/objectives/periods`
- Query: `all`

### List Events
`GET {{instanceUrl}}/api/social/v1/objectives/events`

### List Tags
`GET {{instanceUrl}}/api/social/v1/objectives/tags`
- Query: `all`

### List Categories
`GET {{instanceUrl}}/api/social/v1/objectives/tags/categories`
- Query: `all`

### List Objectives to Update
`GET {{instanceUrl}}/api/social/v1/objectives/needs-update`
- Query: `filterKeyResults`, `periodId`, `userId`

### List Objective Drafts
`GET {{instanceUrl}}/api/social/v2/objectives/draft`
- Query: `filterKeyResults`, `periodId`, `userId`

### Get Company Objectives Report
`GET {{instanceUrl}}/api/social/v2/objectives/report`
- Query: `filterKeyResults`, `periodId`, `type`

### Get Key Result Chart
`GET {{instanceUrl}}/api/social/v1/objectives/key-results/:id/chart`
- Path: `:id`

### Get Key Result Values
`GET {{instanceUrl}}/api/social/v1/objectives/key-results/:id/values`
- Path: `:id`

### Create Objective
`POST {{instanceUrl}}/api/social/v1/objectives`
- Body:
  ```json
  {
    "name": "<string>",
    "description": "<string>",
    "startsAt": "2025-01-01T12:00:00",
    "expiresAt": "2025-01-01T12:00:00",
    "status": "GOOD",
    "ownerId": null,
    "owners": [
      {
        "ownerId": 12345,
        "ownerType": "USER",
        "primary": true
      }
    ],
    "assignees": [],
    "periodId": 2,
    "parentId": null,
    "keyResults": [
      {
        "state": "OPEN",
        "ownerId": 12345,
        "ownerType": "USER",
        "owners": [
          {
            "ownerId": 12345,
            "ownerType": "USER",
            "primary": true
          }
        ],
        "alertId": 123,
        "resourceId": "12345",
        "resourceType": "CARD",
        "name": "<string>",
        "description": "<string>",
        "dataAchievementScore": 0.0,
        "measurement": "",
        "startValue": 1,
        "currentValue": 1,
        "targetValue": 1,
        "status": "POOR",
        "colorValue": "#F34847",
        "operator": "GREATER_THAN_EQUALS_TO",
        "likes": [],
        "dislikes": [],
        "relatedResources": [],
        "tags": [],
        "writeAccess": true,
        "fixedWeight": false,
        "targets": [],
        "startsAt": "2025-01-01T12:00:00",
        "expiresAt": "2025-01-01T12:00:00",
        "curePeriod": "2025-01-01T12:00:00",
        "draft": false,
        "assigned": false
      }
    ],
    "tags": [],
    "writeAccess": true,
    "type": "PERSONAL"
  }
  ```

### Create Key Result
`POST {{instanceUrl}}/api/social/v1/objectives/key-results`
- Body:
  ```json
  {
    "keyResult": {
      "state": "OPEN",
      "ownerId": 12345,
      "ownerType": "USER",
      "owners": [
        {
          "ownerId": 12345,
          "ownerType": "USER",
          "primary": true
        }
      ],
      "alertId": 213,
      "resourceId": "12345",
      "resourceType": "CARD",
      "name": "<string>",
      "description": "<string>",
      "dataAchievementScore": 0.0,
      "measurement": "",
      "startValue": 1,
      "currentValue": 1,
      "targetValue": 1,
      "status": "POOR",
      "colorValue": "#F34847",
      "operator": "GREATER_THAN_EQUALS_TO",
      "likes": [],
      "dislikes": [],
      "relatedResources": [],
      "tags": [],
      "writeAccess": true,
      "fixedWeight": false,
      "targets": [],
      "startsAt": "2025-01-01T12:00:00",
      "expiresAt": "2025-01-01T12:00:00",
      "curePeriod": "2025-01-01T12:00:00",
      "draft": false,
      "assigned": false
    }
  }
  ```

### Create Tag
`POST {{instanceUrl}}/api/social/v1/objectives/tags`
- Body: `{"name":"<string>","category":{"id":1,"name":"<string>"}}`

### Create Category
`POST {{instanceUrl}}/api/social/v1/objectives/tags/categories`
- Body: `{"name":"<string>"}`

### Update Objective
`PUT {{instanceUrl}}/api/social/v1/objectives/:id`
- Path: `:id`
- Query: `periodId`
- Body:
  ```json
  {
    "id": 123,
    "name": "<string>",
    "type": "PERSONAL",
    "description": "<string>",
    "startsAt": "2025-01-01T12:00:00",
    "expiresAt": "2025-01-01T12:00:00",
    "status": "NOT_STARTED",
    "ownerId": 12345,
    "ownerType": "USER",
    "owners": [
      {
        "ownerId": 12345,
        "ownerType": "USER",
        "primary": true
      }
    ],
    "assignees": [],
    "periodId": 2,
    "periodIds": [
      2
    ],
    "state": "OPEN",
    "parentIds": [],
    "parents": [],
    "keyResults": [],
    "childCount": 0,
    "autoScore": 0,
    "overrideAchievementScore": 1,
    "colorValue": "#B3B3B3",
    "useAutoScore": false,
    "childIds": [],
    "children": [],
    "likes": [],
    "dislikes": [],
    "subscriptions": [],
    "tags": [],
    "writeAccess": true,
    "company": false,
    "draft": false,
    "sample": false,
    "assigned": false,
    "assignee": false
  }
  ```

### Update Key Result
`PUT {{instanceUrl}}/api/social/v1/objectives/key-results/:id`
- Path: `:id`
- Body:
  ```json
  {
    "id": 5,
    "objectiveId": 5,
    "state": "OPEN",
    "ownerId": 12345,
    "ownerType": "USER",
    "owners": [
      {
        "ownerId": 12345,
        "ownerType": "USER",
        "primary": true
      }
    ],
    "alertId": null,
    "alert": null,
    "resourceId": null,
    "resourceType": null,
    "name": "<string>",
    "description": "",
    "dataAchievementScore": 0,
    "measurement": "t",
    "startValue": 0,
    "currentValue": 0,
    "targetValue": 2,
    "status": "POOR",
    "colorValue": "#F34847",
    "manualType": "VALUE",
    "unitType": "NUMERICAL",
    "operator": "EQUALS",
    "likes": [],
    "dislikes": [],
    "relatedResources": [],
    "tags": [
      {
        "id": 1,
        "name": "<string>",
        "category": null
      }
    ],
    "writeAccess": true,
    "fixedWeight": false,
    "targets": [],
    "startsAt": "2025-01-01T12:00:00",
    "expiresAt": "2025-01-01T12:00:00",
    "curePeriod": "2025-01-01T12:00:00",
    "draft": false,
    "assigned": false,
    "targetUpperValue": null
  }
  ```

### Update Key Result Tags
`PUT {{instanceUrl}}/api/social/v1/objectives/key-results/:id/tags`
- Path: `:id`
- Query: `periodId`
- Body: `[1]`

### Update Tag
`PUT {{instanceUrl}}/api/social/v1/objectives/tags/:id`
- Path: `:id`
- Body: `{"id":2,"name":"<string>","category":{"id":1,"name":"<string>"}}`

### Update Category
`PUT {{instanceUrl}}/api/social/v1/objectives/tags/categories/:id`
- Path: `:id`
- Body: `{"id":1,"name":"<string>"}`

### Delete Objective
`DELETE {{instanceUrl}}/api/social/v1/objectives/:id`
- Path: `:id`

### Delete Key Result
`DELETE {{instanceUrl}}/api/social/v1/objectives/key-results/:id`
- Path: `:id`

### Delete Tag
`DELETE {{instanceUrl}}/api/social/v1/objectives/tags/:id`
- Path: `:id`

### Delete Category
`DELETE {{instanceUrl}}/api/social/v1/objectives/tags/categories/:id`
- Path: `:id`
