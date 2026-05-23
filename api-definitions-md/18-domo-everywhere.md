# Domo Everywhere

## Publications

### List Publications
`GET {{instanceUrl}}/api/publish/v2/publications`

### List Summaries
`GET {{instanceUrl}}/api/publish/v2/publications/summaries`
- Query: `public`, `limit`, `offset`, `searchTerm`, `sort`

### Get Publication
`GET {{instanceUrl}}/api/publish/v2/publications/:id`
- Path: `:id`

### Get Summary
`GET {{instanceUrl}}/api/publish/v2/publications/summaries/:publicationId`
- Path: `:publicationId`

### Get Status
`GET {{instanceUrl}}/api/publish/v2/publications/status`

## Subscriptions

### List Summaries
`GET {{instanceUrl}}/api/publish/v2/subscriptions/summaries`
- Query: `searchTerm`, `limit`, `offset`

### List Automatic Subscriptions
`GET {{instanceUrl}}/api/publish/v2/automatic-subscriptions`

### List Automatic Subscription Shares
`GET {{instanceUrl}}/api/publish/v2/automatic-subscriptions/shares/v1`

### List Invites
`GET {{instanceUrl}}/api/publish/v2/subscriptions/invites`
- Query: `searchTerm`, `limit`, `offset`

### Count Summaries
`GET {{instanceUrl}}/api/publish/v2/subscriptions/summaries/counts`
- Query: `searchTerm`

### Count Invites
`GET {{instanceUrl}}/api/publish/v2/subscriptions/invites/counts`
- Query: `searchTerm`

### Get Subscription Share
`GET {{instanceUrl}}/api/publish/v2/subscriptions/:subscriptionId/share`
- Path: `:subscriptionId`

### Update Subscription
`PUT {{instanceUrl}}/api/publish/v2/subscriptions/:subscriptionId`
- Path: `:subscriptionId`
- Body: `{"publicationId":"00000000-0000-0000-0000-000000000000","domain":"<string>","customerId":"<string>","userId":1234,"userIds":[2345,3456],"groupIds":[4567]}`
