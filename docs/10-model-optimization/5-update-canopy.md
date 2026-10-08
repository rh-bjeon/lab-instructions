# 🔄 Canopy가 압축된 Llama 3.2 FP8 모델을 사용하도록 업데이트하기

실험 환경을 Tiny Llama에서 FP8 모델을 가리키도록 바꿔봅시다. 동일한 단계를 거칠 것입니다.

## 🦙 Llama Stack 설정 업데이트

1. **OpenShift Console** → **Helm** → **Releases**로 이동해서 `<USER_NAME>-canopy` 프로젝트에 있는 `llama-stack-operator-instance` 릴리스를 찾습니다.

2. 릴리스를 클릭하고 **Upgrade**를 선택합니다.

    ![fp8-llama-upgrade.png](./images/fp8-llama-upgrade.png)

3. 이전에 TinyLlama에 했던 것처럼, 양자화된 Llama 3.2 FP8 모델을 Llama Stack의 또 다른 모델 엔드포인트로 추가합니다. 이렇게 하면 클라우드 모델, TinyLlama, 그리고 이 새 모델에 모두 접근할 수 있게 됩니다.

    Form view에서 `Add models`를 클릭해서 `models` 아래에 추가합니다:

    - **Model Name**: `llama32-fp8`
    - **Model URL**: `http://llama-32-fp8-predictor.ai501.svc.cluster.local:8080/v1`
    - **Token**: (비워 둡니다)

4. 변경 사항을 적용하려면 **Upgrade**를 클릭합니다.

    ![fp8-llama-upgrade2.png](./images/fp8-llama-upgrade2.png)

5. 이제 `backend`가 이 새로 사용 가능해진 모델을 가리키도록 설정해봅시다 😌 **OpenShift Console** → **Helm** → **Releases**에서 `canopy-backend`를 찾습니다.

    ![fp8-backend-upgrade.png](./images/fp8-backend-upgrade.png)

6. `llama32` 및/또는 `tinyllama`로 되어 있는 부분을 모두 `llama32-fp8`로 변경해야 합니다. 그리고 `max_token`도 다시 늘릴 수 있습니다. `summarize`의 경우:

    ```yaml
    summarization:
      enabled: true
      mlflow_prompt_version: latest
      mlflow_prompt: summarization
      endpoint: 'http://llama-stack-service:8321/v1'
      max_tokens: 2048 # 👈 update this ❗️❗️❗️
      model: vllm-llama32-fp8/llama32-fp8 # 👈 update this ❗️❗️❗️
    ```

7. 변경 사항을 적용하려면 **Upgrade**를 클릭합니다.

    ![fp8-backend-upgrade2.png](./images/fp8-backend-upgrade2.png)

### 🌳 새 모델로 Canopy 테스트하기

Llama Stack과 backend가 실행되면, 양자화된 모델과 통신할 수 있는지 확인해봅시다.

1. [Canopy UI](https://canopy-ui-<USER_NAME>-canopy.<CLUSTER_DOMAIN>)로 이동해서 요약 기능을 테스트합니다. 원한다면 이전 챕터의 터키 차에 관한 텍스트를 복사해서 사용해도 됩니다 ☕️

2. 양자화된 모델로부터 응답을 받게 되는데, 여전히 양자화되지 않은 모델을 사용하는 것 같은 느낌이 들 것입니다 😌 그러니 왜 test와 production 환경으로 가져가는 것을 미루고 있을까요?

### Test와 Prod를 On-Prem으로 전환하기 🦙

1. 먼저 Llama Stack 설정을 업데이트해봅시다. 워크벤치로 돌아가서 **test**용 `genaiops-gitops/canopy/test/ogx/config.yaml`을 열고 새 모델 이름과 모델 URL을 추가합니다:

    ```yaml
    ---
    chart_path: charts/llama-stack-operator-instance
    models:
      - name: "llama32"
        url: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
      - name: "llama32-fp8"     # 👈 Add this ❗︎❗︎
        url: "http://llama-32-fp8-predictor.ai501.svc.cluster.local:8080/v1" # 👈 Add this ❗︎❗︎
    rag:
      enabled: true
      milvus:
        service: "milvus-test"
    ```

2. 이제 `backend`를 업데이트해봅시다. `genaiops-gitops/canopy/test/backend/config.yaml`을 열고 `llama32`로 되어 있는 부분을 모두 `llama32-fp8`로 변경합니다.

    ```yaml
    repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
    chart_path: chart
    summarization:
      enabled: true
      model: vllm-llama32-fp8/llama32-fp8 # 👈 Update this  ❗︎❗︎
      endpoint: "http://llama-stack-service:8321/v1"
      mlflow_prompt: summarization
      mlflow_prompt_version: latest
    information-search:
      enabled: true
      endpoint: "http://llama-stack-service:8321/v1"
      model: vllm-llama32-fp8/llama32-fp8 # 👈 Update this  ❗︎❗︎
      vector_db_id: genaiops_2026_09_30_10_24
      mlflow_prompt: information-search
      mlflow_prompt_version: latest
    feedback:
      enabled: false
    ab_testing:
      enabled: false
    shields: 
      enabled: true
      endpoint: http://canopy-guardrails/v1
      model: llama32
      config: canopy-guardrails
    student-assistant: 
      enabled: true
      model: vllm-llama32-fp8/llama32-fp8 # 👈 Update this  ❗︎❗︎
      temperature: 0.1
      vector_db_id: latest
      mcp_calendar_url: "http://canopy-mcp-calendar-mcp-server:8080/sse"
      mlflow_prompt: student-assistant
      mlflow_prompt_version: latest
    ```

3. 변경 사항을 push합니다:

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "🏦 Switch to FP8 🏦"
    git push
    ```

    backend를 변경하면 어떤 일이 일어나는지 기억하시나요? 맞습니다! 평가(Evaluation) 파이프라인이 시작됩니다! OpenShift console > Pipelines > Pipeline Runs로 이동해서 `<USER_NAME>-toolings` 네임스페이스 아래에서 평가 과정을 관찰해보세요.

4. **prod** 파일에도 동일한 단계를 따라 하면 production Canopy도 on-prem으로 전환할 수 있습니다!

---

## 달성한 것

축하합니다! RDU가 학생들을 서빙하는 방식을 완전히 바꿔놓았습니다. 다음은 여러분이 달성한 내용입니다:

- **양자화 기본 원리 숙달** — 이제 정밀도 형식(FP16, INT8, INT4) 간의 트레이드오프를 이해하고, 압축 전략에 대해 정보에 기반한 결정을 내릴 수 있습니다
- **직접 모델 압축** — llm-compressor를 사용해 GPTQ 양자화를 적용하고, 모델이 능력을 잃지 않으면서도 축소되는 모습을 직접 확인했습니다
- **벤치마크로 품질 검증** — lm-evaluation-harness를 사용해 압축된 모델이 여전히 프로덕션 기준을 충족한다는 것을 증명하는 방법을 배웠습니다
- **GitOps를 통한 배포** — Canopy가 FP8 양자화된 Llama 3.2 3B 모델을 사용하도록 업데이트하고, CI/CD 파이프라인을 통해 변경 사항을 push했습니다

### RDU가 얻은 것

온프레미스 양자화 모델로 전환함으로써, Redwood Digital University는 몇 가지 중요한 성과를 얻었습니다:

| 이점 | 영향 |
|---------|--------|
| **데이터 주권** | 학생들의 질의와 학술 데이터가 RDU의 인프라를 벗어나지 않습니다 — 외부 API 호출도, 제3자에게 데이터가 노출되는 일도 없습니다 |
| **비용 절감** | FP8 모델은 FP16 대비 약 절반의 GPU 메모리를 사용하므로, RDU는 동일한 하드웨어로 더 많은 학생을 서빙하거나 인프라 비용을 줄일 수 있습니다 |
| **지연시간 감소** | On-prem 추론은 외부 API로의 네트워크 왕복을 없애므로, 학생들에게 더 빠른 응답을 제공합니다 |
| **운영 제어력** | RDU가 전체 스택을 소유합니다 — 벤더 종속(vendor lock-in)도, 예상치 못한 API 지원 종료도, 사용량 기반 가격의 갑작스런 변동도 없습니다 |
| **지속가능성** | 더 작은 모델은 추론당 에너지 소비가 적어, 품질을 유지하면서도 RDU의 탄소 발자국을 줄입니다 🌳🌳🌳🌳|

결론: RDU는 이제 더 빠르고, 더 저렴하면서도 학생 데이터를 있어야 할 곳—캠퍼스 내—에 정확히 유지하는 프로덕션급 AI 어시스턴트를 운영하고 있습니다.

