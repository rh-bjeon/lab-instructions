# 🧪 Extra Credit: Prompt Optimization

observability 루프를 완성했습니다. 메트릭, 로그, 트레이스, 그리고 사용자 피드백이 모두 MLflow로 흘러들어가고 있습니다. 이제 그 데이터를 실제로 활용해 봅시다. 요약 프롬프트를 수동으로 조정하며 잘 되길 바라는 대신, **자동화된 프롬프트 최적화**를 사용해 실제 평가 결과를 기반으로 체계적으로 프롬프트를 개선해 봅니다.

이 섹션은 완전히 선택 사항이지만, GenAIOps가 자동화된 ML과 어떻게 만나는지 궁금하다면 바로 이 내용입니다.

## GEPA란 무엇인가?

GEPA(Generate, Evaluate, Predict, Adapt)는 MLflow의 자동화된 프롬프트 최적화 알고리즘입니다. 다음을 입력으로 제공하면 됩니다.

- 개선하고자 하는 프롬프트
- expectation이 포함된 평가 데이터셋
- "좋음"을 정의하는 일련의 scorer들

GEPA는 데이터셋을 모델에 통과시키고, 어떤 케이스가 실패했는지와 그 이유를 분석한 다음, 그 약점을 해결하는 재작성된 프롬프트를 생성하고 그 결과를 Prompt Registry에 새로운 버전으로 등록합니다. 모두 자동으로 이루어집니다.

따라서 무엇이 더 나은 프롬프트를 만드는지 추측하는 대신, 실패 케이스가 스스로 답을 알려주게 하는 것입니다.

## 사전 준비 사항

이 노트북을 실행하기 전에 다음이 준비되어 있어야 합니다.

- [Feedback Loops](5-feedback-loops.md) 섹션을 완료했어야 합니다. 가능하면 몇 개의 👍와 👎도 수집해 두세요.
- MLflow 대시보드에 접근할 수 있어야 합니다.
- workbench가 실행 중이어야 합니다(노트북이 거기서 실행됩니다).

Canopy에서 나온 싫어요가 눌린 트레이스가 이상적인 입력입니다. 아직 충분히 모으지 못했다면, 노트북에는 대안으로 시뮬레이션된 피드백이 포함되어 있으므로 전체 최적화 루프가 동작하는 것을 여전히 확인할 수 있습니다.

## 노트북

workbench를 열고 다음으로 이동합니다.

```
experiments/6-observability/1-prompt-optimization.ipynb
```

노트북은 다섯 단계로 진행됩니다.

| Step | 내용 |
|------|-------------|
| 0. Setup | MLflow에 연결하고 Prompt Registry에서 가장 최신 요약 프롬프트를 불러옵니다 |
| 2. Build Dataset | test workspace에서 MLflow `eval` 데이터셋과 `summary_tests.yaml`의 테스트 케이스를 불러온 다음, 이들을 합쳐 학습 데이터셋을 만듭니다 |
| 3. Define Scorers | `summary_quality`(`judge_prompt.txt`에서 불러온 LLM judge)와 `is_shorter` scorer를 정의합니다 |
| 4. Baseline Evaluation | 현재 프롬프트를 합쳐진 데이터셋에 대해 평가해 기준(before) 점수를 산출합니다 |
| 5. Optimize | GEPA가 실패 케이스를 고치기 위해 프롬프트를 재작성하고 새 버전으로 등록합니다 |

이제 노트북을 진행해 보고 끝나면 여기로 다시 돌아오세요.

## 얻게 되는 것

노트북이 끝나면 다음을 갖게 됩니다.

- 무엇이 왜 바뀌었는지를 정확히 보여주는, 버전 관리된 프롬프트 히스토리(MLflow)
- 단순한 느낌이 아니라 정량화된 before/after 점수
- 프롬프트를 개선하고 싶을 때마다 재사용할 수 있는 평가 데이터셋
- 승리한 프롬프트를 Canopy로 다시 승격시키는 구체적인 경로(설정 파일 또는 Prompt Registry를 통해)

사용자가 👎를 클릭하면서 시작된 루프는 측정 가능하게 더 나아진 AI 애플리케이션으로 끝납니다.

![mlflow-gepa.png](./images/mlflow-gepa.png)

새로운 테스트 프롬프트를 만들었으므로, 새로운 평가 파이프라인도 함께 시작됩니다(자동화 마법 ✨).
이전과 마찬가지로 **<USER_NAME>-toolings** 네임스페이스에서 OpenShift Pipelines, OpenShift AI Pipeline Runs, MLflow로 이동해 이 평가 실행을 추적할 수 있습니다.
완료된 후에는, 노트북에서 수행한 기준(baseline) 평가 실행과 파이프라인으로 실행된 평가 실행을 비교할 수도 있습니다. 또는 이전 파이프라인 실행(`summary_tests_...`라는 이름의 평가 실행)과 비교할 수도 있습니다.

![compare-eval-runs.png](./images/compare-eval-runs.png)

GEPA 실행에 대해 더 궁금하다면, MLflow에서 훨씬 더 많은 세부 정보를 확인할 수 있습니다.
간단히:

1. OpenShift AI -> Experiments (MLflow)로 이동해 **<USER_NAME>-toolings** Project -> Summarization을 선택하고 상단의 `Model Training` 탭을 클릭합니다.

    ![model-training-tab.png](./images/model-training-tab.png)

2. `Training` 태그가 붙은 가장 최근 Run을 선택합니다(이것이 GEPA 실행입니다).

    ![training-run.png](./images/training-run.png)

3. 실행 내용을 살펴봅니다. `Model metrics`는 멋진 시각화를 제공합니다.

    ![model-metrics.png](./images/model-metrics.png)



참고로, 단순화를 위해 여기서는 몇 가지를 생략했습니다.

- 백엔드를 거치지 않고 모델로 바로 연결합니다.
- 또한 git에서 `summary_test.yaml`을 불러오지 않고, 로컬 폴더를 그냥 참조합니다.
- 프롬프트를 "학습"하는 데 사용한 데이터셋을 "검증"하는 데에도 그대로 사용합니다. 이는 좋은 방식이 아니며, 이상적으로는 학습용과 검증/평가용으로 별도의 데이터셋을 두어야 합니다.

이 모든 것은 쉽게 고칠 수 있는 부분들이며(실제로 평가 파이프라인에서는 이미 이렇게 하고 있습니다), 여기서는 단순화를 위해 그대로 남겨두었습니다.