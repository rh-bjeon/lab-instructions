## 📚 EXTRA CREDITS 🤓

### 사전 구성된 대시보드 살펴보기

여러분이 배포한 Grafana 인스턴스에는 전체 AI 스택을 모니터링하기 위한 여러 사전 구성된 대시보드가 포함되어 있습니다. 공유 vLLM 모델, Canopy UI, Canopy Backend, 그리고 LlamaStack입니다.

### Dashboard 1: vLLM Shared Model Performance

이 대시보드는 모든 사용자가 의존하는 공유 llama-3.2 추론 서비스의 상태와 성능을 보여줍니다. 요청 수와 응답 시간에 초점을 맞추는 전통적인 웹 애플리케이션과 달리, LLM 시스템은 AI 워크로드의 고유한 특성을 반영하는 특화된 메트릭이 필요합니다.

아래 단계를 시도하기 전에 CLI를 통해 OpenShift에 로그인되어 있는지 확인하세요. OpenShift에 로그인하려면 웹 콘솔로 이동해 계정 이름을 클릭하고 "Copy Login Command"를 선택한 다음, 해당 명령어를 사용해 터미널에서 로그인합니다.

AI 특화 성능 메트릭을 보려면 **vLLM AI501 Metrics Dashboard**를 엽니다.

   ![Metrics Dashboard](./images/metrics2.1.png)

   **Token Throughput Metrics:**
   - **Generation Token Throughput (TPS)**: 모델이 초당 몇 개의 토큰을 생성하고 있는지 보여줍니다. 이는 응답이 얼마나 빠르게 스트리밍되는지를 측정하는 값으로, TPS가 높을수록 답변이 더 빨리 완성됩니다. 피크 시간대에는 TPS가 저하되지 않도록 신경 써야 합니다. 이는 API 처리량만을 측정하는 것이 아니라 모델의 텍스트 생성 속도를 측정하기 때문에 전통적인 "초당 요청 수"와는 근본적으로 다릅니다.
   - **Prompt Token Throughput**: 초당 처리되는 프롬프트 토큰 수(요청량과 컨텍스트 크기 추세를 나타냄)
   - **Scheduler State**: 실행 중, 대기 중, 또는 스왑된 요청 수. 대기열이 많다는 것은 공유 모델이 과부하 상태라는 신호이며, 전통적인 stateless API에는 존재하지 않는 중요한 신호입니다.

   ![Metrics Dashboard](./images/metrics2.2.png)

   **Request Characteristics - 컨텍스트 이해하기:**
   - **Request Prompt Length**: 프롬프트 크기 분포를 보여주는 히트맵입니다. 얼마나 많은 대화 기록을 유지하고 있나요? 더 긴 컨텍스트는 더 나은 답변을 제공하지만 더 많은 메모리를 소비하고 추론 속도를 늦춥니다.
   - **Request Generation Length**: 응답 크기 분포를 보여주는 히트맵

   **Resource and Scheduler Metrics:**
   - **KV Cache Utilization**: attention 캐싱을 위한 메모리 사용량(값이 높으면 추론이 느려질 수 있음). 이는 어텐션 메커니즘의 "K"(key)와 "V"(value) 행렬이 재계산을 피하기 위해 캐시되는 트랜스포머 모델에 고유한 지표입니다.
   - **Successfully Processed Requests**: 종료 이유별 분류(EOS 토큰 도달 vs 최대 길이 도달)

   **Latency Metrics - AI 사용자 경험:**
   - **E2E Request Latency**: 요청부터 완료까지의 엔드투엔드 시간(p50, p90, p95, p99 백분위수). 전통적인 웹 앱에서는 이 하나만 측정할 수도 있지만, LLM에서는 이를 더 세분화해야 합니다.
   - **Time To First Token (TTFT)**: 모델이 응답을 시작하는 데 걸리는 시간. 체감 응답성에 영향을 줍니다.
   - **Time Per Output Token**: 생성 중 토큰 간 지연 시간(스트리밍 속도에 영향을 주고 텍스트가 얼마나 부드럽게 나타나는지를 결정함)

<!-- **Why These AI-Specific Metrics Matter:** Beyond basic infrastructure metrics (CPU, memory), these measurements reflect the unique characteristics of LLM workloads. They distinguish monitoring an AI system from monitoring a traditional web application - your Canopy backend might have great API response times, but if the underlying model has poor TTFT or low TPS, the user experience suffers. -->

### Dashboard 2: Canopy-UI Metrics

Canopy UI는 사용자가 질문하고 답변을 받는 사용자 대면 인터페이스, 즉 웹 애플리케이션입니다. 이 대시보드는 프론트엔드가 얼마나 잘 동작하고 있는지를 보여줍니다.

<!-- > For your Canopy application components ([UI](https://github.com/rhoai-genaiops/frontend/blob/main/chart/templates/deployment.yaml#L21) and [Backend](https://github.com/rhoai-genaiops/backend/blob/main/chart/templates/deployment.yaml#L17)), metrics collection requires an additional label. The Canopy Helm charts have already been configured with `monitoring.opendatahub.io/scrape: 'true'` in their deployment templates, which tells Prometheus to scrape metrics from these workloads. This label is essential for custom applications, without it, Red Hat OpenShift AI Observability stack won't collect their metrics even if they expose them. -->

<!-- TODO: Add autoinstrumentation explanation also here. Canopy UI/Backend relies also in the auto-instrumentation to publish some metrics -->

1. Grafana에서 **Dashboards → Browse → `<USER_NAME>-toolings Canopy Dashboards`**로 이동합니다.

2. **Canopy UI Metrics Dashboard**를 엽니다.

   > **Tip**: 메트릭이 적게 보인다면 시간 범위를 1~3시간으로 확장하세요. 시간 선택기는 대시보드 오른쪽 위 모서리에 있습니다.

   ![Metrics Dashboard](./images/metrics1.2.png)

3. **메트릭을 보기 위한 트래픽 생성하기**: 대시보드가 비어 있다면, test 환경에서 Canopy UI를 열고 상호작용해 보세요.

   예를 들어 긴 텍스트를 복사해서 붙여넣고 **Summarize** 버튼을 3~5번 클릭합니다. 이는 전체 스택(UI → Backend → LlamaStack)을 거치는 트래픽을 생성하고 "Backend Request Duration"을 포함한 모든 패널을 채워줍니다.

   Prometheus가 메트릭을 스크랩할 때까지 10~15초 기다린 다음, Grafana 대시보드를 새로고침합니다.

4. 대시보드에는 다음이 표시됩니다.

   ![Metrics Dashboard](./images/metrics3.png)

   **High-Level Stats (맨 위 행):**
   - **Total Requests (Last Hour)**: UI가 처리한 HTTP 요청 수
   - **Average Response Time**: UI 응답에 대한 p50 지연 시간(좋은 UX를 위해서는 500ms 미만이어야 함)
   - **Error Rate (%)**: 실패한 요청의 비율(1% 미만이어야 함)
   - **Active Requests**: 현재 처리 중인 요청 수

   **Request Patterns:**
   - **Request Rate (req/sec)**: UI로 들어오는 트래픽의 실시간 뷰
   - **Response Time Percentiles**: 시간에 따른 p50, p95, p99 지연 시간(급증 여부를 확인)

   **Health Indicators:**
   - **HTTP Status Codes**: 2xx, 4xx, 5xx 응답의 분포
   - **Backend Request Duration**: UI에서 백엔드로의 호출이 얼마나 걸리는지(p95)

UI 대시보드는 사용자 경험을 이해하는 데 도움이 됩니다. 여기서 지연 시간이나 오류율이 높다는 것은 백엔드와 모델이 건강하더라도 사용자가 나쁜 경험을 하고 있다는 의미입니다.

### Dashboard 3: Canopy-Backend Metrics

Canopy Backend는 UI와 LlamaStack 간의 호출을 조율하는 API 계층입니다. 이 대시보드는 백엔드의 성능과 병목을 드러냅니다.

1. 같은 Grafana 폴더에서 **Canopy Backend Metrics Dashboard**를 열어 다음을 확인합니다.

   **High-Level Stats (맨 위 행):**
   - **Total API Requests (Last Hour)**: 백엔드 API 호출량
   - **API Response Time (p95)**: 백엔드 엔드포인트의 95번째 백분위 지연 시간
   - **Error Rate (%)**: 실패한 API 호출의 비율
   - **Active Requests**: 현재 백엔드 요청 큐 깊이

   ![Metrics Dashboard](./images/metrics3.1.png)

   **Endpoint Performance:**
   - **Request Rate by Endpoint**: 어떤 API 엔드포인트가 가장 많은 트래픽을 받고 있는지
   - **Response Time by Endpoint (p95)**: 엔드포인트별 지연 시간 분석(느린 API를 식별하는 데 도움)
   - **Endpoint Performance Summary**: 엔드포인트별 요청률, 지연 시간, 오류율을 보여주는 테이블 뷰

   **External Service Metrics:**
   - **LLM Call Duration (Outbound to llamastack)**: 공유 vLLM 모델에 대한 호출이 얼마나 걸리는지(p50, p95, p99)
   - **HTTP Status Distribution**: 백엔드로부터의 성공 응답 대 오류 응답

   ![Metrics Dashboard](./images/metrics3.2.png)

백엔드 대시보드는 성능 문제를 디버깅하는 데 매우 중요합니다.

---

⚠️⚠️  이 대시보드는 아직 작업 중입니다. 곧 다시 찾아올게요. ⚠️ ⚠️ 

### Dashboard 4: LlamaStack Token Metrics

LlamaStack은 Canopy Backend와 vLLM 사이의 LLM 호출을 조율하며, OpenTelemetry를 통해 토큰 사용량을 추적합니다. 그런데 왜 여기의 메트릭은 vLLM과 다를까요? LlamaStack은 특히 여러분의 애플리케이션의 토큰 사용량을 추적하는 반면, vLLM은 전체 인프라 부하를 보여주기 때문입니다. `ai501`의 vLLM 모델은 공유되고 있으므로, 이 대시보드들은 서로 다른 관점을 보여줍니다.

1. **LlamaStack Metrics Dashboard**를 엽니다.

   > **Tip**: 메트릭이 적게 보인다면 시간 범위를 1~3시간으로 확장하세요.

2. **메트릭을 보기 위한 트래픽 생성하기**: 대시보드가 비어 있다면, code-server 터미널에서 추론 요청을 생성해 보세요.

   ```bash
   for i in {1..10}; do echo "Request $i:"; curl -s -X POST "http://llama-stack-service.<USER_NAME>-canopy.svc.cluster.local:8321/v1/chat/completions" -H "Content-Type: application/json" -d '{"model":"llama32","messages":[{"role":"user","content":"Hello, how are you?"}],"stream":false}' | jq -r '.usage.total_tokens // "error"'; sleep 2; done
   ```

   이는 LlamaStack 인스턴스로 10개의 non-streaming 요청을 보냅니다. 메트릭은 60초마다 배치로 처리되므로, 1분 정도 기다린 다음 대시보드를 새로고침해서 토큰 수를 확인하세요.

   ![Metrics Dashboard](./images/metrics4.png)

   **Dashboard Panels:**
   - **Token Usage Overview**: 총, 프롬프트, 완성(completion) 토큰(지난 1시간) 및 실시간 비율(토큰/초)
   - **Token Processing Rate**: 프롬프트, 완성, 전체 토큰 처리량을 보여주는 시계열 그래프
   - **Cumulative Token Usage**: 배포 이후 누적된 총량
   - **Model Summary Table**: 모델/provider별 토큰 분류

   > **⚠️ 제한 사항**: LlamaStack telemetry는 non-streaming 추론 요청만 추적하며([#3981](https://github.com/llamastack/llama-stack/issues/3981)), 에이전트나 safety check 같은 다른 API는 계측하지 않습니다([#2596](https://github.com/llamastack/llama-stack/issues/2596)). Canopy의 streaming 트래픽은 여기에 나타나지 않습니다.

<!-- ## Understanding the Metrics Flow

Your AI assistant spans four layers, each with its own metrics:

**1. Canopy-UI (`<USER_NAME>-canopy` namespace)** - The student-facing frontend
- Metrics show: request rate, response time, HTTP status codes
- **What it tells you**: Are students having a good experience?

**2. Canopy-Backend (`<USER_NAME>-canopy` namespace)** - The backend
- Metrics show: endpoint performance, outbound call duration, error rates
- **What it tells you**: Where are bottlenecks in your application logic?

**3. LlamaStack (`<USER_NAME>-canopy` namespace)** - The AI orchestration layer
- Metrics show: token usage (prompt/completion), processing rate, model-specific throughput
- **What it tells you**: How efficiently are you using LLM tokens? What's the prompt-to-completion ratio?

**4. Shared vLLM Model (ai501 namespace)** - The inference engine
- Metrics show: token throughput, latency, queue depth, cache usage
- **What it tells you**: Is the shared model healthy and responsive? -->
