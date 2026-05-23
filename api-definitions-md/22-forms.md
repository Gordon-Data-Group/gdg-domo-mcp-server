# Forms

### List/Search Forms
`POST {{instanceUrl}}/api/search/v1/query`
- Body:
  ```json
  {
    "count": 50,
    "offset": 0,
    "filters": [],
    "useEntities": true,
    "combineResults": true,
    "facetValueLimit": 1000,
    "entityList": [
      [
        "form"
      ]
    ],
    "sort": {
      "isRelevance": true,
      "fieldSorts": [
        {
          "field": "lastModified",
          "sortOrder": "DESC"
        }
      ]
    },
    "query": "*",
    "hideSearchObjects": false,
    "state": "facet"
  }
  ```

### Get Form
`GET {{instanceUrl}}/api/forms/v1/:id`
- Path: `:id`

### Create Instance
`POST {{instanceUrl}}/api/forms/v1/instances`
- Body:
  ```json
  {
    "formId": "00000000-0000-0000-0000-000000000000",
    "fieldConfiguration": {
      "00000000-0000-0000-0000-000000000000": {
        "options": {
          "type": "DATASET",
          "customMapping": null,
          "datasetMapping": {
            "id": "00000000-0000-0000-0000-000000000000",
            "column": "Column 1"
          }
        },
        "value": {
          "type": "DATASET"
        }
      }
    },
    "submitConfiguration": {
      "type": "DATASET",
      "name": "<string>"
    }
  }
  ```

### Create Submission
`POST {{instanceUrl}}/api/forms/v1/instances/:id/submission`
- Path: `:id`
- Body:
  ```json
  [
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "label": "<string>",
      "optional": false,
      "fieldType": "SINGLE_CHOICE",
      "dataType": "text",
      "acceptsInput": true,
      "acceptsOutput": true,
      "options": {
        "values": []
      },
      "alias": "<string>",
      "isList": true,
      "useExternalValues": true,
      "displayAsDropdown": true,
      "value": "<string>"
    }
  ]
  ```

### Update Instance
`PUT {{instanceUrl}}/api/forms/v1/instances/:id`
- Path: `:id`
- Body:
  ```json
  {
    "formInstanceId": "00000000-0000-0000-0000-000000000000",
    "formId": "00000000-0000-0000-0000-000000000000",
    "fieldConfiguration": {
      "00000000-0000-0000-0000-000000000000": {
        "options": {
          "type": "DATASET",
          "customMapping": null,
          "datasetMapping": {
            "id": "00000000-0000-0000-0000-000000000000",
            "column": "Column 1"
          }
        },
        "value": {
          "type": "DATASET"
        }
      }
    },
    "submitConfiguration": {
      "type": "DATASET",
      "id": "00000000-0000-0000-0000-000000000000",
      "name": "<dataset_name>"
    }
  }
  ```

### Update Form Fields
`POST {{instanceUrl}}/api/forms/v1/:id/hydration`
- Path: `:id`
- Body:
  ```json
  {
    "00000000-0000-0000-0000-000000000000": {
      "options": {
        "type": "DATASET",
        "customMapping": null,
        "datasetMapping": {
          "id": "00000000-0000-0000-0000-000000000000",
          "column": "Column 1"
        }
      },
      "value": {
        "type": "DATASET"
      }
    }
  }
  ```
