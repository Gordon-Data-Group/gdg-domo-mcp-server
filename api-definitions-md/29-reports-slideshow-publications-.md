# Reports (Slideshow Publications)

### List Reports
`GET {{instanceUrl}}/api/content/v1/reports`

### Create Reports
`POST {{instanceUrl}}/api/content/v1/reports`
- Body: `{"title":"<string>","type":"slideshow","properties":{"isShared":false,"tokenId":null,"isAccessCodeRequired":false,"accessCode":null},"cardIds":["1234","2345"]}`

### Update Reports
`PUT {{instanceUrl}}/api/content/v1/reports/:id`
- Path: `:id`
- Body:
  ```json
  {
    "id": 1234,
    "ownerId": 1234,
    "title": "<string>",
    "created": null,
    "updated": null,
    "subject": null,
    "schedule": null,
    "properties": {
      "isShared": false,
      "tokenId": null,
      "isAccessCodeRequired": false,
      "accessCode": null
    },
    "cardIds": [
      1234,
      "2345"
    ]
  }
  ```

### Delete Reports
`DELETE {{instanceUrl}}/api/content/v1/reports/:id`
- Path: `:id`
