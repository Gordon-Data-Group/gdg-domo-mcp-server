# Approvals

### Search Templates
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  {
    "operationName": "getApprovalTemplatesConnection",
    "query": "\nquery getApprovalTemplatesConnection(\n  $first: Int\n  $after: ID\n  $orderBy: OrderBy\n  $reverseSort: Boolean\n  $query: TemplateQueryRequest!\n) {\n  templateConnection(\n    first: $first\n    after: $after\n    orderBy: $orderBy\n    reverseSort: $reverseSort\n    query: $query\n  ) {\n    edges {\n      cursor\n      node {\n        id\n        datasetId\n        title\n        isPublic\n        providerName\n        description\n        observers {\n          id\n          type\n          displayName\n          avatarKey\n          title\n          ... on Group {\n            userCount\n          }\n        }\n        owner {\n          id\n          displayName\n          avatarKey\n          isCurrentUser\n          title\n        }\n        fieldCount\n        useCount\n        categories {\n          id\n          name\n        }\n      }\n    }\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n    }\n  }\n}",
    "variables": {
      "first": 20,
      "after": null,
      "orderBy": "TEMPLATE",
      "reverseSort": false,
      "query": {
        "type": "AC",
        "searchTerm": "",
        "category": [],
        "ownerId": null,
        "publishedOnly": false
      }
    }
  }
  ```

### Search Approvals
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  {
    "operationName": "getFilteredRequests",
    "variables": {
      "query": {
        "active": null,
        "submitterId": null,
        "approverId": null,
        "templateId": null,
        "title": null,
        "lastModifiedBefore": null
      },
      "after": null,
      "reverseSort": false
    },
    "query": "query getFilteredRequests($query: QueryRequest!, $after: ID, $reverseSort: Boolean) {\n  workflowSearch(\n    query: $query\n    type: \"AC\"\n    after: $after\n    reverseSort: $reverseSort\n  ) {\n    edges {\n      cursor\n      node {\n        approval {\n          id\n          title\n          templateID\n          templateTitle\n          status\n          modifiedTime\n          version\n          providerName\n          approvalChainIdx\n          pendingApprover: pendingApproverEx {\n            id\n            type\n            displayName\n            ... on User {\n              title\n              avatarKey\n              __typename\n            }\n            ... on Group {\n              isDeleted\n              __typename\n            }\n            __typename\n          }\n          submitter {\n            id\n            type\n            displayName\n            avatarKey\n            isCurrentUser\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n      __typename\n    }\n    __typename\n  }\n}"
  }
  ```

### List Templates
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  {
    "operationName": "listTemplates",
    "query": "query listTemplates {\n  templates {\n    id\n    title\n    titleName\n    titlePlaceholder\n    acknowledgment\n    instructions\n    description\n    providerName\n    isPublic\n    chainIsLocked\n    type\n    isPublished\n    observers {\n      id\n      type\n      displayName\n      avatarKey\n      title\n      ... on Group {\n        userCount\n        __typename\n      }\n      __typename\n    }\n    categories {\n      id\n      name\n      __typename\n    }\n    owner {\n      id\n      displayName\n      avatarKey\n      __typename\n    }\n    __typename\n  }\n}"
  }
  ```

### Get Template
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
    {
      "operationName": "getTemplateForEdit",
      "variables": {
        "id": "00000000-0000-0000-0000-000000000000"
      },
      "query": "query getTemplateForEdit($id: ID!) {\n  template(id: $id) {\n    id\n    title\n    titleName\n    titlePlaceholder\n    acknowledgment\n    instructions\n    description\n    providerName\n    isPublic\n    chainIsLocked\n    type\n    isPublished\n    observers {\n      id\n      type\n      displayName\n      avatarKey\n      title\n      ... on Group {\n        userCount\n        __typename\n      }\n      __typename\n    }\n    categories {\n      id\n      name\n      __typename\n    }\n    owner {\n      id\n      displayName\n      avatarKey\n      __typename\n    }\n    fields {\n      key\n      type\n      name\n      data\n      placeholder\n      required\n      isPrivate\n      ... on SelectField {\n        option\n        multiselect\n        datasource\n        column\n        order\n        __typename\n      }\n      __typename\n    }\n    approvers {\n      type\n      originalType: type\n      key\n      ... on ApproverPerson {\n        id: approverId\n        approverId\n        userDetails {\n          id\n          displayName\n          title\n          avatarKey\n          isDeleted\n          __typename\n        }\n        __typename\n      }\n      ... on ApproverGroup {\n        id: approverId\n        approverId\n        groupDetails {\n          id\n          displayName\n          userCount\n          isDeleted\n          __typename\n        }\n        __typename\n      }\n      ... on ApproverPlaceholder {\n        placeholderText\n        __typename\n      }\n      __typename\n    }\n    workflowIntegration {\n      modelId\n      modelVersion\n      startName\n      modelName\n      parameterMapping {\n        fields {\n          field\n          parameter\n          required\n          type\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  categories {\n    id\n    name\n    __typename\n  }\n}"
    }
  ]
  ```

### Get Approval
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  {
    "operationName": "getApprovalForDetails",
    "variables": {
      "id": "00000000-0000-0000-0000-000000000000"
    },
    "query": "query getApprovalForDetails($id: ID!) {\n  request: approval(id: $id) {\n    ...approvalFields\n    __typename\n  }\n}\n\nfragment approvalFields on Approval {\n  newActivity\n  observers {\n    id\n    type\n    displayName\n    title\n    ... on Group {\n      currentUserIsMember\n      memberCount: userCount\n      __typename\n    }\n    __typename\n  }\n  lastViewed\n  newActivity\n  newMessage {\n    created\n    createdByType\n    createdBy {\n      id\n      displayName\n      __typename\n    }\n    content {\n      text\n      __typename\n    }\n    __typename\n  }\n  lastAction\n  version\n  submittedTime\n  id\n  title\n  status\n  providerName\n  templateTitle\n  buzzChannelId\n  buzzGeneralThreadId\n  templateInstructions\n  templateDescription\n  acknowledgment\n  snooze\n  snoozed\n  type\n  categories {\n    id\n    name\n    __typename\n  }\n  total {\n    value\n    currency\n    __typename\n  }\n  modifiedTime\n  previousApprover: previousApproverEx {\n    id\n    type\n    displayName\n    ... on User {\n      title\n      avatarKey\n      isCurrentUser\n      __typename\n    }\n    ... on Group {\n      currentUserIsMember\n      userCount\n      isDeleted\n      actor {\n        displayName\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  pendingApprover: pendingApproverEx {\n    id\n    type\n    displayName\n    ... on User {\n      title\n      avatarKey\n      isCurrentUser\n      __typename\n    }\n    ... on Group {\n      currentUserIsMember\n      userCount\n      isDeleted\n      __typename\n    }\n    __typename\n  }\n  submitter {\n    id\n    displayName\n    title\n    avatarKey\n    isCurrentUser\n    type\n    __typename\n  }\n  approvalChainIdx\n  reminder {\n    sent\n    sentBy {\n      displayName\n      title\n      id\n      isCurrentUser\n      type\n      __typename\n    }\n    __typename\n  }\n  chain {\n    actor {\n      displayName\n      __typename\n    }\n    approver {\n      id\n      type\n      displayName\n      ... on User {\n        title\n        avatarKey\n        isCurrentUser\n        __typename\n      }\n      ... on Group {\n        currentUserIsMember\n        userCount\n        isDeleted\n        __typename\n      }\n      __typename\n    }\n    status\n    time\n    type\n    key\n    __typename\n  }\n  fields {\n    data\n    name\n    type\n    key\n    ... on HeaderField {\n      fields {\n        data\n        name\n        type\n        key\n        ... on HeaderField {\n          fields {\n            data\n            name\n            type\n            key\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ... on ItemListField {\n      fields {\n        data\n        name\n        type\n        key\n        ... on HeaderField {\n          fields {\n            data\n            name\n            type\n            key\n            ... on HeaderField {\n              fields {\n                data\n                name\n                type\n                key\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ... on NumberField {\n      value\n      __typename\n    }\n    ... on CurrencyField {\n      number: value\n      currency\n      __typename\n    }\n    ... on DateField {\n      date: value\n      __typename\n    }\n    ... on DataSetAttachmentField {\n      dataSet: value {\n        id\n        name\n        description\n        owner {\n          id\n          displayName\n          __typename\n        }\n        provider\n        cardCount\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  history {\n    actor {\n      type\n      id\n      displayName\n      ... on User {\n        avatarKey\n        isCurrentUser\n        __typename\n      }\n      __typename\n    }\n    status\n    time\n    __typename\n  }\n  latestMessage {\n    created\n    __typename\n  }\n  latestMentioned {\n    created\n    __typename\n  }\n  workflowIntegration {\n    modelId\n    modelVersion\n    startName\n    instanceId\n    modelName\n    __typename\n  }\n  __typename\n}"
  }
  ```

### Replace Approver
`POST {{instanceUrl}}/api/synapse/approval/graphql`

### Update Template
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
    {
      "operationName": "saveTemplate",
      "variables": {
        "template": {
          "id": "00000000-0000-0000-0000-000000000000",
          "title": "<string>",
          "description": "",
          "acknowledgment": null,
          "fields": [
            {
              "__typename": "StringField",
              "key": "53",
              "type": "TEXT",
              "name": "<string>",
              "data": "",
              "placeholder": null,
              "required": true,
              "isPrivate": false,
              "invalid": false
            },
            {
              "__typename": "SelectField",
              "key": "54",
              "type": "SELECT",
              "name": "<string>",
              "data": "",
              "placeholder": null,
              "required": true,
              "isPrivate": false,
              "option": [
                "<string>",
                "<string>",
                "<string>"
              ],
              "multiselect": false,
              "order": null,
              "invalid": false,
              "mode": "MANUAL"
            },
            {
              "__typename": "DateField",
              "key": "55",
              "type": "DATE",
              "name": "<string>",
              "data": "",
              "placeholder": null,
              "required": true,
              "isPrivate": false,
              "invalid": false
            },
            {
              "__typename": "DateField",
              "key": "56",
              "type": "DATE",
              "name": "<string>",
              "data": "",
              "placeholder": null,
              "required": true,
              "isPrivate": false,
              "invalid": false
            },
            {
              "__typename": "CardAttachmentField",
              "key": "57",
              "type": "ATTACHMENT",
              "name": "<string>",
              "data": "",
              "placeholder": null,
              "required": true,
              "isPrivate": false,
              "invalid": false
            }
          ],
          "approvers": [
            {
              "__typename": "ApproverGroup",
              "type": "GROUP",
              "originalType": "GROUP",
              "key": "51",
              "id": "2345",
              "approverId": "2345",
              "groupDetails": {
                "__typename": "Group",
                "id": "2345",
                "displayName": "<string>",
                "userCount": 3,
                "isDeleted": false,
                "memberCount": 3
              },
              "originalPlaceholderText": ""
            }
          ],
          "observers": [
            {
              "id": "1234",
              "type": "PERSON",
              "displayName": "<string>",
              "avatarKey": "<string>",
              "title": "<string>",
              "__typename": "User"
            }
          ],
          "isPublic": true,
          "providerName": "workbench",
          "chainIsLocked": false,
          "categories": {
            "id": "12"
          },
          "ownerId": 1234
        }
      },
      "query": "mutation saveTemplate($template: TemplateInput!) {\n  template: saveTemplate(template: $template) {\n    id\n    title\n    titleName\n    titlePlaceholder\n    acknowledgment\n    instructions\n    description\n    providerName\n    isPublic\n    chainIsLocked\n    owner {\n      id\n      displayName\n      avatarKey\n      __typename\n    }\n    fields {\n      key\n      type\n      name\n      placeholder\n      required\n      isLocked\n      __typename\n    }\n    approvers {\n      type\n      originalType: type\n      key\n      ... on ApproverPerson {\n        approverId\n        userDetails {\n          id\n          displayName\n          title\n          avatarKey\n          __typename\n        }\n        __typename\n      }\n      ... on ApproverGroup {\n        approverId\n        groupDetails {\n          id\n          displayName\n          userCount\n          isDeleted\n          __typename\n        }\n        __typename\n      }\n      ... on ApproverPlaceholder {\n        placeholderText\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
    }
  ]
  ```
