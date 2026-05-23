# FileSets

### List/Search FileSets
`POST {{instanceUrl}}/api/files/v1/filesets/search`
- Query: `limit`, `offset`
- Body:
  ```json
  {
    "fieldSort": [
      {
        "field": "updated",
        "order": "DESC"
      }
    ],
    "filters": [
      {
        "field": "owner",
        "value": [
          "1234"
        ],
        "not": false,
        "operator": "EQUALS"
      },
      {
        "field": "name",
        "value": [
          ""
        ],
        "not": false,
        "operator": "LIKE"
      }
    ],
    "dateFilters": []
  }
  ```

### Get/Search Files
`POST {{instanceUrl}}/api/files/v1/filesets/:filesetId/files/search`
- Path: `:filesetId`
- Query: `directoryPath`, `immediateChildren`, `limit`, `next`
- Body: `{"fieldSort":[{"field":"created","order":"DESC"}],"filters":[],"dateFilters":[]}`

### Search Files with AI
`POST {{instanceUrl}}/api/files/v1/filesets/:id/query`
- Path: `:id`
- Body: `{"query":"","directoryPath":"","topK":10}`

### Get FileSet
`GET {{instanceUrl}}/api/files/v1/filesets/:id`
- Path: `:id`

### Get File
`GET {{instanceUrl}}/api/files/v1/filesets/:filesetId/files/:fileId`
- Path: `:filesetId`, `:fileId`

### Get File by Path
`GET {{instanceUrl}}/api/files/v1/filesets/:filesetId/path`
- Path: `:filesetId`
- Query: `path`

### Get FileSet Access
`GET {{instanceUrl}}/api/files/v1/filesets/:id/access`
- Path: `:id`

### Get FileSet Stats
`GET {{instanceUrl}}/api/files/v1/filesets/:id/stats`
- Path: `:id`

### Download File
`GET {{instanceUrl}}/api/files/v1/filesets/:filesetId/files/:fileId/download`
- Path: `:filesetId`, `:fileId`

### Download File by Path
`GET {{instanceUrl}}/api/files/v1/filesets/:filesetId/path/download`
- Path: `:filesetId`
- Query: `path`

### Create FileSet
`POST {{instanceUrl}}/api/files/v1/filesets`
- Body: `{"name":"<string>","description":"<string>","aiEnabled":false,"batchType":"INCREMENTAL","connector":"DOMO","accountId":null}`

### Create Folder
`POST {{instanceUrl}}/api/files/v1/filesets/:filesetId/files`
- Path: `:filesetId`
- Body: `{"directoryPath":"<string>"}`

### Upload File
`POST {{instanceUrl}}/api/files/v1/filesets/:id/files`
- Path: `:id`

### Update FileSet
`POST {{instanceUrl}}/api/files/v1/filesets/:id`
- Path: `:id`
- Body: `{"name":"<string>","description":"<string>","aiEnabled":true}`

### Update FileSet Access
`POST {{instanceUrl}}/api/files/v1/filesets/:id/access`
- Path: `:id`
- Body: `{"fileSetAccess":[{"entityId":1234,"entityType":"USER","permission":"READ"}]}`

### Update FileSet Owner
`POST {{instanceUrl}}/api/files/v1/filesets/:id/ownership`
- Path: `:id`
- Body: `{"userId":1234}`

### Delete FileSet
`DELETE {{instanceUrl}}/api/files/v1/filesets/:id`
- Path: `:id`

### Delete File
`DELETE {{instanceUrl}}/api/files/v1/filesets/:filesetId/files/:fileId`
- Path: `:filesetId`, `:fileId`

### Delete File by Path
`DELETE {{instanceUrl}}/api/files/v1/filesets/:filesetId/path`
- Path: `:filesetId`
- Query: `path`
