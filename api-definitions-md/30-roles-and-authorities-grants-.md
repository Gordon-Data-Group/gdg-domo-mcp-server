# Roles and Authorities (Grants)

### List Roles
`GET {{instanceUrl}}/api/authorization/v1/roles`

### List Authorities (Grants)
`GET {{instanceUrl}}/api/authorization/v1/authorities`

### Get Users for Authority (Grant)
`GET {{instanceUrl}}/api/content/v1/typeahead`
- Query: `authorities`, `limit`, `type`, `type`, `filter`, `fields`

### Get Role
`GET {{instanceUrl}}/api/authorization/v1/roles/:id`
- Path: `:id`

### Get Role Authorities (Grants)
`GET {{instanceUrl}}/api/authorization/v1/roles/:id/authorities`
- Path: `:id`
