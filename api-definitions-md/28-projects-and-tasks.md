# Projects and Tasks

### List Projects
`GET {{instanceUrl}}/api/content/v1/projects`
- Query: `limit`, `offset`, `status`

### List Tags
`GET {{instanceUrl}}/api/content/v1/tags`
- Query: `q`

### Get Projects for User
`GET {{instanceUrl}}/api/content/v2/users/:userId/projects`
- Path: `:userId`
- Query: `limit`, `offset`, `status`

### Get Tasks for Project
`GET {{instanceUrl}}/api/content/v1/projects/:projectId/tasks`
- Path: `:projectId`
- Query: `search`, `archived`, `assignedToOwnerId`

### Get Tasks for List
`GET {{instanceUrl}}/api/content/v1/projects/:projectId/lists/:listId/tasks`
- Path: `:projectId`, `:listId`
- Query: `fields`

### Get Task Assignments for User
`GET {{instanceUrl}}/api/content/v2/users/:userId/tasks/assignments`
- Path: `:userId`
- Query: `limit`, `offset`, `status`

### Get Lists for Project
`GET {{instanceUrl}}/api/content/v1/projects/:projectId/lists`
- Path: `:projectId`
- Query: `archived`

### Get Tags for Project
`GET {{instanceUrl}}/api/content/v1/projects/:projectId/tags`
- Path: `:projectId`
- Query: `archived`

### Get Project
`GET {{instanceUrl}}/api/content/v1/projects/:projectId`
- Path: `:projectId`

### Get Task
`GET {{instanceUrl}}/api/content/v1/tasks/:taskId`
- Path: `:taskId`

### Create Project
`POST {{instanceUrl}}/api/v1/projects`
- Body: `{"projectName":"<string>","description":"<string>","invalidProjectName":false,"hidden":false,"members":[1234],"dueDate":1735689600000}`

### Create Task
`POST {{instanceUrl}}/api/content/v1/projects/:projectId/lists/:listId/tasks`
- Path: `:projectId`, `:listId`
- Body: `{"id":123456789,"taskName":"<string>","disabled":true,"owners":[{"assignedTo":1234}],"priority":1}`

### Create User Task
`POST {{instanceUrl}}/api/content/v2/users/:userId/tasks`
- Path: `:userId`
- Body:
  ```json
  {
    "attachments": [],
    "realProjectListId": null,
    "tags": [
      {
        "tag": "<string>"
      }
    ],
    "contributors": [
      {
        "assignedTo": 1234
      }
    ],
    "taskName": "<string>",
    "dueDate": 1735689600000,
    "primaryTaskOwner": 1234,
    "description": "<string>"
  }
  ```

### Create List
`POST {{instanceUrl}}/api/content/v1/projects/:projectId/lists`
- Path: `:projectId`
- Body: `{"name":"<string>","type":"complete","listOrder":1000000}`

### Create Attachment for Task
`POST {{instanceUrl}}/api/content/v1/tasks/:taskId/attachments`
- Path: `:taskId`
- Body: `{"dataFileId":1234,"name":"<string>","type":"<string>","previewImage":"data:<mime_type>;base64,<base64_encoded_string>"}`

### Update Project
`PUT {{instanceUrl}}/api/content/v1/projects/:projectId`
- Path: `:projectId`
- Body:
  ```json
  {
    "id": 1,
    "creator": 1234,
    "assignedTo": 1234,
    "projectName": "<string>",
    "created": 1735689600000,
    "hidden": true,
    "personalUserProject": true,
    "todoCount": 0,
    "workingOnCount": 0,
    "completedCount": 0,
    "members": [
      1234
    ],
    "private": true,
    "userPersonalProject": true,
    "description": "<string>",
    "invalidProjectName": false
  }
  ```

### Update Task
`PUT {{instanceUrl}}/api/content/v1/tasks/:taskId`
- Path: `:taskId`
- Body:
  ```json
  {
    "id": 1,
    "projectId": 1,
    "projectListId": 1,
    "realProjectListId": null,
    "projectName": "<string>",
    "taskName": "<string>",
    "description": "<string>",
    "created": 1735689600000,
    "dueDate": 1735689600000,
    "priority": 1,
    "creator": 1234,
    "primaryTaskOwner": 1234,
    "status": "todo",
    "contributors": [
      {
        "id": 1,
        "assignedTo": 1234,
        "assignedBy": 1234,
        "created": 1735689600000
      }
    ],
    "attachments": [
      {
        "id": 1,
        "taskId": 1,
        "dataFileId": 1234,
        "type": "<string>",
        "creator": 1234,
        "created": 1735689600000,
        "previewImage": "data:<mime_type>;base64,<string>",
        "name": "<string>"
      }
    ],
    "tags": [
      {
        "tag": "<string>"
      }
    ],
    "archived": false
  }
  ```

### Update List
`PUT {{instanceUrl}}/api/content/v1/projects/:projectId/lists/:listId`
- Path: `:projectId`, `:listId`
- Body: `{"id":1,"projectId":1234,"type":"todo","name":"<string>","listOrder":1,"taskCount":3,"archived":true,"limit":20,"hovered":true}`

### Delete Project
`DELETE {{instanceUrl}}/api/content/v1/projects/:projectId`
- Path: `:projectId`
