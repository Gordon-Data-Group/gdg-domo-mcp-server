# Bricks and Pro-Code Apps

### List App Designs
`GET {{instanceUrl}}/api/apps/v1/designs`
- Query: `checkAdminAuthority`, `creator`, `deleted`, `order`, `direction`, `limit`, `offset`, `search`, `withPermission`, `parts`

### Get App
`GET {{instanceUrl}}/api/domoapps/apps/v2/:id`
- Path: `:id`

### Get App Design
`GET {{instanceUrl}}/api/apps/v1/designs/:id`
- Path: `:id`
- Query: `parts`

### Get App File
`GET {{instanceUrl}}/api/v1/designs/:designId/versions/:versionNumber/assets`
- Path: `:designId`, `:versionNumber`
- Query: `path`

### Get App Version
`GET {{instanceUrl}}/api/v1/designs/:designId/versions/:versionNumber`
- Path: `:designId`, `:versionNumber`

### Get App Context
`GET {{instanceUrl}}/api/domoapps/apps/v2/contexts/:contextId`
- Path: `:contextId`

### Count App Designs
`GET {{instanceUrl}}/api/apps/v1/designs/count`
- Query: `checkAdminAuthority`, `creator`, `deleted`, `search`, `withPermission`

### Create App Instance
`POST {{instanceUrl}}/api/apps/v1/instances`
- Query: `temporary`
- Body: `{"designId":"00000000-0000-0000-0000-000000000000","designVersion":"0.0.1","id":null}`

### Share App Design
`POST {{instanceUrl}}/api/apps/v1/designs/:id/permissions/:permissions`
- Path: `:id`, `:permissions`
- Body: `["1234","2345"]`

### Release App Design Version
`POST {{instanceUrl}}/api/domoapps/designs/:id/release`
- Path: `:id`
- Query: `version`

### Update App File
`POST {{instanceUrl}}/api/apps/v1/designs/:designId/versions/:versionNumber/assets`
- Path: `:designId`, `:versionNumber`
- Query: `path`
- Body: `{"id":"00000000-0000-0000-0000-000000000000","name":"<string>","version":"0.0.1","datasetsMapping":[],"size":{"width":1,"height":"2"}}`

### Update App Instance
`PUT {{instanceUrl}}/api/apps/v1/instances/:instanceId`
- Path: `:instanceId`
- Body:
  ```json
  {
    "id": "00000000-0000-0000-0000-000000000000",
    "designId": "00000000-0000-0000-0000-000000000000",
    "designVersion": "0.0.1",
    "datasetsMapping": null,
    "collectionsMapping": null,
    "databasesMapping": null,
    "accountsMapping": null,
    "actionsMapping": null,
    "workflowsMapping": null,
    "packagesMapping": null,
    "owner": "1234",
    "createdBy": "1234",
    "createdDate": "2025-01-01T12:00:00Z",
    "updatedBy": "1234",
    "updatedDate": "2025-01-01T12:00:00Z",
    "disabled": false
  }
  ```

### Update App Context
`PUT {{instanceUrl}}/api/domoapps/apps/v2/contexts/:id`
- Path: `:id`
- Body:
  ```json
  {
    "id": "00000000-0000-0000-0000-000000000000",
    "designId": "00000000-0000-0000-0000-000000000000",
    "designVersion": "0.0.1",
    "mapping": [],
    "collections": [],
    "accountMapping": [],
    "actionMapping": [],
    "workflowMapping": [],
    "packageMapping": [],
    "isDisabled": false
  }
  ```

### Delete App Design (/domoapps)
`DELETE {{instanceUrl}}/api/domoapps/designs/:id`
- Path: `:id`

### Delete App Design (/apps/v1)
`DELETE {{instanceUrl}}/api/apps/v1/designs/:designId`
- Path: `:designId`

### Delete App Instance
`DELETE {{instanceUrl}}/api/apps/v1/instances/:instanceId`
- Path: `:instanceId`

### Restore App Design
`PUT {{instanceUrl}}/api/apps/v1/designs/:designId/undelete`
- Path: `:designId`
