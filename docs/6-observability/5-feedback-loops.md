# 🔄 Feedback Loops

메트릭은 시스템이 *얼마나 빠르게* 동작하는지 알려줍니다. 로그는 *무슨 일이 일어났는지* 알려줍니다. 트레이스는 *시간이 어디서 소요되었는지* 알려줍니다. 하지만 이들 중 어느 것도 가장 중요한 질문에는 답하지 못합니다. **사용자가 실제로 AI의 응답에 만족하고 있는가?**

사용자 피드백은 GenAIOps 루프를 완성하는 빠진 조각입니다. 사용자로부터 좋아요/싫어요 신호를 수집함으로써, AI가 어디서 성공하고 어디서 실패하는지에 대한 직접적인 증거를 얻을 수 있습니다. 그리고 그 증거를 평가 파이프라인에 다시 반영해 시스템을 체계적으로 개선할 수 있습니다.

## 피드백이 중요한 이유

이런 시나리오를 생각해 봅시다. Canopy의 요약(summarization) 기능이 훌륭한 지연 시간(메트릭은 건강해 보임)을 보이고, 로그에도 오류가 없으며, MLFlow를 거치는 트레이스도 깔끔합니다. 인프라 관점에서는 모든 것이 *괜찮아 보입니다*. 하지만 일부 프롬프트에서는 시스템 프롬프트가 특정 유형의 입력에 잘 맞게 튜닝되어 있지 않아서 사용자들이 계속 저품질 요약을 받고 있고, 이 사용 사례를 평가(evals)에서 포착하지 못하고 있으며 여러분은 이 사실조차 모르고 있습니다!

사용자 피드백이 없다면 절대 알 수 없었을 것입니다. 지금까지 배운 observability의 기둥들(메트릭, 로그, 트레이스)은 **시스템 상태**를 모니터링합니다. 피드백은 **출력 품질**을 모니터링하는데, 이것이야말로 AI 애플리케이션에서 궁극적으로 중요한 것입니다.

피드백 루프는 observability를 실제 행동과 연결합니다.

1. AI 애플리케이션을 **배포**(Deploy)합니다.
2. 그 동작을 **관찰**(Observe)합니다(메트릭, 로그, 트레이스).
3. 사용자로부터 **피드백을 수집**(Collect feedback)합니다.
4. 부정적인 피드백을 테스트 케이스로 사용해 **평가**(Evaluate)합니다.
5. 평가 결과를 바탕으로 프롬프트나 모델을 **개선**(Improve)합니다.
6. **재배포**(Redeploy)하고 반복합니다.

## Feedback 기능 활성화하기

이 코스 전반에서 활성화해 온 다른 Canopy 기능들과 마찬가지로, 피드백 기능도 feature flag 뒤에 숨겨져 있습니다.

간단하게 하기 위해 바로 `test` 환경에서 이를 수행해 봅시다.

1. workbench에서 `genaiops-gitos` 저장소로 이동해, `canopy/test/backend/config.yaml`을 수정하여 feedback을 활성화합니다. 먼저 최신 변경 사항을 pull합니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    ```

   그리고 `canopy/test/backend/config.yaml` 마지막에 아래 블록을 추가해 수정합니다.

   ```yaml
   feedback:
     enabled: true
   ```

   아래와 같은 모습이 되어야 합니다.

      ```yaml
      ---
      repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
      chart_path: chart
      summarization:
        enabled: true
        model: llama32
        endpoint: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
        mlflow_prompt: summarization
        mlflow_prompt_version: latest
      information-search:         
        enabled: true
        endpoint: "http://llama-stack-service:8321/v1"
        model: vllm-llama32/llama32
        vector_db_id: genaiops_2026_05_25_21_39
        mlflow_prompt: information-search
        mlflow_prompt_version: latest
      feedback:  # 👈 add this block 📚❗︎❗︎❗︎❗︎❗︎
        enabled: true
      ```

   
2. 변경 사항을 커밋하고 push합니다. ArgoCD가 배포를 동기화할 때까지 기다립니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git add .
    git commit -m  "🫶 Enable feedback collection 🫶"
    git push origin main
    ```

3. test 환경에서 Canopy UI를 열고 **Summarization**을 선택합니다.

   ```bash
   https://canopy-ui-<USER_NAME>-test.<CLUSTER_DOMAIN>/
   ```
4. 텍스트를 붙여넣고 **Summarize**를 클릭합니다.

   ```bash
   Collecting constant user feedback is one of the most reliable ways to make sure you're building the right thing—and building it well. It helps you validate assumptions early, catch usability issues before they turn into costly rework, and prioritize improvements based on real-world needs instead of internal guesses. A steady feedback loop also builds trust—when users see their input reflected in updates, they feel heard and become more willing to engage, which strengthens adoption and creates a virtuous cycle of better insights and better outcomes.
   ```

5. 요약이 나타난 후, **"Was this summary helpful?"** 라는 문구와 함께 좋아요/싫어요 버튼이 보일 것입니다 👍👎

   만족스럽지 않은 요약에는 싫어요를 클릭하세요 🥺 👎

   잘 된 요약에는 좋아요를 클릭하세요 🥹 👍

   _트레이스가 MLflow에 등록되는 데 시간이 걸릴 수 있으므로, UI가 "Thanks for the feedback!"라고 표시하기까지 잠시 시간이 걸릴 수 있습니다._

   > ⚠️ **참고:** 이것이 보이지 않거나 오류가 발생하면, OpenShift에서 `<USER_NAME>-test` 네임스페이스 안의 `canopy-ui` 파드를 재시작하세요. 가장 쉬운 방법은 파드를 삭제하는 것입니다.
   ![delete-pod-for-feedback.png](./images/delete-pod-for-feedback.png)

6. 데이터를 좀 더 만들기 위해 몇 번 더 시도해 보고, 좋아요/싫어요를 눌러본 다음 결과를 살펴봅시다!

   ![canopy-feedback.png](./images/canopy-feedback.png)

## MLflow에서 피드백 확인하기

Canopy는 이미 트레이싱을 위해 MLflow를 사용하고 있으므로, 피드백은 해당 응답을 생성한 트레이스에 **직접** 저장됩니다. 별도의 시스템이 필요 없습니다. 각각의 👍 또는 👎는 정확히 해당 span에 첨부된 `user_satisfaction` assessment가 됩니다.

1. OpenShift AI Dashboard로 이동합니다. Develop & train > Experiments (MLflow)로 이동해 프로젝트로 **<USER_NAME>-test**를, 실험으로 **summarization**을 선택한 다음 **Traces**로 이동합니다.

2. 각 대화가 하나의 트레이스로 표시됩니다. 아무 트레이스나 클릭해 열어봅니다.

3. 트레이스 상세 뷰에서 **Assessments** 패널을 찾습니다. `user_satisfaction` 피드백이 `True`(좋아요) 또는 `False`(싫어요)로 표시되어 있는 것을 볼 수 있습니다.

   ![mlflow-trace-feedback.png](./images/mlflow-trace-feedback.png)

4. `Traces` 뷰에 `user_satisfaction` 컬럼을 추가해서 좀 더 전반적인 느낌을 파악할 수도 있습니다.

이것이 강력한 이유는 피드백이 전체 프롬프트, 응답, 지연 시간, 모델 메타데이터 바로 옆에 자리하고 있기 때문입니다.

   ![mlflow-trace-feedback-2.png](./images/mlflow-trace-feedback-2.png)

## 피드백에서 평가(Evaluations)로

피드백을 수집하는 것은 이야기의 절반에 불과합니다. 진짜 가치는 부정적인 피드백을 사용해 AI 시스템을 개선하는 데서 나옵니다. 이제 싫어요가 눌린 응답들이 MLflow에서 트레이스로 보이게 되었으니, 이를 바로 평가 데이터셋으로 전환할 수 있습니다.

1. 가장 먼저 해야 할 일은 시스템 프롬프트를 개선해서 이 찡그린 얼굴들을 웃는 얼굴로 바꾸는 것입니다. 프롬프트 최적화에는 여러 접근 방식이 있습니다. (지금 우리가 하고 있는) 수동 반복(iteration)부터 [DSPy](https://dspy.ai/)나 [MLflow의 prompt engineering 도구](https://mlflow.org/docs/latest/llms/prompt-engineering/index.html) 같은 자동화된 기법까지요. 더 구체적으로 작성하거나, 예시를 추가하거나, 톤을 조정하는 것 같은 단순한 수동 변경만으로도 큰 차이를 만들 수 있습니다.

하지만 여기에 함정이 있습니다. 개선한 프롬프트가 이미 잘 작동하던 케이스에서 *회귀(regress)*하지 않는다는 것을 어떻게 알 수 있을까요? 바로 이 때문에 부정적인 피드백을 평가 테스트 케이스로 전환하는 것입니다. 싫어요가 눌린 항목들은 회귀 테스트가 되어, 프롬프트를 조정할 때 나쁜 케이스를 고치면서도 좋은 케이스를 망가뜨리지 않았는지 검증할 수 있게 해줍니다.

2. MLflow에서 트레이스를 부정적인 피드백(Assessment `user_satisfaction = false`)으로 필터링합니다. 이것들이 바로 문제가 있는 케이스들입니다.

3. 이전에 했던 것처럼 이 트레이스들로부터 평가 데이터셋을 구축합니다. 그 트레이스 중 하나를 선택하고, 더 나은 요약과 같은 `expected_result` assessment를 가진 `expectation`을 생성합니다. 그런 다음 이를 평가 데이터셋에 추가합니다.

   ![mlflow-add-trace-expectation-evals.png](./images/mlflow-add-trace-expectation-evals.png)

4. 그다음 `Create dataset`을 클릭하고 이름을 `eval`로 지정합니다. 그런 다음 이 `eval` 데이터셋을 선택해 트레이스들을 `Export`합니다.

   ![mlflow-add-trace-evals-2.png](./images/mlflow-add-trace-evals-2.png)

   ![mlflow-add-trace-evals-3.png](./images/mlflow-add-trace-evals-3.png)

   _워크벤치에서 아래 단계를 실행해 `mlflow.genai.create_dataset()`을 통해 해당 트레이스들로부터 평가 데이터셋을 만들 수도 있습니다. 피드백을 반영하고 싶을 때 유용한 방식입니다. 하지만 지금은 참고 자료로만 공유하는 것이니 참고만 해두세요 😊:_

   ```python
   # In your notebook or evaluation script
   negative_traces = mlflow.search_traces(
      experiment_names=["summarization"],
      filter_string="assessments.user_satisfaction.value = 'false'",
   )

   eval_dataset = mlflow.genai.create_dataset(
      name="eval",
      experiment_id=experiment.experiment_id,
      tags={"source": "negative-user-feedback"},
   )
   eval_dataset.merge_records(negative_traces)
   ```

4. human-in-the-loop로서, 사용자가 만족하지 못했던 응답을 검토하고 각 케이스에 대해 좋은 요약은 어떤 모습이어야 하는지를 expectation으로 추가합니다. 이는 실제 사용자의 불만족을 구체적인 테스트 케이스로 전환시켜 줍니다.

5. 이제 시스템 프롬프트를 반복 개선해 봅시다. OpenShift AI Dashboard > Gen AI studio > Prompts > **<USER_NAME>-toolings** > summarization에서 요약 프롬프트를 변경하고 새 버전을 만듭니다.

6. 여기서 새 프롬프트를 생성하면 어떤 일이 벌어지는지 기억하시나요? 맞습니다! 평가 파이프라인이 실행되어, 방금 만든 것을 포함해 우리가 가진 모든 평가 데이터셋에 대해 돌아갑니다!

7. 파이프라인이 성공적으로 끝나면, **<USER_NAME>-toolings** 아래의 MLflow Evaluation runs에서 결과를 확인할 수 있습니다.

## A/B 테스트: 데이터 기반 프롬프트 엔지니어링

좋아요/싫어요 피드백을 수집하면 사용자가 *만족하는지*는 알 수 있지만, *어떤 시스템 프롬프트가 더 나은지*는 알 수 없습니다. A/B 테스트는 동일한 사용자 입력을 두 개의 서로 다른 시스템 프롬프트에 동시에 통과시키고 사용자가 더 나은 응답을 선택하게 함으로써 이 문제를 해결합니다.

어떤 프롬프트가 더 나은 요약을 만드는지 추측하는 대신, 실제 사용자가 직접 결정하도록 합니다. 프로덕션 ML 시스템이 모델 변형을 비교하는 방식과 비슷합니다.

이는 **champion/challenger** 패턴을 사용합니다. 현재 프롬프트가 **champion**(오늘 사용자가 받고 있는 것)이고, 테스트하고 싶은 새 프롬프트가 **challenger**입니다. 두 프롬프트 모두 MLflow Prompt Registry에 존재합니다.

### Champion/Challenger 프롬프트 설정하기

1. 먼저, 현재 프롬프트를 MLflow에서 **champion**으로 표시합시다. **<USER_NAME>-toolings** 프로젝트의 `summarization`에서 현재 프롬프트 버전에 `champion` 별칭(alias)을 추가합니다.

   ![champ-prompt.png](./images/champ-prompt.png)

2. 이제 challenger 프롬프트를 만들고 새 버전으로 등록합니다. 새 버전은 자동으로 `latest` 별칭을 갖게 됩니다. `champion` 별칭은 그대로 유지됩니다.

3. A/B 테스트를 활성화하기 위해 `genaiops-gitops/canopy/test/backend/config.yaml`을 수정합니다. Prompt A는 `champion`을 가리키게 하고, A/B 설정에서는 `latest`를 challenger로 사용하도록 설정합니다.

   ```yaml
   summarization:
     enabled: true
     model: llama32
     endpoint: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
     mlflow_prompt: summarization
     mlflow_prompt_version: champion  # 👈 ❗︎❗︎❗︎ pin to champion for A/B ❗︎❗︎❗︎❗︎❗︎❗︎

   information-search:         
     enabled: true
     endpoint: "http://llama-stack-service:8321/v1"
     model: vllm-llama32/llama32
     vector_db_id: genaiops_2026_05_25_21_39
     mlflow_prompt: information-search
     mlflow_prompt_version: latest

   feedback:
     enabled: true

   ab_testing:               # 👈 ADD THIS ❗︎
     enabled: true           # 👈 ADD THIS ❗︎
     mlflow_prompt_b_version: latest  # 👈 the challenger ❗︎
   ```

4. 변경 사항을 커밋하고 push합니다. ArgoCD가 배포를 동기화할 때까지 기다립니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m  "💙 A/B Testing enabled: champion vs challenger 💚"
    git push origin main
    ```

5. Canopy UI를 다시 열고 **Summarization**을 선택합니다.

   ```bash
   https://canopy-ui-<USER_NAME>-test.<CLUSTER_DOMAIN>/
   ```

6. 텍스트를 붙여넣고 **Summarize**를 클릭합니다.

   ```bash
   Collecting constant user feedback is one of the most reliable ways to make sure you're building the right thing—and building it well. It helps you validate assumptions early, catch usability issues before they turn into costly rework, and prioritize improvements based on real-world needs instead of internal guesses. A steady feedback loop also makes product quality more resilient over time: as user expectations, workflows, and constraints change, feedback acts like an early-warning system that surfaces friction, confusion, and missing capabilities. Just as importantly, it builds trust—when users see their input reflected in updates, they feel heard and become more willing to engage, which strengthens adoption and creates a virtuous cycle of better insights and better outcomes.
   ```

7. `Summarize`를 클릭하면 두 개의 열이 나타납니다. **Response A**와 **Response B**로, 서로 다른 프롬프트로부터 동시에 스트리밍됩니다.

   ![ab-testing.png](./images/ab-testing.png)

   두 응답이 모두 완료되면 **A is better**와 **B is better** 두 개의 버튼이 나타납니다.

   _다시 한번, 트레이스가 MLflow에 등록되는 데 시간이 걸릴 수 있으므로 UI가 응답하기까지 잠시 시간이 걸릴 수 있습니다._

   > ⚠️ **참고:** 이것이 보이지 않거나 오류가 발생하면, OpenShift에서 `<USER_NAME>-test` 네임스페이스 안의 `canopy-ui` 파드를 재시작하세요. 가장 쉬운 방법은 파드를 삭제하는 것입니다.
   ![delete-pod-for-feedback.png](./images/delete-pod-for-feedback.png)

8. 선호하는 쪽을 선택하고 데이터를 좀 더 만들기 위해 몇 번 더 시도해 봅니다. 시스템은 각 트레이스에 실제로 어떤 프롬프트가 이겼는지를 `ab_preference` assessment로 MLflow에 기록합니다. (Columns 목록에서 `ab_preference`를 선택할 수 있습니다.)

9. **MLflow → Traces**로 돌아갑니다. 각 A/B 응답은 `ab_preference` assessment를 가진 자신만의 트레이스를 생성합니다. 승자는 `true`, 패자는 `false`입니다. 이것으로 트레이스를 필터링해 어떤 프롬프트가 꾸준히 이기는지 확인할 수 있습니다.

   > ⚠️ **참고:** 위치 편향(positioning bias)을 피하기 위해 프론트엔드에서 어떤 프롬프트가 A 또는 B로 표시될지는 무작위로 결정되지만, 피드백을 기록할 때는 올바른 `champion` 또는 `challenger`로 다시 매핑합니다. 즉, "A is better"를 눌러도 MLflow에서는 challenger가 승리한 것으로 보일 수 있습니다. 사용자에게는 A로 위장하고 있었지만 사실은 challenger였기 때문입니다 🥷

   ![ab_preference.png](./images/ab_preference.png)

### 데이터에 따라 행동하기

하나의 프롬프트가 여러 비교에서 꾸준히 이길 때는 다음을 수행합니다.

1. **challenger가 승리**했다면, MLflow에서 이를 `champion`으로 승격시킵니다. 프롬프트 텍스트 자체를 위해 설정 파일을 변경할 필요는 없습니다.

   실행 중인 애플리케이션은 다음 요청부터 새로운 champion을 자동으로 반영합니다.

2. 정상 운영 상태로 되돌리기 위해 `genaiops-gitops/canopy/test/backend/config.yaml`을 수정합니다. 다시 `latest`를 가리키게 하고 A/B를 비활성화합니다.

    ```yaml
    summarization:
      enabled: true
      mlflow_prompt: summarization
      mlflow_prompt_version: latest  # back to normal iteration ❗︎

    feedback:
      enabled: false                 # 👈 UPDATE THIS ❗︎

    ab_testing:
      enabled: false                  # 👈 UPDATE THIS ❗︎
    ```

3. 커밋하고 push해서 Argo CD가 재배포하도록 합니다.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git add .
    git commit -m  "🦋 Challenger promoted to champion 🦋"
    git push origin main
    ```

이는 주관적인 판단이 아니라 실제 사용자 선호에 의해 주도되는 지속적인 개선 사이클을 만들어냅니다.

## GenAIOps Lifecycle

이 섹션에서 구축한 것이 GenAIOps 라이프사이클을 완성합니다.

```
  Deploy AI App
       |
       v
  Observe (Metrics, Logs, Traces)    <-- Module 6.1-6.4
       |
       v
  Collect User Feedback              <-- This section
       |
       v
  MLflow Traces with Assessments
       |
       v
  Build Eval Dataset (Module 4)
       |
       v
  Improve Prompts / Models
       |
       v
  Redeploy (GitOps)                  <-- Module 3
       |
       '-------> back to Observe
```

이것이 데모용 AI 프로젝트와 프로덕션 AI 시스템의 근본적인 차이입니다. 프로덕션 시스템은 **사용자로부터 학습**하고 **체계적으로 개선**됩니다. 피드백을 MLflow 트레이스에 직접 연결함으로써, 무엇이 언급되었는지, 얼마나 빨랐는지, 사용자가 만족했는지를 한 곳에서 확인할 수 있고, 그 신호에서 평가 파이프라인으로 이어지는 직접적인 경로를 갖게 됩니다.

이 섹션에서는 좋아요/싫어요로 사용자 피드백을 수집했고, 이를 MLflow 트레이스에 노출시켰으며, 부정적인 피드백을 평가 테스트 케이스로 전환했고, A/B 테스트를 사용해 프롬프트를 나란히 비교했으며, GitOps를 통해 승리한 프롬프트를 승격시켰습니다. 다음으로는 **guardrails**를 사용해 AI 애플리케이션을 유해한 입력과 출력으로부터 보호하는 방법을 살펴보겠습니다.