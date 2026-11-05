# 프로덕션을 위한 준비

지금까지 workbench나 playground에서 RAG의 여러 요소들을 경험해보았습니다. 이제 상위 환경을 위해 GitOps로 설정을 구성하고, 더 많은 자동화를 적용하며, RAG를 더 강력하고 이동 가능하게 만들어줄 오케스트레이션 계층을 도입해야 합니다 — 이에 대해서는 곧 자세히 다루겠습니다!

## 📊 Milvus Test & Prod 배포

1. workbench로 다시 돌아갑니다 🧑‍🏭

2. `genaiops-gitops` 폴더 아래에, test와 prod 환경을 위한 별도의 설정을 만들겠습니다:

    ```bash
    mkdir -p /opt/app-root/src/genaiops-gitops/canopy/test/milvus
    mkdir -p /opt/app-root/src/genaiops-gitops/canopy/prod/milvus
    touch /opt/app-root/src/genaiops-gitops/canopy/test/milvus/config.yaml
    touch /opt/app-root/src/genaiops-gitops/canopy/prod/milvus/config.yaml
    ```

3. `canopy/test/milvus/config.yaml`과 `canopy/prod/milvus/config.yaml` 두 파일을 동일한 설정으로 업데이트합니다:

    **TEST와 PROD 모두:**

    ```yaml
    chart_path: charts/milvus
    ```

    지금은 Milvus의 기본값으로 충분합니다.

4. 이제 이 설정들을 배포해봅시다! 파일들을 Git에 커밋합니다:

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "📊 ADD - Milvus test & prod vector databases 📊"
    git push
    ```

5. 두 Milvus pod가 모두 정상 동작할 때까지 기다립니다. 즉, `Ready` 열 아래 `1/1`이 표시되는지 확인하세요:

  ```bash
  oc get po -n <USER_NAME>-test -w
  ```

    <div class="highlight" style="background: #f7f7f7">
    <pre><code class="language-python">
    $ oc get po -n user2-test -w
    NAME                                      READY   STATUS    RESTARTS   AGE
    canopy-backend-6785f999cf-946fx           1/1     Running   0          15m
    canopy-ui-568d7cd989-zsqbx                1/1     Running   0          4h9m
    milvus-test-attu-5dd559c7dd-xtgzc         1/1     Running   0          2m14s
    milvus-test-standalone-67585987cd-k72b7   1/1     Running   0          2m14s
    </code></pre>
    </div>

  _watch을 중단하려면 `Ctrl + C`를 누르세요._

1. 각 Milvus 배포에는 이전에 경험했던 것과 마찬가지로 Attu가 포함되어 있습니다. 방금 배포한 test 환경의 Attu를 확인해보고 싶다면 👇

    ```
    https://milvus-test-attu-<USER_NAME>-test.<CLUSTER_DOMAIN>
    ```
    연결하려면 Milvus Address를 아래와 같이 업데이트하세요:

    ```bash
    http://milvus-test.<USER_NAME>-test.svc.cluster.local:19530
    ```

    ![milvus-attu-connect.png](./images/milvus-attu-connect.png)

    보시다시피 완전히 비어 있지만, 곧 자동화된 방식으로 이를 채워보겠습니다 🔨

# 🦙 OGX (Open GenAI Stack) - 통합 프레임워크

지금까지 Canopy는 항상 모델과 직접 통신했습니다 — 단일한 하드코딩된 엔드포인트였죠. 프롬프트를 보내고 응답을 받는 것만 필요했을 때는 그것만으로도 충분했습니다.

RAG에는 벡터 데이터베이스라는 두 번째 구성 요소가 필요합니다. 팀이나 요구 사항에 따라 사용하는 벡터 데이터베이스가 달라질 수 있지만, 애플리케이션 코드는 구체적인 제품에 의존하지 않는 편이 좋습니다.

**OGX**(Open GenAI Stack, 이전 이름 Llama Stack)는 여러분의 애플리케이션과 RAG 인프라 사이에 위치합니다. vector store 작업을 위한 통합 API를 제공하므로, 데이터베이스 백엔드를 교체하는 작업이 애플리케이션 코드 변경이 아니라 OGX의 설정 변경으로 끝나게 됩니다. OGX는 Milvus, Chroma, pgvector, Qdrant, Weaviate 등 16개의 vector store 공급자를 기본적으로 지원합니다.

공급자 이동성 외에도, OGX는 직접 구축하기 어려운 RAG 기능들도 제공합니다:

- **Hybrid search(하이브리드 검색)** — 벡터 유사도 검색과 키워드 검색을 하나의 쿼리에서 결합하여, 실제 콘텐츠에 대한 검색 품질을 크게 향상시킵니다
- **Contextual chunking(컨텍스트 기반 청킹)** — 문서를 토큰 수로 단순히 나누는 대신, LLM이 저장되기 전에 각 chunk를 주변 컨텍스트로 보강하여 검색 정확도를 훨씬 높입니다
- **Multiple embedding models(다중 embedding 모델)** — 애플리케이션 코드를 변경하지 않고도 nomic-embed, BGE, MiniLM, 또는 어떤 sentence-transformers 모델이든 전환할 수 있습니다

이번 실습에서 모든 기능을 사용하지는 않지만 필요할 때 확장할 수 있습니다. 자세한 내용은 [OGX 검색 기능 문서](https://ogx-ai.github.io/docs/concepts/file_operations_vector_stores#search-capabilities)에서 확인하세요.

이제 Canopy에서 사용할 OGX(Llama Stack)를 배포합니다.

(살짝 힌트를 드리면: 여러분의 Gen AI Playground는 처음부터 OGX를 사용하고 있었습니다 🥳)

1. 다른 도구들을 배포했던 것과 같은 방식으로 실험 환경에 빠르게 배포해보겠습니다. Openshift console에서 다시 왼쪽 메뉴의 `Helm` 섹션을 펼치고, `Releases`를 클릭한 뒤 `<USER_NAME>-canopy` 프로젝트에 있는지 확인하세요. 그런 다음 우측 상단에서 `Create Helm Release`를 선택합니다.

    ![llama-stack-helm-release.png](./images/llama-stack-helm-release.png)

2. Chart Repositories 목록에서 `GenAIOps Helm Charts`를 선택하고 `Llama Stack Operator Instance`를 고릅니다.

    ![llama-stack-helmchart.png](./images/llama-stack-helmchart.png)

3. Canopy frontend에 했던 것과 마찬가지로 Llama Stack에도 LLM 엔드포인트를 제공해야 합니다. 이 helm chart에는 이미 적절한 기본값이 들어 있습니다. `models` 아래에 다음 값들이 올바르게 설정되어 있는지, 그리고 RAG가 활성화되어 있는지 확인하세요:

    - name: `llama32`
    - url: `http://llama-32-predictor.ai501.svc.cluster.local:8080/v1`
    - rag: `enabled:true`

..그리고 `Create`를 클릭합니다.

4. 여러분의 환경에서 Llama Stack이 실행 중인지 확인해보세요:

    ![llama-stack-ocp.png](./images/llama-stack-ocp.png)

5. 최종 사용자에게는 달라지는 점이 없어야 합니다. 백엔드가 모델을 직접 호출하는 대신 OGX(Llama Stack)가 모델을 호출하며, 곧 Milvus도 같은 계층을 통해 사용합니다. `<USER_NAME>-canopy` 환경의 Canopy UI에서 정상 동작을 확인합니다.

6. `test`와 `prod`에서도 Llama Stack을 Argo CD로 배포하도록 설정해봅시다. `test/ogx/config.yaml`과 `prod/ogx/config.yaml`을 생성하세요:

    ```bash
    mkdir -p /opt/app-root/src/genaiops-gitops/canopy/test/ogx
    mkdir -p /opt/app-root/src/genaiops-gitops/canopy/prod/ogx
    touch /opt/app-root/src/genaiops-gitops/canopy/test/ogx/config.yaml
    touch /opt/app-root/src/genaiops-gitops/canopy/prod/ogx/config.yaml
    ```

    그리고 아래 설정을 각각의 `config.yaml`에 붙여넣으세요. (즉, `genaiops-gitops/canopy/test/ogx/config.yaml` 파일과 `genaiops-gitops/canopy/prod/ogx/config.yaml` 파일)

    **TEST용**:

    ```yaml
    ---
    chart_path: charts/llama-stack-operator-instance
    models:
      - name: "llama32"
        url: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
    rag:
      enabled: true
      milvus:
        service: "milvus-test"
    ``` 

    **PROD용**:

    ```yaml
    ---
    chart_path: charts/llama-stack-operator-instance
    models:
      - name: "llama32"
        url: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
    rag:
      enabled: true
      milvus:
        service: "milvus-prod"
    ``` 

7. 변경 사항을 Git에 푸시해 배포합니다. GitOps에서는 Git에 저장된 구성이 배포의 기준입니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m  "🦙 ADD - Open GenAI Stack instances 🦙"
    git push 
    ```

    이제, 직접 손으로 해볼 차례입니다!

# OGX를 통해 Milvus에 요청 보내기

backend가 OGX를 사용하도록 업데이트하기 전에, 먼저 OGX를 직접 다뤄볼 수 있는 노트북이 하나 더 있습니다.

workbench로 이동해 `experiments/5-rag/4-using-ogx.ipynb` 노트북을 따라 진행하세요.

완료했다면, RDU 학생들을 위한 자동화를 활성화해봅시다 🌳📚
