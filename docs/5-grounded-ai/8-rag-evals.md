# RAG 평가하기

이제 RAG 시스템을 구축했으니, 여러분 모두가 무슨 생각을 하고 있는지 압니다...

![testing_meme](images/testing_meme.png)

저도 동의합니다. 그러니 이 섹션은 여기서 끝입니다!

...

하지만, 우리에게는 이미 평가 프레임워크가 있으니, 이를 사용하지 않는 것은 아쉬운 일이겠죠. 그러니 RAG가 예상대로 동작하는지 확인하기 위한 평가를 몇 가지 추가해봅시다.

RAG에서는 검색된(retrieved) 텍스트 chunk도 있으므로, 이를 위한 테스트도 만들 수 있습니다. 여기서는 특히 검색된 chunk가 사용자의 질문과 관련이 있는지, 그리고 LLM이 그것들을 바탕으로 답변에 근거(ground)를 두는지를 테스트합니다.
MLflow에는 이를 위한 내장 테스트가 있으므로 이를 사용하겠습니다. 자세한 내용은 여기에서 확인할 수 있습니다: https://mlflow.org/docs/latest/genai/eval-monitor/scorers/llm-judge/rag/

새로운 RAG 평가를 추가하려면, 단순히 몇 가지 테스트가 담긴 새로운 eval 폴더를 추가하면 됩니다.

1. workbench로 이동해 `evals` 폴더로 들어가세요.

2. 그 아래에 `information-search` 폴더를 만들고, 그 안에 `judge_prompt.txt`와 `information_search_tests.yaml` 파일을 생성하세요. 직접 하지 않고 명령어로 하고 싶다면 다음을 사용하세요:

    ```bash
    mkdir /opt/app-root/src/evals/information-search
    touch /opt/app-root/src/evals/information-search/information_search_tests.yaml
    touch /opt/app-root/src/evals/information-search/judge_prompt.txt
    ```

3. `information-search` 폴더 안의 `judge_prompt.txt`에 아래 텍스트를 추가하세요. summarization의 judge prompt는 사용자의 질문에 없는 사실을 끌어오는 답변에 감점을 주는데, 이는 검색된 문서를 바탕으로 한 유효한 RAG 응답을 잘못 실패시킬 수 있습니다. 그래서 RAG 전용 prompt가 필요한 것입니다:

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
    

  **참고:** 이 prompt들은 AI501 과목을 기준으로 작성되었습니다. 이전에 어떤 과목을 수집(ingest)했는지에 따라 내용에 맞게 수정해야 할 수 있습니다. 좋은 prompt와 예상 응답을 찾으려면 **Canopy UI**나 **Gen AI Playground**에서 몇 가지를 직접 실행해보세요.

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

