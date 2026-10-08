# 📊 LLM 성능과 하드웨어 :id=llm-performance-and-hardware

## 📚 목차 :id=contents
- [📊 LLM 성능과 하드웨어](#llm-performance-and-hardware)
  - [📚 목차](#contents)
  - [📊 주요 성능 지표](#key-performance-metrics)
  - [📦 모델 크기와 요구 사항](#model-sizes-and-requirements)
  - [📃 모델 카드로부터 모델 리소스 요구 사항 이해하기](#how-to-understand-model-resource-requirements-from-model-cards)
  - [👀 실제로 확인해 보기](#lets-see-this-in-practice)
  - [✅ 요약](#summary)

## 📊 주요 성능 지표 :id=key-performance-metrics

하드웨어와 모델 크기를 다루기 전에, 모델의 응답성과 효율성을 어떻게 측정하는지 이해하는 것이 도움이 됩니다. 이 핵심 지표들은 모델이 얼마나 빨리 말을 시작하는지, 각 단어를 얼마나 빠르게 생성하는지, 그리고 얼마나 많은 자원을 사용하는지를 파악하는 데 도움을 줍니다.

| 지표                  | 의미                                                      |
|-------------------------|--------------------------------------------------------------|
| **TTFT**                | Time to First Token – 질문을 한 후 모델이 첫 번째 토큰을 내놓기까지 걸리는 시간. |
| **TPOT**                | Time Per Output Token – 응답이 시작된 후 각 다음 토큰이 생성되는 속도. |
| **Throughput**          | 시스템이 속도 저하 없이 동시에 처리할 수 있는 요청의 수. |
| **VRAM 사용량**          | 모델이 필요로 하는 GPU 메모리의 양(모델이 크거나 대화가 길어질수록 더 많은 메모리가 필요함). |

이 지표들은 OpenShift AI 배포에서 지연 시간(latency)과 비용 사이의 균형을 맞추는 데 도움이 됩니다.

<!-- 📏 Latency root-cause quiz -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📏 퀴즈</h3>

<p style="color:#495057;font-weight:500;">
당신의 데모는 LLM 답변을 스트리밍한 뒤, 맨 마지막에 <b>약 900 KB</b> 크기의 PNG 차트를 덧붙입니다.<br>
텔레메트리 결과는 다음과 같습니다.
</p>

<ul style="margin-left:1.2em;color:#5a5a5a;">
  <li>TTFT 약 4초</li>
  <li>TPOT 약 30ms</li>
  <li>PNG 전송 시간 약 3초</li>
</ul>

<p style="color:#495057;font-weight:500;">
사용자가 느끼는 체감 속도를 <b>가장 직접적으로</b> 개선할 수 있는 변경 사항은 무엇일까요?
</p>

<style>
.latOpt{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;
       border:2px solid #e9ecef;color:#495057;transition:.2s}
.latOpt:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.latRad{display:none}
.latRad:checked + .latOpt[data-good="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.latRad:checked + .latOpt[data-good="false"]{background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.latFeed{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#lat-good:checked ~ .latFeed[data-type="good"],
#lat-w1:checked  ~ .latFeed[data-type="bad1"],
#lat-w2:checked  ~ .latFeed[data-type="bad2"]{display:block}
.latFeed[data-type="good"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.latFeed[data-type="bad1"], .latFeed[data-type="bad2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div>
  <input type="radio" id="lat-w1" name="lat" class="latRad">
  <label for="lat-w1" class="latOpt" data-good="false">
    🖼️ PNG를 900 KB → 150 KB로 압축한다.
  </label>

  <input type="radio" id="lat-good" name="lat" class="latRad">
  <label for="lat-good" class="latOpt" data-good="true">
    ⚡ 모델을 더 빠르고 항상 준비된(always-warm) GPU로 옮긴다(가중치와 캐시가 미리 로드됨).
  </label>

  <input type="radio" id="lat-w2" name="lat" class="latRad">
  <label for="lat-w2" class="latOpt" data-good="false">
    ✏️ 응답 길이를 20% 줄인다.
  </label>

  <div class="latFeed" data-type="good">
    ✅ 가장 큰 문제는 텍스트가 스트리밍되기 <em>전</em>의 4초간의 침묵입니다.
    워밍업된 GPU에서 모델 시작 시간을 줄이는 것이 이 공백을 직접 해결합니다.
  </div>
  <div class="latFeed" data-type="bad1">
    ❌ PNG 압축은 도움이 되지만, 끝부분의 작은 지연만을 줄여줄 뿐입니다.
  </div>
  <div class="latFeed" data-type="bad2">
    ❌ 응답을 짧게 하면 전체 시간이 줄어들지만, 몇 초 동안 텍스트가 스트리밍되는 것을 지켜보는 것보다 더 답답한 것이 있습니다.
  </div>
</div>
</div>

---

## 📦 모델 크기와 요구 사항 :id=model-sizes-and-requirements

모델은 다양한 크기로 존재합니다. 모델이 클수록(파라미터 수십억 개 단위로 측정) 응답이 더 똑똑하고 상세해질 수 있습니다. 하지만 큰 모델은 더 강력한 GPU와 더 많은 메모리를 필요로 하며, 이는 실행을 더 느리게 하거나 비용을 더 많이 들게 할 수 있습니다.

모델을 로드하고 실행할 때 가장 큰 병목은 GPU 메모리입니다.
간단히 생각하면: 파라미터 수 × 4 = 필요한 GPU 메모리입니다.
예를 들어, 30억(3B) 파라미터 모델은 로드하고 실행하는 데 약 12GB의 GPU 메모리가 필요합니다.

| 모델 크기     | 파라미터 | GPU 요구 사항            | 비고                            |
|----------------|------------|-----------------------------|----------------------------------|
| **<3B**         | 소형      | VRAM 8–12GB                | 경량, 빠름, 배포가 쉬움             |
| **7B–13B**      | 중형     | VRAM ≥24GB 또는 양자화됨*     | 성능과 비용의 균형          |
| **>30B**        | 대형      | 멀티 GPU 또는 고사양 카드 | 맥락 이해는 더 뛰어나지만 느리고 비용이 많이 듦 |

🧠 더 큰 모델이 더 똑똑할 수는 있지만, 더 작은 모델이 흔히 더 빠르고 배포하기도 쉽습니다.

_* 양자화(Quantization)는 모델이 차지하는 공간을 줄여, 더 빠르게 실행되고 더 작은 GPU에도 들어갈 수 있게 합니다. 품질이 약간 저하되지만 대부분의 경우 충분히 잘 작동합니다._


## 📃 모델 카드로부터 모델 리소스 요구 사항 이해하기 :id=how-to-understand-model-resource-requirements-from-model-cards


[Hugging Face](https://huggingface.co/)는 개발자들이 머신러닝 모델, 특히 대형 언어 모델을 공유하고 탐색하고 배포하는 플랫폼이자 모델 허브입니다.
우리 중 많은 사람이 Hugging Face를 이용해 모델을 둘러보고 다운로드합니다.

Hugging Face에서 대형 언어 모델을 둘러보면, 각 모델에는 **모델 카드**(model card)가 있습니다 — 모델의 아키텍처, 학습 데이터, 사용 목적, 그리고 종종 하드웨어 요구 사항까지 담긴 요약 페이지입니다. 예를 들어 Llama 4 컬렉션의 [Llama-4-Scout-17B-16E-Instruct](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct) 모델을 살펴보세요.

리소스에 대한 힌트를 찾을 수 있는 곳:

* **모델 크기 / 파라미터 수:** 대개 "Model Details" 또는 "Model Information" 섹션에 나와 있습니다. 이를 통해 모델의 대략적인 규모를 파악할 수 있습니다(예: 7B, 13B, 70B 파라미터).
* **하드웨어 요구 사항:** 때로는 "Requirements" 또는 "Inference Performance"와 같은 섹션에 명시적으로 나와 있으며, VRAM 요구량이나 추천 GPU 종류를 언급할 수 있습니다.
* **양자화 지원:** 일부 모델 카드는 모델이 4비트 또는 8비트 양자화를 지원하는지 명시하는데, 이는 VRAM 사용량을 줄이는 데 도움이 됩니다.
* **최대 컨텍스트 길이:** 컨텍스트 윈도우가 길수록 더 많은 메모리가 필요하며, 모델마다 처리할 수 있는 컨텍스트 윈도우 크기가 다르므로 VRAM 요구량을 추정할 때 중요한 요소입니다.

이러한 세부 정보가 직접 명시되어 있지 않다면, 앞서 설명한 것처럼 모델 크기를 바탕으로 대략적인 메모리 요구량을 추정할 수 있습니다. 파라미터 수에 **4바이트**(FP32의 경우) 또는 **2바이트**(FP16/half precision의 경우)를 곱하면 모델 가중치를 로드하는 데 필요한 VRAM의 대략적인 수치를 얻을 수 있습니다. 추론(inference) 중 활성화 버퍼나 KV 캐시를 위한 추가 VRAM도 필요하다는 점을 잊지 마세요.

Hugging Face에서 이러한 세부 사항을 확인하고 위의 대략적인 가이드라인을 활용하면, 모델을 원활하게 실행하는 데 필요한 하드웨어를 추정할 수 있습니다.

<!-- 📦 model size / GPU trade-off -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📦 퀴즈</h3>

<p style="color:#495057;font-weight:500;">
당신은 지원 티켓을 50개 카테고리 중 하나로 <b>자동 분류</b>하는 어시스턴트가 필요합니다.<br>
목표 트래픽: 초당 약 20건의 요청.<br>
GPU 예산: A10 24GB 1개.
</p>

<p style="color:#495057;font-weight:500;">어떤 모델 선택이 가장 적합할까요?</p>

<style>
.szOpt{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;
       border:2px solid #e9ecef;color:#495057;transition:.2s}
.szOpt:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.szRad{display:none}
.szRad:checked + .szOpt[data-good="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.szRad:checked + .szOpt[data-good="false"]{background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.szFeed{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#sz-good:checked ~ .szFeed[data-type="good"],
#sz-w1:checked  ~ .szFeed[data-type="bad1"],
#sz-w2:checked  ~ .szFeed[data-type="bad2"]{display:block}
.szFeed[data-type="good"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.szFeed[data-type="bad1"], .szFeed[data-type="bad2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div>
  <input type="radio" id="sz-w1" name="sz" class="szRad">
  <label for="sz-w1" class="szOpt" data-good="false">
    70B를 4비트로 양자화
  </label>

  <input type="radio" id="sz-good" name="sz" class="szRad">
  <label for="sz-good" class="szOpt" data-good="true">
    7B를 16비트로 양자화
  </label>

  <input type="radio" id="sz-w2" name="sz" class="szRad">
  <label for="sz-w2" class="szOpt" data-good="false">
    양자화하지 않은 3B(FP32)를 CPU에서 실행
  </label>

  <div class="szFeed" data-type="good">
    ✅ 7B @ 16비트 ≈ 7B × 2바이트 ≈ 14GB → KV 캐시(컨텍스트 윈도우)를 위한 여유 공간까지 포함해 24GB에 충분히 들어가며, 초당 20건의 요청도 처리할 수 있습니다.
  </div>
  <div class="szFeed" data-type="bad1">
    ❌ 4비트로 양자화해도(파라미터당 약 0.5바이트), 70B ≈ 35GB → 24GB 예산을 초과합니다. 게다가 4비트 양자화는 정확도를 떨어뜨릴 수 있습니다.
  </div>
  <div class="szFeed" data-type="bad2">
    ❌ 3B FP32 = 약 12GB로 용량 자체는 맞을 수 있지만, CPU 추론은 초당 20건의 요청을 처리하기에는 너무 느립니다. 이 처리량 요구 사항을 맞추려면 GPU 가속이 필요합니다.
  </div>
</div>
</div>

## 👀 실제로 확인해 보기 :id=lets-see-this-in-practice

아래에서 Llama 3.2 3B의 두 가지 버전을 나란히 비교해볼 수 있습니다.

- **모델 1 (Llama 3.2 3B):** FP16 정밀도의 원본 모델
- **모델 2 (Llama 3.2 3B FP8):** 동일한 모델을 FP8 정밀도로 압축한 버전(FP8 정밀도가 무엇을 의미하는지는 곧 배우게 됩니다)

FP8 버전은 메모리를 **절반만** 사용합니다. 하지만 품질의 차이를 느낄 수 있을까요?

**다음 프롬프트들을 시도해보고 응답을 비교해 보세요.**

1. `Explain photosynthesis in simple terms`
2. `Write a haiku about debugging code`
3. `What are Ireland's chances in the upcoming Six Nations?`

<iframe
    src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/compare?embed"
    frameborder="0"
    width="850"
    height="1000"
    style="border: 1px solid #ccc; border-radius: 8px;"
    loading="lazy">
</iframe>


어떤 점을 느꼈나요?

- **품질:** 어떤 응답이 "더 나은지" 구별할 수 있었나요?
- **일관성:** 두 모델 모두 비슷한 답변을 주었나요?
- **속도:** 한쪽이 눈에 띄게 더 빨랐나요? (참고: 서로 다른 GPU에서 실행되므로 여기서 속도 비교는 공정하지 않습니다)

만약 응답의 품질이 비슷하게 느껴졌다면... 바로 그것이 핵심입니다. FP8 모델은 파라미터당 **절반의 비트**만 사용하면서도 거의 동일한 출력을 만들어냅니다.

모델을 절반 크기로 압축해도 *왜* 망가지지 않는 걸까요? 이것이 바로 이 모듈에서 다루는 내용입니다.

---


## ✅ 요약 :id=summary

이 장에서 살펴본 중요한 개념들을 간단히 복습하며 마무리하겠습니다. 이 용어들은 LLM이 내부적으로 어떻게 작동하는지, 그리고 성능과 배포를 어떻게 생각해야 하는지를 이해하는 데 도움이 될 것입니다.

| 개념                | 핵심 아이디어                                                            |
|------------------------|---------------------------------------------------------------------|
| **토큰 (Token)**              | LLM이 한 번에 처리하는 가장 작은 텍스트 단위 — 단어 전체 또는 단어의 일부와 비슷합니다. 토큰을 모델이 사용하는 언어의 기본 구성 단위라고 생각하면 됩니다. |
| **다음 토큰 기계** | LLM은 이전에 나온 내용을 바탕으로 한 번에 하나의 토큰을 예측하는 방식으로 작동합니다. 응답을 한 단계씩 생성합니다. |
| **어텐션 (Attention)**          | 다음에 생성할 토큰을 결정할 때, 모델이 입력의 중요한 부분에 집중할 수 있게 해주는 방법입니다. |
| **컨텍스트 길이**     | 모델이 한 번에 "기억"할 수 있는 최근 대화나 텍스트의 양으로, 보통 토큰 단위로 측정됩니다. |
| **KV 캐시**           | 이전 계산의 일부를 기억함으로써 토큰 생성 속도를 높여주는 메모리 단축 기법입니다. |
| **프롬프팅**          | 모델에게 제공하는 입력 텍스트를 신중하게 설계함으로써 모델의 동작을 이끄는 방법입니다. |
| **환각 (Hallucination)**      | 모델이 실제처럼 들리지만 잘못된 사실이나 세부 정보를 만들어내는 현상입니다. |
| **가드레일 (Guardrails)**         | 모델의 출력을 안전하고, 정확하며, 주제에서 벗어나지 않도록 유지하는 기법과 통제 수단입니다. |
| **TTFT & TPOT**        | 모델이 응답을 시작하는 속도와 각 다음 단어를 생성하는 속도를 보여주는 지표입니다. |
| **VRAM & Throughput**  | 필요한 GPU 메모리의 양과 동시에 서비스할 수 있는 사용자 수를 나타냅니다. |
| **모델 크기 & GPU**   | 하드웨어와 필요에 맞는 적절한 모델 크기를 선택하면 성능과 비용의 최적 균형을 이룰 수 있습니다. |



[🔝 목차로 돌아가기](#contents)
</content>
