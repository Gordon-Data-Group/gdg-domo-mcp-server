# Toolkit

### List Applications
`GET {{instanceUrl}}/api/executor/v1/applications`

### Get Jobs
`GET {{instanceUrl}}/api/executor/v2/applications/:applicationId/jobs`
- Path: `:applicationId`
- Query: `limit`, `offset`

### Get Job
`GET {{instanceUrl}}/api/executor/v1/applications/:applicationId/jobs/:jobId`
- Path: `:applicationId`, `:jobId`

### Run Job
`POST {{instanceUrl}}/api/executor/v1/applications/:applicationId/jobs/:jobId/executions`
- Path: `:applicationId`, `:jobId`
- Body: `{}`

### Share/Unshare Job
`PUT {{instanceUrl}}/api/executor/v1/applications/:applicationId/jobs/:jobId/share`
- Path: `:applicationId`, `:jobId`
- Body: `{"ownerUserId":123456,"grantUserIds":[],"revokeUserIds":[],"grantGroupIds":[123456],"revokeGroupIds":[]}`

### Create Trigger
`POST {{instanceUrl}}/api/executor/v1/applications/:appId/jobs/:jobId/triggers`
- Path: `:appId`, `:jobId`
- Body: `{ "eventEntity": "00000000-0000-0000-0000-000000000000", //DataSet UUID "eventType": "datasetUpdated" }`

### Update Job
`PUT {{instanceUrl}}/api/executor/v1/applications/:appId/jobs/:jobId`
- Path: `:appId`, `:jobId`
- Body:
  ```json
  {
    "jobId": "00000000-0000-0000-0000-000000000000",
    "applicationId": "00000000-0000-0000-0000-000000000000",
    "customerId": "<string>",
    "jobName": "<string>",
    "jobDescription": "<string>",
    "userId": 123456,
    "executionTimeout": 1440,
    "jobStatus": "idle",
    "executionPayload": {},
    "executionResponse": {},
    "accounts": [
      123
    ],
    "executionClass": "com.domo.executor.dataset.DataSetSharingApplication",
    "created": 1735689600000,
    "updated": 1735689600000,
    "triggers": [],
    "compressPayload": false
  }
  ```

### Delete Job
`DELETE {{instanceUrl}}/api/executor/v1/applications/:appId/jobs/:jobId`
- Path: `:appId`, `:jobId`
