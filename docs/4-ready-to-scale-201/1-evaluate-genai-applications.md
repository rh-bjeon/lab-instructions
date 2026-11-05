# GenAI 애플리케이션 평가하기

운영 환경에 배포한 백엔드를 수동으로 테스트해 정상 동작을 확인했습니다. 앞으로 애플리케이션이 바뀌더라도 지금의 품질과 성능을 유지하는지 지속적으로 검증해야 합니다.

이를 위해 여러 변경 시점에 자동으로 실행되는 평가 체계를 구성하겠습니다. 💫

하지만 자동 평가를 설정하기 전에, 먼저 자동 평가가 어떻게 동작하는지 이해해야 합니다.

Canopy를 평가하려면 먼저 애플리케이션이 요청을 어떻게 처리하고 어떤 응답을 반환하는지 알아야 합니다.

이때 MLflow의 추적(Tracing) 기능을 사용합니다. 트레이싱은 뒤에서 더 자세히 다룹니다.

## MLflow tracing

1. OpenShift AI > `Develop & train` > `Experiments (MLflow)`로 이동하여 `<USER_NAME>-canopy`를 선택합니다. experiment로 `summarization`을 클릭합니다.

    ![mlflow-traces.png](./images/mlflow-traces.png)

2. 메뉴에서 `Traces`를 선택합니다. 프롬프트들이 익숙해 보이나요? 🙃 

    ![mlflow-traces-2.png](./images/mlflow-traces-2.png)

3. 트레이스 하나를 클릭합니다. 요청에 사용한 시스템 프롬프트와 사용자 프롬프트, 모델 응답을 한 화면에서 확인할 수 있습니다.

    ![mlflow-trace-3.png](./images/mlflow-trace-3.png)

이 정보가 있으면 응답이 기대한 결과와 일치하는지 __평가__할 수 있습니다.

좋습니다, 이제 평가를 시작해 봅시다!

## GenAI 애플리케이션을 평가하는 방법

GenAI 애플리케이션에서 평가할 수 있는 구성 요소는 몇 가지가 있습니다.
1. **LLM** - 애플리케이션 로직을 제외하고 모델 자체의 품질을 평가합니다. 사용할 모델을 선택하거나 새 모델로 교체하기 전에 수행합니다.
2. **애플리케이션 백엔드** - 시스템 프롬프트를 추가하는 단순한 로직부터 LLM에 전달할 데이터를 수집·가공하는 복잡한 워크플로까지 평가합니다. 프롬프트나 백엔드 코드, 워크플로 구성 요소가 바뀔 때마다 검증해야 합니다.
3. **워크플로 구성 요소** - 백엔드 전체를 블랙박스로 테스트하는 것과 별개로, 각 구성 요소가 올바르게 동작하는지도 개별적으로 확인합니다.

이번 섹션은 애플리케이션 백엔드 평가에 집중합니다. 사용할 LLM은 이미 정했고 백엔드에 별도의 구성 요소도 없기 때문입니다. MLflow에 기록된 최종 프롬프트에는 백엔드가 수행한 모든 변환이 반영되어 있으므로, 이 프롬프트와 응답을 기준으로 백엔드를 평가합니다.

다른 종류의 테스트에 대한 예시는 이후 섹션에서 확인할 수 있습니다.

## MLflow로 평가하기

프롬프트 평가는 MLflow를 사용합니다.
트레이스에 `expectations`를 추가해 "이 컨텍스트와 프롬프트에서 어떤 결과가 나와야 하는가"를 정의할 수 있습니다. 이후 새 프롬프트로 같은 요청을 실행하고, `scorer`를 사용해 새 응답과 기대값을 비교합니다. 이번 실습에서는 요약문이 지정한 길이보다 짧은지 검사하는 scorer를 사용합니다.

실제로 한번 해봅시다!

1. Experiments (MLflow) -> **<USER_NAME>-canopy** -> `summarization` -> Traces로 이동합니다.

    ![traces](./images/traces.png)

2. 원하는 trace를 클릭하여 선택합니다.

3. 왼쪽 상단의 `Show assessments`를 클릭합니다.

    ![show-assessments](./images/show-assessments.png)

4. `+ Add expectations`를 클릭하고 다음 내용을 추가합니다.

    - Assessment Name: `length`
    - Data Type: `Number`
    - Value: `200`
    - Rationale: _원하는 내용을 자유롭게 추가하세요 🧙‍♂️_ 예: `This text really should not be longer than 200 chars`

    아래와 같은 모습이 되어야 합니다. 완료되면 `Create`를 클릭합니다.

    ![expectation](./images/expectation.png)

    이렇게 하면 키-값 쌍(Assessment Name, Value)이 생성되며, 이후 scorer에서 이를 가져와 응답의 문자 수가 200보다 작은지 확인할 수 있습니다 :)

5. 이제 상단의 `+ Add to dataset` 버튼을 클릭하여 이 trace를 평가 데이터셋에 추가하면 됩니다.

    ![add-to-dataset](./images/add-to-dataset.png)

6. 이 trace를 평가용 데이터로 참고할 데이터셋을 지정해야 하는데, 아직 아무런 데이터셋도 없습니다. 새 데이터셋을 생성하고 이름을 `eval`로 지정합니다.

    ![create-dataset](./images/create-dataset.png)

7. 방금 생성한 데이터셋을 선택하고 `Export`를 클릭해 트레이스를 추가합니다. 첫 평가 데이터셋이 완성되었습니다. 😊

    ![add-to-eval-dataset.png](./images/add-to-eval-dataset.png)

8. X를 눌러 trace에서 나와 `Datasets`로 들어가면, 이제 해당 trace와 expectation이 하나 포함된 eval 데이터셋을 확인할 수 있습니다.

    ![new-dataset](./images/new-dataset.png)

이제 Workbench로 가서 `experiments/4-ready-to-scale-201/1-mlflow-eval.ipynb`를 열고, 새로 만든 eval 데이터셋을 사용하여 평가를 실행해 봅시다!

완료되면 다시 이곳으로 돌아와 OpenShift AI 대시보드에서 `Evaluation runs`를 확인하세요.

![eval-runs.png](./images/eval-runs.png)

트레이스를 클릭해 평가 결과를 자세히 확인합니다. `summary_quality`는 사용자 질문에 대한 LLM 응답의 품질을, `is_concise`는 출력이 글자 수 제한을 지켰는지를 평가합니다.

![eval-runs-2.png](./images/eval-runs-2.png)

'답변의 내용'에 대한 평가를 완료했으니, 이제 '성능'에 대한 평가를 진행해 보겠습니다!

## GuideLLM을 이용한 속도 테스트

GuideLLM을 사용하여 백엔드의 응답성을 테스트하겠습니다. 
여기에는 다음과 같은 것들이 포함됩니다.
- 응답을 시작하는 속도 (Time To First Token)
- 토큰을 생성하는 속도 (Time Per Output Token)
- 속도가 저하되지 않고 동시에 처리할 수 있는 요청의 수 (Throughput)

성능 평가는 현재 하드웨어에서의 모델 성능뿐 아니라 백엔드 시스템 전체의 응답성을 검증하는 데도 중요합니다. 기능이 복잡해질수록 응답이 느려질 수 있으며, 그 결과 모델이나 설계가 실제 사용 사례의 요구 사항을 충족하지 못할 수도 있습니다.

직접 시도해보려면, 다시 workbench로 이동하여 `experiments/4-ready-to-scale-201/2-guidellm-test.ipynb` 노트북을 진행하세요.
