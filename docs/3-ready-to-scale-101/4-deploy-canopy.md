## Canopy Test & Prod 배포하기

실험 환경에서는 `canopy`를 수동으로 배포했지만, 상위 환경에서는 GitOps가 제공하는 모든 이점을 얻기 위해 정의를 Git에 저장하고 Argo CD를 통해 애플리케이션을 배포해야 합니다. 

하지만 먼저 해야 할 일이 두 가지 있습니다. 하나는 프로덕션 준비가 된 프롬프트("프로덕션으로 승격"하고자 하는 system prompt)를 위한 별도의 공간을 마련하는 것입니다. 그리고 두 번째로, test 및 production 환경에서 GenAI 애플리케이션 로직을 처리할 GitOps 저장소를 설정해야 합니다.

프롬프트부터 시작해 봅시다.

1. OpenShift AI 대시보드로 돌아가서, 왼쪽 메뉴에서 `Gen AI studio` > `Prompts`로 이동합니다. 이번에는 프로젝트로 **`<USER_NAME>-toolings`**를 선택합니다. `<USER_NAME>-toolings`는 프로덕션으로 가는 과정에서 필요한 도구들을 보관하는 중앙 영역이 됩니다! 그리고 프롬프트 레지스트리도 그러한 도구 중 하나입니다.

  ![prompt-toolings](./images/prompt-toolings.png)

1. `Create prompt`를 클릭하고 이전에 사용했던 것과 동일한 이름인 `summarization`으로 지정합니다. 그리고 test 환경으로 가져가고자 하는 System Prompt를 붙여넣습니다.

  원한다면 적절한 커밋 메시지도 추가할 수 있으며, `Create`를 클릭합니다. 

  ![prompt-toolings-2.png](./images/prompt-toolings-2.png)

  test에서는 항상 최신 상태를 유지하기 위해 최신 프롬프트(latest)를 사용할 것이며, prod에 있는 프롬프트에는 별칭(alias, 태그)을 사용할 것입니다. 이 별칭을 `prod`라고 부릅니다.
  새로 만든 프롬프트에 이 별칭을 추가해 보세요.

  ![prompt-toolings-3.png](./images/prompt-toolings-3.png)

  ![prompt-toolings-4.png](./images/prompt-toolings-4.png)

  이제 GitOps 부분으로 넘어갑니다. workbench로 이동하세요!

### Argo CD로 Canopy 설정하기

1. 도구(tooling)에서 했던 것과 마찬가지로, 모델 배포를 위한 `ApplicationSet` 정의를 생성해야 합니다. 우리는 `test` 환경용과 `prod` 환경용, 두 개의 별도 `ApplicationSet` 정의를 갖게 됩니다. 교육의 단순화를 위해 이들을 같은 저장소에 보관합니다. 하지만 실제 환경에서는 보호된 `main` 브랜치에 Pull Request를 통해서만 변경하는 별도의 저장소로 prod 정의를 분리하고 싶을 수도 있습니다. 나중에 prod 정의를 다른 곳으로 쉽게 옮길 수 있도록 `ApplicationSet` 정의를 분리해서 유지합니다 :)

    이전과 마찬가지로 `CLUSTER_DOMAIN`과 `USER_NAME` 값으로 `ApplicationSet` 정의를 업데이트합시다. `genaiops-gitops/appset-test.yaml`과 `genaiops-gitops/appset-prod.yaml` 파일을 열고 값을 교체합니다. 귀찮으신 분들을 위해 명령어도 준비해 두었습니다.

  ```bash
    sed -i -e 's/CLUSTER_DOMAIN/<CLUSTER_DOMAIN>/g' /opt/app-root/src/genaiops-gitops/appset-test.yaml
    sed -i -e 's/USER_NAME/<USER_NAME>/g' /opt/app-root/src/genaiops-gitops/appset-test.yaml
    sed -i -e 's/CLUSTER_DOMAIN/<CLUSTER_DOMAIN>/g' /opt/app-root/src/genaiops-gitops/appset-prod.yaml
    sed -i -e 's/USER_NAME/<USER_NAME>/g' /opt/app-root/src/genaiops-gitops/appset-prod.yaml
  ```

2. `frontend` 정의를 추가해 봅시다. `test`와 `prod`라는 두 개의 서로 다른 환경이 있으므로 두 개의 파일을 생성했습니다. 따라서 업데이트해야 할 파일도 두 개입니다. `genaiops-gitops` 아래에서, `canopy/test/frontend/config.yaml`과 `canopy/prod/frontend/config.yaml` 파일을 다음과 같이 업데이트합니다. 

    이렇게 하면 UI 배포 helm-chart를 가져와서 이미지 버전과 같은 추가 구성을 적용하게 됩니다. 기본적으로 실험 환경에서 수동으로 했던 모든 작업과 동일합니다.

    ```yaml
    repo_url: https://github.com/rhoai-genaiops/frontend.git
    chart_path: chart
    BACKEND_ENDPOINT: "http://canopy-backend:8000"
    image:
      name: "canopy-ui"
      tag: "0.12"
    ```
3. `backend`의 경우, 아래 yaml을 test와 prod의 `config.yaml` 파일에 각각 붙여넣습니다. 지금은 동일하지만, 서로 다른 별칭(alias)을 가리키고 있다는 점에 유의하세요. 프롬프트를 반복 개발해 나가면서 이 부분이 어떻게 달라지는지 확인하게 될 것입니다.

    TEST (`genaiops-gitops/canopy/test/backend/config.yaml`):

    ```yaml
    ---
    repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
    chart_path: chart
    summarization:
      enabled: true
      model: llama32
      endpoint: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
      mlflow_prompt: summarization
      mlflow_prompt_version: latest # 👈 always on latest
    ```

    PROD (`genaiops-gitops/canopy/prod/backend/config.yaml`):

    ```yaml
    ---
    repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
    chart_path: chart
    summarization:
      enabled: true
      model: llama32
      endpoint: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
      mlflow_prompt: summarization
      mlflow_prompt_version: prod # 👈 what we wrote as alias
    ```

<!-- 4. Lastly, let's setup Llama Stack to deploy via Argo CD. We just need Llama Stack Server here, Playground is something we only use in the experimentation phase. Update **both** `test/ogx/config.yaml` and `prod/ogx/config.yaml` as below:

    ```yaml
    chart_path: charts/llama-stack-operator-instance
    models:
      - name: "llama32"
        url: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
    ```  -->

  <!-- For now, we are happy with the default Llama Stack values. We will get some exciting updates as we continue to the other chapters :) -->

1. 이제 이 모든 것을 배포해 봅시다! 물론, git에 들어가지 않으면 실제가 아니니까요!

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git add .
    git commit -m  "🌳 ADD - ApplicationSets and Canopy components to deploy 🌳"
    git push 
    ```

2. 모든 애플리케이션 값이 Git에 저장되었으니, 이제 Argo CD에게 이러한 환경들의 변경 사항을 가져오라고 알려봅시다. 이를 위해서는 단순히 ApplicationSets를 생성하기만 하면 됩니다.

    ```bash
    oc apply -f /opt/app-root/src/genaiops-gitops/appset-test.yaml -n <USER_NAME>-toolings
    oc apply -f /opt/app-root/src/genaiops-gitops/appset-prod.yaml -n <USER_NAME>-toolings
    ```

3. 검색창에 `test` 또는 `prod`로 필터링하면 canopy 애플리케이션을 볼 수 있을 것입니다. 

    ![canopy-gitops.png](./images/canopy-gitops.png)

4. OpenShift Console로 이동하여 `<USER_NAME>-test` 네임스페이스를 확인함으로써 Canopy가 배포되었는지 확인할 수도 있습니다.

    ![canopy-test-ns.png](./images/canopy-test-ns.png)

5. `test` 환경에 Canopy가 배포되었으니, [Canopy UI](https://canopy-ui-<USER_NAME>-test.<CLUSTER_DOMAIN>/)를 열고 프롬프트를 전송하여 제대로 동작하는지 확인해 보세요! :D

    ![canopy-test.png](./images/canopy-test.png)
