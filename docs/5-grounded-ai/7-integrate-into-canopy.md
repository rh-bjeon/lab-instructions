# 🌐 Canopy에 RAG 기능 적용하기

## Canopy에 RAG 통합하기

Canopy backend에는 이미 feature flag 뒤에 RAG 설정이 준비되어 있습니다. 이 기능이 무엇에 관한 것인지 시스템에 알려주는 좋은 시스템 프롬프트를 작성하고 feature flag를 활성화하기만 하면 됩니다.


1. **`<USER_NAME>-toolings`** 프로젝트 아래의 OpenShift AI Dashboard > Gen AI Studio > Prompts로 이동하세요.

2. `information-search`라는 새 prompt를 생성하고 아래 prompt를 사용하세요:

    ```bash
    You are a helpful assistant specializing in document intelligence and academic content analysis.
    ```
    ![information-search-prompt-2.png](./images/information-search-prompt-2.png)

    테스트 환경은 최신 변경을 바로 검증할 수 있도록 `latest` 프롬프트를 사용합니다. 운영 환경은 검증된 버전만 사용하도록 `prod` 별칭을 지정합니다. 새 프롬프트에 이 별칭을 추가하세요.

3. 그런 다음 workbench로 이동해 `genaiops-gitops/canopy/test/backend/config.yaml`과 `genaiops-gitops/canopy/prod/backend/config.yaml` 두 파일을 모두 여세요.

4. 파일을 수정해 `information-search` feature flag를 포함시키세요. 이전과 마찬가지로 이것은 시스템 프롬프트이므로 자유롭게 prompt를 변경해도 됩니다.

TEST(`genaiops-gitops/canopy/test/backend/config.yaml`)

    ---
    repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
    chart_path: chart
    summarization:
      enabled: true
      model: llama32
      endpoint: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
      mlflow_prompt: summarization
      mlflow_prompt_version: latest
    information-search:          # 👈 add this block 📚❗︎❗︎❗︎❗︎❗︎
      enabled: true
      endpoint: "http://llama-stack-service:8321/v1"
      model: vllm-llama32/llama32
      vector_db_id: latest
      mlflow_prompt: information-search
      mlflow_prompt_version: latest
    

PROD(`genaiops-gitops/canopy/prod/backend/config.yaml`)

    ---
    repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
    chart_path: chart
    summarization:
      enabled: true
      model: llama32
      endpoint: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
      mlflow_prompt: summarization
      mlflow_prompt_version: prod
    information-search:          # 👈 add this block 📚❗︎❗︎❗︎❗︎❗︎
      enabled: true
      endpoint: "http://llama-stack-service:8321/v1"
      model: vllm-llama32/llama32
      vector_db_id: latest
      mlflow_prompt: information-search
      mlflow_prompt_version: prod
    

5. 변경사항을 git에 push하세요:

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "🔨 RAG feature added 🔨"
    git push
    ```

6. Canopy UI(마지막으로 사용한 뒤 닫았다면 https://canopy-ui-<USER_NAME>-test.<CLUSTER_DOMAIN> )를 열고, 왼쪽 메뉴에서 *Information Search* 기능을 선택한 뒤 `what is the total credits in Biotechnology program in Redwood Digital University?`와 같이 질문해보세요.

prompt 안의 "Biotechnology"를 Minio에 업로드한 프로그램의 교육계획서로 바꾸세요. 예를 들어 "Computer Science" 교육계획서만 업로드했다면, prompt에서 "Biotechnology" 대신 "Computer Science"라고 적으세요.

  ![ask-canopy.png](images/ask-canopy.png)

축하합니다! 🎉  
이제 복잡한 문서를 필요에 따라 수집할 수 있는 RAG 시스템이 완성되었습니다.

현재는 문서를 추가할 때마다 파이프라인을 수동으로 실행해야 합니다. 다음 단계에서는 이 과정을 자동화하고 운영 환경에 반영하기 전에 평가를 수행하도록 구성합니다.

하지만 그 전에, 몇 가지 평가(eval)를 먼저 해봅시다!

다음 섹션으로 넘어가봅시다!
