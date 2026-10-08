# 🚀 Deploy to Canopy

이제 새로운 모델을 Canopy에 배포하고 사용해 봅시다!  
먼저 모델을 배포해야 하는데, 여기서는 실험용 네임스페이스에 배포한 다음 MaaS와 Llamastack을 통해 이를 가져올 것입니다.  
좀 더 엄격한 프로세스를 원한다면

## Model Registry에서 배포하기

이전 노트북에서 모델을 Model Registry에 막 푸시했습니다. 이제 가서 어떤 모습인지 한번 살펴봅시다!

1. OpenShift AI Dashboard -> AI hub -> Models -> Registry로 이동합니다.

  ![model-registry](images/model-registry.png)

2. 여기서 새로 파인튜닝한 모델을 위해 방금 생성한 모델카(modelcar)🚗를 확인할 수 있습니다!

  `Latest version` (0.0.1)로 이동한 다음 `Model location URI`를 복사하세요. 배포할 때 필요합니다.

  여기서 모델에 대한 메타데이터나 상세 정보도 확인할 수 있습니다 🤩

  ![uri-copy](images/uri-copy.png)

3. 이제 오른쪽 상단의 `Deploy`를 클릭하고 프로젝트로 `<USER_NAME>-canopy`를 선택한 다음 Deploy를 누르세요.
![choose-deploy-project.png](images/choose-deploy-project.png)

4. Model details 페이지에서 다음 옵션을 선택하세요.
- Model location: **URI**
- URI: **oci://default-route-openshift-image-registry.<CLUSTER_DOMAIN>/<USER_NAME>-canopy/socratic-model:0.0.1**
- Create a connection to this location: **선택 해제(Unchecked)**
- Model type: **Generative AI model (예: LLM)**

    그런 다음 Next를 누르세요.
    ![model-details.png](images/model-details.png)

5. Model deployment 페이지에서 다음 옵션을 선택하세요.

- Name: **socratic-model**

- `Customize resource request and limits`를 클릭하고 `Memory requests`와 `Memory limits`를 모두 **8 GiB**로 설정하세요.

- Serving runtime: `CUSTOM - vLLM Serving Runtime for CPU`

나머지는 그대로 두고 Next를 누르세요.

  ![model-deployment.png](images/model-deployment.png)

6. `Advanced settings` 페이지에서 커스텀 파라미터를 하나 추가해 봅시다.

  ```
    --served-model-name=socratic-model
  ```

  ![custom-args.png](./images/custom-args.png)

  그런 다음 `Next`를 누르고, Review 페이지에서 모든 세부 정보가 올바른지 확인한 후 `Deploy model`을 누르세요.

  ![advanced-and-review.png](images/advanced-and-review.png)

7. 모델이 배포될 때까지 기다리세요.

  자동으로 업데이트되지 않으면 페이지를 새로고침해 보세요.

  ![deployment.png](images/deployment.png)

## 모델을 MaaS에 추가하기

새로운 모델이 배포되었으니, 필요한 사람 누구나 사용할 수 있도록 MaaS에 추가해 봅시다 🚀

1. MaaS 대시보드로 이동해서(닫았다면 https://litemaas-<USER_NAME>-maas.<CLUSTER_DOMAIN>) 새 모델을 추가하세요.

  ![create-model.png](images/create-model.png)

2. 다음 세부 정보를 입력하세요.
- **Model name:** socratic-model
- **Description:** A fine-tuned Qwen2-0.5B-Instruct model to act as a socratic tutor
- **API Base URL:** http://socratic-model-predictor.<USER_NAME>-canopy.svc.cluster.local:8080/v1
- **Backend Model Name:** socratic-model
- **API Key:** fakekey
![maas-model](images/maas-model.png)

3. `Models`로 이동해서 새로 만든 `socratic-model`을 클릭하고 Subscribe를 클릭하세요.
![subscribe](images/subscribe.png)

4. `API Keys`로 이동해서 `Create API Key`를 클릭하고, 이름을 `socratic-model`이라고 지정하고, `socratic-model`을 선택한 다음 Create API Key를 누르세요.
![create-key](images/create-key.png)

5. API 키를 꼭 복사해 두세요. 다음 섹션에서 사용할 것입니다 🤭

## 새 모델을 Llama Stack에 추가하기

이제 MaaS에 새 모델이 생겼으니, 테스트용 Llama Stack에도 추가해서 Canopy에서 테스트해 봅시다! 🙌

1. 워크벤치로 들어가서 `genaiops/test/ogx/config.yaml`을 엽니다.

2. socratic-model을 반영하도록 yaml에 새 모델을 추가합니다.

```yaml
  ---
  chart_path: charts/llama-stack-operator-instance
  models:
    - name: "llama32"
      url: "http://llama-32-predictor.ai501.svc.cluster.local:8080/v1"
    - name: "llama32-fp8"   
      url: "http://llama-32-fp8-predictor.ai501.svc.cluster.local:8080/v1" 
    - name: "Llama-3.2-3B-Instruct-FP8"    
      url: "https://litemaas-litellm-<USER_NAME>-maas.<CLUSTER_DOMAIN>/v1"
    - name: "socratic-model"    # 👈 Add this ❗︎❗︎
      url: "https://litemaas-litellm-<USER_NAME>-maas.<CLUSTER_DOMAIN>/v1"   # 👈 Add this ❗︎❗︎
      token: "<YOUR-COPIED-API-KEY>"    # 👈 Add this ❗︎❗︎
  rag:                  
    enabled: true
  mcp:                
    enabled: true 
  sealed_secrets: 
    enabled: true   
    secretName: llama-fp8-maas-token 
```

  (네, 알고 있습니다. 키를 git에 그대로 올리는 건 안전하지 않다는 것을요... 원하신다면 이 부분도 sealed secret으로 처리해 보셔도 좋지만, 시간 관계상 이번에는 쉬운 방법을 택하겠습니다 🙈)

  3. 이를 git에 커밋합니다.
```bash
cd /opt/app-root/src/genaiops-gitops
git pull
git add .
git commit -m "💭 Add Socratic Model from MaaS 💭"
git push
```

이제 Llama Stack에 새 모델이 추가되어 사용할 준비가 되었습니다!

이 작업 이후 LlamaStack이 정상적으로 시작되는지 꼭 확인하세요(`<USER_NAME>-test` 네임스페이스의 Topology 뷰에서 Llama Stack의 🔵 원을 확인하세요). 그러면 새 모델을 새로운 Canopy 기능에 추가할 준비가 끝납니다 😁

## 소크라테스식 Canopy

![meme.jpg](images/meme.jpg)

이제 이 소크라테스식 튜터를 Canopy에 완전히 셋업해 봅시다!

1. 먼저, 소크라테스식 튜터를 위한 시스템 프롬프트를 만들어야 합니다. OpenShift AI Dashboard > Gen AI Studio > Prompts로 이동하고, **`<USER_NAME>-toolings`** 프로젝트 아래에서 작업하세요.

2. `socratic-tutor`라는 새 프롬프트를 만들고 아래 프롬프트를 사용하세요.

    ```bash
    You are a Socratic tutor. Your role is to guide students to discover answers themselves through thoughtful questions rather than providing direct answers. Ask clarifying questions, prompt critical thinking, and help students explore different angles of their question.
    ```
  ![socratic-tutor-prompt.png](./images/socratic-tutor-prompt.png)

3. 그런 다음 `genaiops-gitops/canopy/test/backend/config.yaml`로 이동해서 새 기능 플래그를 추가합니다.

```yaml
  repo_url: https://gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/backend
  chart_path: chart
  summarization:
    enabled: true
    model: vllm-Llama-3.2-3B-Instruct-FP8/Llama-3.2-3B-Instruct-FP8
    endpoint: "http://llama-stack-service:8321/v1"
    mlflow_prompt: summarization
    mlflow_prompt_version: latest
  information-search:
    enabled: true
    endpoint: "http://llama-stack-service:8321/v1"
    model: vllm-Llama-3.2-3B-Instruct-FP8/Llama-3.2-3B-Instruct-FP8
    vector_db_id: genaiops_2026_09_30_10_24
    mlflow_prompt: information-search
    mlflow_prompt_version: latest
  feedback:
    enabled: false
  ab_testing:
    enabled: false
  shields: 
    enabled: true
    endpoint: http://canopy-guardrails/v1
    model: llama32
    config: canopy-guardrails
  student-assistant: 
    enabled: true
    model: vllm-Llama-3.2-3B-Instruct-FP8/Llama-3.2-3B-Instruct-FP8 
    temperature: 0.1
    vector_db_id: latest
    mcp_calendar_url: "http://canopy-mcp-calendar-mcp-server:8080/sse"
    mlflow_prompt: student-assistant
    mlflow_prompt_version: latest     
  socratic-tutor:    # 👈 Add this ❗︎❗︎
    enabled: true    # 👈 Add this ❗︎❗︎
    model: vllm-socratic-model/socratic-model    # 👈 Add this ❗︎❗︎
    endpoint: "http://llama-stack-service:8321/v1"   # 👈 Add this ❗︎❗︎
    mlflow_prompt: socratic-tutor   # 👈 Add this ❗︎❗︎
    mlflow_prompt_version: latest   # 👈 Add this ❗︎❗︎
    temperature: 0.9    # 👈 Add this ❗︎❗︎
    max_tokens: 1500    # 👈 Add this ❗︎❗︎
```

4. git에 커밋합니다.

  ```bash
  cd /opt/app-root/src/genaiops-gitops
  git pull
  git add .
  git commit -m "🤔 Add the Socratic Tutor feature 🤔"
  git push
  ```

5. Canopy를 열고, 왼쪽 메뉴에서 Socratic Tutor를 선택한 다음 예를 들어 `What is 1+1?`처럼 질문을 던져 보세요.

_(튜터가 다소 느릴 수 있는데, CPU에서 실행되고 있기 때문입니다 🙈)_

  ![tutor-in-action](images/tutor-in-action.png)

축하합니다! 🎉

이제 모델을 튜닝하고 온보딩하는 전체 흐름을 모두 거쳤습니다. 결코 작은 성취가 아닙니다.

다음 단계는 이 모든 과정을 자동화해서 버튼 클릭(또는 PR 머지) 한 번으로 모델이 업데이트되도록 만드는 것입니다.  
이를 우리는 지속적 학습(Continous Training, CT) 파이프라인이라고 부르며, 관심이 있다면 [**AI500 MLOps Enablement with Red Hat AI Enterprise**](https://www.redhat.com/en/services/training/ai500-mlops-practices-with-red-hat-openshift-ai)에서 자세히 다루고 있습니다.
