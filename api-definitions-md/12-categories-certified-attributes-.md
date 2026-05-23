# Categories (Certified Attributes)

### List Categories
`GET {{instanceUrl}}/api/entity/v1/properties/category`

### List Usage
`GET {{instanceUrl}}/api/entity/v1/properties/category/usage`

### Get Entity Categories
`GET {{instanceUrl}}/api/entity/v1/properties/entity/:type/:id`
- Path: `:type`, `:id`

### Create Category
`POST {{instanceUrl}}/api/entity/v1/properties/category`
- Body: `{"key":"<string>","description":"<string>","values":["<string>"]}`

### Upsert Entity Categories
`PUT {{instanceUrl}}/api/entity/v1/properties/entity/:type/:id`
- Path: `:type`, `:id`
- Body: `[{"key":"<string>","values":["<string>"]}]`
