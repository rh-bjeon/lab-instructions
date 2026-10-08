# GenAI 애플리케이션 평가하기

이제 프로덕션에 올라간 백엔드를 수동으로 테스트했고, 정상적으로 동작하는 것을 확인했습니다. 그리고 앞으로 여기에 가하는 모든 변경 사항이 적어도 지금과 같은 수준으로 동작하는지 확인하고 싶습니다.  

이를 위해 다양한 시점에 트리거되는 자동 평가를 설정하겠습니다 💫  

하지만 자동 평가를 설정하기 전에, 먼저 그것이 어떻게 동작하는지 이해해야 합니다.

그리고 그보다도 먼저, Canopy의 동작을 평가하려면 그것이 어떻게 동작하는지 알아야 합니다. 고객에게 어떻게 응답하는지 모른다면 어떻게 평가할 수 있겠습니까?

바로 여기서 MLflow의 Tracing 기능을 활용하게 됩니다. tracing 개념에 대해서는 나중에 다시 더 깊이 다룰 것입니다. 

## MLflow tracing

1. OpenShift AI > `Develop & train` > `Experiments (MLflow)`로 이동하여 `<USER_NAME>-canopy`를 선택합니다. experiment로 `summarization`을 클릭합니다.

    ![mlflow-traces.png](./images/mlflow-traces.png)

2. 메뉴에서 `Traces`를 선택합니다. 프롬프트들이 익숙해 보이나요? 🙃 

    ![mlflow-traces-2.png](./images/mlflow-traces-2.png)

3. 그중 하나를 클릭해 보세요. 마법 같죠! system prompt가 무엇이었는지, user prompt가 무엇이었는지, 그리고 모델의 응답이 무엇이었는지를 아주 깔끔하게 확인할 수 있습니다.

    ![mlflow-trace-3.png](./images/mlflow-trace-3.png)

이 모든 것을 확인할 수 있으므로, 응답이 예상대로인지, 좋은지 나쁜지도 _평가_할 수 있습니다.

좋습니다, 이제 평가를 시작해 봅시다!

## GenAI 애플리케이션을 평가하는 방법

GenAI 애플리케이션에서 평가할 수 있는 구성 요소는 몇 가지가 있습니다.
1. **LLM** - 별다른 장식 없이 모델 자체가 얼마나 우수한지를 평가하는 것입니다. 어떤 모델을 사용할지 결정하거나 새로운 모델로 업그레이드하기 전에 수행하면 좋습니다.
2. **애플리케이션 백엔드** - 백엔드는 LLM 로직을 구현하는 부분입니다. 이는 (우리가 했던 것처럼) system prompt를 추가하는 단순한 작업부터, LLM에 보낼 데이터를 가져오는 더 복잡한 워크플로우까지 포함할 수 있습니다. 프롬프트, 백엔드 코드 자체, 또는 워크플로우 구성 요소 중 어느 것이든 변경될 때마다 백엔드를 테스트하고 싶을 것입니다.
3. **워크플로우 구성 요소** - 백엔드를 통해 블랙박스처럼 테스트하는 것뿐만 아니라, 각 구성 요소가 제대로 동작하는지 확인하기 위해 개별적으로도 테스트하고자 합니다.

이번 섹션에서는 주로 애플리케이션 백엔드를 평가하는 데 집중하겠습니다. 이미 LLM을 선택했고, 백엔드에서 사용하는 추가적인 구성 요소가 없기 때문입니다.  
백엔드에서 수행하는 모든 변환이 담겨 있는, LLM에 전송되기 전 MLFlow에 의해 트레이싱된 최종 프롬프트를 평가함으로써 애플리케이션 백엔드를 평가하겠습니다.

다른 종류의 테스트에 대한 예시는 이후 섹션에서 보게 될 것입니다.

## MLflow로 평가하기

프롬프트를 평가하기 위해 MLFlow를 사용하겠습니다.  
이를 위해 트레이스(trace)에 `expectations`를 추가할 수 있는데, 이는 "이 컨텍스트와 프롬프트가 주어졌을 때, 어떤 종류의 출력을 기대하는가"를 나타냅니다.
그런 다음, 새로운 프롬프트와 함께 그 트레이스들을 LLM에 보내 새로운 출력을 얻고, `scorers`를 사용하여 그 새로운 출력을 기대치와 비교하여 평가할 수 있습니다.
예를 들어, 우리가 사용할 scorer 중 하나는 요약된 텍스트가 원하는 길이보다 짧은지 확인하는 것입니다.

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
    - Rationale: _원하는 내용을 자유롭게 추가하세요 🧙‍♂️_

    아래와 같은 모습이 되어야 합니다. 완료되면 `Create`를 클릭합니다.

    ![expectation](./images/expectation.png)

    이렇게 하면 키-값 쌍(Assessment Name, Value)이 생성되며, 이후 scorer에서 이를 가져와 응답의 문자 수가 200보다 작은지 확인할 수 있습니다 :)

5. 이제 상단의 `+ Add to dataset` 버튼을 클릭하여 이 trace를 평가 데이터셋에 추가하면 됩니다.

    ![add-to-dataset](./images/add-to-dataset.png)

6. 새 데이터셋을 생성하고 이름을 `eval`로 지정합니다.

    ![create-dataset](./images/create-dataset.png)

7. 마지막으로, 새 데이터셋을 선택하고 `Export`를 클릭하여 우리의 trace를 이 데이터셋에 추가합니다. 축하합니다, 첫 번째 평가 데이터셋을 만들었습니다 😊

    ![add-to-eval-dataset.png](./images/add-to-eval-dataset.png)

8. trace에서 나와 `Datasets`로 들어가면, 이제 해당 trace와 expectation이 하나 포함된 eval 데이터셋을 볼 수 있을 것입니다.

    ![new-dataset](./images/new-dataset.png)

이제 Workbench로 가서 `experiments/4-ready-to-scale-201/1-mlflow-eval.ipynb`를 열고, 새로 만든 eval 데이터셋을 사용하여 평가를 실행해 봅시다!

완료되면 다시 이곳으로 돌아와 OpenShift AI 대시보드에서 `Evaluation runs`를 확인하세요.

![eval-runs.png](./images/eval-runs.png)

그리고 trace를 클릭하여 평가의 세부 결과를 확인합니다.

![eval-runs-2.png](./images/eval-runs-2.png)

이제 성능 기반 평가로 넘어가 봅시다!

## GuideLLM을 이용한 속도 테스트

GuideLLM을 사용하여 백엔드의 응답성을 테스트하겠습니다. 
여기에는 다음과 같은 것들이 포함됩니다.
- 응답을 시작하는 속도 (Time To First Token)
- 토큰을 생성하는 속도 (Time Per Output Token)
- 속도가 저하되지 않고 동시에 처리할 수 있는 요청의 수 (Throughput)

이는 사용 중인 하드웨어 기준으로 모델을 테스트하는 데에도 중요하지만, 백엔드 시스템 전체를 테스트하는 데에도 중요합니다. 더 복잡한 기능을 계속 추가해 나가면 모델이 응답하는 속도가 느려지게 되고, 때로는 우리의 사용 사례에 적합하지 않은 선택이 될 수도 있기 때문입니다.

직접 시도해보려면, 다시 workbench로 이동하여 `experiments/4-ready-to-scale-201/2-guidellm-test.ipynb` 노트북을 진행하세요.
