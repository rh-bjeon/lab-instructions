# 🔍 Tracing: 여정 따라가기

학생이 Canopy에게 "양자 얽힘(quantum entanglement)을 설명해줘"라고 물으면, 이 단순한 질문 하나가 여러 서비스를 거치는 복잡한 춤을 유발합니다.

시간이 어디에서 소요되는지 어떻게 알 수 있을까요? 어느 서비스가 병목인가요? 오류는 실제로 어디에서 시작되었나요? **분산 트레이싱**(Distributed tracing)은 전체 시스템에 걸쳐 점들을 연결함으로써 이러한 질문에 답하고, 각 요청의 전체 여정을 보여줍니다.

## 분산 트레이싱 이해하기

캠퍼스에서 학생 한 명을 하루 종일 따라다닌다고 생각해 보세요. 도서관에서 실험실로, 그리고 오피스 아워까지. 어디에서 가장 많은 시간을 보내는지, 어디서 막히는지, 어떤 경로를 거치는지 알 수 있을 것입니다(물론 전혀 섬뜩하지 않은, 가정에 불과한 방식으로요). 분산 트레이싱은 Canopy의 마이크로서비스를 거쳐가는 요청에 대해 바로 이 일을 해줍니다.

각 서비스는 **span**(수행된 작업의 기록)을 내보내도록 코드를 계측합니다. 이 span에는 다음이 포함됩니다.
- **Operation name**: 수행된 작업이 무엇인지(예: "RAG query", "LLM inference")
- **Duration**: 얼마나 걸렸는지(병목을 찾는 데 핵심적인 정보)
- **Parent span**: 이 작업을 트리거한 것이 무엇인지(요청 트리를 구성함)
- **Attributes**: 사용자 ID, 쿼리 텍스트, 검색된 문서, 생성된 토큰 수와 같은 메타데이터

span들이 부모-자식 관계로 연결되면 **trace**(학생의 질문부터 Canopy의 답변까지, 단일 요청의 전체 이야기)를 형성합니다.

![Example Trace Visualization](./images/tracing0.png)

이 트레이스 시각화에서는 다음을 보여주는 waterfall 뷰를 확인할 수 있습니다.
- 전체 요청 시간과 각 서비스의 비중
- 어떤 작업이 순차적으로 실행되고 어떤 작업이 병렬로 실행되는지
- 시간이 가장 많이 소요된 곳(가장 긴 막대)
- 부모-자식 관계(트리 구조)


## MLflow를 이용한 Auto Tracing

MLflow에는 autologging이라는 기능이 있어서, 활성화해 두면 관련된 모든 요청을 자동으로 캡처합니다.
여기서는 이를 사용해 백엔드에서 모델과 통신할 때 사용하는 모든 OpenAI 호출을 캡처할 것입니다.
MLflow에서 이미 트레이스를 본 적이 있지만, 이번에는 MLflow가 캡처하는 타임라인 데이터도 함께 살펴보겠습니다.
지금은 비교적 단순한 트레이싱이지만, 에이전트까지 다루게 되면 훨씬 복잡한 트레이싱을 보게 될 것입니다 🤖

1. OpenShift AI -> Develop & train -> Experiments (MLflow) -> <USER_NAME>-test project로 이동합니다.

2. summarization 또는 information-search 실험 중 하나를 선택합니다. Information Search 쪽이 트레이싱이 조금 더 많지만, 둘 다 괜찮습니다.

3. Traces로 들어가서 방금 보낸 가장 최근 트레이스를 선택하고 `Details & Timelines`로 이동합니다.

   ![trace-timeline.png](./images/trace-timeline.png)

4. 여기서 모든 span과 관련 메타데이터를 포함한 트레이스의 전체 분석을 볼 수 있습니다.
   여기저기 클릭해보면서 각 span에 무엇이 기술되어 있는지 확인해 보세요. `Completions` 아래를 보면 어떤 모델이 사용되었는지에 대한 정보도 찾을 수 있습니다.

   ![model-name-completions.png](./images/model-name-completions.png)

5. `Timeline` 버튼을 눌러 각 span이 얼마나 걸렸는지에 대한 전체 분석도 확인할 수 있습니다.

   ![timeline-breakdown.png](./images/timeline-breakdown.png)


이 트레이스는 MLflow가 직접 볼 수 있는 span만 캡처한다는 점에 유의하세요. 예를 들어 여기에는 OGX나 프론트엔드가 포함되어 있지 않습니다.
MLflow 바깥에 있는 스택 부분에 대한 정보를 더 추가하려면, 자동 또는 수동으로 해당 부분들을 `instrument`(계측)해야 합니다.
하지만 지금 우리에게 필요한 정보는 MLflow가 모두 제공해 주고 있으므로, 여기서는 추가적인 instrumentation을 하지 않겠습니다.

이제 observability의 세 가지 기둥인 metrics, logs, traces가 모두 갖춰졌습니다. 하지만 AI 시스템에서 중요한 신호가 하나 더 있습니다. 바로 **사용자 피드백**입니다. 고객이 AI의 응답에 만족하고 있는지 어떻게 알 수 있을까요?