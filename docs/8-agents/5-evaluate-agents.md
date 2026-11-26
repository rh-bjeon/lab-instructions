# Evaluate Agents

이제 agent가 실제로 동작하고 있습니다. 학생들을 도와주고 교수님과의 미팅도 예약해주고 있죠. 그런데 과연 그것이 제대로 동작하고 있는지 어떻게 알 수 있을까요?
이전 챕터들에서 했던 것처럼, agent를 위한 평가(evaluation)를 추가해 봅시다!

## Agent traces

summarization이나 RAG에서처럼, agent에 대해서도 trace를 얻을 수 있으며, 이를 통해 어떤 도구가 어떤 순서로 사용되었는지 좋은 통찰을 얻을 수 있습니다.
한번 살펴봅시다.

1. OpenShift AI -> Develop & train -> Experiments (MLflow) -> **<USER_NAME>-test** 프로젝트로 이동해서 `student-assistant` experiment를 클릭하세요.

2. 임의의 trace를 클릭하고 `Summary`와 `Details & Timeline`을 살펴보세요.

    ![agent-traces](./images/agent-traces.png)

    여기서는 사용된 모든 도구와 agent의 선택, 그리고 계속 진행할지 여부를 결정하기까지의 전체 상호작용을 볼 수 있습니다.
    우리는 이러한 trace에 담긴 내용을 테스트의 기반으로 활용하겠습니다.


## Agent 테스트의 세 가지 계층

Agent를 평가할 때는 다음 세 가지 영역에 집중합니다.

1. **개별 도구에 대한 Unit test** - 각 도구를 독립적으로 테스트합니다. Calendar API가 실제로 이벤트를 생성하나요? 검색이 관련성 있는 결과를 반환하나요?
2. **Text-to-JSON 검증** - LLM이 도구 호출을 올바른 형식으로 구성할 수 있나요? 그리고 올바른 도구를 선택하나요? (스포일러: 많은 agent가 깨지는 지점은 바로 형식이 잘못된 JSON입니다)
3. **End-to-end 평가** - 전체 워크플로가 사용자에게 실제로 도움이 되나요?

이미 앞서 eval framework를 구축해 두었으니, 이제 이를 활용해서 agent를 테스트해 봅시다!

## 1. Agent 도구 Unit 테스트하기

전체 agent를 테스트하기 전에, 먼저 각각의 도구가 올바르게 동작하는지 확인해 봅시다. 케이크를 굽기 전에 재료를 먼저 테스트하는 것과 같은 개념입니다.

canopy 백엔드에는 이미 student assistant 도구에 대한 unit test가 설정되어 있습니다. 실행해 봅시다!

```bash
cd /opt/app-root/src/backend
pip install pytest pytest-asyncio
pytest tests/test_tools.py -v
```

다음과 같은 출력을 확인할 수 있습니다.

```
tests/test_tools.py::test_search_knowledge_base PASSED                    [ 25%]
tests/test_tools.py::test_find_professors_by_expertise PASSED            [ 50%]
tests/test_tools.py::test_mcp_calendar_list_tools PASSED                 [ 75%]
tests/test_tools.py::test_mcp_calendar_list_events PASSED                [100%]

======================== 4 passed in 1.22s ========================
```

> 
> 💡 **TIP**
> 
> 아래와 같은 에러는 무시하셔도 됩니다.
> `2026/11/26 08:20:40 WARNING mlflow.tracing.export.mlflow_v3: Failed to send trace to MLflow backend: INTERNAL_ERROR: Response: {'error': {'code': 'PERMISSION_DENIED', 'message': 'Permission denied for requested operation.'}}`
> 

**방금 우리가 테스트한 것은 무엇일까요?**

- **search_knowledge_base** - 도구가 벡터 스토어에서 관련 콘텐츠를 가져올 수 있는지 확인했습니다
- **find_professors_by_expertise** - 교수 매칭이 올바르게 동작하는지 확인했습니다
- **MCP calendar tools** - MCP 서버에 접근 가능하며 올바른 도구들을 노출하는지 확인했습니다

**Pro tip:** 도구가 반환하는 값을 직접 보고 싶으신가요? `-s` 플래그를 붙여서 실행해 보세요.

```bash
pytest tests/test_tools.py -v -s
```

이렇게 하면 실제 검색 결과가 표시되어, 도구들이 어떤 데이터를 다루고 있는지 이해하는 데 도움이 됩니다.

## 2. CI/CD 파이프라인에 Unit 테스트 추가하기

로컬에서 unit test가 잘 동작하는 것을 확인했으니, 이제 CI/CD 파이프라인에서 이를 자동화해 봅시다! 이렇게 하면 모든 코드 변경 사항이 프로덕션으로 승격되기 전에 반드시 테스트를 거치게 됩니다.

### Tekton 파이프라인에서 Unit 테스트 활성화하기

평가 파이프라인은 다른 평가들과 함께 unit test도 실행할 수 있습니다. 이 단계를 활성화해 봅시다.

1. 워크벤치에서 `genaiops-gitops/toolings/evaluation-pipeline/config.yaml`로 이동해서, unit test 단계를 활성화하도록 설정 파일을 업데이트하세요.

    ```yaml
    chart_path: charts/canopy-evals-pipeline
    USER_NAME: <USER_NAME>
    CLUSTER_DOMAIN: <CLUSTER_DOMAIN>
    kfp:
      llsUrl: http://llama-stack-service.<USER_NAME>-test.svc.cluster.local:8321
      backendUrl: http://canopy-backend.<USER_NAME>-test.svc.cluster.local:8000
    testing:                    # 👈 Add this
      enableUnitTests: true     # 👈 Add this
    ```

2. 이를 git에 push하세요.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "1️⃣ Enabled unit tests 1️⃣"
    git push
    ```

3. 제대로 추가되었는지 확인하기 위해, OpenShift Console -> Pipelines -> canopy-evals-pipeline로 이동해서 `tool-unit-tests`가 거기에 있는지 확인하세요.

    ![unit-test-step.png](images/unit-test-step.png)

실제 동작하는 모습은 곧 확인하겠지만, 먼저 agent에 대한 end-to-end 테스트도 잘 동작하는지 확인해 봅시다.

### Agent E2E 테스트 추가하기

1. 워크벤치로 이동해서 `evals` 저장소로 이동하세요.

    ```bash
    cd /opt/app-root/src/evals
    ```

2. student assistant 테스트를 위한 새 폴더를 생성하세요.

    ```bash
    mkdir student-assistant
    ```

3. 테스트 설정 파일을 생성하세요. 새 파일 `student-assistant/student_assistant_tests.yaml`을 열고 다음을 붙여넣으세요.

```yaml
name: student_assistant_tests
description: End-to-end tests for the student assistant agent with tool choice validation
usecase: student-assistant
endpoint: /student-assistant
scorers:
  - answer_quality
  - tool_call_correctness
  - tool_call_efficiency
judge_prompt: judge_prompt.txt
tests:
  - inputs:
      prompt: "What is a forest canopy?"
    expectations:
      expected_result: "A forest canopy is the upper layer of a forest, formed by the crowns of trees. It's an important ecosystem component that provides habitat for many species and plays a crucial role in photosynthesis and the forest's overall health."
      expected_tools:
        - search_knowledge_base
  - inputs:
      prompt: "Who can help me with machine learning?"
    expectations:
      expected_result: "Dr. Sarah Chen from the Computer Science department can help you with machine learning. She specializes in Machine Learning, Neural Networks, AI Ethics, and Agentic Workflows. You can reach her at s.chen@university.edu."
      expected_tools:
        - find_professors_by_expertise
```

위 설정 파일의 내용을 번역하면 다음과 같습니다.
<pre style="background-color: #EAF6FF; padding: 15px; border-radius: 6px;"><code class="language-yaml">
# 이 내용은 실습생의 이해를 돕기 위해 student_assistant_tests.yaml의 내용을 일부 번역한 것입니다.
name: student_assistant_tests
description: 학생 도우미 에이전트의 도구 선택 검증을 포함한 엔드투엔드 테스트
usecase: student-assistant
endpoint: /student-assistant
scorers:
  - answer_quality
  - tool_call_correctness
  - tool_call_efficiency
judge_prompt: judge_prompt.txt
tests:
  - inputs:
      prompt: "숲의 수관층(Forest Canopy)이란 무엇인가요?"
    expectations:
      expected_result: "숲의 수관층은 나무의 수관(나뭇가지와 잎이 우거진 부분)으로 형성된 숲의 상층부입니다. 수관층은 다양한 생물종에게 서식지를 제공하고, 광합성과 숲 전체의 건강을 유지하는 데 중요한 역할을 하는 생태계의 핵심 구성 요소입니다."
      expected_tools:
        - search_knowledge_base
  - inputs:
      prompt: "머신러닝에 대해 도움을 받을 수 있는 교수님은 누구인가요?"
    expectations:
      expected_result: "컴퓨터공학과의 Sarah Chen 교수님이 머신러닝에 관한 도움을 주실 수 있습니다. Chen 교수님의 전문 분야는 머신러닝, 신경망, AI 윤리, 에이전트 워크플로입니다. 이메일(s.chen@university.edu)로 연락하실 수 있습니다."
      expected_tools:
        - find_professors_by_expertise
</code></pre>


같은 폴더에 `judge_prompt.txt`도 추가하세요.
```bash
You are an expert evaluator judging the quality of a generated answer to a question.

Your task is to decide whether the GENERATED_ANSWER correctly and faithfully answers the QUESTION, compared against the EXPECTED_ANSWER.

A high-quality answer must satisfy ALL of the following criteria:
- It correctly addresses the QUESTION
- Its key facts and claims are consistent with the EXPECTED_ANSWER
- It does not contradict or misrepresent information present in the EXPECTED_ANSWER
- It is coherent and directly useful as a standalone answer

INPUT:
{{ inputs }}

GENERATED_ANSWER:
{{ outputs }}

EXPECTED_ANSWER:
{{ expectations }}

Answer "yes" if the GENERATED_ANSWER meets all of the criteria above.
Answer "no" if it gives incorrect information, contradicts the expected answer, or fails to address the question.

Respond with only "yes" or "no".
```

<pre style="background-color: #EAF6FF; padding: 15px; border-radius: 6px;"><code class="language-yaml">
당신은 질문에 대해 생성된 답변의 품질을 평가하는 전문 평가자입니다.

당신의 임무는 생성된 답변(GENERATED_ANSWER)이 질문(QUESTION)에 정확하고 충실하게 답변했는지, 기대 답변(EXPECTED_ANSWER)과 비교하여 판단하는 것입니다.

높은 품질의 답변은 다음 기준을 모두 충족해야 합니다.
- 질문(QUESTION)에 정확하게 답변해야 합니다.
- 핵심 사실과 주장이 기대 답변(EXPECTED_ANSWER)과 일치해야 합니다.
- 기대 답변(EXPECTED_ANSWER)에 포함된 정보와 모순되거나 해당 정보를 왜곡해서는 안 됩니다.
- 답변이 논리적으로 일관되고, 그 자체로 직접적인 도움이 되어야 합니다.

입력(INPUT):
{{ inputs }}

생성된 답변(GENERATED_ANSWER):
{{ outputs }}

기대 답변(EXPECTED_ANSWER):
{{ expectations }}

생성된 답변이 위의 모든 기준을 충족하면 "yes"로 답변하세요.
잘못된 정보를 제공하거나, 기대 답변과 모순되거나, 질문에 적절하게 답변하지 못한 경우 "no"로 답변하세요.

반드시 "yes" 또는 "no"로만 응답하세요.
</code></pre>


4. 테스트 안의 `expected_tools` 필드를 눈여겨보세요 - 이는 agent가 어떤 도구를 호출해야 하는지 평가자에게 알려줍니다. 이 필드는 `tool_call_correctness`와 `tool_call_efficiency`라는 두 가지 새로운 scorer에서 사용됩니다. 이제 eval 파이프라인은 다음을 확인하게 됩니다.
    - canopy 질문에 대해 agent가 `search_knowledge_base`를 호출했는가?
    - 교수 질문에 대해 `find_professors_by_expertise`를 호출했는가?

6. 변경 사항을 커밋하고 push하세요.

    ```bash
    cd /opt/app-root/src/evals/student-assistant
    git add .
    git commit -m "🤖 Agent E2E tests added 🤖"
    git push
    ```

7. eval 파이프라인이 자동으로 트리거되어야 합니다. `<USER_NAME>-toolings` 프로젝트에서 **OpenShift Pipelines**로 이동해 실행되는 모습을 확인해 보세요!


완료되면 MLflow에서 평가 결과를 확인할 수 있습니다 🎉
