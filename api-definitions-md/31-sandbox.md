# Sandbox

### List Repositories
`POST {{instanceUrl}}/api/version/v1/repositories/search`
- Body: `{"query":{"offset":0,"limit":50,"fieldSearchMap":{},"sort":"started","order":"desc","filters":{"userId":null},"dateFilters":{}},"shared":true}`

### List Promotion History
`POST {{instanceUrl}}/api/version/v1/promotions/search`
- Body:
  ```json
  {
    "offset": 0,
    "limit": 500,
    "filters": {
      "repositoryName": [
        "Sandbox Testing Link"
      ],
      "commitName": [],
      "status": [],
      "userId": []
    },
    "fieldSearchMap": {},
    "sort": "completed",
    "order": "desc",
    "searchDistinct": false,
    "dateFilters": {}
  }
  ```

### List Commit History
`POST {{instanceUrl}}/api/version/v1/commitRequests/search`
- Body: `{"offset":0,"limit":500,"filters":{"repositoryName":[],"commitName":[],"status":[]},"fieldSearchMap":{},"sort":"completed","order":"desc","searchDistinct":false,"dateFilters":{}}`

### List Instances
`GET {{instanceUrl}}/api/version/v1/authorizations`
- Query: `limit`

### Get Repository
`GET {{instanceUrl}}/api/version/v1/repositories/:repositoryId`
- Path: `:repositoryId`

### Get Repository Commits
`GET {{instanceUrl}}/api/version/v1/repositories/:repositoryId/commits`
- Path: `:repositoryId`

### Get Repository Commit Requests
`GET {{instanceUrl}}/api/version/v1/repositories/:repositoryId/commitRequests`
- Path: `:repositoryId`

### Get User/Group Permissions
`GET {{instanceUrl}}/api/version/v1/repositories/:repositoryId/permissions`
- Path: `:repositoryId`

### Get Instance Access
`GET {{instanceUrl}}/api/version/v1/repositories/:repositoryId/access`
- Path: `:repositoryId`

### Get Sandbox Settings
`GET {{instanceUrl}}/api/version/v1/settings`

### Promote and Link
`POST {{instanceUrl}}/api/version/v1/repositories/:repositoryId/deployments/:deploymentId/promoteAndSeed`
- Path: `:repositoryId`, `:deploymentId`
- Body:
  ```json
  {
    "commitId": "00000000-0000-0000-0000-000000000000",
    "mapping": [
      {
        "mappingId": "00000000-0000-0000-0000-000000000000",
        "deployObjectId": "00000000-0000-0000-0000-000000000000",
        "repositoryObjectId": "00000000-0000-0000-0000-000000000000",
        "contentType": "DATASET",
        "link": false
      }
    ],
    "pusherEventId": "00000000-0000-0000-0000-000000000000",
    "approvalId": "",
    "seedingRepoName": "<string>"
  }
  ```

### Create Commit
`POST {{instanceUrl}}/api/version/v1/repositories/:repositoryId/commitRequests`
- Path: `:repositoryId`
- Body: `{"summary":"<string>","hidden":false,"pusherEventId":"00000000-0000-0000-0000-000000000000"}`

### Update Respoitory User/Group Permissions
`POST {{instanceUrl}}/api/version/v1/repositories/:repositoryId/permissions`
- Path: `:repositoryId`
- Body: `{"repositoryPermissionUpdates":[{"userId":"1813188617","groupId":"","permission":"NONE"}]}`

### Update Repository Instance Access
`POST {{instanceUrl}}/api/version/v1/repositories:repositoryId/access`
- Body: `["sub1.domain1.tld","sub2.domain1.tld","sub1.domain2.tld"]`

### Update Instance Alias
`POST {{instanceUrl}}/api/version/v1/authorizations/aliases`
- Body: `{"aliasedDomain":"test.domo.com","alias":"test"}`
