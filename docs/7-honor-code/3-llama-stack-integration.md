# NeMo Guardrails를 Open GenAI Stack(Llama Stack)과 통합하기

노트북에서는 NeMo Guardrails 엔드포인트를 직접 호출했습니다. 5장에서는 Canopy 백엔드의 요청을 모델로 전달하는 추상화 계층으로 Llama Stack을 사용했습니다. NeMo를 Llama Stack의 **safety provider**로 연결하면 Llama Stack을 지나는 모든 요청에 가드레일이 자동으로 적용됩니다.

통합 구조는 다음과 같습니다.

```
Canopy Backend → Llama Stack → NeMo Guardrails → LLM
                                     ↕
                           (blocks if unsafe)
```

## Llama Stack 업데이트하기

1. `<USER_NAME>-canopy` 환경에서 **Helm > Releases > llama-stack-operator-instance > Upgrade**로 이동합니다.

    ![llama-stack-upgrade.png](./images/llama-stack-upgrade.png)

2. Form 뷰에서 **Guardrails** 섹션을 찾아 체크박스를 선택해 활성화합니다.

    ![llama-stack-safety-enable.png](./images/llama-stack-safety-enable.png)

    이는 NeMo 서비스를 기반으로 하는 `nemo-guardrail`이라는 Llama Stack **shield**를 등록합니다. Canopy 백엔드는 이미 이를 사용하는 방법을 알고 있어서, shield가 활성화되면 모든 요청에 `guardrails: ["nemo-guardrail"]`을 함께 전달합니다.

3. 아직 `summarization` 기능은 OGX를 사용하도록 옮기지 않았습니다. RAG에서만 그렇게 했었죠. 이제 `summarization` 기능도 orchestration 기능을 사용하도록 옮겨 봅시다. 다시 **Helm > Releases > canopy-backend > Upgrade**로 이동합니다. YAML 뷰에서 `summarization` 블록을 찾아 `model`과 `endpoint` 값을 업데이트합니다.

    ```yaml
    summarization:
      enabled: true
      model: vllm-llama32/llama32  # 👈 UPDATE THIS ‼️‼️‼️‼️
      endpoint: 'http://llama-stack-service:8321/v1' # 👈 UPDATE THIS ‼️‼️‼️‼️
      mlflow_prompt: summarization
      mlflow_prompt_version: latest
  ```

4. 모든 것이 정상인지 확인하기 위해 Topology 뷰를 확인합니다 ❤️

    ![canopy-topology.png](./images/canopy-topology.png)

이제 Canopy의 모든 요청은 모델에 도달하기 전에 NeMo를 거칩니다. 백엔드는 개별 탐지기의 구현을 알 필요 없이 shield 이름만 전달하면 되고, 나머지 처리는 NeMo가 담당합니다.

이제 결과가 만족스럽다면, 이를 상위 환경에 배포하기 전에 시스템에 대한 신뢰를 한층 더 높여봅시다!
