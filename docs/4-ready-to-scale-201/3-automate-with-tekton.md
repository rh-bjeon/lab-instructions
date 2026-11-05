# Git 변경 시 자동으로 실행하기

평가 파이프라인을 성공적으로 실행했습니다. 🎉 이제 평가 테스트나 프롬프트, 백엔드가 바뀔 때마다 자동으로 평가가 시작되도록 구성하겠습니다. Git 웹훅과 연결된 Tekton 파이프라인이 앞에서 수동으로 실행한 Kubeflow 평가 파이프라인을 시작하도록 만듭니다.

## 파이프라인 서버 설치

`<USER_NAME>-canopy` 네임스페이스에서 했던 것처럼 `toolings` 네임스페이스에도 파이프라인 서버가 필요합니다. 이번에는 Argo CD로 배포합니다.

1. 이전과 마찬가지로 `<USER_NAME>-canopy` 네임스페이스에서 workbench를 엽니다.

2. `genaiops-gitops/toolings` 아래에 DSPA(**D**ata **S**cience **P**ipeline **A**pplication, 파이프라인 서버) 폴더와 `config.yaml`을 추가합니다.

    ```bash
    mkdir /opt/app-root/src/genaiops-gitops/toolings/dspa
    touch /opt/app-root/src/genaiops-gitops/toolings/dspa/config.yaml
    ```
    DSPA에는 특별한 설정이 필요하지 않습니다. 다음 단계에서 `config.yaml`에 내용을 추가해 봅시다.

3. `genaiops-gitops/toolings/dspa/config.yaml` 안에 다음을 추가합니다.

    ```yaml
    ---
    chart_path: charts/dspa
    ```

4. Argo CD가 변경 사항을 가져올 수 있도록 push 합시다. 터미널에서 다음 명령어를 실행하면 됩니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git add .
    git commit -m  "🪈 Set up our pipeline server 🪈"
    git push 
    ```

5. 준비가 완료되면 `OpenShift AI` -> `Projects` -> `<USER_NAME>-toolings` -> `Pipelines`로 이동하여, 파이프라인을 가져올 수 있게 되었는지 확인할 수 있습니다.  

    ![dspa-ready](images/dspa-ready.png)

좋습니다, 이제 모든 준비가 끝났습니다!  

## Tekton 파이프라인을 통해 Kubeflow 파이프라인 트리거하기

이제 Kubeflow 파이프라인의 자동 실행을 설정할 준비가 되었습니다!  
Tekton Pipeline에서 이를 트리거할 것이며, 여기에는 MLflow 평가를 위한 단계와 GuideLLM을 위한 단계가 모두 포함됩니다.  

1. Argo CD를 통해 Tekton 파이프라인을 배포합니다. 먼저 다음을 실행합니다.

    ```bash
    mkdir /opt/app-root/src/genaiops-gitops/toolings/evaluation-pipeline
    touch /opt/app-root/src/genaiops-gitops/toolings/evaluation-pipeline/config.yaml
    ```
    이렇게 하면 `genaiops-gitops/toolings/evaluation-pipeline` 안에 구성 파일이 생성됩니다.

2. `evaluation-pipeline/config.yaml` 파일을 열고 아래 yaml을 config.yaml에 붙여넣습니다.

    ```yaml
    ---
    chart_path: charts/canopy-evals-pipeline
    USER_NAME: <USER_NAME>
    CLUSTER_DOMAIN: <CLUSTER_DOMAIN>
    kfp:
      backendUrl: http://canopy-backend.<USER_NAME>-test.svc.cluster.local:8000
      llmEndpoint: "http://llama-32-predictor.ai501.svc.cluster.local:8080"
    ```

3. 변경 사항을 Git에 커밋하고 푸시합니다. GitOps에서는 Git에 기록된 상태가 배포의 기준입니다. 😉 터미널에서 다음 명령어를 실행하면 됩니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git add .
    git commit -m "🚄 Evaluation Pipelines 🚄"
    git push
    ```

4. 이제 `OpenShift Dashboard` -> `Pipelines` -> `<USER_NAME>-toolings` -> `canopy-evals-pipeline`로 이동하여 살펴봅시다.

    이 파이프라인은 최신 저장소를 `git clone`한 뒤 Kubeflow 파이프라인을 시작합니다.

    파이프라인이 완료되면 `test`의 변경 사항을 `prod`로 승격하기 위한 PR(Pull Request)도 생성됩니다.

    ![tekton-pipeline](images/tekton-pipeline.png)

5. 좋습니다, 파이프라인이 준비되었습니다! 하지만 지금까지는 여전히 수동으로 파이프라인을 시작해야 하며, 이전과의 유일한 차이점은 이제 Tekton 파이프라인을 시작하면 그것이 Kubeflow 파이프라인을 시작한다는 점뿐입니다. 그 이상은 아직 없습니다...

    ![super-important-meme](images/super-important-meme.jpg)

    > 💡 **잠깐, Kubeflow 파이프라인이랑 Tekton 파이프라인이 왜 따로 있나요?**
    >
    > Kubeflow 파이프라인은 **"무엇을 평가할 것인가"**를 담당합니다 — MLflow 평가, GuideLLM 부하 테스트처럼 데이터 과학자가 작성한 평가 로직 그 자체입니다.
    > Tekton 파이프라인은 **"언제, 어떻게 그 평가를 실행시킬 것인가"**를 담당합니다 — git push나 새 프롬프트 등록 같은 이벤트를 받아서 최신 코드를 `git clone`하고, Kubeflow 파이프라인을 실행시켜 주는 역할만 합니다.
    >
    > 이렇게 둘을 분리해 두면 평가 로직(Kubeflow)은 그대로 둔 채 트리거 방식(Tekton)만 자유롭게 바꿀 수 있습니다. 수동 실행이든, git push든, 새 프롬프트 등록이든 트리거 조건이 바뀌어도 Kubeflow 파이프라인 자체는 손댈 필요가 없는 거죠. 게다가 Tekton은 OpenShift Pipelines와 잘 통합된 범용 CI/CD 엔진이라 webhook, PR 생성 같은 GitOps 작업을 잘하고, Kubeflow는 평가 지표 계산이나 MLflow 연동 같은 ML 특화 작업을 잘합니다 — 각자 잘하는 일을 하도록 역할을 나눠둔 셈입니다.

    이제 코드 저장소가 바뀌면 Tekton 파이프라인이 자동으로 실행되도록 구성하겠습니다.
    먼저 Gitea로 이동합니다.

6. Gitea 안에서 `evals` 저장소로 이동합니다. Settings로 이동합니다.

    ![gitea-evals-settings.png](./images/gitea-evals-settings.png)

7. `Webhooks` > `Add`를 클릭하고 Gitea를 선택합니다.

    ![gitea-evals-webhook.png](./images/gitea-evals-webhook.png)

8. Pipeline Event Listener를 위해 아래 URL을 입력하고 `Add Webhook`을 클릭합니다.

    ```bash
    http://el-canopy-evals-event-listener.<USER_NAME>-toolings.svc.cluster.local:8080
    ```

    ![githook](images/githook.png)

9. 또한 시스템에 변경이 생길 때마다 평가를 트리거해야 합니다. 예를 들어 설정의 무언가를 변경하거나, 새로운 기능을 추가하는 등의 경우, 시스템을 다시 평가해야 합니다. 그러니 `genaiops-gitops` 저장소에도 동일한 webhook을 추가해 봅시다. 이곳에 외부화된 백엔드 설정이 저장되어 있습니다.

    (이 웹훅은 GitOps 저장소에 대한 __모든 push__에 대해 파이프라인을 트리거하지는 않습니다. `canopy/test/backend/config.yaml` 파일에 변경이 있을 때만 파이프라인을 트리거하는 [interceptor 설정](https://github.com/rhoai-genaiops/genaiops-helmcharts/blob/main/charts/canopy-evals-pipeline/templates/triggers/triggers.yaml#L83)이 있습니다.)

    ```bash
    http://el-canopy-evals-event-listener.<USER_NAME>-toolings.svc.cluster.local:8080
    ```

    ![webhook-gitops.png](./images/webhook-gitops.png)

10. 그리고 마지막으로 **프롬프트**에 대해서도 같은 작업을 해야 합니다 💥💥💥 

    code-server workbench로 이동하여 `experiments/4-ready-to-scale-201/3-mlflow-webhook.ipynb`를 열고 처음 3개의 코드 셀을 실행합니다. 이렇게 하면 MLflow 쪽에 webhook이 생성되어, 새로운 프롬프트를 추가할 때 Tekton 파이프라인을 트리거하게 됩니다.

    ![mlflow-webhook-notebook.png](./images/mlflow-webhook-notebook.png)

11. 셀 실행을 마쳤다면, OpenShift AI Dashboard > Gen AI studio > Prompts로 이동하여 `<USER_NAME>-toolings`를 선택하여 테스트해 봅시다. `summarization`으로 이동하여 새로운 프롬프트 버전을 생성합니다. 

    ![new-prompt-toolings.png](./images/new-prompt-toolings.png)

12. Tekton 파이프라인이 시작된 것을 확인하세요. 이제 사람이 개입하는 단계(human in the loop)로서, test 환경에서 Canopy를 테스트하는 것뿐만 아니라, 평가 결과를 확인하고 이 프롬프트를 프로덕션으로 보내도 괜찮을지 판단할 수 있습니다.

    ![new-prompt-eval-pipeline.png](./images/new-prompt-eval-pipeline.png)

13. 파이프라인이 끝나면 OpenShift AI Dashboard에서 `Experiments (MLflow)` > 프로젝트로 **<USER_NAME>-toolings** 선택 > `summarization` > `Evaluation runs`로 이동하여 최신 프롬프트를 기반으로 한 평가 결과를 확인합니다.

    ![eval-results.png](./images/eval-results.png)

    그리고 `test-results` 버킷 아래에 아티팩트로 저장된 S3 버킷의 GuideLLM 결과도 확인할 수 있습니다. 

    MinIO UI로 이동하여 본인의 자격 증명으로 로그인하세요. [https://minio-ui-<USER_NAME>-toolings.<CLUSTER_DOMAIN>/browser](https://minio-ui-<USER_NAME>-toolings.<CLUSTER_DOMAIN>/browser)

    ![guidellm-results.png](./images/guidellm-results.png)

축하합니다! 🎉 MLflow와 `evals` 저장소를 평가 파이프라인에 연결했으므로 평가 기준이나 프롬프트를 업데이트할 때마다 테스트가 실행됩니다.

_실제 환경에서는 새로운 백엔드를 빌드할 때마다도 테스트를 실행하겠지만, 지금은 사전에 빌드된 백엔드 이미지를 사용하고 있으므로 그 부분은 생략합니다._

평가 결과가 기준을 충족했다면 이제 애플리케이션을 운영 환경으로 승격할 차례입니다.

## 프롬프트 변경 사항을 프로덕션으로 가져가는 방법

평가를 실행했고, GuideLLM 결과도 확인했으며, 모든 것이 프로덕션에 적합해 보입니다. 그렇다면 무엇이 변경되었는지 가시성을 확보하고, 프로덕션의 시스템 프롬프트를 문제가 생겼을 때 쉽게 롤백할 수 있는 방식으로 어떻게 업데이트할 수 있을까요?

1. `summarization` 기능을 위한 프롬프트를 여러 버전으로 테스트해 본 결과, 최신 버전의 프롬프트를 canopy 애플리케이션에서 사용하기로 결정했습니다. 프로덕션 용도임을 표시하는 `prod` 별칭(alias)을 해당 버전 프롬프트로 옮겨보겠습니다. 프롬프트에 별칭을 추가하면, 해당 프롬프트의 ID를 사용하도록 GitOps 저장소를 업데이트하는 파이프라인이 자동 실행되어야 합니다. 이를 통해 프로덕션에 무슨 프롬프트가, 언제 올라갔는지 알 수 있습니다. 프롬프트 ID가 Git 커밋 히스토리에 저장되어 있으므로 이전 ID로 쉽게 롤백할 수 있습니다.

    위와 같은 과정을 구성하기 위해, `prompt-promotion-pipeline`이라는 폴더를 생성하여 도구에 또 다른 파이프라인을 추가해 봅시다. 

    Argo CD를 통해 Tekton 파이프라인을 배포해 봅시다. 먼저 다음을 실행합니다. 

    ```bash
    mkdir /opt/app-root/src/genaiops-gitops/toolings/prompt-promotion-pipeline
    touch /opt/app-root/src/genaiops-gitops/toolings/prompt-promotion-pipeline/config.yaml
    ```

    이렇게 하면 `genaiops-gitops/toolings/prompt-promotion-pipeline` 안에 구성 파일이 생성됩니다.

2. `prompt-promotion-pipeline/config.yaml` 파일을 열고 아래 yaml을 config.yaml에 붙여넣습니다.

    ```yaml
    ---
    chart_path: charts/prompt-promotion-pipeline
    USER_NAME: <USER_NAME>
    CLUSTER_DOMAIN: <CLUSTER_DOMAIN>

3. 터미널에서 아래 명령어를 입력합니다. 그러면 다시 git에 커밋하고 push 하게 됩니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git add .
    git commit -m "🌊 Prompt Promotion Pipelines 🌊"
    git push
    ```

    Argo CD에 의해 동기화된 `OpenShift Dashboard` -> `Pipelines` -> `<USER_NAME>-toolings` -> `prompt-promotion-pipeline`을 확인하세요.

    ![prompt-promotion-pipeline.png](./images/prompt-promotion-pipeline.png)

4. 이전에 작업했던 노트북(`experiments/4-ready-to-scale-201/3-mlflow-webhook.ipynb`)으로 돌아가서, 프롬프트 버전에 새로운 별칭이 추가될 때만 트리거되도록 MLflow에 webhook 정의를 추가하는 마지막 셀을 실행합니다.

    ![mlflow-webhook-notebook2.png](./images/mlflow-webhook-notebook2.png)


5. 이제 테스트해 봅시다! OpenShift AI Dashboard > Gen AI studio > Prompts로 이동하여 프로젝트로 `<USER_NAME>-toolings`를 선택합니다. `summarization`으로 이동하여 최신 버전에 `prod` 별칭을 추가합니다.

    ![add-alias.png](./images/add-alias.png)

    ![add-alia-2.png](./images/add-alias-2.png)

6. OpenShift console > Pipelines > `<USER_NAME>-toolings` 프로젝트 아래에서 파이프라인이 실행되는 것을 지켜보세요.

    ![prompt-promotion-pipeline-run.png](./images/prompt-promotion-pipeline-run.png)

7. 파이프라인이 끝나면, GitOps 저장소가 업데이트되는 것을 확인하세요. [Gitea](https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/genaiops-gitops/) > `genaiops-gitops`로 이동하여, 평온한 고양이 Tekton 🐈 이 만든 새로운 커밋이 있는지 확인합니다.

    ![prompt-promotion-git-update.png](./images/prompt-promotion-git-update.png)

8. 마지막으로, [https://canopy-ui-<USER_NAME>-prod.<CLUSTER_DOMAIN>/](https://canopy-ui-<USER_NAME>-prod.<CLUSTER_DOMAIN>/)에서 prod Canopy에 접속하여 프롬프트를 몇 개 전송해 봄으로써 변경 사항을 확인합니다.

> 또는, 이 변경 사항을 브랜치에 push하고 다른 사람이 승인할 수 있도록 PR을 생성하는 방법도 있습니다. 다만 이번 흐름에서는 평가 결과를 검토하는 단계에서 이미 사람의 리뷰가 이루어집니다.


## 평가 데이터 추가하기

[Evaluating with MLflow](1-evaluate-genai-applications.md#evaluating-with-mlflow) 섹션에서 했던 것처럼, MLflow trace로부터 평가 데이터셋을 키워나갈 수 있습니다. 각 환경은 자신만의 작업 공간에 trace를 저장합니다.

예를 들어, 프로덕션 환경의 trace를 평가 데이터셋에 추가하려면 다음과 같이 합니다. 

1. **OpenShift AI Dashboard** > **Experiments(MLflow)**로 이동하여 `<USER_NAME>-prod`를 선택합니다.
2. **summarization** > **Traces**를 열고 trace를 하나 선택합니다. (summarization trace가 보이지 않는다면, 위의 8번 단계에 따라 prod Canopy에 접속하여 채팅을 쳐보세요)
3. **Show assessments** > **Add expectations**를 클릭하고 기대값을 입력합니다. (아래는 예시)
    - Assessment Name: `length`
    - Data Type: `Number`
    - Value: `200`
    - Rationale: `This text really should not be longer than 200 chars`
4. **Add to dataset**을 클릭하고 기존의 `eval` 데이터셋을 선택한 다음 **Export**를 클릭합니다.


### 내 프롬프트는 어디에 있을까? 내 trace는 어디에 있을까?

번호가 매겨진 단계를 따라가며, 프롬프트 변경이 어떻게 평가 실행을 트리거하는지, trace는 어디에 수집되는지, 그리고 결과는 사람이 검토할 수 있도록 어디에 도착하는지 살펴보세요.

![where-are-my-prompts.jpg](./images/where-are-my-prompts.jpg)

1. 프롬프트 레지스트리에서 프롬프트를 변경하면 `toolings` 네임스페이스에서 평가 파이프라인을 자동으로 시작시킵니다.
2. 파이프라인은 세 곳에서 평가 데이터셋을 수집합니다. Git, 그리고 `test`와 `prod` 환경 각각의 trace 컬렉션입니다.
3. 평가용 프롬프트가 `test` 백엔드로 전송되고, 백엔드는 LLM을 호출합니다. 그 결과로 `test` 환경에 새로운 trace가 생성됩니다.
4. 평가 결과는 `toolings` 네임스페이스에 저장됩니다.
5. 어떤 승격(promotion)이든 이루어지기 전에 사람이 결과를 검토합니다.

----

이제 모든 변경을 추적하고 관찰할 수 있는 엔드투엔드 자동화 흐름이 완성되었습니다. 이 구조를 바탕으로 더 복잡한 사용 사례까지 확장할 수 있습니다. 🚀
