# Certification

### List Certifications
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
      {
          "operationName": "getWorkflowConnection",
          "variables": {
              "type": "CC",
              "view": "WAITING", //WAITING or SUBMITTED
              "timePeriod": "ACTIVE", //PAST or ACTIVE
              "first": 30,
              "after": null,
              "orderBy": "DATE",
              "reverseSort": false,
              "searchTerm": "",
              "templateId": null
          },
          "query": "query getWorkflowConnection($type: String!, $after: ID, $view: View, $timePeriod: TimePeriod, $orderBy: OrderBy, $reverseSort: Boolean, $searchTerm: String, $first: Int, $templateId: ID) {\n  workflowConnection(type: $type, after: $after, view: $view, timePeriod: $timePeriod, orderBy: $orderBy, reverseSort: $reverseSort, searchTerm: $searchTerm, first: $first, templateId: $templateId) {\n    edges {\n      cursor\n      node {\n        certificationRequest {\n          id\n          type\n          status\n          entityType\n          entityId\n          entityTitle\n          previousActor {\n            id\n            type\n            displayName\n            ... on User {\n              title\n              avatarKey\n              isCurrentUser\n              __typename\n            }\n            ... on Group {\n              currentUserIsMember\n              userCount\n              isDeleted\n              __typename\n            }\n            __typename\n          }\n          entityOwnerEx {\n            id\n            type\n            displayName\n            ... on User {\n              title\n              avatarKey\n              isCurrentUser\n              __typename\n            }\n            ... on Group {\n              currentUserIsMember\n              userCount\n              isDeleted\n              __typename\n            }\n            __typename\n          }\n          entityOwners {\n            id\n            type\n            displayName\n            ... on User {\n              title\n              avatarKey\n              isCurrentUser\n              __typename\n            }\n            ... on Group {\n              currentUserIsMember\n              userCount\n              isDeleted\n              __typename\n            }\n            __typename\n          }\n          requestor {\n            id\n            displayName\n            title\n            isCurrentUser\n            __typename\n          }\n          modifiedTime\n          createdTime\n          __typename\n        }\n        approval {\n          newActivity\n          observers {\n            id\n            type\n            displayName\n            title\n            ... on Group {\n              memberCount: userCount\n              __typename\n            }\n            __typename\n          }\n          lastViewed\n          newActivity\n          newMessage {\n            created\n            createdByType\n            createdBy {\n              id\n              displayName\n              __typename\n            }\n            content {\n              text\n              __typename\n            }\n            __typename\n          }\n          lastAction\n          version\n          templateInstructions\n          submittedTime\n          id\n          title\n          status\n          providerName\n          templateTitle\n          buzzChannelId\n          buzzGeneralThreadId\n          templateInstructions\n          templateDescription\n          type\n          total {\n            value\n            currency\n            __typename\n          }\n          modifiedTime\n          previousApprover: previousApproverEx {\n            id\n            type\n            displayName\n            ... on User {\n              title\n              avatarKey\n              isCurrentUser\n              __typename\n            }\n            ... on Group {\n              currentUserIsMember\n              userCount\n              isDeleted\n              actor {\n                displayName\n                id\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          pendingApprover: pendingApproverEx {\n            id\n            type\n            displayName\n            ... on User {\n              title\n              avatarKey\n              isCurrentUser\n              __typename\n            }\n            ... on Group {\n              currentUserIsMember\n              userCount\n              isDeleted\n              __typename\n            }\n            __typename\n          }\n          submitter {\n            id\n            displayName\n            title\n            avatarKey\n            isCurrentUser\n            __typename\n          }\n          approvalChainIdx\n          chain {\n            actor {\n              displayName\n              __typename\n            }\n            approver {\n              id\n              type\n              displayName\n              ... on User {\n                title\n                avatarKey\n                isCurrentUser\n                __typename\n              }\n              ... on Group {\n                userCount\n                isDeleted\n                __typename\n              }\n              __typename\n            }\n            status\n            time\n            type\n            key\n            __typename\n          }\n          fields {\n            type\n            name\n            data\n            key\n            ... on NumberField {\n              value\n              __typename\n            }\n            ... on CurrencyField {\n              number: value\n              currency\n              __typename\n            }\n            ... on DateField {\n              date: value\n              __typename\n            }\n            ... on DataSetAttachmentField {\n              dataSet: value {\n                id\n                name\n                description\n                owner {\n                  id\n                  displayName\n                  __typename\n                }\n                provider\n                cardCount\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          history {\n            actor {\n              type\n              id\n              displayName\n              ... on User {\n                avatarKey\n                __typename\n              }\n              __typename\n            }\n            status\n            time\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n      __typename\n    }\n    __typename\n  }\n}\n"
      }
  ]
  ```

### List Certification Templates
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
      {
          "operationName": "getCertifiedTemplates",
          "variables": {
              "type": "CC:CARD", //CC:CARD or CC:DSET
              "includeUnpublished": false
          },
          "query": "query getCertifiedTemplates($type: String, $includeUnpublished: Boolean) {\n  templates(type: $type, includeUnpublished: $includeUnpublished) {\n    type\n    id\n    title\n    description\n    isPublic\n    isPublished\n    providerName\n    owner {\n      id\n      displayName\n      avatarKey\n      isCurrentUser\n      title\n      __typename\n    }\n    fieldCount\n    useCount\n    __typename\n  }\n}\n"
      }
  ]
  ```

### List Certified Entities
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  {
      "operationName": "getCertifiedEntities",
      "variables": {
          "type": "CC:CARD", //CC:CARD or CC:DSET
          "first": 100,
          "after": null,
          "searchTerm": "",
          "stateFilter": "EXPIRED" //null, PENDING, EXPIRED, CERTIFIED, or REQUESTED
      },
      "query": "\nquery getCertifiedEntities(\n  $type: String!\n  $first: Int\n  $after: ID\n  $searchTerm: String\n  $stateFilter: CertifyState\n) {\n  certifyEntitiesConnection(\n    type: $type\n    first: $first\n    after: $after\n    searchTerm: $searchTerm\n    stateFilter: $stateFilter\n  ) {\n    edges {\n      cursor\n      node {\n        id\n        title\n        entityType\n        description\n        processType\n        previousActor {\n          id\n          type\n          displayName\n          ... on User {\n            title\n            avatarKey\n            isCurrentUser\n          }\n          ... on Group {\n            currentUserIsMember\n            userCount\n            isDeleted\n          }\n        }\n        ownerEx {\n          id\n          type\n          displayName\n          ... on User {\n            title\n            avatarKey\n            isCurrentUser\n          }\n          ... on Group {\n            currentUserIsMember\n            userCount\n            isDeleted\n          }\n        }\n        owners {\n          id\n          type\n          displayName\n          ... on User {\n            title\n            avatarKey\n            isCurrentUser\n          }\n          ... on Group {\n            currentUserIsMember\n            userCount\n            isDeleted\n          }\n        }\n        lastUpdated\n        views\n        dateCertified\n        certifyState\n        certifyApprovalId\n        provider\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n      startCursor\n    }\n  }\n}\n"
  }
  ```

### Get Certification
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
    {
      "operationName": "getCertificationDetails",
      "variables": {
        "id": "00000000-0000-0000-0000-000000000000"
      },
      "query": "query getCertificationDetails($id: ID!) {\n  certification(id: $id) {\n    id\n    request {\n      id\n      type\n      status\n      entityType\n      entityId\n      entityTitle\n      entityOwnerEx {\n        id\n        type\n        displayName\n        ... on User {\n          title\n          avatarKey\n          isCurrentUser\n          __typename\n        }\n        ... on Group {\n          currentUserIsMember\n          userCount\n          isDeleted\n          __typename\n        }\n        __typename\n      }\n      entityOwners {\n        id\n        type\n        displayName\n        ... on User {\n          title\n          avatarKey\n          isCurrentUser\n          __typename\n        }\n        ... on Group {\n          currentUserIsMember\n          userCount\n          isDeleted\n          __typename\n        }\n        __typename\n      }\n      requestor {\n        id\n        displayName\n        title\n        avatarKey\n        isCurrentUser\n        isDeleted\n        __typename\n      }\n      modifiedTime\n      createdTime\n      __typename\n    }\n    approval {\n      id\n      version\n      type\n      title\n      status\n      providerName\n      templateTitle\n      buzzChannelId\n      buzzGeneralThreadId\n      templateInstructions\n      templateDescription\n      total {\n        value\n        currency\n        __typename\n      }\n      modifiedTime\n      previousApprover: previousApproverEx {\n        id\n        type\n        displayName\n        ... on User {\n          title\n          avatarKey\n          isCurrentUser\n          __typename\n        }\n        ... on Group {\n          currentUserIsMember\n          userCount\n          isDeleted\n          actor {\n            displayName\n            id\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      pendingApprover: pendingApproverEx {\n        id\n        type\n        displayName\n        ... on User {\n          title\n          avatarKey\n          isCurrentUser\n          __typename\n        }\n        ... on Group {\n          userCount\n          isDeleted\n          currentUserIsMember\n          __typename\n        }\n        __typename\n      }\n      submitter {\n        id\n        displayName\n        title\n        avatarKey\n        isCurrentUser\n        __typename\n      }\n      approvalChainIdx\n      chain {\n        actor {\n          displayName\n          __typename\n        }\n        approver {\n          id\n          type\n          displayName\n          ... on User {\n            title\n            avatarKey\n            isCurrentUser\n            __typename\n          }\n          ... on Group {\n            userCount\n            isDeleted\n            __typename\n          }\n          __typename\n        }\n        status\n        time\n        type\n        key\n        __typename\n      }\n      observers {\n        id\n        type\n        displayName\n        avatarKey\n        title\n        ... on Group {\n          userCount\n          __typename\n        }\n        __typename\n      }\n      fields {\n        type\n        name\n        data\n        key\n        ... on NumberField {\n          value\n          __typename\n        }\n        ... on CurrencyField {\n          number: value\n          currency\n          __typename\n        }\n        ... on DateField {\n          date: value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
  ]
  ```

### Get Certification Template
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
      {
          "operationName": "getCertifiedTemplate",
          "variables": {
              "type": "CARD", //CARD or DATASET
              "templateId": "00000000-0000-0000-0000-000000000000",
              "id": 123456,
              "title": "<string>"
          },
          "query": "query getCertifiedTemplate($templateId: ID, $type: CertifyType!, $id: ID, $title: String) {\n  companyName\n  template: certifyTemplate(templateId: $templateId, type: $type, id: $id, title: $title) {\n    id\n    type\n    title\n    titleName\n    titleData\n    titlePlaceholder\n    instructions\n    description\n    providerName\n    isPublic\n    chainIsLocked\n    owner {\n      id\n      displayName\n      avatarKey\n      __typename\n    }\n    fields {\n      key\n      type\n      name\n      data\n      placeholder\n      required\n      disabled\n      __typename\n    }\n    approvers {\n      type\n      originalType: type\n      key\n      ... on ApproverPerson {\n        id: approverId\n        approverId\n        userDetails {\n          id\n          displayName\n          title\n          avatarKey\n          __typename\n        }\n        __typename\n      }\n      ... on ApproverGroup {\n        id: approverId\n        approverId\n        groupDetails {\n          id\n          displayName\n          userCount\n          isDeleted\n          __typename\n        }\n        __typename\n      }\n      ... on ApproverPlaceholder {\n        placeholderText\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
      }
  ]
  ```

### Get Certification ID from Approval ID
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
    {
      "operationName": "getCertificationIdFromApprovalId",
      "variables": {
        "id": "00000000-0000-0000-0000-000000000000"
      },
      "query": "query getCertificationIdFromApprovalId($id: ID!) {\n  certificationId: certificationByApprovalId(id: $id) {\n    id\n    __typename\n  }\n}\n"
    }
  ]
  ```

### Get Entity Access
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
      {
          "operationName": "checkEntityAccess",
          "variables": {
              "entityType": "CARD", //CARD or DATASET
              "entityId": 123456, //Card or DataSet ID
              "approvers": [
                  {
                      "type": "GROUP",
                      "originalType": "GROUP",
                      "key": "00000000-0000-0000-0000-000000000000",
                      "id": "12345",
                      "approverId": "12345",
                      "groupDetails": {
                          "id": "12345",
                          "displayName": "<string>",
                          "userCount": 11, //For GROUP
                          "isDeleted": false,
                          "__typename": "Group" //Group or User
                      },
                      "__typename": "ApproverGroup"
                  }
              ]
          },
          "query": "query checkEntityAccess($entityId: ID!, $entityType: CertifyType!, $approvers: [ApproverInput!]!) {\n  isEntityAccessGranted(entityId: $entityId, entityType: $entityType, approvers: $approvers) {\n    deniedUsers {\n      type\n      id\n      displayName\n      ... on User {\n        title\n        avatarKey\n        isCurrentUser\n        __typename\n      }\n      __typename\n    }\n    deniedGroups {\n      id\n      type\n      displayName\n      ... on Group {\n        userCount\n        isDeleted\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
      }
  ]
  ```

### Get Waiting on Me Count
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body: `[{"operationName":"getWaitingOnMeCount","variables":{"type":"CC"},"query":"query getWaitingOnMeCount($type: String = \"CC\") {\n  count: waitingOnMeCount(type: $type)\n}\n"}]`

### Get Certification Expire on Edit
`GET {{instanceUrl}}/api/customer/v1/properties/:type`
- Path: `:type`

### Create Certification
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
    {
      "operationName": "newApproval",
      "variables": {
        "request": {
          "templateId": "00000000-0000-0000-0000-000000000000",
          "title": "<card_or_dataset_name>",
          "fields": [
            {
              "key": "00000000-0000-0000-0000-000000000000",
              "type": "ATTACHMENT",
              "name": "Card to certify",
              "data": "CARD:1234",
              "placeholder": null,
              "required": true,
              "disabled": false,
              "attachmentName": "<string>",
              "__typename": "CardAttachmentField"
            }
          ],
          "approvers": [
            {
              "approverId": 123456,
              "id": 123456,
              "originalType": "PERSON",
              "type": "PERSON",
              "userDetails": {
                "displayName": "<string>",
                "id": 123456
              }
            }
          ],
          "attachments": []
        },
        "adminCertified": true
      },
      "query": "mutation newApproval($request: ApprovalRequest!, $adminCertified: Boolean) {\n  approval: submitRequest(request: $request, adminCertified: $adminCertified) {\n    id\n    type\n    submittedTime\n    modifiedTime\n    status\n    title\n    providerName\n    templateTitle\n    amount\n    version\n    attachmentsCount\n    submitter {\n      id\n      displayName\n      __typename\n    }\n    observers {\n      id\n      type\n      displayName\n      __typename\n    }\n    history {\n      actor {\n        type\n        id\n        displayName\n        ... on User {\n          avatarKey\n          __typename\n        }\n        __typename\n      }\n      status\n      time\n      __typename\n    }\n    fields {\n      data\n      name\n      type\n      key\n      ... on HeaderField {\n        fields {\n          data\n          name\n          type\n          key\n          ... on HeaderField {\n            fields {\n              data\n              name\n              type\n              key\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on ItemListField {\n        fields {\n          data\n          name\n          type\n          key\n          ... on HeaderField {\n            fields {\n              data\n              name\n              type\n              key\n              ... on HeaderField {\n                fields {\n                  data\n                  name\n                  type\n                  key\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on NumberField {\n        value\n        __typename\n      }\n      ... on CurrencyField {\n        number: value\n        currency\n        __typename\n      }\n      ... on DateField {\n        date: value\n        __typename\n      }\n      ... on DataSetAttachmentField {\n        dataSet: value {\n          id\n          name\n          description\n          owner {\n            id\n            displayName\n            __typename\n          }\n          provider\n          cardCount\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    pendingApprover: pendingApproverEx {\n      id\n      type\n      displayName\n      ... on User {\n        title\n        avatarKey\n        isCurrentUser\n        __typename\n      }\n      ... on Group {\n        userCount\n        isDeleted\n        currentUserIsMember\n        __typename\n      }\n      __typename\n    }\n    chain {\n      actor {\n        displayName\n        __typename\n      }\n      approver {\n        id\n        type\n        displayName\n        ... on User {\n          title\n          avatarKey\n          isCurrentUser\n          __typename\n        }\n        ... on Group {\n          userCount\n          isDeleted\n          __typename\n        }\n        __typename\n      }\n      status\n      time\n      type\n      key\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
  ]
  ```

### Remove Certification
`POST {{instanceUrl}}/api/synapse/approval/graphql`
- Body:
  ```json
  [
      {
          "operationName": "remove",
          "variables": {
              "type": "CARD", //CARD or DATASET
              "id": "12345"
          },
          "query": "mutation remove($type: CertifyType!, $id: ID!) {\n  removeCertification(type: $type, id: $id)\n}\n"
      }
  ]
  ```
