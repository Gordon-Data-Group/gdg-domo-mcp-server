# Task Center

### List Queues
`GET {{instanceUrl}}/api/queues/v1`
- Query: `combineAttributes`, `archived`

### Search Queues
`POST {{instanceUrl}}/api/search/v1/query`
- Body:
  ```json
  {
    "query": "*",
    "entityList": [
      [
        "queue"
      ]
    ],
    "count": 100,
    "offset": 0,
    "sort": {
      "isRelevance": true,
      "fieldSorts": [
        {
          "field": "lastModified",
          "sortOrder": "DESC"
        }
      ]
    },
    "filters": [],
    "useEntities": true,
    "combineResults": true,
    "facetValueLimit": 1000,
    "hideSearchObjects": false,
    "state": "facet"
  }
  ```

### List Tasks
`POST {{instanceUrl}}/api/queues/v1/tasks/list`
- Query: `limit`, `offset`, `render`, `renderParts`, `direction`, `orderBy`
- Body:
  ```json
  {
    "queueId": [
      "00000000-0000-0000-0000-000000000000"
    ],
    "displayType": [
      "ENIGMA_FORM",
      "EMAIL",
      "UNKNOWN"
    ],
    "status": [
      "OPEN",
      "COMPLETED",
      "VOIDED"
    ],
    "assignedBy": [
      "1234"
    ],
    "assignedTo": [
      "1234"
    ],
    "createdOn": [
      [
        "2023-10-04T12:22:54.239Z",
        "2024-01-02T13:22:54.239Z"
      ]
    ],
    "createdBy": [
      "1234"
    ],
    "assignedOn": [
      [
        "2023-10-04T12:22:54.239Z",
        "2024-01-02T13:22:54.239Z"
      ]
    ],
    "updatedOn": [
      [
        "2023-10-04T12:22:54.239Z",
        "2024-01-02T13:22:54.239Z"
      ]
    ],
    "completedOn": [
      [
        "2023-10-04T12:22:54.239Z",
        "2024-01-02T13:22:54.239Z"
      ]
    ],
    "completedBy": [
      "1234"
    ],
    "orderByString": [
      "createdOn"
    ],
    "version": [
      "1"
    ]
  }
  ```

### Get Queue
`GET {{instanceUrl}}/api/queues/v1/:queueId`
- Path: `:queueId`

### Get Task
`GET {{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId`
- Path: `:queueId`, `:taskId`
- Query: `render`

### Save Task Progress
`PUT {{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId/outputs`
- Path: `:queueId`, `:taskId`
- Body:
  ```json
  {
    "Suggested_Action_Items": "1. Investigate assembly line for misalignment issues near the hinge area\n2. Inspect and replace seals in the actuator's main chamber to prevent hydraulic leaks\n3. Address the issue of missing or loose fasteners with the supplier\n",
    "Send_to_QA_Team": true
  }
  ```

### Complete Task
`POST {{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId/complete`
- Path: `:queueId`, `:taskId`
- Query: `version`
- Body: `{}`

### Transfer Task to Another Queue
`PUT {{instanceUrl}}/api/queues/v1/:currentQueueId/tasks/:taskId/move`
- Path: `:currentQueueId`, `:taskId`
- Query: `targetQueueId`

### Transfer Task to Another User/Group
`PUT {{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId/assign`
- Path: `:queueId`, `:taskId`
- Body: `{"tasksId":[],"type":"USER","userId":"700632941"}`

### Void Task
`POST {{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId/void`
- Path: `:queueId`, `:taskId`

### Create Task
`POST {{instanceUrl}}/api/queues/v1/:queueId/tasks`
- Path: `:queueId`
- Body:
  ```json
  {
    "attributes": [],
    "queueId": "00000000-0000-0000-0000-000000000000",
    "version": 1,
    "completedOn": null,
    "completedBy": null,
    "assignedOn": null,
    "assignedBy": null,
    "assignedTo": null,
    "assigneeType": "USER",
    "lockedOn": "2025-01-01T12:00:00Z",
    "lockedBy": "1234",
    "status": "OPEN",
    "tags": [],
    "comments": [],
    "sourceSystem": "ODYSSEY",
    "sourceInfo": {
      "modelId": "00000000-0000-0000-0000-000000000000",
      "modelVersion": "1.0.1",
      "instanceId": "00000000-0000-0000-0000-000000000000",
      "deploymentId": "00000000-0000-0000-0000-000000000000",
      "instanceCreatedBy": "1234",
      "taskKey": "6755399776345339",
      "workflowInstanceId": "6755399776345326",
      "flowNodeId": "PQxCrPWaeTvqdFE",
      "elementInstanceKey": "6755399776345337"
    },
    "displayType": "ENIGMA_FORM",
    "displayId": "00000000-0000-0000-0000-000000000000",
    "displayEntity": {
      "id": "00000000-0000-0000-0000-000000000000",
      "version": "0.0.0",
      "domainType": "WORKFLOW",
      "domainId": "00000000-0000-0000-0000-000000000000 - 1.0.1",
      "name": "test - Copy",
      "description": "",
      "sections": [
        {
          "id": "00000000-0000-0000-0000-000000000000",
          "title": "",
          "fields": [
            {
              "id": "00000000-0000-0000-0000-000000000000",
              "label": "<string>",
              "placeholder": "",
              "optional": false,
              "fieldType": "SINGLE_CHOICE",
              "dataType": "text",
              "acceptsInput": false,
              "acceptsOutput": true,
              "options": {
                "values": [
                  "<string>"
                ],
                "acceptsOther": false
              },
              "alias": "<string>",
              "isList": false,
              "displayAsDropdown": false
            }
          ],
          "description": ""
        }
      ],
      "settings": {
        "hideSectionHeaderDetails": true
      },
      "attributes": [
        {
          "type": "paragraph",
          "children": [
            {
              "text": ""
            }
          ]
        }
      ],
      "fieldConfiguration": {
        "be59330c-61c0-425b-a5f9-f84968b678e6": {
          "options": {
            "type": "CUSTOM"
          },
          "targetMapping": {
            "target": "<string>"
          }
        }
      },
      "submitConfiguration": {
        "type": "UNASSIGNED",
        "isDatasetOwner": false
      },
      "searchable": true,
      "userPermissions": [],
      "submitConfigurationType": "UNASSIGNED"
    },
    "contract": {
      "input": [],
      "output": [
        {
          "name": "<string>",
          "displayName": null,
          "type": "text",
          "required": true,
          "list": false,
          "validValues": null,
          "entitySubType": null
        }
      ]
    },
    "inputVariables": {},
    "outputVariables": {}
  }
  ```

### Update Queue Permissions
`POST {{instanceUrl}}/api/queues/v1/:queueId/permissions`
- Path: `:queueId`
- Body:
  ```json
  [
    {
      "id": "337992616",
      "permissions": [
        "ADMIN",
        "SHARE",
        "DELETE",
        "WRITE",
        "READ",
        "CREATE_CONTENT",
        "READ_CONTENT",
        "UPDATE_CONTENT"
      ],
      "name": "<string>",
      "type": "USER"
    },
    {
      "id": "700632923",
      "permissions": [
        "ADMIN"
      ],
      "name": "<string>",
      "type": "USER"
    },
    {
      "id": "519150798",
      "permissions": [],
      "name": "<string>",
      "type": "USER"
    },
    {
      "id": "264236964",
      "permissions": [
        "DELETE",
        "WRITE",
        "SHARE",
        "EXPORT",
        "EXECUTE",
        "CREATE_CONTENT",
        "READ_CONTENT",
        "UPDATE_CONTENT",
        "DELETE_CONTENT"
      ],
      "name": "<string>",
      "type": "GROUP"
    }
  ]
  ```

### Update Queue Owner
`PUT {{instanceUrl}}/api/queues/v1/:queueId/owner/:ownerId`
- Path: `:queueId`, `:ownerId`
