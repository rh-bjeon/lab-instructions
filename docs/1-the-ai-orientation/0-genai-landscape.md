# 🌐 GenAI 환경과 파운데이션 모델

## 📝 생성형 AI란 무엇인가?

생성형 AI(Generative AI, GenAI)는 대규모 데이터셋에서 패턴을 학습하여 텍스트, 이미지, 오디오, 비디오, 심지어 코드까지 새로운 콘텐츠를 만들어낼 수 있는 모델을 가리킵니다.

수천 가지 요리를 맛본 마스터 셰프를 떠올려 보세요. 셰프는 모든 레시피를 직접 발명하지는 않았지만, 배운 맛의 조합을 바탕으로 새로운 요리를 만들어낼 수 있습니다. 마찬가지로 GenAI 모델은 인간처럼 "생각"하지 않습니다. 대신 학습 과정에서 익힌 공통 패턴을 바탕으로 결과물을 생성합니다.

아마 다음과 같은 것들을 본 적이 있을 것입니다.

* 친근한 어시스턴트처럼 질문에 답하는 챗봇
* 한 문장만으로 사실적인 이미지를 만들어내는 AI 도구
* 유명 아티스트의 스타일로 AI가 작곡한 음악

이 모든 것이 바로 실제로 작동하는 GenAI의 예시입니다!

> 🎯 **미리 보기:** 다음 장에서는 이러한 모델에게 효과적으로 "말을 거는" 방법, 즉 **프롬프팅(prompting)**이라고 불리는 기법을 살펴보겠습니다.

---

## 🏗️ 파운데이션 모델 — GenAI의 근간

GenAI 모델이 인상적인 결과를 내기 전에는 먼저 견고한 기반이 필요합니다. 바로 **파운데이션 모델(Foundation Models, FMs)**이 제공하는 것이 그 기반입니다. 이들은 매우 다양한 데이터로 학습된 대규모 모델로, 최소한의 추가 학습만으로도 수많은 작업에 범용적으로 활용할 수 있습니다.

GenAI가 노래를 연주하는 것이라면, 파운데이션 모델은 다양한 장르에 사용할 수 있는 잘 만들어진 악기와 같습니다. 일단 악기를 손에 넣으면, 연주할 올바른 곡(또는 프롬프트)만 알면 됩니다.

### 대표적인 파운데이션 모델:

* **GPT 시리즈 (OpenAI)** — 인간과 유사한 텍스트를 생성 (예: ChatGPT)
* **Stable Diffusion (Stability AI)** — 텍스트 설명으로부터 이미지를 생성
* **Whisper (OpenAI)** — 음성을 높은 정확도로 텍스트로 변환
* **Gemini (Google DeepMind)** — 텍스트, 이미지, 오디오 등을 처리하고 이해
* **Code LLaMA (Meta)** — 다양한 프로그래밍 언어로 코드를 생성하고 설명

> 🗣️ **알아두면 좋은 사실:** 오늘날 많은 모델이 "멀티모달(multimodal)"입니다. 즉, 한 번에 여러 종류의 데이터를 다룰 수 있다는 뜻입니다. 예를 들어 그림을 이해하면서 **동시에** 그 그림에 대해 대화를 나눌 수 있습니다.

---

## 📊 오픈 모델 vs 클로즈드 모델

소프트웨어와 마찬가지로 GenAI 모델에도 **오픈(open)** 방식과 **클로즈드(closed)** 방식이 있습니다.

| 특징    | 오픈 모델                             | 클로즈드 모델               |
| -------- | --------------------------------------- | --------------------------- |
| 접근성   | 무료 / 소스 공개                         | API 전용 / 상업적           |
| 제어권  | 가중치(weight) 및 파인튜닝에 대한 완전한 제어 | 제한적인 제어 / 블랙박스 |
| 예시 | LLaMA 3, Mistral, Stable Diffusion      | GPT-4, Claude, Gemini       |

**오픈 모델**은 자유롭게 실험하고, 자체 인프라에 배포하거나, 심지어 자신의 데이터로 파인튜닝할 수 있는 자유를 제공합니다.

**클로즈드 모델**은 다듬어진 사용 경험과 API를 통한 손쉬운 접근을 제공하지만, 투명성과 커스터마이징 측면에서는 제한적입니다.

> 💡 **팁:** 실제로는 많은 조직이 프라이버시, 제어, 성능에 대한 필요에 따라 두 방식을 혼용합니다. 이 주제도 앞으로 다루게 될 것입니다.

---

## 🔄 사전 학습, 파인튜닝, 프롬프팅

모델을 학습시키는 과정을 운동선수를 훈련시키는 것과 비슷하다고 생각해 보세요.

* **사전 학습(Pretraining)**은 전반적인 체력 훈련입니다 — 체력과 힘을 기르는 과정입니다(이 과정을 거쳐 파운데이션/베이스 모델이 만들어집니다).
* **파인튜닝(Fine-tuning)**은 특정 스포츠를 위한 전문 코칭입니다.
* **프롬프팅(Prompting)**은 경기 직전에 내리는 지시입니다.

| 단계       | 일어나는 일                                     | 예시                                         |
| ----------- | ------------------------------------------------ | ----------------------------------------------- |
| 사전 학습 | 모델이 거대한 데이터셋에서 일반적인 패턴을 학습 | 다양한 인터넷 데이터로 GPT-4를 학습         |
| 파인튜닝 | 모델이 특정 작업이나 도메인에 맞게 적응 | 법률 문서 분석을 위해 LLaMA 3를 파인튜닝 |
| 프롬프팅   | 사전 학습된 모델을 특정 작업에 활용하도록 유도     | ChatGPT에게 제품 소개 문구 작성을 요청 |

> 🗝️ **살짝 미리 보기:** 프롬프팅은 단순히 원하는 것을 모델에게 묻는 것처럼 간단해 보일 수 있지만, 올바른 프롬프트를 작성하는 일은 마법의 주문을 쓰는 것처럼 느껴질 수 있습니다. 다음 장에서 프롬프팅 전략을 더 깊이 살펴보겠습니다!

---

## 🌟 실제로 작동하는 GenAI의 예시

* **Claude (Anthropic)** — 더 안전하고 제어 가능한 AI 대화 경험으로 알려짐
* **Suno AI** — 간단한 텍스트 프롬프트로부터 AI가 생성한 음악을 만듦
* **LLaVA (Large Language and Vision Assistant)** — 텍스트와 이미지 이해를 결합
* **Gemini 2.5 Pro (Google)** — 멀티모달이며, 최대 100만 토큰에 이르는 거대한 컨텍스트를 처리할 수 있음

> 🚀 GenAI의 환경은 빠르게 진화하고 있습니다 — 오늘 최첨단으로 보이는 것이 내일은 표준이 될 수도 있습니다!

---

## 📝 간단 퀴즈!

<!-- 🔍 Foundation Model Identification -->

<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 퀴즈 1: 파운데이션 모델 식별하기</h3>

<p style="color:#495057; font-weight:500;">
다음 중 파운데이션 모델의 예시는 무엇일까요?
</p>

<style>
.quiz-container-next-easy{position:relative}
.quiz-option-next-easy{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-next-easy:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-next-easy{display:none}
.quiz-radio-next-easy:checked+.quiz-option-next-easy[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-next-easy:checked+.quiz-option-next-easy:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-next-easy{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#foundation-correct:checked~.feedback-next-easy[data-feedback="correct"],
#foundation-wrong1:checked~.feedback-next-easy[data-feedback="wrong1"],
#foundation-wrong2:checked~.feedback-next-easy[data-feedback="wrong2"]{display:block}
.feedback-next-easy[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-next-easy[data-feedback="wrong1"], .feedback-next-easy[data-feedback="wrong2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-next-easy">
  <input type="radio" name="quiz-foundation-1" id="foundation-wrong1" class="quiz-radio-next-easy">
  <label for="foundation-wrong1" class="quiz-option-next-easy" data-correct="false">📊 Random Forest</label>

  <input type="radio" name="quiz-foundation-1" id="foundation-correct" class="quiz-radio-next-easy">
  <label for="foundation-correct" class="quiz-option-next-easy" data-correct="true">📝 GPT-4</label>

  <input type="radio" name="quiz-foundation-1" id="foundation-wrong2" class="quiz-radio-next-easy">
  <label for="foundation-wrong2" class="quiz-option-next-easy" data-correct="false">📈 Logistic Regression</label>

  <div class="feedback-next-easy" data-feedback="correct">✅ 정답입니다! GPT-4는 파운데이션 모델입니다.</div>
  <div class="feedback-next-easy" data-feedback="wrong1">❌ Random Forest는 파운데이션 모델이 아니라 전통적인 머신러닝 알고리즘입니다. 파운데이션 모델은 다양한 데이터로 학습된 대규모 신경망입니다.</div>
  <div class="feedback-next-easy" data-feedback="wrong2">❌ Logistic Regression은 분류를 위한 통계적 기법이며, 파운데이션 모델이 아닙니다. 파운데이션 모델은 GPT, LLaMA와 같은 거대한 신경망을 말합니다.</div>
</div>
</div>

---
<!-- 
## 🧩 Activities for Peer Learning

### 🗺️ Activity 1 — **Model Map**

* Form small groups
* Each group picks a model type: LLM, Diffusion Model, Speech Model, Multimodal Model
* Research (or use provided materials) to fill out:

  * Model Name
  * Open or Closed
  * Known Use Case
  * Example Product using it
* Share with the class using sticky notes / whiteboard / Miro

---

### 🗣️ Activity 2 — **Open vs Closed Debate**

* Split into two teams
* Scenario: "You need to build a secure customer support chatbot for a bank."
* One team argues for Open Models, the other for Closed Models
* Discuss trade-offs on:

  * Privacy
  * Cost
  * Control
  * Performance
* End with a group reflection

---

## 💬 Discussion Prompt

> What are some risks of relying only on prompting with closed models in your industry?
> *(Share in small groups and report back)* -->

<!-- 🎯 Open vs Closed -->

<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 퀴즈 2: 오픈 모델 vs 클로즈드 모델</h3>

<p style="color:#495057; font-weight:500;">
오픈 파운데이션 모델에 대한 다음 설명 중 올바른 것은 무엇일까요?
</p>

<div class="quiz-container-next-easy">
  <input type="radio" name="quiz-open-closed" id="open-wrong1" class="quiz-radio-next-easy">
  <label for="open-wrong1" class="quiz-option-next-easy" data-correct="false">💰 상업적 목적으로 항상 무료로 사용할 수 있다</label>

  <input type="radio" name="quiz-open-closed" id="open-correct" class="quiz-radio-next-easy">
  <label for="open-correct" class="quiz-option-next-easy" data-correct="true">🔍 모델 가중치(weight)에 접근하고 이를 수정할 수 있게 해준다</label>

  <input type="radio" name="quiz-open-closed" id="open-wrong2" class="quiz-radio-next-easy">
  <label for="open-wrong2" class="quiz-option-next-easy" data-correct="false">🗣️ 모든 경우에 클로즈드 모델보다 성능이 더 좋다</label>

  <div class="feedback-next-easy" data-feedback="correct">✅ 정확합니다! 오픈 모델은 가중치에 접근할 수 있게 해주어 더 많은 제어권을 제공합니다.</div>
  <div class="feedback-next-easy" data-feedback="wrong1">❌ 항상 그렇지는 않습니다! "오픈"은 모델 가중치에 접근할 수 있다는 의미이지, 상업적 라이선스를 뜻하는 것은 아닙니다. 많은 오픈 모델이 상업적 사용에 제약을 두고 있습니다.</div>
  <div class="feedback-next-easy" data-feedback="wrong2">❌ 반드시 그렇지는 않습니다! 성능은 모델 크기, 학습 데이터, 구체적인 사용 사례 등 여러 요인에 따라 달라집니다. 클로즈드 모델이 오픈 모델보다 더 나은 성능을 보이는 경우도 많습니다.</div>
</div>

<style>
#open-correct:checked~.feedback-next-easy[data-feedback="correct"],
#open-wrong1:checked~.feedback-next-easy[data-feedback="wrong1"],
#open-wrong2:checked~.feedback-next-easy[data-feedback="wrong2"]{display:block}
</style>
</div>

---

## 📌 요약

* GenAI는 방대한 데이터셋으로 학습된 파운데이션 모델을 사용합니다
* 사전 학습, 파인튜닝, 프롬프팅은 핵심적인 적응 전략입니다
* 오픈 모델과 클로즈드 모델은 각각의 장단점이 있으며 — 모든 상황에 맞는 단 하나의 정답은 없습니다
* 협업과 토론은 실제 세계에서의 함의를 이해하는 데 도움이 됩니다
</content>
