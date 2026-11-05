# 🔄 온프레미스 모델을 사용하도록 Canopy 업데이트하기

모델이 로컬에서 실행되고 있으므로 애플리케이션 스택에 연결하겠습니다. Llama Stack이 새 모델 엔드포인트를 사용하도록 설정한 뒤 Canopy가 온프레미스 구성에서도 정상적으로 동작하는지 확인합니다.

## 🦙 Llama Stack 설정 업데이트하기

1. **OpenShift Console** → **Helm** → **Releases**로 이동해서, `<USER_NAME>-canopy` 프로젝트에 있는 `llama-stack-operator-instance` release를 찾으세요.

2. 해당 release를 클릭하고 **Upgrade**를 선택하세요.

    ![tiny-llama-upgrade.png](./images/tiny-llama-upgrade.png)

3. 방금 배포한 온프레미스 TinyLlama를 Llama Stack에 새 모델 엔드포인트로 추가합니다. 그러면 Llama Stack을 통해 클라우드의 Llama 3.2 3B와 로컬의 TinyLlama를 모두 사용할 수 있습니다.

    Form view에서, **Add models**를 클릭해서 `models` 아래 Llama Stack 설정에 TinyLlama 엔드포인트를 추가하세요.

    - **Model Name**: `tinyllama`
    - **Model URL**: `http://tinyllama-predictor:8080/v1`
    - **Token**: (비워두세요)

4. **Upgrade**를 클릭해서 변경 사항을 적용하세요.

    ![tiny-llama-upgrade2.png](./images/tiny-llama-upgrade2.png)

5. 요약 기능이 TinyLlama를 사용하도록 백엔드를 설정합니다. TinyLlama의 처리 능력을 고려해 `max_tokens`도 낮춥니다. 😅 **OpenShift Console** → **Helm** → **Releases**에서 `canopy-backend`를 찾으세요.

    ![tiny-backend-upgrade.png](./images/tiny-backend-upgrade.png)

6. 먼저 새 모델로 summarization 사용 사례를 평가해 봅시다. `summarize` 아래에 다음을 추가하세요.

    ```yaml
    summarization:
      enabled: true
      mlflow_prompt_version: latest
      mlflow_prompt: summarization
      endpoint: 'http://llama-stack-service:8321/v1'
      model: vllm-tinyllama/tinyllama # 👈 UPDATE this ❗️❗️❗️
      max_tokens: 512 # 👈 ADD this ❗️❗️❗️
    ```

7. **Upgrade**를 클릭해서 변경 사항을 적용하세요.

### 🌳 새 모델로 Canopy 테스트하기

Llama Stack과 backend가 다시 정상화되면, on-prem 모델과 통신할 수 있는지 확인해 봅시다.

1. [Canopy UI](https://canopy-ui-<USER_NAME>-canopy.<CLUSTER_DOMAIN>)로 이동해서 summarization을 테스트하세요. 원한다면 이전 챕터에 있던 터키 차(Turkish tea)에 관한 텍스트를 복사해서 사용해도 됩니다 ☕️

   그리고 조금만 기다려 주세요. TinyLlama가 최선을 다하고 있습니다 🦙🏋️‍♀️♥️

2. TinyLlama의 응답을 확인합니다. 모델 크기가 작으므로 응답 스타일과 품질이 Llama 3.2 3B와 다를 수 있습니다.

> **관찰 포인트**: TinyLlama의 응답은 GPU에서 실행되는 더 큰 모델에 비해 덜 정교하고(그리고 더 느릴) 수 있지만, CPU에서 실행되기 때문에 훨씬 더 저렴한 경우가 많습니다. 이것이 CPU 전용 배포를 선택할 때의 트레이드오프입니다.

3. 클라우드 호스팅 모델에서 경험했던 것과 응답을 비교해 보세요. 고려할 점은 다음과 같습니다.
   - **응답 품질**: 답변이 여전히 도움이 되고 정확한가요?
   - **응답 시간**: 지연 시간(latency)은 어떻게 비교되나요?

    실험 환경의 Canopy와 테스트 환경의 Canopy를 비교할 수 있습니다. 아직 GitOps 설정을 바꾸지 않았으므로 `test`와 `prod`는 계속 클라우드 모델을 사용합니다. [테스트 환경의 Canopy](https://canopy-ui-<USER_NAME>-test.<CLUSTER_DOMAIN>)를 열거나 아래 URL로 접속하세요.

    ```bash
    https://canopy-ui-<USER_NAME>-test.<CLUSTER_DOMAIN>
    ```

## 📊 성능 고려사항

모델을 CPU에서 실행하면 서로 다른 성능 특성이 나타납니다.

| 지표 | Cloud Endpoint | On-Prem CPU |
| ------ | -------------- | ----------- |
| Time to First Token | ~100-500ms | ~1-3초 |
| Tokens per Second | 50-100+ | 5-15 |
| Concurrency | High | Limited |
| Data Privacy | External | Full control |

개발 및 테스트 용도로는 CPU 추론이 충분히 적합합니다. 트래픽이 더 많은 프로덕션 워크로드를 위해서는, GPU 할당을 다시 검토하거나 모델 최적화 기법을 고려해야 할 것입니다 😉

여러분은 학생 데이터를 인프라 안에 완전히 머물게 하는 방법을 찾아냈습니다. 하지만 동료 학생들과 교수님들이 이 상황에 만족할까요?

TinyLlama로 정착하기 전에, 모델 최적화와 압축에 대해 먼저 살펴봅시다 🦙🌿
