# AppDB

### Search Collections
`POST {{instanceUrl}}/api/datastores/v1/collections/query`
- Body:
  ```json
  {
    "collectionFilteringList": [
      {
        "filterType": "nameof",
        "typedValue": "%%"
      },
      {
        "filterType": "owendby",
        "typedValue": "1234",
        "comparingCriteria": "equals"
      }
    ],
    "sortBy": "createdOn",
    "direction": "desc",
    "pageSize": 100,
    "pageNumber": 1
  }
  ```

### Query Collection Documents
`POST {{instanceUrl}}/api/datastores/v2/collections/:id/documents/query`
- Path: `:id`
- Query: `limit`, `offset`, `count`, `avg`, `sum`, `max`, `min`, `orderby`, `groupby`
- Body: `{"$or":[{"content.comments":{"$regex":"happy"}},{"content.username":{"$ne":"Eeyore"}}]}`

### List Datastores
`GET {{instanceUrl}}/api/datastores/v1`

### List Collections
`GET {{instanceUrl}}/api/datastores/v1/collections`

### Get Datastore
`GET {{instanceUrl}}/api/datastores/v1/:id`
- Path: `:id`

### Get Datastore Collections
`GET {{instanceUrl}}/api/datastores/v1/:id/collections`
- Path: `:id`

### Get Collection
`GET {{instanceUrl}}/api/datastores/v1/collections/:id`
- Path: `:id`

### Get Collection Documents
`GET {{instanceUrl}}/api/datastores/v1/collections/:collectionId/documents`
- Path: `:collectionId`

### Get Collection Permissions
`GET {{instanceUrl}}/api/datastores/v1/collections/:id/permission`
- Path: `:id`

### Get Datastore Cards
`POST {{instanceUrl}}/api/domoapps/apps/v2/card`
- Body: `["00000000-0000-0000-0000-000000000000"]`

### Create Datastore
`POST {{instanceUrl}}/api/datastores/v1`
- Body: `{"name":"<string>"}`

### Create Collection in Datastore
`POST {{instanceUrl}}/api/datastores/v1/:datastoreId/collections/`
- Path: `:datastoreId`
- Body: `{"name":"<string>","schema":{"columns":[{"name":"Column 1","type":"STRING"},{"name":"Column 2","type":"STRING"}]},"syncEnabled":true}`

### Create Collection and Datastore
`POST {{instanceUrl}}/api/datastores/v1/collections`
- Body: `{"name":"<string>","schema":{"columns":[{"name":"Column 1","type":"STRING"},{"name":"Column 2","type":"STRING"}]},"syncEnabled":true}`

### Create Document
`POST {{instanceUrl}}/api/datastores/v1/collections/:collectionId/documents`
- Path: `:collectionId`
- Body: `{"content":{"column1":"<string>","column2":"<timestamp>"}}`

### Create Documents
`POST {{instanceUrl}}/api/datastores/v1/collections/:collectionId/documents/bulk`
- Path: `:collectionId`
- Body: `[{"content":{"column1":"<string>","column2":"<timestamp>"}},{"content":{"column1":"<string>","column2":"<timestamp>"}}]`

### Disable Sync to DataSet
`PUT {{instanceUrl}}/api/datastores/v1/collections/:id`
- Path: `:id`
- Body: `{"id":"00000000-0000-0000-0000-000000000000","syncEnabled":false}`

### Update Collection
`PUT {{instanceUrl}}/api/datastores/v1/collections/:id`
- Path: `:id`
- Body: `{"id":"00000000-0000-0000-0000-000000000000","owner":1234,"schema":{"columns":[{"name":"Column 1","type":"STRING"}]}}`

### Update Collection Permissions
`PUT {{instanceUrl}}/api/datastores/v1/collections/:collectionId/permission/:entityType/:entityId`
- Path: `:collectionId`, `:entityType`, `:entityId`
- Query: `overwrite`, `permissions`

### Update Document
`PUT {{instanceUrl}}/api/datastores/v2/collections/:collectionId/documents/:documentId`
- Path: `:collectionId`, `:documentId`
- Body: `{"content":{"column1":"<string>","column2":"<timestamp>"}}`

### Upsert Documents
`PUT {{instanceUrl}}/api/datastores/v2/collections/:collectionId/documents/bulk`
- Path: `:collectionId`
- Body:
  ```json
  [
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "content": {
          "column1": "<string>",
          "column2": "<timestamp>"
      }
    },
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "content": {
          "column1": "<string>",
          "column2": "<timestamp>"
      }
    },
    {
      //documents with a missing id or without a matching id will be created
      "content": {
          "column1": "<string>",
          "column2": "<timestamp>"
      }
    }
  ]
  ```

### Delete Datastore
`DELETE {{instanceUrl}}/api/datastores/v1/:id`
- Path: `:id`

### Delete Collection
`DELETE {{instanceUrl}}/api/datastores/v1/collections/:id`
- Path: `:id`

### Remove Collection Access
`DELETE {{instanceUrl}}/api/datastores/v1/collections/:collectionId/permission/:entityType/:entityId`
- Path: `:collectionId`, `:entityType`, `:entityId`

### Delete Document
`DELETE {{instanceUrl}}/api/datastores/v2/collections/:collectionId/documents/:documentId`
- Path: `:collectionId`, `:documentId`

### Delete Documents
`DELETE {{instanceUrl}}/api/datastores/v2/collections/:collectionId/documents/bulk`
- Path: `:collectionId`
- Query: `ids`
