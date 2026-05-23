# App Studio

### List Apps
`GET {{instanceUrl}}/api/content/v1/dataapps`
- Query: `parts`, `includeHiddenViews`, `authoring`

### List Apps (Admin Summary)
`POST {{instanceUrl}}/api/content/v1/dataapps/adminsummary`
- Query: `limit`, `skip`
- Body: `{"includeTitleClause":true,"includeOwnerClause":true,"orderBy":"title","ascending":false,"titleSearchText":""}`

### Get App
`GET {{instanceUrl}}/api/content/v1/dataapps/:appId`
- Path: `:appId`

### Get App (Admin Summary)
`GET {{instanceUrl}}/api/content/v1/dataapps/:appId/adminsummary`
- Path: `:appId`

### Get App Access
`GET {{instanceUrl}}/api/content/v1/dataapps/:appId/access`
- Path: `:appId`

### Share App
`POST {{instanceUrl}}/api/content/v1/dataapps/share`
- Query: `sendEmail`
- Body: `{"message":"I thought you might find this app interesting.","dataAppIds":["12345"],"recipients":[{"id":123456,"type":"user"}]}`

### Create App View (Page)
`POST {{instanceUrl}}/api/content/v1/dataapps/:appId/views`
- Path: `:appId`
- Body: `{"type":"dataappview","title":"<string>","hasLayout":true}`

### Bulk Add Owners
`PUT {{instanceUrl}}/api/content/v1/dataapps/bulk/owners`
- Body: `{"note":"","entityIds":["123456"],"owners":[{"type":"USER","id":1234}],"sendEmail":false}`

### Duplicate App
`PUT {{instanceUrl}}/api/content/v1/dataapps/:appId/duplicate`
- Path: `:appId`
- Body: `{"title":"string","duplicateCards":true,"beacon":0,"cardPrefix":"string","worksheetToApp":true}`

### Duplicate App Synchronously
`PUT {{instanceUrl}}/api/content/v1/dataapps/:appId/duplicate/synchronous`
- Path: `:appId`
- Body: `{"title":"string","duplicateCards":true,"beacon":0,"cardPrefix":"string","worksheetToApp":true}`

### Delete App
`DELETE {{instanceUrl}}/api/content/v1/dataapps/:appId`
- Path: `:appId`

### Delete App View (Page)
`DELETE {{instanceUrl}}/api/content/v1/dataapps/:appId/views/:viewId`
- Path: `:appId`, `:viewId`

### Bulk Remove Owners
`POST {{instanceUrl}}/api/content/v1/dataapps/bulk/owners/remove`
- Body: `{"entityIds":["123456"],"owners":[{"type":"USER","id":"1234","displayName":"<string>"}]}`
