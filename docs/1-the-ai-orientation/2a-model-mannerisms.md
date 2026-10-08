# 🎓 GenAI 101: 모델의 특성 :id=-genai-101-model-mannerisms

## 📚 목차 :id=-contents
- [🎓 GenAI 101: 모델의 특성](#-genai-101-model-mannerisms)
  - [📚 목차](#-contents)
  - [🧠 세상에는 다양한 AI가 있다](#there-is-a-lot-of-different-ai-out-there)
  - [🤖 생성형 AI 모델](#generative-ai-models)
  - [📜 GenAI 모델에 대한 4가지 진실](#truths-about-genai-models)
  - [🔍 진실 1: 말을 걸어야만 답한다](#truth-1-they-only-speak-when-spoken-to)
    - [🔍 실습: 직접 해보기!](#hands-on-lets-play)
  - [🎲 진실 2: 비결정적(non-deterministic)이다](#truth-2-they-are-non-deterministic)
    - [🔍 실습: 직접 테스트해보기](#hands-on-test-it-yourself)
  - [🤥 진실 3: 진실을 말하는 게 아니라 가능성이 높은 것을 말한다](#truth-3-they-dont-speak-the-truth-they-speak-the-probable)
    - [🔍 실습: 모델이 거짓말을 할 수 있을까?](#hands-on-can-the-model-lie)
  - [🧠 진실 4: 기억력이 없다](#truth-4-they-have-no-memory)
    - [🔍 실습: 모델이 당신을 기억할까?](#hands-on-does-the-model-remember-you)
  - [✅ 요약](#recap)

## 🧠 세상에는 다양한 AI가 있다 :id=there-is-a-lot-of-different-ai-out-there

본격적으로 들어가기 전에, 중요한 구분 하나를 명확히 해 둡시다.

- **생성형 AI(Generative AI)**는 무언가를 **생성(generate)**하려 하며, 여기에는 종종 많은 변동성(variance)이 포함됩니다
- **예측형 AI(Predictive AI)**는 가장 가능성이 높은 답을 **예측(predict)**하려고만 합니다

예를 들어, **예측형 AI**에게 개에 대해 물으면, 이미지를 분류해서 각각을 "DOG" 또는 "NOT DOG"로 레이블을 붙일 것입니다.

반면 **생성형 AI**에게 개에 대해 물으면, 이전에는 존재하지 않았던 완전히 새로운 개 이미지를 *만들어낼* 것입니다.

![예측형 AI vs 생성형 AI — 개 예시](images/predictive-vs-generative-dogs.png)

> 이 교육에서는 **생성형 AI(GenAI)**에 초점을 맞춥니다.

GenAI 모델이 생성할 수 있는 데이터 유형은 다양합니다.

| 유형 | 예시 |
|------|----------|
| 📷 이미지 | DALL-E, Stable Diffusion |
| 📝 텍스트 | LLaMA, GPT, Granite |
| 🔊 오디오 | Whisper, Bark |
| 🎬 비디오 | Sora, Runway |

우리는 **텍스트 생성**, 그중에서도 특히 **대형 언어 모델(LLM)**에 초점을 맞출 것입니다.

<!-- ![GenAI can generate many types of data](images/genai-data-types.png) -->


<!-- 📝 Pop Quiz – What do LLMs generate? -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">대형 언어 모델(LLM)은 어떤 종류의 데이터를 생성할까요?</p>

<style>
.quiz-container-llm-type{position:relative}
.quiz-option-llm-type{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-llm-type:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-llm-type{display:none}
.quiz-radio-llm-type:checked+.quiz-option-llm-type[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-llm-type:checked+.quiz-option-llm-type:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-llm-type{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#llm-type-correct:checked~.feedback-llm-type[data-feedback="correct"],
#llm-type-wrong1:checked~.feedback-llm-type[data-feedback="wrong1"],
#llm-type-wrong2:checked~.feedback-llm-type[data-feedback="wrong2"],
#llm-type-wrong3:checked~.feedback-llm-type[data-feedback="wrong3"]{display:block}
.feedback-llm-type[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-llm-type[data-feedback="wrong1"], .feedback-llm-type[data-feedback="wrong2"], .feedback-llm-type[data-feedback="wrong3"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-llm-type">
  <input type="radio" name="quiz-llm-type" id="llm-type-wrong1" class="quiz-radio-llm-type">
  <label for="llm-type-wrong1" class="quiz-option-llm-type" data-correct="false">📷 이미지</label>

  <input type="radio" name="quiz-llm-type" id="llm-type-correct" class="quiz-radio-llm-type">
  <label for="llm-type-correct" class="quiz-option-llm-type" data-correct="true">📝 텍스트</label>

  <input type="radio" name="quiz-llm-type" id="llm-type-wrong2" class="quiz-radio-llm-type">
  <label for="llm-type-wrong2" class="quiz-option-llm-type" data-correct="false">🔊 오디오</label>

  <input type="radio" name="quiz-llm-type" id="llm-type-wrong3" class="quiz-radio-llm-type">
  <label for="llm-type-wrong3" class="quiz-option-llm-type" data-correct="false">🎬 비디오</label>

  <div class="feedback-llm-type" data-feedback="correct">✅ 정답입니다! LLM의 두 번째 "L"은 Language(언어)를 의미합니다 — 텍스트를 입력받아 텍스트를 출력합니다. 이 5일 동안 단 하나만 마음에 새겨야 한다면, 바로 이것입니다!</div>
  <div class="feedback-llm-type" data-feedback="wrong1">❌ 이미지 생성 모델도 존재하지만, LLM은 특히 텍스트를 다룹니다. Large Language Model에서 "Language"가 바로 그 힌트입니다!</div>
  <div class="feedback-llm-type" data-feedback="wrong2">❌ Whisper와 같은 오디오 모델도 존재하지만, LLM은 전적으로 텍스트에 관한 것입니다. 두 번째 "L"은 Language를 뜻합니다!</div>
  <div class="feedback-llm-type" data-feedback="wrong3">❌ 비디오 생성도 존재하지만, LLM은 특히 텍스트를 생성합니다. Large *Language* Model이라는 점을 기억하세요.</div>
</div>
</div>

> **핵심 요점:** LLM은 **텍스트**를 입력으로 받아 **텍스트**를 출력으로 만들어냅니다. 그게 전부입니다.
>
> `Text → LLM → Text`


## 🤖 생성형 AI 모델 :id=generative-ai-models

모델을 둘러싸고 있는 것들은 매우 많습니다. 구성(configuration), 데이터 검증, 안전성, 서빙 인프라, 관찰 가능성(observability), 도구 및 API, 프로세스 자동화, 데이터 준비, 분석 및 평가, 사용자 인터페이스, 프로세스 관리 도구, 벡터 데이터베이스 등이 있습니다.

![모델을 둘러싼 수많은 요소들](images/model-ecosystem.png)

이 모든 것들이 모델의 역량을 확장시킵니다. 하지만 먼저 **모델 자체**에만 집중해 봅시다.

![모델 자체에만 집중해 봅시다](images/model-focus.png)


## 📜 GenAI 모델에 대한 4가지 진실 :id=truths-about-genai-models

GenAI 모델이 작동하는 방식에 대해 **4가지 근본적인 진실**이 있습니다. 실습을 통해 하나씩 살펴보겠습니다.

1. **말을 걸어야만 답한다**
2. **비결정적(non-deterministic)이다** (무작위적)
3. **진실을 말하는 게 아니라 가능성이 높은 것을 말한다**
4. **기억력이 없다**

실제로 확인해 봅시다!


## 🔍 진실 1: 말을 걸어야만 답한다 :id=truth-1-they-only-speak-when-spoken-to

우리가 **프롬프트**를 보내지 않으면 모델 자체는 아무것도 하지 않습니다.

프롬프트가 주어지지 않으면(즉 입력이 전송되지 않으면), 모델은 아무것도 출력하지 않습니다. 커피 머신을 떠올려 보세요. 커피를 요청하지 않으면 아무것도 만들어내지 않습니다.

![커피 머신 비유](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcm51bjBqazB4emVtdnNuN2Vxc3ZiNjU1dTBqYjRta3ppMWY3MjlhayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YA6FYcwm2QUHpDtvF2/giphy.gif)

### 🔍 실습: 직접 해보기! :id=hands-on-lets-play

아래 채팅 인터페이스를 사용해 보세요. 모델에게 무엇이든 물어보세요. 예를 들어 간단하게 이렇게 물어볼 수 있습니다.

```
Hi, how are you feeling today?
```

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

모델이 무언가를 보낸 **후에만** 응답한다는 점에 주목하세요. 모델은 결코 스스로 먼저 대화를 시작하지 않습니다.


## 🎲 진실 2: 비결정적(non-deterministic)이다 :id=truth-2-they-are-non-deterministic

LLM에게서 항상 같은 답을 받게 될까요?

### 🔍 실습: 직접 테스트해보기 :id=hands-on-test-it-yourself

모델에게 **정확히 같은 질문을 두 번** 해보세요.

```
Hi, how are you feeling today?
```

두 응답을 비교해 보세요. 같은 답을 받았나요?

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

<!-- 🍿 Pop Quiz – Same answer? -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">LLM에게서 항상 같은 답을 받게 될까요?</p>

<style>
.quiz-container-deterministic{position:relative}
.quiz-option-deterministic{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-deterministic:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-deterministic{display:none}
.quiz-radio-deterministic:checked+.quiz-option-deterministic[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-deterministic:checked+.quiz-option-deterministic:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-deterministic{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#deterministic-correct:checked~.feedback-deterministic[data-feedback="correct"],
#deterministic-wrong1:checked~.feedback-deterministic[data-feedback="wrong1"]{display:block}
.feedback-deterministic[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-deterministic[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-deterministic">
  <input type="radio" name="quiz-deterministic" id="deterministic-wrong1" class="quiz-radio-deterministic">
  <label for="deterministic-wrong1" class="quiz-option-deterministic" data-correct="false">✅ TRUE — 네, 항상 같은 답입니다</label>

  <input type="radio" name="quiz-deterministic" id="deterministic-correct" class="quiz-radio-deterministic">
  <label for="deterministic-correct" class="quiz-option-deterministic" data-correct="true">❌ FALSE — 아니요, 답은 매번 달라집니다</label>

  <div class="feedback-deterministic" data-feedback="correct">✅ 정답입니다! LLM은 비결정적(non-deterministic)입니다 — 답을 생성할 때 무작위성을 사용하므로, 매번 다른 응답을 받게 됩니다. 이는 동시에 당신의 질문에 결코 지치지 않는다는 뜻이기도 합니다!</div>
  <div class="feedback-deterministic" data-feedback="wrong1">❌ 아닙니다! 방금 보았듯이 같은 질문에도 다른 답이 나옵니다. LLM은 생성 과정에 어느 정도의 무작위성을 포함하고 있습니다.</div>
</div>
</div>


## 🤥 진실 3: 진실을 말하는 게 아니라 가능성이 높은 것을 말한다 :id=truth-3-they-dont-speak-the-truth-they-speak-the-probable

LLM은 사실 아무것도 "알지" 못합니다! 학습 과정에서 본 패턴을 바탕으로 **가장 가능성이 높은** 다음 단어를 생성할 뿐입니다.

### 🔍 실습: 모델이 거짓말을 할 수 있을까? :id=hands-on-can-the-model-lie

모델에게 다음과 같이 물어보세요.

```
What are the last two digits of pi?
```

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

모델이 답을 주었나요? 파이(pi)는 **무리수(irrational number)**입니다 — "마지막 두 자리"라는 것이 존재하지 않습니다. 그럼에도 모델은 자신 있게 답을 내놓을 것입니다!

![어머, 모델이 방금 우리에게 거짓말을 한 걸까요?](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdG5sdWRianF6OXQ3bHZ2bzRzemMxYXNheTR2anc1aTJnN3IxNXAzdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Nm8ZPAGOwZUQM/giphy.gif)

> 마치 전에 들었던 말을 그것이 진실인지 아닌지도 모른 채 그대로 따라 말하는 앵무새와 비슷합니다. 그리고 그 대답은 **자신 있게** 전달됩니다!


## 🧠 진실 4: 기억력이 없다 :id=truth-4-they-have-no-memory

LLM은 당신이 말한 것으로부터 배울 수 있을까요?

### 🔍 실습: 모델이 당신을 기억할까? :id=hands-on-does-the-model-remember-you

다음을 두 단계로 시도해 보세요.

1. **모델에게 당신의 이름을 알려주세요** (예: "Hi, my name is Robert")
2. **새로운 대화를 시작**하고 물어보세요: "What is my name?"

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

모델이 당신의 이름을 기억했나요? 아마 아닐 것입니다!

<!-- 🍿 Pop Quiz – Memory -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">모델이 당신의 이름을 학습했습니다.</p>

<style>
.quiz-container-memory{position:relative}
.quiz-option-memory{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-memory:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-memory{display:none}
.quiz-radio-memory:checked+.quiz-option-memory[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-memory:checked+.quiz-option-memory:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-memory{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#memory-correct:checked~.feedback-memory[data-feedback="correct"],
#memory-wrong1:checked~.feedback-memory[data-feedback="wrong1"]{display:block}
.feedback-memory[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-memory[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-memory">
  <input type="radio" name="quiz-memory" id="memory-wrong1" class="quiz-radio-memory">
  <label for="memory-wrong1" class="quiz-option-memory" data-correct="false">✅ TRUE</label>

  <input type="radio" name="quiz-memory" id="memory-correct" class="quiz-radio-memory">
  <label for="memory-correct" class="quiz-option-memory" data-correct="true">❌ FALSE</label>

  <div class="feedback-memory" data-feedback="correct">✅ 정답입니다! 모델은 당신의 이름을 *학습*하지 않았습니다 — 지속적인 메모리가 없기 때문입니다. 새로운 대화는 매번 완전히 처음부터 시작됩니다. 모델은 결국 우리의 이름을 배우지 못했습니다 :'(</div>
  <div class="feedback-memory" data-feedback="wrong1">❌ 모델은 대화로부터 학습하지 않습니다. 한 세션에서 이름을 알려주고 새 세션을 시작하면, 모델은 당신이 누구인지 전혀 알지 못합니다. 모든 대화는 처음부터 다시 시작됩니다.</div>
</div>
</div>

> 이는 또한 모델이 **당신의 질문에 결코 지치지 않는다는** 뜻이기도 합니다! 같은 것을 백만 번 물어봐도, 매번 처음인 것처럼 기꺼이 답해줄 것입니다 🙈


## ✅ 요약 :id=recap

이제 **GenAI 모델에 대한 4가지 진실**의 베일을 벗겨 보았습니다.

| 진실 | 실제로 의미하는 것 |
|-------|--------------------------|
| 말을 걸어야만 답한다 | 무언가를 보내지 않으면 모델은 아무것도 하지 않았다 |
| 비결정적이다 | 매번 다르게 응답한다 |
| 진실을 말하는 게 아니라 가능성이 높은 것을 말한다 | **자신 있게** 우리에게 그냥 거짓말을 할 수도 있다 |
| 기억력이 없다 | 결국 우리의 이름을 배우지 못했다 :'( |

이제 모델이 *어떻게* 행동하는지 이해했으니, 프롬프팅을 통해 그 행동을 **제어**하는 방법을 배워봅시다.
</content>
