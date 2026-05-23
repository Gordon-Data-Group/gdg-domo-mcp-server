# Achievements

### List Achievements
`GET {{instanceUrl}}/api/content/v1/achievements/bulk`
- Query: `limit`, `offset`

### Get Achievement
`GET {{instanceUrl}}/api/content/v1/achievements/:id`
- Path: `:id`

### Get Achievement Admins
`GET {{instanceUrl}}/api/content/v1/achievements/:id/admins`
- Path: `:id`

### Create Achievement
`POST {{instanceUrl}}/api/content/v1/achievements`
- Body: `{"name":"<string>","description":"<string>","image":"<base64>","administrators":[{"userId":1234}]}`

### Create Achievement Admin
`POST {{instanceUrl}}/api/content/v1/achievements/:achievementId/admins`
- Path: `:achievementId`
- Body: `{"userId":1234}`

### Update Achievement
`PUT {{instanceUrl}}/api/content/v1/achievements/:id`
- Path: `:id`
- Body: `{"name":"<string>","description":"<string>","image":"<base64>"}`

### Delete Achievement
`DELETE {{instanceUrl}}/api/content/v1/achievements/:id`
- Path: `:id`

### Delete Achievement Admin
`DELETE {{instanceUrl}}/api/content/v1/achievements/:achievementId/admins/:adminId`
- Path: `:achievementId`, `:adminId`
