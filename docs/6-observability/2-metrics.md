# 📊 Metrics: 중요한 것을 측정하기

## RHOAI Observability Stack에서 vLLM 메트릭 살펴보기

시각화 도구를 배포하기 전에, Prometheus에서 메트릭을 직접 조회해 보는 것이 유익합니다. 이렇게 하면 데이터를 대시보드로 추상화하기 전에 원시 데이터를 먼저 이해할 수 있습니다.

여기서는 여러분 모두가 `ai501` 네임스페이스에 배포된 **하나의 llama-3.2 모델을 공유**합니다. 이 공유 모델은 모든 사람의 CanopyUI 애플리케이션에 대한 LLM 백엔드 역할을 합니다.

<!-- Why share a model? Running large language models requires significant GPU resources. By deploying one shared inference service, the lab environment can support many students simultaneously without requiring dedicated GPUs for each user. Your Canopy application sends requests to this shared vLLM endpoint, which processes them and returns generated text. -->

이 공유 모델을 구동하는 vLLM 추론 엔진은 토큰 생성, 요청 처리, 모델 성능에 대한 메트릭을 자동으로 노출합니다. 이 모델이 OpenShift AI의 관리형 인프라에 속해 있기 때문에, 이러한 메트릭은 자동으로 Prometheus로 흘러들어갑니다.

> 기술적인 세부 사항이 궁금하다면, [여기](https://github.com/rhoai-genaiops/deploy-lab/blob/main/student-content/templates/cloud-model/inferenceservice.yaml#L33)에서 InferenceService 구성을 확인할 수 있습니다. 이는 llama-3.2 모델이 어떻게 배포되고 노출되는지를 정의합니다.

### RHOAI Prometheus에서 vLLM 메트릭 살펴보기

Prometheus는 공유 vLLM 모델이 배포된 이후부터 메트릭을 계속 수집해 왔습니다. 이를 Grafana로 시각화하기 전에, 먼저 직접 조회해서 원시 메트릭이 어떤 모습인지 이해해 봅시다.

1. `Observe` > `Metrics`로 이동해 `ai501` 네임스페이스의 OpenShift Metrics Dashboard를 엽니다.

   ![ai501-metrics.png](./images/ai501-metrics.png)

2. 쿼리 박스에 아래 PromQL 쿼리를 입력하고 Enter를 누르거나(또는 "Run Queries"를 클릭해) 공유 모델이 생성한 총 토큰 수를 확인합니다.

   ```promql
   vllm:generation_tokens_total{namespace="ai501"}
   ```

   ![Obsv 1](./images/obs1.png)

   이는 공유된 llama-3.2 모델이 모든 사용자에 걸쳐 생성한 누적 토큰 수를 보여줍니다. 실습 전체가 제공하고 있는 AI 지원의 양을 가늠할 수 있는 지표입니다.

   _참고: "Access restricted" 경고가 보일 수 있지만, 이는 단순히 화면상의 표시일 뿐이며 메트릭 쿼리 자체에는 영향을 주지 않습니다._

3. 아래 쿼리로 공유 모델의 요청 성공률을 확인합니다.

   ```promql
   rate(vllm:request_success_total{namespace="ai501"}[5m])
   ```

   ![Obsv 2](./images/obs2.png)

   이는 공유 추론 서비스의 초당 성공 요청 수를 보여줍니다. 갑작스러운 하락은 모든 사용자에게 영향을 주는 모델 또는 인프라 문제를 의미합니다.

## Grafana로 메트릭 시각화하기

Prometheus 쿼리는 조사를 위해서는 강력하지만, Grafana 대시보드는 팀의 모든 사람이 메트릭에 쉽게 접근할 수 있게 해줍니다. 시스템이 정상인지 확인하기 위해 PromQL을 직접 작성하고 싶은 사람은 없을 겁니다!

RHOAI Observability 스택은 플랫폼 전역의 메트릭을 수집하지만, 이는 Canopy 배포에 대한 애플리케이션 특화 인사이트를 드러내지 않는 범용 인프라 신호일 뿐입니다. AI 어시스턴트와 관련해 중요한 것들 - 토큰 사용 패턴, LLM 지연 시간, 백엔드 API 성능 - 을 시각화하려면, 네임스페이스와 구성 요소에 특화된 필터로 Prometheus를 조회하는 커스텀 Grafana 대시보드가 필요합니다.

### Grafana 배포하기

Canopy의 엔드투엔드 observability 여정을 지원하기 위해 toolings 네임스페이스에 Grafana 인스턴스를 배포해 봅시다. GitOps 워크플로를 통해 `genaiops-gitops/toolings/`에 설치합니다.

1. `toolings` 아래에 `grafana` 폴더를 만듭니다. 그다음 `grafana` 폴더 아래에 `config.yaml`이라는 파일을 만듭니다. 또는 아래 명령어를 그대로 실행해도 됩니다.

    ```bash
    mkdir /opt/app-root/src/genaiops-gitops/toolings/grafana
    touch /opt/app-root/src/genaiops-gitops/toolings/grafana/config.yaml
    ```

2. `grafana/config.yaml` 파일을 열고 아래 줄을 붙여 넣어 Argo CD에게 어떤 차트를 배포할지 알려줍니다.

    ```yaml
    ---
    chart_path: charts/grafana
    ```

3. 이전에 했던 것처럼 변경 사항을 저장소에 커밋합니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "📈 Grafana added 📈"
    git push
    ```

4. 이 변경 사항이 동기화되면(Argo CD에서 확인할 수 있습니다), [여기](https://canopy-grafana-route-<USER_NAME>-toolings.<CLUSTER_DOMAIN>)를 클릭해 Grafana에 로그인하고 Canopy를 위해 미리 정의된 대시보드를 확인합니다. 또는 code-server workbench 터미널에서 아래 명령어를 실행할 수도 있습니다.

    ```bash
    # get the route and open it in your browser
    echo https://$(oc get route canopy-grafana-route --template='{{ .spec.host }}' -n <USER_NAME>-toolings)
    ```

    OpenShift 자격 증명을 사용하고 `Allow selected permissions`를 클릭해 로그인합니다.

> ArgoCD가 동기화 중 멈춘다면, Synching을 클릭하고 sync를 Terminate한 다음, `canopy-grafana-sa-token` 오브젝트의 점 3개를 클릭해 해당 CR 오브젝트에 대한 sync를 수동으로 트리거하세요.

   ![Grafana Issue 1](./images/grafana-argocd-issue.png)

5. Prometheus 데이터 소스에 대한 연결을 생성합니다. **Connections** → **Data sources**로 이동한 다음 **UWM Prometheus**를 선택하고 아래로 스크롤해 **Save & test**를 클릭합니다.

   ![Grafana Data Source 1](./images/grafana-data-source1.png)

   ![Grafana Data Source 2](./images/grafana-data-source2.png)

   _데이터 소스가 보이지 않는다면, 아직 동기화되지 않은 것입니다. 페이지를 몇 번 새로고침해 보세요 :)_


6. 대시보드를 보려면 **Dashboards** → **Browse**로 이동해 `<USER_NAME>-toolings Canopy Dashboards` 폴더를 찾습니다.

   ![Obsv 1](./images/metrics1.png)

   _모든 대시보드가 보이지 않는다면, 아직 동기화되지 않은 것입니다. 페이지를 몇 번 새로고침해 보세요 :)_

7. **Canopy Backend Metrics Dasboard**를 클릭한 다음, 데이터 소스로 `UWM Prometheus`를 선택해 백엔드 서비스 메트릭 대시보드를 확인합니다.

   ![Select Datasource](./images/dashboard-ds.png)

   `UWM Prometheus` 데이터 소스를 선택하는 방식으로 다른 대시보드들도 비슷하게 살펴볼 수 있습니다. 해당 서비스를 아직 호출하지 않았다면 일부 대시보드는 비어 있을 수 있다는 점을 참고하세요.

대시보드를 더 깊이 살펴보고 싶다면 [Extra Credits](6-observability/6-extra-credit-metrics-dashboard) 섹션을 확인해 보세요 🤓


## 🎯 다음 단계: 로그로 동작 이해하기

메트릭은 **얼마나**, **얼마나 빠르게**를 알려주지만, 애플리케이션 내부에서 **무슨 일이 일어나고 있는지**는 알려주지 않습니다. 메트릭이 문제(성공률 하락, 지연 시간 급증)를 보여줄 때, 무엇이 잘못되었는지에 대한 자세한 정보가 필요합니다.

이를 위해서는 로그가 필요합니다. 로그는 Canopy 동작 중 발생하는 모든 이벤트의 상세한 기록입니다. **[Logging](3-logging.md)** 으로 이동해 Canopy의 로그를 수집하고 조회하는 방법을 배워봅시다 📝