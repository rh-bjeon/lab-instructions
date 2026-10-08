# Take Agents to Prod

새로 만든 agent가 준비되었으니, 이제 프로덕션으로 가져가 봅시다!
평가(evaluating)와 모니터링(observing) 같이 해야 할 일들이 몇 가지 있지만, 먼저 백엔드에서 이를 활성화하기 위한 feature flag를 추가하는 것부터 시작하겠습니다.

## GitOps를 통해 Agent 배포하기

1. 먼저 test와 prod의 Llama Stack을 업그레이드해야 합니다. `genaiops-gitops/canopy/test/ogx/config.yaml`로 이동해서 다음과 같이 업데이트하세요.

    ```yaml
    ---
    chart_path: charts/llama-stack-operator-instance
    models:
      - name: "llama32"
        url: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
    rag:                
      enabled: true     
      milvus:                 
        service: "milvus-test" 
    guardrails:
      enabled: true
    mcp:                # 👈 Add this ❗︎❗︎
      enabled: true     # 👈 Add this ❗︎❗︎❗︎
    ```

2. 이것을 git에 push해서 적용되도록 하세요.

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git pull
    git add .
    git commit -m "📃 enable MCP 📃"
    git push origin main
    ```

3. Llama Stack에서 MCP가 활성화된 후에는, agent 기능을 사용할 수 있도록 Canopy 백엔드도 업데이트해야 합니다. 워크벤치로 이동해서 `genaiops-gitops/canopy/test/backend/config.yaml` 파일을 여세요.

4. 파일을 편집해서 `student-assistant` feature flag를 추가하세요. 프롬프트는 자유롭게 변경해도 됩니다. 이전과 마찬가지로 이것은 system prompt입니다.

    ```yaml
    ---
    repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
    chart_path: chart
    summarization:
      enabled: true
      model: vllm-llama32/llama32
      endpoint: "http://llama-stack-service:8321/v1"
      mlflow_prompt: summarization
      mlflow_prompt_version: latest
    information-search:
      enabled: true
      endpoint: "http://llama-stack-service:8321/v1"
      model: vllm-llama32/llama32
      vector_db_id: genaiops_2026_05_25_21_39
      mlflow_prompt: information-search
      mlflow_prompt_version: latest
    feedback:
      enabled: false
    ab_testing:             
      enabled: false         
      mlflow_prompt_b_version: latest 
    shields:
      enabled: true
      endpoint: http://canopy-guardrails/v1
      model: llama32
      config: canopy-guardrails
    student-assistant:         # 👈 just add this block ❗︎❗︎❗︎ ❗︎❗︎❗︎ ❗︎❗︎❗︎
      enabled: true
      model: vllm-llama32/llama32
      temperature: 0.1
      vector_db_id: latest
      mcp_calendar_url: "http://canopy-mcp-calendar-mcp-server:8080/sse"
      mlflow_prompt: student-assistant
      mlflow_prompt_version: latest
    ```

5. 이 변경 사항을 push하기 전에, 먼저 prompt registry에 `student-assistant` 프롬프트를 생성해야 합니다. OpenShift Dashboard > Gen AI Studio > Prompts로 이동해서 `<USER_NAME>-toolings` 프로젝트 아래에 `student-assistant` 프롬프트를 생성하세요. 그런 다음 아래 프롬프트를 추가하고 적절한 커밋 메시지를 남기세요.

    ```bash
    You are a helpful assistant that helps students with their calendar and studies.
    Today is {datetime.today().strftime('%Y-%m-%d')}.

    Your workflow:

    1. If student asks about their schedule ("What lectures do I have?"):
      - Call get_upcoming_events
      - Show them the results
      - DONE (don't modify anything)

    2. If student asks a question about a topic ("I need help understanding X"):
      - First: call search_knowledge_base with the topic
      - If knowledge base has relevant information: answer their question with that information, DONE
      - If knowledge base has NO relevant information:
        a) Call find_professors_by_expertise to find an expert
        b) Call get_events_by_date to check for scheduling conflicts
        c) Call create_event to schedule a meeting with the professor at a free time
        d) Tell the student you scheduled the meeting

    When scheduling with create_event:
    - Pick a reasonable time that's free (check with get_events_by_date first)
    - Use these parameters: name, category, level, start_time, end_time, content
    - Do NOT include sid, status, or creation_time
    ```


6. test 환경에서도 GitOps를 통해 calendar API를 배포하세요. 이렇게 하면 test 환경에서 추가적인 평가(evaluation) 테스트를 계속 진행하는 동시에, 실험(experiment) 환경에서도 자유롭게 실험을 이어갈 수 있습니다. 이후 현재 구성을 프로덕션으로 가져가게 됩니다.

  단, 이번에는 GitOps를 통해 배포해 봅시다! `/opt/app-root/src/genaiops-gitops/canopy/test` 아래에 `calendar-mcp` 폴더를 만들고, 그 안에 `config.yaml` 파일을 생성하세요. 또는 아래 명령어를 그대로 실행해도 됩니다.

  ```bash
   mkdir /opt/app-root/src/genaiops-gitops/canopy/test/calendar-mcp
   touch /opt/app-root/src/genaiops-gitops/canopy/test/calendar-mcp/config.yaml
  ```

  그리고 관련 helm chart를 가리키는 아래 설정을 추가하세요.

  ```yaml
  repo_url: https://github.com/rhoai-genaiops/mcp.git
  chart_path: mcp-calendar-app/helm
  fullnameOverride: canopy-mcp-calendar
  ```

7. 변경 사항을 Git에 push하세요.. 아시죠, GitOps니까요!

  ```bash
    cd /opt/app-root/src/genaiops-gitops/canopy/
    git pull
    git add .
    git commit -m "📆 Agent feature and Calendar MCP added 📆"
    git push
  ```

8. Canopy UI를 열고, 왼쪽에서 Student Assistant로 전환한 다음 `I need help understanding quantum chromodynamics.`라고 물어보세요.
    Agent는 정보를 찾으려고 시도했다가 실패한 후, 도와줄 교수님을 찾아서 해당 교수님과의 미팅을 예약할 것입니다.

    Canopy를 더 이상 열어두지 않았다면, 여기서 다시 찾을 수 있습니다: [https://canopy-ui-<USER_NAME>-test.<CLUSTER_DOMAIN>](https://canopy-ui-<USER_NAME>-test.<CLUSTER_DOMAIN>)

    ![ask-canopy.png](images/ask-canopy.png)
