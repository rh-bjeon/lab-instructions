# 🔍 Enable Monitoring

프로덕션 GenAI 시스템의 맥락에서 observability(관측 가능성)란 AI 애플리케이션이 생성하는 데이터를 살펴봄으로써 그 내부에서 무슨 일이 벌어지고 있는지 이해할 수 있는 능력을 의미합니다. 교실을 관찰하는 선생님을 떠올려 보세요. 학생들이 집중하고 있는지, 어려움을 겪고 있는지, 잘 따라오고 있는지를 파악해야 합니다.

observability가 없으면 프로덕션에서 AI를 운영하는 것은 눈을 가리고 비행하는 것과 같습니다. 사용자가 불만을 제기해야 비로소 문제가 있다는 것을 알게 되죠. 제대로 된 observability가 있다면 학생들에게 영향을 미치기 전에 문제를 발견하고 빠르게 해결할 수 있습니다.

## Observability의 세 가지 기둥 (Three Pillars)

현대의 observability는 서로 보완적인 세 가지 데이터 유형에 기반합니다.
  - **Metrics** 📊 - 시간에 따른 정량적 측정값(응답 지연 시간, 요청 비율, 오류 비율, 첫 토큰까지의 시간 등).

  - **Logs** 📝 - 애플리케이션에서 나오는 상세한 이벤트 기록(오류 메시지, 사용자 요청, 시스템 이벤트 등).

  - **Traces** 🔍 - 분산 서비스를 거치는 요청 경로(학생의 질문이 Canopy의 마이크로서비스, MCP 도구, LLM을 어떻게 거쳐가는지).

이 세 가지 기둥이 모여 Canopy의 동작을 완전히 들여다볼 수 있게 해줍니다. 그럼 Canopy에서 observability를 활성화하는 방법을 살펴봅시다!

## Red Hat AI Observability Stack

Red Hat OpenShift AI는 [중앙화된 플랫폼 observability](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.0/html/managing_openshift_ai/managing-observability_managing-rhoai)를 제공합니다. 이는 OpenShift AI 인스턴스와 사용자 워크로드의 상태 및 성능을 모니터링하기 위한 통합된 out-of-the-box 솔루션입니다.

이 사전 구성된 observability 스택은 세 가지 핵심 구성 요소를 포함합니다. 표준화된 텔레메트리 데이터 수집을 위한 **OpenTelemetry Collector (OTC)**, 메트릭 저장 및 알림을 위한 **Prometheus**, 그리고 분산 트레이싱을 위한 **Red Hat build of Tempo**입니다.

![Obsv 0](./images/obs0.png)

이 아키텍처는 OpenShift AI 플랫폼 구성 요소에 대한 상태 메트릭과 알림을 제공하는 동시에, **Grafana**와 같은 외부 observability 도구와의 통합 지점도 제공합니다.

> **사전 구성된 인프라:** OpenTelemetry Collector, Prometheus, Tempo를 포함한 RHOAI Observability 스택은 이 실습 환경을 위해 이미 배포 및 구성되어 있습니다. Canopy 구성 요소(UI, Backend)와 LlamaStack은 이러한 수집기로 텔레메트리 데이터를 자동으로 전송하도록 instrumentation(계측)되어 있습니다.

## 🔍 OpenTelemetry: Observability의 표준

Red Hat OpenShift AI는 분산 트레이싱과 메트릭 수집을 위한 오픈소스 표준인 **OpenTelemetry**(OTel)를 사용합니다. OpenTelemetry는 다음을 제공합니다.

* 일반적인 프레임워크(Flask, FastAPI, Express 등)를 위한 **자동 instrumentation**
* 애플리케이션에 특화된 작업을 위한 **수동 instrumentation**
* 어떤 트레이싱 백엔드와도 동작하는 **벤더 중립적 형식**
* 완전한 observability를 위한 **메트릭 및 로그와의 통합**

### OpenTelemetry 🔍 와 LlamaStack 🦙

LlamaStack은 **meta-reference telemetry provider**를 통해 내장된 [OpenTelemetry 지원](https://llamastack.github.io/docs/building_applications/telemetry#configuration)을 제공하며, 이는 추론(inference) 작업을 자동으로 계측하여 트레이스와 메트릭을 포함한 observability 데이터를 생성합니다. auto-injection을 사용하는 Canopy의 구성 요소와 달리, LlamaStack의 텔레메트리는 환경 변수를 통해 직접 구성됩니다.

**LlamaStack Telemetry의 동작 방식:**

텔레메트리가 활성화되면, LlamaStack은 각 추론 요청마다 자동으로 span을 생성하고 토큰 사용량 메트릭을 내보냅니다. 각 요청은 다음을 생성합니다.
- **Traces**: 타이밍 데이터와 함께 추론 요청의 흐름을 보여주는 분산 트레이스
- **Metrics**: `model_id`와 `provider_id`로 레이블링된 토큰 카운터(`llama_stack_prompt_tokens_total`, `llama_stack_completion_tokens_total`, `llama_stack_tokens_total`)

LlamaStack 배포의 텔레메트리 구성에는 다음이 포함됩니다.

  <div class="highlight" style="background: #f7f7f7; overflow-x: auto; padding: 8px;">
  <pre><code class="language-yaml"> 
  env:
    - name: OTEL_SERVICE_NAME
      value: llamastack-user1-canopy  # Identifies this instance
    - name: OTEL_EXPORTER_OTLP_ENDPOINT
      value: http://data-science-collector-collector-headless.redhat-ods-monitoring:4318
    - name: TELEMETRY_SINKS
      value: otel_trace, otel_metric  # Enables both traces and metrics
  </code></pre>
  </div>

이 환경 변수들은 LlamaStack을 다음과 같이 구성합니다.
1. OTLP(포트 4318)를 통해 텔레메트리 데이터를 RHOAI OpenTelemetry Collector로 내보냄
2. 포괄적인 observability를 위해 트레이스와 메트릭 sink를 모두 활성화함
3. Tempo와 Prometheus에서 필터링할 수 있도록 모든 텔레메트리에 서비스 이름을 태그함

> **참고**: OpenTelemetry는 [LlamaStack Helm chart](https://github.com/rhoai-genaiops/genaiops-helmcharts/blob/main/charts/llama-stack-operator-instance/templates/lls-distribution.yaml#L15)에 사전 구성되어 있으므로, 추가 설정 없이도 메트릭과 트레이스가 자동으로 수집됩니다.

## 🎯 다음 단계: 메트릭 이해하기

RHOAI Observability 플랫폼과 OpenShift User Workload Monitoring이 구성되면서, 이제 vLLM(토큰 생성, 지연 시간), LlamaStack(토큰 사용량), Canopy UI/Backend(HTTP 요청, 응답 시간)로부터 메트릭을 수집하고 있습니다. 다음 섹션에서는 Prometheus에서 이러한 메트릭을 조회하고, 시각화를 위해 Grafana를 배포하며, 대시보드를 해석해 AI 스택의 성능을 이해하는 방법을 배웁니다.

**[Metrics](6-observability/2-metrics.md)**로 이동해 여러분의 AI 스택이 성능에 대해 무엇을 알려주는지 살펴봅시다.