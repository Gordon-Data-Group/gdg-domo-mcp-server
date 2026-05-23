# Groups

### List Groups
`GET {{instanceUrl}}/api/content/v2/groups/grouplist`
- Query: `ascending`, `sort`, `limit`, `offset`, `includeFullMembership`, `owner`, `ownerType`, `groupType`, `createdAfter`, `createdBefore`, `members`, `isManageable`, `search`

### Get Groups
`POST {{instanceUrl}}/api/content/v2/groups/get`
- Query: `includeActive`, `includeUsers`
- Body: `["1234","2345"]`

### Get Group
`GET {{instanceUrl}}/api/content/v2/groups/:id`
- Path: `:id`

### Get Permissions
`GET {{instanceUrl}}/api/content/v2/groups/:id/permissions`
- Path: `:id`
- Query: `checkOwnership`, `includeUsers`

### Get Avatar
`GET {{instanceUrl}}/api/content/v1/avatar/GROUP/:id`
- Path: `:id`
- Query: `size`, `defaultBackground`, `defaultForeground`, `defaultText`

### Create Group
`POST {{instanceUrl}}/api/content/v2/groups`
- Body: `{"name":"<string>","type":"dynamic","description":""}`

### Add or Remove Owners
`PUT {{instanceUrl}}/api/content/v2/groups/access`
- Body: `[ { "groupId": 123456, "addOwners": [ { "type": "GROUP", //USER or GROUP "id": "123456" } ], "removeOwners": [ { "type": "USER", //USER or GROUP "id": "123456" } ] } ]`

### Add Members to Group
`PUT {{instanceUrl}}/api/content/v2/groups/access`
- Body: `[{"groupId":252073910,"addMembers":[{"type":"USER","id":"901072511"}]}]`

### Update Dynamic Group Rules
`PUT {{instanceUrl}}/api/content/v2/groups`
- Body:
  ```json
  [
    {
      "groupId": 123456,
      "dynamicDefinition": {
        "expression": {
          "operator": "OR",
          "expressions": [
            {
              "operator": "OR",
              "operands": [],
              "expressions": [
                {
                  "operator": "OR",
                  "operands": [
                    {
                      "key": "DEPARTMENT",
                      "value": "<string>"
                    },
                    {
                      "key": "DEPARTMENT",
                      "value": "<string>"
                    }
                  ],
                  "expressions": []
                },
                {
                  "operator": "OR",
                  "operands": [
                    {
                      "key": "EMPLOYEE_ID",
                      "value": "10"
                    }
                  ],
                  "expressions": []
                }
              ]
            },
            {
              "operator": "OR",
              "operands": [],
              "expressions": [
                {
                  "operator": "OR",
                  "operands": [
                    {
                      "key": "LOCATION",
                      "value": "<string>"
                    }
                  ],
                  "expressions": []
                }
              ]
            }
          ]
        }
      }
    }
  ]
  ```

### Delete Group
`DELETE {{instanceUrl}}/api/content/v2/groups/:id`
- Path: `:id`

### Bulk Delete Groups
`DELETE {{instanceUrl}}/api/content/v2/groups`
- Body: `[1234,2345]`
