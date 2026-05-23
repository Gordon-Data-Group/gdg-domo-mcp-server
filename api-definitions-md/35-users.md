# Users

### Search Users
`POST {{instanceUrl}}/api/identity/v1/users/search`
- Query: `explain`, `cacheBuster`
- Body:
  ```json
  {
    "cacheBuster": 1700000000000,
    "showCount": true,
    "count": false,
    "includeDeleted": true,
    "onlyDeleted": false,
    "includeSupport": true,
    "offset": 0,
    "limit": 100,
    "sort": {
      "field": "displayName",
      "order": "ASC"
    },
    "filters": [
      {
        "field": "reportsTo",
        "values": [
          "123456"
        ],
        "operator": "EQ",
        "filterType": "value"
      }
    ],
    "ids": [],
    "attributes": [
      "id",
      "displayName",
      "department",
      "userName",
      "emailAddress",
      "phoneNumber",
      "deskPhoneNumber",
      "title",
      "timeZone",
      "hireDate",
      "created",
      "modified",
      "alternateEmail",
      "employeeLocation",
      "employeeNumber",
      "employeeId",
      "locale",
      "reportsTo",
      "isAnonymous",
      "isSystemUser",
      "isPending",
      "isActive",
      "invitorUserId",
      "lastActivity",
      "lastLogin",
      "avatarKey"
    ],
    "parts": [
      "DETAILED",
      "GROUPS",
      "ROLE",
      "MINIMAL"
    ]
  }
  ```

### List Users (/identity/v1)
`GET {{instanceUrl}}/api/identity/v1/users/`
- Query: `limit`, `offset`, `attributes`

### List Users (/content/v3)
`GET {{instanceUrl}}/api/content/v3/users/`
- Query: `limit`, `offset`, `active`

### Get Users
`GET {{instanceUrl}}/api/users/index`
- Query: `cvUserIds`

### Get User (/identity/v1)
`GET {{instanceUrl}}/api/identity/v1/users/:id`
- Path: `:id`
- Query: `attributes`, `parts`

### Get User (/content/v2)
`GET {{instanceUrl}}/api/content/v2/users/:id`
- Path: `:id`

### Get User (/content/v3)
`GET {{instanceUrl}}/api/content/v3/users/:id`
- Path: `:id`

### Get User Locations
`GET {{instanceUrl}}/api/content/v2/users/attributeTypeahead/EMPLOYEELOCATION`
- Query: `limit`, `offset`, `search`

### Two Factor Enabled
`GET {{instanceUrl}}/api/content/v2/users/:id/state`
- Path: `:id`
- Query: `keys`

### Create User
`POST {{instanceUrl}}/api/content/v3/users`
- Query: `sendInvite`
- Body: `{"displayName":"<string>","roleId":123456,"detail":{"email":"test@domain.tld"}}`

### Update User (/identity/v1)
`PATCH {{instanceUrl}}/api/identity/v1/users/:id`
- Path: `:id`
- Body: `{"attributes":[{"key":"emailAddress","values":["test@domain.tld"]}]}`

### Update User (/content/v3)
`PUT {{instanceUrl}}/api/content/v3/users`
- Body:
  ```json
  {
    "id": 1234,
    "invitorUserId": 2345,
    "displayName": "string",
    "avatarKey": "string",
    "role": "Anonymous",
    "roleId": 1,
    "detail": {
      "title": "string",
      "email": "string",
      "alternateEmail": "string",
      "phoneNumber": "string",
      "deskPhoneNumber": "string",
      "employeeNumber": 0,
      "pending": true,
      "location": "string",
      "timeZone": "string",
      "locale": "string",
      "active": true,
      "created": 1735689600000,
      "modified": 1735689600000,
      "department": "string",
      "employeeId": "string",
      "hireDate": "string",
      "subjectId": "string"
    },
    "trial": {
      "role": "Anonymous",
      "roleId": 1,
      "started": "2025-09-16T21:36:38.994Z",
      "end": "2025-09-16T21:36:38.994Z",
      "inTrial": true,
      "hasTrialed": true,
      "prevRole": "Anonymous",
      "requested": "2025-09-16T21:36:38.994Z",
      "accepted": true,
      "sessionToken": "string"
    },
    "socialDetail": {
      "facebookProfile": "string",
      "instagramProfile": "string",
      "twitterProfile": "string",
      "linkedinProfile": "string"
    },
    "groups": [
      {
        "id": 0,
        "name": "string",
        "type": "unknown",
        "userIds": [
          0
        ],
        "users": [
          {
            "id": 0,
            "invitorUserId": 0,
            "reportsTo": "2345",
            "displayName": "string",
            "department": "string",
            "userName": "string",
            "emailAddress": "string",
            "phoneNumber": "string",
            "deskPhoneNumber": "string",
            "imageThumb": "string",
            "imageFull": "string",
            "imageMicro": "string",
            "imageOriginal": "string",
            "image600": "string",
            "avatarKey": "string",
            "accepted": true,
            "userType": "USER",
            "title": "string",
            "timeZone": "string",
            "locale": "string",
            "hireDate": 0,
            "lastLogin": 0,
            "modified": 0,
            "created": 0,
            "role": "string",
            "roleId": 0,
            "simplifiedPhoneNumber": 0,
            "simplifiedDeskPhoneNumber": 0,
            "alternateEmail": "string",
            "employeeLocation": "string",
            "employeeNumber": "string",
            "employeeId": "string",
            "subjectId": "string",
            "lastActive": 0,
            "groups": [
              0
            ],
            "systemUser": true,
            "pending": true,
            "anonymous": true,
            "userTypeId": 0,
            "active": true
          }
        ],
        "ldapName": "string",
        "creatorId": 0,
        "created": "2025-09-16T21:36:38.995Z",
        "modified": "2025-09-16T21:36:38.995Z",
        "memberCount": 0,
        "avatar": "string",
        "guid": "string",
        "description": "string",
        "dynamicDefinition": {
          "expression": {
            "operator": "OR",
            "operands": [
              {
                "key": "string",
                "value": "string"
              }
            ],
            "expressions": [
              "string"
            ]
          }
        },
        "transactionId": "string",
        "hidden": true,
        "default": true,
        "active": true
      }
    ]
  }
  ```

### Bulk Update Users
`PUT {{instanceUrl}}/api/content/v2/users/bulk`
- Body:
  ```json
  {
    "transactionId": "00000000-0000-0000-0000-000000000000",
    "users": [
      {
        "id": "123456",
        "displayName": "<string>",
        "emailAddress": "test@domain.tld",
        "title": "<string>",
        "phoneNumber": "1234567890",
        "employeeLocation": "<string>",
        "timeZone": "UTC",
        "employeeNumber": "123",
        "employeeId": "123",
        "department": "<string>",
        "hireDate": 1700000000,
        "reportsTo": "123456"
      }
    ]
  }
  ```

### Update Profile Pictures
`POST {{instanceUrl}}/api/content/v1/avatar/bulk`
- Body: `{"isOpen":false,"transactionId":"00000000-0000-0000-0000-000000000000","entityIds":["123456"],"entityType":"USER","base64Image":"data:image/jpeg;base64,<base64>"}`

### Update Landing Page
`PUT {{instanceUrl}}/api/content/v1/landings/target/:type/entity/PAGE/id/:pageId/:userId`
- Path: `:type`, `:pageId`, `:userId`

### Delete User
`DELETE {{instanceUrl}}/api/identity/v1/users/:id`
- Path: `:id`
