# RAG 평가하기

이제 RAG 시스템을 구축했으니, 여러분 모두가 무슨 생각을 하고 있는지 압니다...

![testing_meme](images/testing_meme.png)

저도 동의합니다. 그러니 이 섹션은 여기서 끝입니다!

...

하지만 이미 평가 프레임워크가 있으므로 RAG가 기대한 대로 동작하는지 검증하는 평가 항목을 추가해 보겠습니다.

RAG에는 검색된 텍스트 청크도 포함되므로 검색 단계 자체를 평가할 수 있습니다. 검색된 청크가 사용자 질문과 관련 있는지, LLM이 그 내용을 근거로 답했는지를 검사합니다. MLflow가 제공하는 내장 평가를 사용하며, 자세한 내용은 [MLflow RAG 평가 문서](https://mlflow.org/docs/latest/genai/eval-monitor/scorers/llm-judge/rag/)에서 확인할 수 있습니다.

새 RAG 평가를 추가하려면 테스트 정의가 들어 있는 평가 폴더를 만들면 됩니다.

1. workbench로 이동해 `evals` 폴더로 들어가세요.

2. 그 아래에 `information-search` 폴더를 만들고, 그 안에 `judge_prompt.txt`와 `information_search_tests.yaml` 파일을 생성하세요. 직접 하지 않고 명령어로 하고 싶다면 다음을 사용하세요:

    ```bash
    mkdir /opt/app-root/src/evals/information-search
    touch /opt/app-root/src/evals/information-search/information_search_tests.yaml
    touch /opt/app-root/src/evals/information-search/judge_prompt.txt
    ```

3. `information-search` 폴더의 `judge_prompt.txt`에 아래 내용을 추가합니다. 요약 기능 평가 프롬프트는 사용자 질문에 없는 정보를 포함한 응답에 감점을 줍니다. 하지만 RAG는 검색한 문서에서 새로운 정보를 가져오는 것이 정상 동작이므로 기존 기준을 그대로 사용하면 올바른 응답도 실패할 수 있습니다. 따라서 RAG 전용 평가 프롬프트가 필요합니다.

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

  위 프롬프트를 한국어로 번역하면 다음과 같습니다. `judge_prompt.txt`에는 위의 영어 원문을 붙여넣으시고, 아래는 참고만 하세요.

  > 당신은 질문에 대해 생성된 답변의 품질을 평가하는 전문 평가자입니다.
  >
  > 당신의 임무는 생성된 답변(GENERATED_ANSWER)이 질문(QUESTION)에 정확하고 충실하게 답변했는지, 기대 답변(EXPECTED_ANSWER)과 비교하여 판단하는 것입니다.
  >
  > 높은 품질의 답변은 다음 기준을 모두 충족해야 합니다.
  > - 질문(QUESTION)에 정확하게 답변해야 합니다.
  > - 핵심 사실과 주장이 기대 답변(EXPECTED_ANSWER)과 일치해야 합니다.
  > - 기대 답변(EXPECTED_ANSWER)에 포함된 정보를 반박하거나 왜곡하지 않아야 합니다.
  > - 답변이 논리적으로 일관되고, 그 자체로 직접적인 도움이 되어야 합니다.
  >
  > **입력:**
  > {{ inputs }}
  >
  > **생성된 답변:**
  > {{ outputs }}
  >
  > **기대 답변:**
  > {{ expectations }}
  >
  > 생성된 답변이 위의 모든 기준을 충족하면 "yes"로 답변하세요.
  > 잘못된 정보를 제공하거나, 기대 답변과 모순되거나, 질문에 적절하게 답변하지 못한 경우 "no"로 답변하세요.
  >
  > **반드시 "yes" 또는 "no"로만 응답하세요.**


4. `evals/information-search/information_search_tests.yaml`을 열고 다음을 붙여넣어 좋은 기준선(baseline)을 만드세요:

```yaml
name: information_search_tests
description: Tests for the information-search prompts of the Llama 3.2 3B model.
usecase: information-search
endpoint: /information-search
scorers:
  - answer_quality
  - retrieval_relevance
  - retrieval_groundedness
judge_prompt: judge_prompt.txt
tests:
  - inputs:
      prompt: "Describe the main learning outcomes for students completing the Advanced Generative AI Systems course."
    expectations:
      expected_result: "Students will learn to design GenAI applications, engineer prompts with evaluation, build production systems with CI/CD, implement RAG pipelines, secure LLM apps with guardrails, integrate multi-modal models, optimize models via quantization, instrument monitoring systems, orchestrate agents with tool-calling, and operate MaaS with APIs and governance."
  - inputs:
      prompt: "What are the key modules covered in weeks 5-8 of the AI501 curriculum?"
    expectations:
      expected_result: "Week 5 covers RAG Foundations (embeddings, chunking, ingestion pipelines), Week 6 covers Guardrails (safety taxonomies, filters, jailbreak defense), Week 7 covers Observability (tracing, metrics, logs, SLI/SLO), and Week 8 covers Tool-Calling & Agents (function calling, MCP, planner/critic loops)."
  - inputs:
      prompt: "What assessment components make up the AI501 course evaluation and what are their weightings?"
    expectations:
      expected_result: "Assessment includes Prompting & Eval Harness (10%), RAG Mini-System (15%), Guardrails & Red-Team (10%), Observability Pack (10%), Optimization Lab (10%), Agent with Tools (10%), Capstone (30%), and Participation (5%)."
  - inputs:
      prompt: "Explain what RAG implementation involves according to the course syllabus."
    expectations:
      expected_result: "RAG implementation involves building pipelines for ingestion, indexing, and retrieval with citations and provenance. Students learn embeddings, chunking strategies, ingestion pipelines, and create ETL→vector DB→retrieval→generation systems with citations."
  - inputs:
      prompt: "What technologies and platforms are used in the AI501 course infrastructure?"
    expectations:
      expected_result: "The course uses AI/ML platforms like Llama Stack and Hugging Face; development tools including Python, PyTorch, LangChain, Docker, and Kubernetes; infrastructure with GPU clusters and vector databases like Pinecone and Weaviate; plus security and monitoring tools for guardrails and observability."
  - inputs:
      prompt: "What are the four practical implementation tracks available in AI501?"
    expectations:
      expected_result: "The four tracks are: Production AI Systems (Llama Stack, GitOps, CI/CD), Knowledge Grounding (RAG design, vector DBs, doc pipelines), AI Safety & Security (Guardrails, red-teaming, observability), and Advanced Applications (Agents/tool-calling, multi-modal, model optimization)."
```
    
  위 내용을 한국어로 번역하면 다음과 같습니다. 위의 영어 원문을 붙여넣으시고, 아래는 참고만 하세요.
  > ```yaml
  > name: information_search_tests
  > description: Llama 3.2 3B 모델의 정보 검색 프롬프트를 평가하기 위한 테스트입니다.
  > usecase: information-search
  > endpoint: /information-search
  > scorers:
  >   - answer_quality
  >   - retrieval_relevance
  >   - retrieval_groundedness
  > judge_prompt: judge_prompt.txt
  > tests:
  >   - inputs:
  >       prompt: "고급 생성형 AI 시스템(Advanced Generative AI Systems) 과정을 수료한 학생들이 달성하게 될 주요 학습 성과를 설명하세요."
  >     expectations:
  >       expected_result: "학생들은 생성형 AI 애플리케이션 설계, 평가를 포함한 프롬프트 엔지니어링, CI/CD를 활용한 프로덕션 시스템 구축, RAG 파이프라인 구현, 가드레일을 통한 LLM 애플리케이션 보안 강화, 멀티모달 모델 통합, 양자화를 통한 모델 최적화, 모니터링 시스템 계측, 도구 호출을 활용한 에이전트 오케스트레이션, API 및 거버넌스를 통한 MaaS 운영 방법을 학습합니다."
  >   - inputs:
  >       prompt: "AI501 교육과정의 5~8주차에서 다루는 주요 모듈은 무엇인가요?"
  >     expectations:
  >       expected_result: "5주차에는 RAG 기초(임베딩, 청킹, 데이터 수집 파이프라인), 6주차에는 가드레일(안전성 분류 체계, 필터, 탈옥 공격 방어), 7주차에는 관측 가능성(트레이싱, 메트릭, 로그, SLI/SLO), 8주차에는 도구 호출 및 에이전트(함수 호출, MCP, 플래너/크리틱 반복 루프)를 다룹니다."
  >   - inputs:
  >       prompt: "AI501 과정의 평가 항목은 무엇이며, 각 항목의 반영 비율은 어떻게 되나요?"
  >     expectations:
  >       expected_result: "평가 항목은 프롬프팅 및 평가 하네스(10%), RAG 미니 시스템(15%), 가드레일 및 레드팀 테스트(10%), 관측 가능성 패키지(10%), 모델 최적화 실습(10%), 도구를 활용하는 에이전트(10%), 캡스톤 프로젝트(30%), 수업 참여도(5%)로 구성됩니다."
  >   - inputs:
  >       prompt: "강의 계획서에 따르면 RAG 구현에는 어떤 작업이 포함되나요?"
  >     expectations:
  >       expected_result: "RAG 구현에는 출처 인용 및 데이터 계보(provenance) 추적 기능을 갖춘 데이터 수집, 인덱싱, 검색 파이프라인 구축이 포함됩니다. 학생들은 임베딩, 청킹 전략, 데이터 수집 파이프라인을 학습하고, ETL → 벡터 데이터베이스 → 검색 → 생성으로 이어지는 시스템을 구축하여 답변에 출처를 포함하는 방법을 배웁니다."
  >   - inputs:
  >       prompt: "AI501 과정의 인프라에는 어떤 기술과 플랫폼이 사용되나요?"
  >     expectations:
  >       expected_result: "이 과정에서는 Llama Stack과 Hugging Face 같은 AI/ML 플랫폼, Python, PyTorch, LangChain, Docker, Kubernetes 등의 개발 도구, GPU 클러스터와 Pinecone 및 Weaviate 같은 벡터 데이터베이스로 구성된 인프라를 사용합니다. 또한 가드레일 및 관측 가능성을 위한 보안 및 모니터링 도구도 활용합니다."
  >   - inputs:
  >       prompt: "AI501에서 선택할 수 있는 네 가지 실습 트랙은 무엇인가요?"
  >     expectations:
  >       expected_result: "네 가지 트랙은 프로덕션 AI 시스템(Production AI Systems: Llama Stack, GitOps, CI/CD), 지식 기반 답변 생성(Knowledge Grounding: RAG 설계, 벡터 데이터베이스, 문서 처리 파이프라인), AI 안전성 및 보안(AI Safety & Security: 가드레일, 레드팀 테스트, 관측 가능성), 고급 애플리케이션(Advanced Applications: 에이전트 및 도구 호출, 멀티모달, 모델 최적화)입니다."
  > ```


  **참고:** 이 프롬프트는 AI501 과목을 기준으로 작성되었습니다. 앞에서 수집한 교육계획서에 맞게 질문과 기대 응답을 수정하세요. **Canopy UI**나 **Gen AI Playground**에서 직접 질문해 보면 적절한 테스트 데이터를 만드는 데 도움이 됩니다.

5. 평가 내용이 만족스럽다면, 반드시 git에 커밋하세요:

    ```bash
    cd /opt/app-root/src/evals
    git add .
    git commit -m "🥼 RAG eval added 🥼"
    git push
    ```

6. 기억하세요, 우리의 eval pipeline은 이 git push에 의해 트리거되어야 합니다! 🥳 `Ready to Scale 201` 섹션에서와 마찬가지로, OpenShift Pipelines로 이동해 진행 상황을 확인할 수 있습니다.

  ![rag-eval-pipeline-run.png](./images/rag-eval-pipeline-run.png)

7. pipeline이 실행되는 동안, `Develop & train` > `Experiments (MLflow)`로 이동해 **<USER_NAME>-test** 프로젝트 아래에서 `information-search`의 Traces를 확인하고 문서 내용이 prompt에 추가되는 모습을 자유롭게 살펴보세요.

  ![information-search-traces.png](./images/information-search-traces.png)
  ![information-search-traces-2.png](./images/information-search-traces-2.png)

8. pipeline이 완료되면, **<USER_NAME>-toolings** 프로젝트 아래의 `Experiments (MLflow)`에서 다시 평가 결과를 확인할 수 있습니다.

  ![rag-mlflow-eval.png](./images/rag-mlflow-eval.png)
