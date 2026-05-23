# Pages (Dashboards)

### List Pages (Admin Summary)
`POST {{instanceUrl}}/api/content/v1/pages/adminsummary`
- Query: `limit`, `skip`
- Body:
  ```json
  {
    "includePageTitleClause": true,
    "orderBy": "createdTime",
    "pageTitleSearchText": "",
    "addPageWithNoOwner": true,
    "ascending": true,
    "includeAllPages": false,
    "includeCardCountClause": false,
    "includeDetails": false,
    "includeLastModifiedDateClause": true,
    "lastModifiedDateOperand": "BETWEEN",
    "lastModifiedStartDate": "2025-01-01",
    "lastModifiedEndDate": "2025-01-02",
    "includePermissionsList": true,
    "referenceId": "1066310937",
    "referenceType": "GROUP"
  }
  ```

### Get Page
`GET {{instanceUrl}}/api/content/v3/stacks/:id`
- Path: `:id`
- Query: `parts`, `includeV4PageLayouts`, `stackLoadContextId`, `stackLoadContext`, `stackLoadTrigger`

### Get Page with Cards
`GET {{instanceUrl}}/api/content/v3/stacks/:id/cards`
- Path: `:id`
- Query: `parts`, `includeV4PageLayouts`, `stackLoadContextId`, `stackLoadContext`, `stackLoadTrigger`

### Get Access
`GET {{instanceUrl}}/api/content/v1/share/accesslist/page/:id`
- Path: `:id`
- Query: `filter`, `limit`, `expandUsers`

### Get Navigation Page Order (Individual User)
`GET {{instanceUrl}}/api/content/v2/pages/navigation`
- Query: `includeStartPage`, `elevateSharedPage`, `includeHidden`

### Create Page
`POST {{instanceUrl}}/api/content/v1/pages`
- Body: `{"parentPageId":0,"title":"<string>"}`

### Share Access
`POST {{instanceUrl}}/api/content/v1/share`
- Query: `sendEmail`
- Body:
  ```json
  {
      "resources": [
          {
              "type": "page",
              "id": "121730951"
          }
      ],
      "recipients": [
          {
              "type": "", //user or group. Must be lowercase.
              "id": "1074337521"
          }
      ],
      "message": "I thought you might find this interesting."
  }
  ```

### Move Pages
`PUT {{instanceUrl}}/api/content/v1/pages/bulk/move`
- Body: `{ "parentPageId": 1602735973, //remove to make top level page "pageIds": [ 1337839338 ], "pagePermission": "ORIGINAL" }`

### Reorder Pages (Individual User)
`PUT {{instanceUrl}}/api/content/v1/pages/pageorder`
- Body: `{ "pageOrderMap": { //Use object key 0 for top level pages. Use a page ID as the key to order its subpages "0": "<page_id>, <page_id>" } }`

### Update Page
`PUT {{instanceUrl}}/api/content/v1/pages/:id`
- Path: `:id`
- Body: `{"title":"<string>","locked":true}`

### Duplicate Page
`PUT {{instanceUrl}}/api/content/v1/pages/:pageId/duplicate`
- Path: `:pageId`
- Query: `doNotDuplicateCards`
- Body: `{"parentPageId":1358,"pageTitle":"string","cardPrefix":"string","beacon":7727}`

### Duplicate Page Async
`PUT {{instanceUrl}}/api/content/v1/pages/:pageId/duplicateAsync`
- Path: `:pageId`
- Query: `doNotDuplicateCards`
- Body: `{"parentPageId":1358,"pageTitle":"string","cardPrefix":"string","beacon":7727}`

### Delete Page
`DELETE {{instanceUrl}}/api/content/v1/pages/:id`
- Path: `:id`

### Remove Access
`DELETE {{instanceUrl}}/api/content/v1/share/bulk/page/:type/:id`
- Path: `:type`, `:id`
- Query: `resourceIds`

### Bulk Remove Owners
`POST {{instanceUrl}}/api/content/v1/pages/bulk/owners/remove`
- Body: `{"owners":[{"id":123456,"type":"USER"}],"pageIds":[1234,2345]}`

## Layouts

### Get Layout
`GET {{instanceUrl}}/api/content/v4/pages/layouts/:layoutId`
- Path: `:layoutId`

### Create Writelock
`PUT {{instanceUrl}}/api/content/v4/pages/layouts/:layoutId/writelock`
- Path: `:layoutId`

### Update Layout
`PUT {{instanceUrl}}/api/content/v4/pages/layouts/:layoutId`
- Path: `:layoutId`
- Body:
  ```json
  {
    "layoutId": 123456,
    "pageUrn": "224746953",
    "printFriendly": true,
    "background": null,
    "isDynamic": true,
    "content": [
      {
        "id": 1234,
        "contentKey": 0,
        "compactInteractionDefault": true,
        "formInstanceId": "<form_instance_uuid>",
        "acceptFilters": true,
        "style": {
          "sourceId": "fo1",
          "textColor": "dark"
        },
        "type": "FORM"
      }
    ],
    "standard": {
      "aspectRatio": 1.67,
      "width": 60,
      "frameMargin": 4,
      "framePadding": 8,
      "type": "STANDARD",
      "template": [
        {
          "contentKey": 2,
          "x": 0,
          "y": 0,
          "width": 60,
          "height": 5,
          "type": "FORM",
          "virtual": false,
          "virtualAppendix": false,
          "children": []
        }
      ]
    },
    "compact": {
      "aspectRatio": 1,
      "width": 12,
      "frameMargin": 4,
      "framePadding": 8,
      "type": "COMPACT",
      "template": [
        {
          "contentKey": 2,
          "x": 0,
          "y": 0,
          "width": 12,
          "height": 2,
          "type": "FORM",
          "virtual": false,
          "virtualAppendix": false,
          "children": []
        }
      ]
    },
    "hasPageBreaks": false,
    "style": null
  }
  ```

### Delete Writelock
`DELETE {{instanceUrl}}/api/content/v4/pages/layouts/:id/writelock`
- Path: `:id`

## Filter Views

### List Filter Views
`GET {{instanceUrl}}/api/content/v3/pages/:pageId/analyzer/named`
- Path: `:pageId`

### Update Filter View
`PUT {{instanceUrl}}/api/content/v3/pages/:pageId/analyzer`
- Path: `:pageId`
- Body:
  ```json
  {
    "analyzerId": 123456,
    "name": "<string>",
    "type": "NAMED",
    "scope": "PAGE",
    "ownerId": "466826668",
    "isDefault": true,
    "order": null,
    "filters": [
      {
        "column": "Column 1",
        "operand": "IN",
        "values": [
          "<string>"
        ],
        "dataType": "string",
        "filterType": "LEGACY",
        "affectedCardUrns": [],
        "key": "Column 1"
      }
    ],
    "graphBy": null,
    "functionOverrides": {},
    "segmentIds": []
  }
  ```

### Delete Filter View
`DELETE {{instanceUrl}}/api/content/v3/pages/analyzer/:filterViewId`
- Path: `:filterViewId`
