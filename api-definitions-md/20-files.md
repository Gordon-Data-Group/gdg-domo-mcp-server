# Files

### Get Revision
`GET {{instanceUrl}}/api/data/v1/data-files/:fileId/revisions/:revisionId`
- Path: `:fileId`, `:revisionId`
- Query: `fileName`

### Get Revision Details
`GET {{instanceUrl}}/api/data/v1/data-files/:fileId/revisions/:revisionId/details`
- Path: `:fileId`, `:revisionId`

### Get File Details
`GET {{instanceUrl}}/api/data/v1/data-files/:id/details`
- Path: `:id`
- Query: `expand`

### Create File
`POST {{instanceUrl}}/api/data/v1/data-files`
- Query: `name`, `public`

### Create File Card
`POST {{instanceUrl}}/api/content/v1/cards`
- Query: `pageId`
- Body: `{"type":"document","description":"<string>","metadata":{"title":"<string>","documentId":"123:123","usingSampleData":"","kpiType":"document","description":"<string>"}}`

### Update File
`PUT {{instanceUrl}}/api/data/v1/data-files/:id`
- Path: `:id`
- Query: `public`, `description`

### Update File Card
`PUT {{instanceUrl}}/api/content/v1/cards/:id`
- Path: `:id`
- Body: `{"metadata":{"documentId":"123:123","revisionId":"123","title":"<string>","kpiType":"document","usingSampleData":""}}`
