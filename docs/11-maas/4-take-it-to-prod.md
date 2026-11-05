# 운영 환경에 _안전하게_ 적용하기

## Sealed Secrets

GitOps에서는 Git에 기록된 선언을 배포 상태의 기준으로 삼습니다. 그렇다면 API 키처럼 민감한 값은 어떻게 Git에서 관리해야 할까요? Kubernetes `Secret`은 값을 base64로 인코딩할 뿐 암호화하지 않으므로 누구나 디코딩할 수 있습니다. 따라서 `Secret` 매니페스트를 그대로 저장해서는 안 됩니다. 이 문제를 해결하기 위해 오픈 소스 도구인 Sealed Secrets를 사용합니다.

Sealed Secrets는 `kubeseal` 유틸리티로 Kubernetes 시크릿을 암호화합니다. 생성된 `SealedSecret`은 클러스터의 컨트롤러만 복호화할 수 있으므로 암호화된 매니페스트를 Git에 저장할 수 있습니다.

### 실제로 Sealed Secrets 사용해보기

API 키를 담은 `SealedSecret`을 만들면 Sealed Secrets 컨트롤러가 대상 네임스페이스에 일반 OpenShift `Secret`을 생성합니다. Llama Stack은 이 `Secret`에서 API 키를 읽습니다.

이를 위해, 봉인해야 할 시크릿이 무엇인지 알려줘야 합니다:

1. 워크벤치로 돌아가서 먼저 API 키를 변수로 노출시킵니다:
   
    ```bash
    api_token="paste-your-key-from-MaaS-here"
    ```

    그런 다음 아래 명령어를 실행합니다:

    ```bash
    cat << EOF > /tmp/test-api-token.yaml
    apiVersion: v1
    data:
      api_token: "$(echo -n ${api_token} | base64 -w0)"
    kind: Secret
    metadata:
      name: llama-fp8-maas-token
    EOF
    ```

2. `kubeseal` 명령으로 시크릿을 봉인합니다. 클러스터의 Sealed Secrets 컨트롤러가 가진 인증서를 사용해 암호화하며, 컨트롤러는 실습 환경에 이미 배포되어 있습니다.

    <p class="warn">
        ⛷️ <b>참고</b> ⛷️ - Kubeseal 명령어를 실행했을 때 "Error: cannot get sealed secret service: Unauthorized" 오류가 발생하면, OpenShift에 다시 로그인하고 명령어를 다시 실행하세요.
    </p>

    ```bash
    export CLUSTER_DOMAIN=<CLUSTER_DOMAIN>
    oc login --server=https://api.${CLUSTER_DOMAIN##apps.}:6443 -u <USER_NAME> -p <PASSWORD>
    ```

    ```bash
    kubeseal < /tmp/test-api-token.yaml > /tmp/sealed-test-api-token.yaml \
    -n <USER_NAME>-test \
    --controller-namespace ai501 \
    --controller-name sealed-secrets \
    -o yaml
    ```

3. 시크릿이 봉인되었는지 확인합니다:

    ```bash
    cat /tmp/sealed-test-api-token.yaml
    ```

    이제 시크릿이 봉인된 것을 볼 수 있어야 하며, 이제 리포지토리에 저장해도 안전합니다. 다음과 비슷하게 보일 것이지만, 더 긴 출력일 것입니다.

    <div class="highlight" style="background: #f7f7f7">
    <pre><code class="language-yaml">
    apiVersion: bitnami.com/v1alpha1
    kind: SealedSecret
    metadata:
      creationTimestamp: null
      name: llama-fp8-maas-token
      namespace: <USER_NAME>-test
    spec:
      encryptedData:
        api_token: AgAj3JQj+EP23pnzu...
    ...
    </code></pre></div>

4. 이 봉인 작업의 결과, 특히 `encryptedData`를 가져와서 git에 추가하고자 합니다. 우리는 이미 <span style="color:blue;">[헬퍼 helm 차트](https://github.com/redhat-cop/helm-charts/tree/master/charts/helper-sealed-secrets)</span>를 작성해두었으며, 이를 사용해 반복 가능한 방식으로 sealed secret을 클러스터에 추가할 수 있습니다. 다음 단계에서 이 차트에 `encryptedData` 값을 제공할 것입니다.

    ```bash
    cat /tmp/sealed-test-api-token.yaml| grep api_token
    ```

    <div class="highlight" style="background: #f7f7f7">
    <pre><code class="language-yaml">
        api_token: AgAj3JQj+EP23pnzu...
    </code></pre></div>

5. `genaiops-gitops/canopy/test`를 열고 `sealed-secrets`라는 폴더를 만든 다음, 그 아래에 `config.yaml` 파일을 만듭니다.

    ```bash
    mkdir /opt/app-root/src/genaiops-gitops/canopy/test/sealed-secrets
    touch /opt/app-root/src/genaiops-gitops/canopy/test/sealed-secrets/config.yaml
    ```

6. `sealed-secrets/config.yaml` 파일을 열고 아래 yaml을 `config.yaml`에 붙여넣습니다.

    먼저, 아래 내용을 복사하세요:

    ```yaml
    ---
    repo_url: https://github.com/redhat-cop/helm-charts.git
    chart_path: charts/helper-sealed-secrets
    ```

    그런 다음, 이전에 얻은 암호화된 비밀번호로 `config.yaml` 파일을 확장합니다:

    ```yaml
    secrets:
      # Additional secrets can be added to this list when necessary
      - name: llama-fp8-maas-token
        type: Opaque
        data:
          api_token: AgAj3JQj+EP23pnzu...
    ```

6. 이 변경 사항을 push하고, Llama Stack에게 그곳에서 API 키를 사용하라고 요청하기 전에 test 환경에 API 키가 있는지 확인합시다.

  ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "🤫 ADD - sealed secret for API token 🤫"
    git push
    ```

### 👩‍🏫 Canopy 업데이트하기

먼저 test부터 해봅시다.

1. `genaiops-gitops/canopy/test/ogx/config.yaml`을 열고 Llama Stack에게 API 토큰을 어디서 가져올지 알려줍니다. 또한, LiteMaaS에서 얻은 모델 이름과 엔드포인트 URL도 제공해야 합니다. 목록에 모델을 추가해서 업데이트하세요:

    ```yaml
    ---
    chart_path: charts/llama-stack-operator-instance
    models:
      - name: "llama32"
        url: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
      - name: "llama32-fp8"   
        url: "http://llama-32-fp8-predictor.ai501.svc.cluster.local:8080/v1" 
      - name: "Llama-3.2-3B-Instruct-FP8"     # 👈 ADD THIS ❗︎❗︎
        url: "https://litemaas-litellm-<USER_NAME>-maas.<CLUSTER_DOMAIN>/v1" # 👈 ADD THIS ❗︎❗︎❗︎❗︎
    rag:                  
      enabled: true
    mcp:                
      enabled: true 
    sealed_secrets:  # 👈 ADD THIS ❗︎❗︎❗︎❗︎
      enabled: true    # 👈 ADD THIS ❗︎❗︎❗︎❗︎
      secretName: llama-fp8-maas-token  # 👈 ADD THIS ❗︎❗︎❗︎❗︎
    ```

  네, _왜 API 키를 Git에 push하는 거지? 이건 옳지 않은 것 같은데!_라고 생각하는 것이 지당합니다. 우리도 전적으로 동의합니다. 시크릿 관리에 대한 이야기로 곧 돌아올 것을 약속합니다!


3. 이제 `backend`를 업데이트해봅시다. `genaiops-gitops/canopy/test/backend/config.yaml`을 열고 `llama32-fp8`로 되어 있는 부분을 모두 MaaS에서 제공하는 `Llama-3.2-3B-Instruct-FP8`로 변경합니다(같은 모델이며, MaaS 게이트웨이를 통해 노출되는 것뿐입니다).

    ```yaml
    repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
    chart_path: chart
    summarization:
      enabled: true
      model: vllm-Llama-3.2-3B-Instruct-FP8/Llama-3.2-3B-Instruct-FP8 # 👈 Update this  ❗︎❗︎
      endpoint: "http://llama-stack-service:8321/v1"
      mlflow_prompt: summarization
      mlflow_prompt_version: latest
    information-search:
      enabled: true
      endpoint: "http://llama-stack-service:8321/v1"
      model: vllm-Llama-3.2-3B-Instruct-FP8/Llama-3.2-3B-Instruct-FP8 # 👈 Update this  ❗︎❗︎
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
      model: vllm-Llama-3.2-3B-Instruct-FP8/Llama-3.2-3B-Instruct-FP8 # 👈 Update this  ❗︎❗︎
      temperature: 0.1
      vector_db_id: latest
      mcp_calendar_url: "http://canopy-mcp-calendar-mcp-server:8080/sse"
      mlflow_prompt: student-assistant
      mlflow_prompt_version: latest        
    ```

4. 이제 변경 사항을 push합니다:

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "🎄 Add FP8 from MaaS 🎄"
    git push
    ```

    backend를 변경하면 어떤 일이 일어나는지 기억하시나요? 맞습니다! 평가(Evaluation) 파이프라인이 시작됩니다! OpenShift console > Pipelines > Pipeline Runs로 이동해서 `<USER_NAME>-toolings` 네임스페이스 아래에서 평가 과정을 관찰해보세요.

5. 원한다면, **prod** 파일에도 동일한 단계를 따라 하면 production Canopy도 MaaS로 전환할 수 있습니다!

---

**이번 실습에서 한 일:** Sealed Secrets로 API 토큰을 암호화해 Git에서 안전하게 관리했습니다. 이어서 백엔드가 MaaS에서 제공하는 `Llama-3.2-3B-Instruct-FP8` 모델을 사용하도록 설정해, 애플리케이션 코드를 바꾸지 않고 LiteLLM 게이트웨이로 전환했습니다. 변경 사항을 Git에 푸시하면 평가 파이프라인이 자동으로 실행되어 모델 교체를 배포 전에 검증합니다. 배포 정의는 Git에서 관리하되 민감한 값은 암호화하는 GitOps 흐름입니다.
