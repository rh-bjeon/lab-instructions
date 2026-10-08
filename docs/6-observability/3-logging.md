# 📝 Logging: 상세한 이야기

메트릭이 "얼마나?"와 "얼마나 빠르게?"에 답한다면, 로그는 "정확히 무슨 일이 일어났는가?"에 답합니다. 로그는 무엇이, 언제, 어떤 맥락에서 일어났는지를 정확히 담아내는 상세한 기록입니다.

## LokiStack을 위한 로그 수집

OpenShift의 내장 로깅은 LokiStack을 사용해 애플리케이션이 STDOUT 또는 STDERR로 쓰는 모든 것을 자동으로 수집합니다. 별도의 설정이 필요하지 않습니다. 각 노드에서 실행되는 수집기(collector)를 통해 로그가 수집되고, 시계열 JSON 형태로 LokiStack에 색인됩니다.

Canopy가 로그에서 무엇을 말하고 있는지 살펴봅시다.

1. **OpenShift Console → Observe → Logs**로 이동합니다.

   ![OpenShift Logging Interface](./images/logging1.png)

   기본적으로는 접근 권한이 있는 모든 네임스페이스에 있는 모든 애플리케이션의 로그가 표시됩니다. 클러스터 운영자에게는 유용하지만, 특정 애플리케이션에 집중하고 싶을 때는 너무 많은 정보가 뒤섞여 있습니다.

2. 테스트 환경의 Canopy만 필터링해 봅시다. **Show Query**를 클릭하고 아래 LogQL 쿼리를 붙여 넣습니다.

   ![show-query.png](./images/show-query.png)
   
   ```logql
   { log_type="application", kubernetes_pod_name=~"canopy-backend.*", kubernetes_namespace_name="<USER_NAME>-canopy" }
   ```

   <!-- This LogQL query uses:
   - `log_type="application"`: Only application logs (not infrastructure/system logs)
   - `kubernetes_pod_name=~"canopy-ui.*"`: Regex matching any canopy-ui pod
   - `kubernetes_namespace_name="<USER_NAME>-test"`: Your test environment namespace -->

3. **Run Query**를 클릭해 Canopy의 최근 로그가 실시간으로 스트리밍되는 것을 확인합니다.

   ![Filtered Canopy Logs](./images/logging2.png)

   로그는 타임스탬프, 파드 이름, 실제 로그 메시지와 함께 표시됩니다. 스크롤하면서 특정 텍스트를 검색하고, 애플리케이션 동작의 패턴을 확인할 수 있습니다.

이는 중요한 문제 하나를 해결해 줍니다. **컨테이너 로그는 일시적**(ephemeral)이라는 점입니다. 컨테이너가 재시작되면(충돌, 재배포, 스케일 다운 등) 다른 곳에 수집되어 있지 않은 한 그 로그는 사라집니다. LokiStack은 관련된 파드가 이미 사라졌더라도 몇 시간 또는 며칠 전의 문제를 조사할 수 있게 해줍니다.

## 로그 수집이 중요한 이유

Canopy가 새벽 2시에 충돌해서 자동으로 재시작되더라도, LokiStack 덕분에 무엇이 충돌을 일으켰는지 여전히 조사할 수 있습니다. LokiStack은 다음을 수행하기 때문입니다.

- 모든 컨테이너에서 자동으로 로그를 지속적으로 수집함
- Kubernetes 메타데이터(네임스페이스, 파드, 컨테이너)로 로그를 색인함
- 설정된 보존 기간 동안 로그를 저장함
- 모든 환경과 시간대에 걸쳐 검색 가능하게 만듦

## 커스텀 로그 생성 및 조회하기

실제 문제를 디버깅하는 과정을 시뮬레이션하기 위해, 의도적으로 로그를 생성한 다음 찾아봅시다.

1. **OpenShift Console → Workloads -> Pods**에서, `<USER_NAME>-canopy` 네임스페이스에 있는 Canopy UI 파드의 Terminal에 연결해 명령을 내부에서 실행합니다.

   ![Logs](./images/logging1.1.png)

2. 컨테이너 내부에서 커스텀 로그 메시지를 생성합니다.

   ```bash
   echo "🪄🪄🪄🪄" >> /tmp/custom.log
   tail -f /tmp/custom.log > /proc/1/fd/1 &
   echo "🪄🪄🪄🪄" >> /tmp/custom.log
   echo "🪄🪄🪄🪄" >> /tmp/custom.log
   echo "🪄🪄🪄🪄" >> /tmp/custom.log
   echo "🪄🪄🪄🪄" >> /tmp/custom.log
   exit
   ```

   이는 로그 파일을 생성하고 이를 STDOUT(프로세스 1의 파일 디스크립터 1)으로 파이프하며, OpenShift의 로깅 에이전트가 이를 자동으로 캡처합니다.

3. `Aggregated Logs` 탭에서 최근 로그를 확인하거나(Show Query 버튼에서) 커스텀 메시지를 직접 조회해 봅니다.

   ```logql
   { log_type="application", kubernetes_pod_name=~"canopy-ui.*", kubernetes_namespace_name="<USER_NAME>-canopy" } |= `🪄🪄🪄🪄` | json
   ```

   ![Custom Log Messages](./images/logging3.png)

방금 문제를 디버깅할 때 벌어지는 일을 그대로 시뮬레이션해 보았습니다. 무엇을 찾아야 하는지 알고 있다면(이번 경우는 라마 이모지, 실제 상황이라면 오류 메시지 등), 그것이 정확히 언제 어디서 발생했는지 로그를 조회해 찾아낼 수 있습니다.

<!-- ## Logs vs. Metrics: When to Use Each (Move to Slides)

**Use metrics for:**
- Quantitative measurements (request rate, latency, error percentage)
- Alerting (when error rate exceeds threshold)
- Trends over time (is performance improving or degrading?)
- Low-cardinality data (service-level aggregates)

**Use logs for:**
- Detailed context (what specific error occurred?)
- Debugging (what sequence of events led to this problem?)
- High-cardinality data (user-specific, query-specific details)
- Audit trails (who did what when?)

**Use them together:**
- Metrics alert you to a problem: "Error rate spiked to 10%"
- Logs tell you what the errors are: "RAG service timeout connecting to Milvus"
- Traces show you where: "Milvus search span taking 30+ seconds" -->

## 🎯 다음 단계: 요청의 여정 따라가기

로그는 개별 구성 요소 안에서 일어난 일을 보여주지만, 현대의 AI 시스템은 분산되어 있어서 학생의 질문 하나가 여러 서비스를 거쳐갑니다. 시스템 전체를 통과하는 요청의 전체 여정을 어떻게 볼 수 있을까요?

바로 여기서 분산 트레이싱(distributed tracing)이 등장합니다. **[Tracing](6-observability/4-tracing.md)** 으로 이동해 요청이 Canopy의 아키텍처를 어떻게 거쳐가는지 살펴봅시다 🔍