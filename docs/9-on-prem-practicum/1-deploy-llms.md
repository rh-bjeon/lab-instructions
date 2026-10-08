# 🏠 LLM을 On-Prem으로 배포하기

데이터 기밀성(confidentiality) 요구사항 때문에, 모델을 직접 호스팅해야 합니다. LLM을 사내(in-house)에서 실행하면 민감한 학생 데이터가 여러분의 인프라 내부에 머물게 되어, 데이터 거버넌스와 컴플라이언스를 완전히 통제할 수 있습니다.

고성능 추론(inference)에는 일반적으로 전용 GPU 리소스가 필요하다는 것을 우리는 알고 있습니다. 하지만 IT 부서에서 방금 지금은 GPU를 내줄 수 없다고 알려왔습니다. 그러면 개인정보 보호 요구사항을 타협하지 않으면서 어떻게 개발을 계속할 수 있을까요?

답은: 인프라를 구축하는 동안 더 작고 CPU 친화적인 모델로 시작하는 것입니다. 어떤 선택지가 있는지 살펴봅시다.

## 🔍 On-Prem에서는 어떤 모델을 실행할 수 있나요?

모든 모델이 거대한 GPU 클러스터를 필요로 하는 것은 아닙니다. LLM 생태계에는 강력한 데이터센터 GPU부터 소박한 CPU 전용 배포까지, 다양한 하드웨어 구성을 위해 설계된 모델들이 포함되어 있습니다.

### 📄 Model Card(모델 카드) 읽는 방법

[Hugging Face](https://huggingface.co/models)와 같은 플랫폼에 잘 문서화된 모든 LLM에는 **model card**(모델 카드)가 함께 제공됩니다. 이는 본질적으로 해당 모델에 대한 팩트 시트(fact sheet)입니다. Canopy를 위해 모델을 평가할 때 살펴볼 항목은 다음과 같습니다.

| 항목                   | 확인할 내용                                                          |
| ------------------------- | ------------------------------------------------------------------------- |
| **Model Architecture (모델 아키텍처)**    | LLaMA, Mistral, GPT 등 어떤 모델을 기반으로 하는가?                                 |
| **Size (파라미터 수)**     | 파라미터가 많을수록 보통 역량도 커지지만, 리소스 소모도 커집니다 |
| **Intended Use (사용 목적)**          | instruction-following, 일반 대화, 코드 등 어떤 용도에 최적화되어 있는가?      |
| **Training Data (학습 데이터)**         | 교육 목적 사용에 적합한가? 어떤 필터링이 이루어졌는가?               |
| **Limitations (한계)**           | 알려진 편향이나 약점이 있는가?                                                  |
| **License (라이선스)**               | 상업적/교육적 용도로 자유롭게 사용할 수 있는가?                                |
| **Hardware Requirements (하드웨어 요구사항)** | CPU 전용인가, GPU가 필요한가, 혹은 특정 메모리 제약이 있는가?                      |

지금까지 Canopy에는 Llama 3.2 3B를 사용해 왔습니다. 해당 모델의 model card를 살펴보세요: [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)

model card가 사용 목적, 학습 방법론, 하드웨어 권장 사항을 어떻게 명시하고 있는지 주목하세요. 이 정보는 모델이 여러분의 배포 제약 조건에 맞는지 판단할 때 매우 중요합니다.

## 💻 인프라 요구사항은 무엇인가요?

모든 모델이 고성능 GPU를 필요로 하는 것은 아니지만, 분명히 필요로 하는 모델들도 있습니다. 다음은 일반적인 사이징 가이드입니다.

| 모델 크기 | 필요한 GPU 메모리 | 예시 모델 |
| ---------- | ------------------- | -------------- |
| **< 3B parameters** | ~8–12GB VRAM (또는 CPU 전용) | TinyLlama 1.1B, Granite 2B |
| **3B–7B parameters** | ~16–24GB VRAM | Llama 3.2 3B, Mistral 7B |
| **7B–13B parameters** | ≥24GB GPU 메모리 | Llama 3.1 8B, CodeLlama 13B |
| **> 30B parameters** | 멀티 GPU 구성 | Llama 3.1 70B, Mixtral 8x7B |

**GPU가 없으신가요?** 몇 가지 선택지가 있습니다.

* **CPU 전용 런타임**: 추론 속도는 느리지만, 개발, 데모, 또는 트래픽이 적은 배포에는 충분히 적합합니다
* **양자화된(Quantized) 모델**: 메모리 사용량이 적은 저정밀도 모델 (4-bit, 8-bit) (스포일러는 여기까지만! 🤫🤫🤫)
* **클라우드 기반 엔드포인트**: 지금까지 사용해온 방식이지만, 기밀 데이터에는 적합하지 않습니다

GPU 할당이 지금 당장 불가능하고, 컴플라이언스 문제로 클라우드 엔드포인트도 선택지에서 제외된 상황이니, CPU에서 배포할 수 있는 것들을 살펴봅시다. 그리고 여러분이 라마를 좋아하시니 🦙🦙🦙, CPU 추론을 위해 특별히 설계된 1.1B 파라미터의 소형 모델인 [TinyLlama](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)를 발견하게 됩니다.

GPU 할당을 기다리는 동안 시작하기에 딱 좋습니다!


## 🚀 모델을 서빙(serve)하려면 어떻게 해야 하나요?

모델을 서빙한다는 것은, Canopy나 Llama Stack Playground와 같은 애플리케이션이 호출할 수 있는 API 엔드포인트를 통해 모델을 접근 가능하게 만드는 것을 의미합니다. 모델을 애플리케이션에 직접 포함시키는 대신, 추론 요청에 응답하는 독립적인 서비스로 배포합니다.

OpenShift AI에서는 **vLLM**을 서빙 런타임으로 사용하는 **KServe**를 통해 모델을 컨테이너화된 워크로드로 배포합니다. vLLM은 continuous batching과 PagedAttention과 같은 기능을 통해 효율적인 추론과 최적화된 메모리 사용을 제공합니다.

### 첫 On-Prem 모델 배포하기

1. **OpenShift AI** → **AI hub** → **Models**로 이동해서 `Other models`를 선택하세요. 거기서 `TinyLlama`를 찾으세요.

    ![model-catalog.png](./images/model-catalog.png)

2. TinyLlama를 클릭하고 model card를 읽어보세요. Hugging Face에서 읽었던 것과 거의 같은 내용입니다. 오른쪽 상단에서 **Deploy**를 클릭하세요.

    ![model-catalog-2.png](./images/model-catalog-2.png)

3. **Project**로 `<USER_NAME>-canopy`를 선택하고, 양식에 다음 설정을 입력하세요.

    **Model deployment name:** `tinyllama`

    여기서 `Edit resource name`을 클릭하세요.
    
    ![tinyllama-name.png](images/tinyllama-name.png)
    
    그리고 `tinyllamatinyllama-11b-chat-v1`을 그냥 `tinyllama`로 바꾸세요.

    ![tinyllama-name2.png](images/tinyllama-name2.png)

4. Hardware profiles에서: `Customize resource requests and limits`를 펼쳐서 TinyLlama에 CPU를 조금 더 할당하세요.

    **CPU Request:** 3

    **CPU Limit:** 4

    **Memory Request:** 6 GiB

    **Memory Limit:** 8 GiB

    ![tiny-resources.png](./images/tiny-resources.png)

    이제 `Next`를 클릭하세요.

5. **Deployment Resource:** `CUSTOM - vLLM Serving Runtime for CPU`

    ![tiny-deploy.png](./images/tiny-deploy.png)

    아직 `Next`를 누르지 마세요!

6. 이 페이지에서는 아무것도 바꾸지 마세요. 특히 **Model access**와 **Token authentication**은 체크하지 않은 상태로 두세요.

    - `Make deployed models available through an external route`를 **체크 해제**하세요. 모델이 클러스터 외부에서 접근 가능하게 만들고 싶지 않기 때문입니다.
    - `Require token authentication`을 **체크 해제**하세요. 이 부분은 나중에 다시 다룰 예정입니다 :)

  `Next`를 클릭해서 배포 내용을 검토하세요.

7. 검토 화면은 다음과 같아야 합니다.

  ![tiny-review.png](./images/tiny-review.png)

  그런 다음 `Deploy model`을 클릭하세요!

- 배포 진행 상황을 지켜보세요. 상태가 `Started`가 될 때까지 기다리세요. 이는 모델이 요청을 처리할 준비가 되었다는 의미입니다.

    ![tiny-deployed.png](./images/tiny-deployed.png)

## 🌐 모델에 어떻게 접근하나요?

배포가 완료되면, 모델은 OpenAI 호환 API 형식을 따르는 내부 REST 엔드포인트를 갖게 됩니다. 엔드포인트 URL은 다음 패턴을 따릅니다.

```
http://<model-name>-predictor.<namespace>.svc.cluster.local:8080/v1
```

`<USER_NAME>-canopy` 네임스페이스에 TinyLlama를 배포했으므로, 다음과 같은 형태가 됩니다.

```
http://tinyllama-predictor.<USER_NAME>-canopy.svc.cluster.local:8080/v1
```

또는, 대시보드에서 `Internal endpoint`를 클릭해서 확인할 수도 있습니다.

![tiny-endpoint.png](./images/tiny-endpoint.png)

### 모델 엔드포인트 테스트하기

워크벤치로 돌아가서 터미널에서 다음 명령을 실행해 모델이 응답하는지 확인하세요.

```bash
curl -s http://tinyllama-predictor.<USER_NAME>-canopy.svc.cluster.local:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tinyllama",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello! Can you introduce yourself?"}
    ],
    "max_tokens": 100
  }' | jq .
```

모델의 응답이 담긴 JSON 응답을 보게 될 것입니다. 응답 시간은 클라우드 엔드포인트에서 경험했던 것보다 느릴 수 있습니다. CPU 전용 추론에서는 예상되는 현상입니다.

> **참고**: 이 모델은 (외부 route가 없기 때문에) 클러스터 내부에서만 접근 가능합니다. 이는 보안을 위해 의도된 설계입니다 - 모델 엔드포인트를 내부에만 두면 공격 표면(attack surface)을 줄일 수 있습니다.

---

여러분이 원하는 만큼 빠르지는 않을 수도 있지만, 어쨋든 동작합니다! 그리고 가장 중요한 것은, 여러분의 데이터가 인프라 밖으로 절대 나가지 않는다는 점입니다.

이제 이 새로운 on-prem 엔드포인트를 사용하도록 Llama Stack과 Canopy를 업데이트해 봅시다.
