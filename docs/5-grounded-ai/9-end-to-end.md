## Tekton으로 흐름 자동화하기

1. MinIO에 새 문서가 업로드될 때 이 전체 흐름을 자동화해봅시다! 이를 위해서는 KFP (Kubeflow Pipelines) 트리거와 그 주변의 ops 작업들을 처리할 Tekton pipeline을 배포해야 합니다(Ready to Scale 201에서 했던 것과 매우 유사합니다).
    최종적으로 전체 흐름은 다음과 같은 모습이 됩니다:

    ![doc-ingestion-tekton-flow.png](./images/doc-ingestion-tekton-flow.png)


아래와 같이 `genaiops-gitops/toolings` 아래에 폴더를 만들어 Tekton pipeline을 배포해봅시다:

  ```bash
  mkdir -p /opt/app-root/src/genaiops-gitops/toolings/doc-ingestion-pipeline
  touch /opt/app-root/src/genaiops-gitops/toolings/doc-ingestion-pipeline/config.yaml
  ```

2. `config.yaml` 파일을 업데이트하세요:

    ```yaml
    ---
    chart_path: charts/canopy-doc-ingestion-pipeline
    username: <USER_NAME>
    cluster_domain: <CLUSTER_DOMAIN>
    ```

3. 항상 그렇듯 변경사항을 커밋하고 push하세요.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "🦁 RAG doc ingestion pipeline added 🦁"
    git push
    ```

4. 이 pipeline은 MinIO에 추가할 webhook을 제공하여, 파일을 업로드할 때 MinIO가 Tekton pipeline을 트리거할 수 있게 해줍니다.
MinIO([https://minio-ui-<USER_NAME>-toolings.<CLUSTER_DOMAIN>](https://minio-ui-<USER_NAME>-toolings.<CLUSTER_DOMAIN>)) > `Events`로 이동해 우측 상단의 `Add Event Destination`을 클릭하세요. `Webhook`을 선택합니다:

    ![minio-webhook-1.png](./images/minio-webhook-1.png)

5. 다음 두 정보로 양식을 작성하세요:

    **Identifier:** `doc-ingestion-webhook`

    **Endpoint:** `http://el-canopy-doc-ingestion-event-listener.<USER_NAME>-toolings.svc.cluster.local:8080`

    ..그리고 `Save Event Destination`을 누르세요.

    ![minio-webhook-2.png](./images/minio-webhook-2.png)

6. 조금 의외일 수 있지만, 설정을 적용하려면 MinIO를 재시작하라는 메시지가 상단에 표시됩니다. `Restart`를 클릭하고 페이지를 새로고침하세요 🤷

    ![minio-webhook-3.png](./images/minio-webhook-3.png)

7. 이제 이 webhook을 `documents` 버킷과 연결해봅시다. Buckets > documents > Events로 이동해 `Subscribe to Event`를 클릭하세요. ARN 드롭다운 메뉴에서 방금 만든 webhook을 선택하고, 이벤트로 `PUT - Object Uploaded`를 체크하세요. 변경사항을 `Save`하세요. 다시 재시작할 필요는 없습니다 :)

    ![minio-webhook-4.png](./images/minio-webhook-4.png)

8. 이제 [RDU website](https://rdu-website-ai501.<CLUSTER_DOMAIN>)에서 원하는 다른 교육계획서를 다운로드해 `documents` 버킷에 업로드할 수 있습니다. 이를 위해 `Object Browser` > `documents`로 이동하세요.

    ![minio-upload-pdf.gif](./images/minio-upload-pdf.gif)

9. PDF를 업로드한 뒤, `OpenShift console` > `Pipelines`로 이동해 pipeline이 트리거되는 것을 확인하세요.

    ![rag-tekton-pipeline.png](./images/rag-tekton-pipeline.png)

10. 그리고 다시 OpenShift AI console로 돌아가면, `doc-ingestion` Kubeflow Pipeline이 실행 중인 것을 볼 수 있습니다:

    ![rag-kfp-pipelinerun.png](./images/rag-kfp-pipelinerun.png)

11. pipeline이 끝나면, `genaiops-gitops` 저장소에 자동으로 push가 이루어진 것을 볼 수 있습니다(이는 다시 우리의 eval pipeline을 시작시킵니다).

    ![gitea-auto-commit.png](./images/gitea-auto-commit.png)

12. 이제 평가(eval)에 대해서도 생각해봐야 합니다! 만약 여러분의 eval이 마지막에 업로드한 PDF와 관련된 내용을 전혀 다루지 않는다면 어떨까요? 예를 들어 prompt와 예상 결과 쌍을 더 추가하는 식으로 eval을 자유롭게 업데이트해보세요(Prompt Engineering Yay!). 데이터셋을 업데이트하면, eval pipeline이 자동으로(automagically) 트리거됩니다!

<!-- 
    And what happens when we see an update in `backend`?
    You guessed it, we trigger the evals pipeline! 

    ![trigger-evals.png](./images/trigger-evals.png)

    After the eval pipeline finishes, you can find a PR in `backend` repository to update vector DB ID in production. 

    In the description, you'll see a link to evaluation results. You need to check the results and decide whether to accept this change or go back and do some more test, more data ingestions etc. 
      
    You are the human in the loop here :)

    ![canopy-be-rag-pr.png](./images/canopy-be-rag-pr.png)

    And what if your evals doesn't cover anything related to the last PDF you uploaded?  
    Feel free to update your evals by for example adding more prompt & expected result pairs (Prompt Engineering Yay!). 

    ![prompt-tracker-eval-results.png](./images/prompt-tracker-eval-results.png) -->
