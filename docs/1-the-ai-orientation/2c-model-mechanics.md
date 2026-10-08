# 🔬 GenAI 103: 모델 메커니즘

## 📚 목차
- [🔍 모델이란 실제로 무엇인가?](#what-is-a-model-actually)
- [⚙️ 모델을 어떻게 사용하는가?](#how-do-we-use-the-model)
- [📏 모든 모델은 똑똑하지만, 어떤 모델은 더 똑똑하다](#all-models-are-smart-but-some-are-smarter)
- [🖥️ 하드웨어가 중요한 이유](#hardware-matters)
- [🏋️ 학습(Training) vs 파인튜닝(Fine-tuning)](#training-vs-fine-tuning)
- [🎯 모델은 텍스트를 어떻게 생성할까?](#how-does-the-model-generate-text)
- [👻 환각은 어디에 숨어 있을까](#where-hallucinations-hide)
- [✅ 우리가 배운 것](#what-we-have-learned)

## 🔍 모델이란 실제로 무엇인가? :id=what-is-a-model-actually

모델을 좀 더 자세히 살펴봅시다. 실제로 모델이란 무엇일까요?

궁극적으로 모델은 그 내부 동작을 설명하는 하나의 **바이너리 파일**일 뿐입니다.

![스쿠비 두 가면 벗기 — 모델은 그저 바이너리 파일일 뿐](images/scooby-doo-model.png)

모델 바이너리는 입력이 출력으로 어떻게 매핑되는지를 나타내는 수많은 **파라미터**의 집합일 뿐입니다.

- 지금은 이를 **블랙박스**로 취급해도 됩니다
- 파라미터가 많을수록 그 상자(모델)는 더 커집니다


## ⚙️ 모델을 어떻게 사용하는가? :id=how-do-we-use-the-model

모델에 텍스트를 통과시키려면 모델을 **실행**(execute)해야 합니다.

이는 보통 입력을 받으면 자동으로 모델을 실행하는 **런타임**(runtime)을 통해 이루어집니다.

이를 HTML 파일을 서빙해서 누구나 당신의 웹페이지에 접근할 수 있게 하는 것과 비슷하게 생각할 수 있습니다. 다만 HTML 대신, 텍스트 프롬프트에 응답하는 모델을 서빙하는 것입니다.

## 📏 모든 모델은 똑똑하지만, 어떤 모델은 더 똑똑하다 :id=all-models-are-smart-but-some-are-smarter

일반적으로:
- **더 큰 모델** = 더 많은 파라미터
- **더 많은 파라미터** = 더 똑똑한 모델
- 하지만 동시에, **더 많은 파라미터** = 더 느린 응답

![거북이 — 더 큰 모델은 더 느립니다](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbm51eWg4NmU0MTY3aGE5YjM5OXN5dXI0N2YyYzIxZjkzNGdwaG0zdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cYpV2OjeIyBRu5GpHQ/giphy.gif)

<!-- 🍿 Pop Quiz – Bigger = slower? -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">모델이 클수록 더 느립니다.</p>

<style>
.quiz-container-bigger-slower{position:relative}
.quiz-option-bigger-slower{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-bigger-slower:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-bigger-slower{display:none}
.quiz-radio-bigger-slower:checked+.quiz-option-bigger-slower[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-bigger-slower:checked+.quiz-option-bigger-slower:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-bigger-slower{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#bigger-slower-correct:checked~.feedback-bigger-slower[data-feedback="correct"],
#bigger-slower-wrong1:checked~.feedback-bigger-slower[data-feedback="wrong1"]{display:block}
.feedback-bigger-slower[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-bigger-slower[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-bigger-slower">
  <input type="radio" name="quiz-bigger-slower" id="bigger-slower-correct" class="quiz-radio-bigger-slower">
  <label for="bigger-slower-correct" class="quiz-option-bigger-slower" data-correct="true">✅ TRUE</label>

  <input type="radio" name="quiz-bigger-slower" id="bigger-slower-wrong1" class="quiz-radio-bigger-slower">
  <label for="bigger-slower-wrong1" class="quiz-option-bigger-slower" data-correct="false">❌ FALSE</label>

  <div class="feedback-bigger-slower" data-feedback="correct">✅ 정답입니다! 파라미터가 많아질수록 생성되는 단어마다 더 많은 연산이 필요합니다. 더 똑똑하지만 더 느린, 전형적인 트레이드오프입니다.</div>
  <div class="feedback-bigger-slower" data-feedback="wrong1">❌ 사실 더 큰 모델은 더 느립니다. 파라미터가 많아지면 생성되는 단어마다 더 많은 연산이 필요합니다. 더 똑똑한 모델을 위해 치러야 하는 대가입니다.</div>
</div>
</div>


## 🖥️ 하드웨어가 중요한 이유 :id=hardware-matters

### 🔍 실습: CPU vs GPU

모델을 **CPU**에서 실행해보고 느낌을 확인해 보세요.

1. 모델을 CPU로 변경합니다
2. 물어보세요: `"Hi, how are you feeling today?"`

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

속도 차이가 느껴지나요?

<!-- 🍿 Pop Quiz – GPU vs CPU -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">GenAI 모델은 CPU보다 GPU에서 훨씬 더 빠르게 실행됩니다.</p>

<style>
.quiz-container-gpu-cpu{position:relative}
.quiz-option-gpu-cpu{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-gpu-cpu:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-gpu-cpu{display:none}
.quiz-radio-gpu-cpu:checked+.quiz-option-gpu-cpu[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-gpu-cpu:checked+.quiz-option-gpu-cpu:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-gpu-cpu{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#gpu-cpu-correct:checked~.feedback-gpu-cpu[data-feedback="correct"],
#gpu-cpu-wrong1:checked~.feedback-gpu-cpu[data-feedback="wrong1"]{display:block}
.feedback-gpu-cpu[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-gpu-cpu[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-gpu-cpu">
  <input type="radio" name="quiz-gpu-cpu" id="gpu-cpu-correct" class="quiz-radio-gpu-cpu">
  <label for="gpu-cpu-correct" class="quiz-option-gpu-cpu" data-correct="true">✅ TRUE</label>

  <input type="radio" name="quiz-gpu-cpu" id="gpu-cpu-wrong1" class="quiz-radio-gpu-cpu">
  <label for="gpu-cpu-wrong1" class="quiz-option-gpu-cpu" data-correct="false">❌ FALSE</label>

  <div class="feedback-gpu-cpu" data-feedback="correct">✅ 정답입니다! GenAI 모델은 실행해야 하는 연산의 종류 때문에 CPU보다 GPU에서 **훨씬** 더 빠르게 실행됩니다. 일반적으로: GPU가 많을수록 더 빠르게 실행됩니다.</div>
  <div class="feedback-gpu-cpu" data-feedback="wrong1">❌ 사실 GPU는 GenAI 워크로드에서 훨씬 더 빠릅니다. 여기에 관련된 연산의 종류(행렬 연산)는 정확히 GPU가 설계된 목적에 부합합니다.</div>
</div>
</div>

### 트레이드오프 삼각형

모델이 커질수록:
- **더 똑똑해집니다**
- **더 느려집니다**
- **더 많은 하드웨어가 필요합니다**

전형적인 트레이드오프 삼각형입니다: **빠름, 저렴함, 좋음** — 그중 둘만 고를 수 있습니다.

![트레이드오프 삼각형](https://afspublishing.ca/wp-content/uploads/2024/01/Tradeoff-Triangle.png.webp)


## 🏋️ 학습(Training) vs 파인튜닝(Fine-tuning) :id=training-vs-fine-tuning

모델을 처음부터 **학습**(training)시키는 데는 엄청난 데이터, 하드웨어, 기술이 필요합니다. 세상에서 이를 성공적으로 해낼 수 있는 조직은 극히 드뭅니다.

하지만 기존 모델을 당신이 원하는 방식으로 더 잘 동작하도록 **파인튜닝**(fine-tune)할 수는 있습니다. 이는 대부분의 조직이 실현 가능합니다.

| | 학습(Training) | 파인튜닝(Fine-tuning) |
|--|----------|-------------|
| **무엇을 하는가** | 처음부터 모델을 구축 | 기존 모델을 조정 |
| **필요한 데이터** | 막대한 양(테라바이트 단위) | 상대적으로 적음 |
| **비용** | 매우 비쌈 | 감당할 수 있는 수준 |
| **누가 할 수 있는가** | 극히 소수의 조직 | 대부분의 조직 |


## 🎯 모델은 텍스트를 어떻게 생성할까? :id=how-does-the-model-generate-text

재미있는 실습을 해봅시다. 여기서 당신은 무엇을 선택하겠습니까?

> **Never gonna...**
>
> - give you up
> - let you down
> - run around and desert you
> - make you cry
> - say goodbye
> - tell a lie and hurt you

**"give you up"**이라고 답했다면 — 축하합니다, 당신은 방금 LLM처럼 행동한 것입니다!

![Never gonna give you up](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYndwNGtsMHV3MmN4NnVicWN2aWZjdGR4MXA2bGI5azgyYWN5bHczdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lgcUUCXgC8mEo/giphy.gif)

모델은 단순히 **빈도를 바탕으로 다음 단어를 선택**합니다. 학습된 모든 텍스트를 살펴보고, "Never gonna" 뒤에 가장 흔히 따라오는 단어를 파악한 뒤, 가장 확률이 높은 것을 고릅니다.

모델은 문장 전체를 한 번에 만들어내지 않습니다. **한 번에 한 단어씩** 선택하고, 방금 말한 것을 다시 돌아보며 다음에 올 것을 결정합니다.

생성된 각 단어는 다음 예측을 위한 입력의 일부가 됩니다.

1. 입력: `"Never gonna"` → 출력: `"give"`
2. 입력: `"Never gonna give"` → 출력: `"you"`
3. 입력: `"Never gonna give you"` → 출력: `"up"`
4. 이런 식으로 계속됩니다...

<!-- 🍿 Pop Quiz – Output becomes input -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">답변이 생성되는 동안, 새로 생성된 각 단어는 모델에 대한 입력의 일부가 됩니다.</p>

<style>
.quiz-container-autoregressive{position:relative}
.quiz-option-autoregressive{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-autoregressive:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-autoregressive{display:none}
.quiz-radio-autoregressive:checked+.quiz-option-autoregressive[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-autoregressive:checked+.quiz-option-autoregressive:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-autoregressive{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#autoregressive-correct:checked~.feedback-autoregressive[data-feedback="correct"],
#autoregressive-wrong1:checked~.feedback-autoregressive[data-feedback="wrong1"]{display:block}
.feedback-autoregressive[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-autoregressive[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-autoregressive">
  <input type="radio" name="quiz-autoregressive" id="autoregressive-correct" class="quiz-radio-autoregressive">
  <label for="autoregressive-correct" class="quiz-option-autoregressive" data-correct="true">✅ TRUE</label>

  <input type="radio" name="quiz-autoregressive" id="autoregressive-wrong1" class="quiz-radio-autoregressive">
  <label for="autoregressive-wrong1" class="quiz-option-autoregressive" data-correct="false">❌ FALSE</label>

  <div class="feedback-autoregressive" data-feedback="correct">✅ 정답입니다! 이것을 자기회귀적(autoregressive) 생성이라고 부릅니다. 새로운 단어가 생성될 때마다 컨텍스트에 추가되고, 모델은 전체 컨텍스트를 사용해 다음 단어를 예측합니다. 이는 또한 최대 컨텍스트 길이에 원래의 프롬프트와 생성된 출력이 모두 포함된다는 뜻이기도 합니다.</div>
  <div class="feedback-autoregressive" data-feedback="wrong1">❌ 사실 이것은 TRUE입니다! 모델은 한 번에 한 단어씩 생성하며, 다음 단어를 예측하기 전에 각 단어를 컨텍스트에 추가합니다. 이를 자기회귀적(autoregressive) 생성이라고 부릅니다.</div>
</div>
</div>

> **중요한 특징:** 출력된 단어들이 입력의 일부가 되기 때문에, **최대 컨텍스트 길이에는 원래의 프롬프트와 생성된 출력이 모두 포함**됩니다. 긴 프롬프트로 작업할 때는 이 점을 꼭 기억하세요!


## 👻 환각은 어디에 숨어 있을까 :id=where-hallucinations-hide

이제부터 재미있어집니다. 앞서 본 "Never gonna" 예시로 다시 돌아가되, 이번에는 살짝 다른 반전이 있습니다.

컨텍스트가 조금 바뀌면 어떻게 될까요? Rick Astley의 노래가 아니라, 모델의 학습 데이터에 "Never gonna"로 시작하는 다른 노래들도 포함되어 있었다고 상상해 보세요.

> **Never gonna...**
>
> - give you up
> - leave this bed
> - not dance again
> - fall in love again
> - be alone
> - change

충분한 컨텍스트가 없으면, 모델은 **"give you up"** 대신 (다른 노래에서 나온) **"leave this bed"**를 고를 수도 있습니다. 답변은 여전히 *그럴듯해* 보입니다 — 문법적으로 문장을 완성하기는 합니다 — 하지만 **틀린** 노래입니다!

![Never gonna leave this bed — 환각의 사례!](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWZmMzltdXhyeWluNTA4cXVjazFzczdybWRjZGl6YXl1d2d5YWVieSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6nUSg8ARAv5S9rqg/giphy.gif)

**환각은 정확히 이런 방식으로 일어납니다.** 모델은 올바른 컨텍스트가 부족해서, 그럴듯하지만 틀린 다음 내용을 선택합니다.

### 환각에 어떻게 대응할 수 있을까? 답은... 더 많은 컨텍스트입니다!

노래의 첫 부분을 컨텍스트로 제공한다면:

> *"We're no strangers to love..."*
> *...*
> **Never gonna...**

이제 모델은 훨씬 더 많은 컨텍스트를 가지고 작업할 수 있으며, 주변 단어들이 명확히 Rick Astley의 노래를 가리키고 있으므로 올바르게 **"give you up"**을 선택할 것입니다.

> **핵심 통찰:** 관련된 컨텍스트를 더 많이 제공할수록, 모델이 환각을 일으킬 가능성은 줄어듭니다. 이것이 바로 RAG(Retrieval-Augmented Generation)와 같은 기법이 그토록 강력한 이유입니다 — 이런 기법들은 올바른 컨텍스트를 프롬프트에 주입합니다.

---

## ✅ 우리가 배운 것 :id=what-we-have-learned

4가지 진실 — 누가 기억하고 있나요?

| 진실 | 우리가 확인한 것 |
|-------|-------------|
| 말을 걸어야만 답한다 | 무언가를 보내지 않으면 모델은 아무것도 하지 않았다 |
| 비결정적이다 | 매번 다르게 응답한다 |
| 진실을 말하는 게 아니라 가능성이 높은 것을 말한다 | 자신 있게 우리에게 그냥 거짓말을 할 수도 있다 |
| 기억력이 없다 | 결국 우리의 이름을 배우지 못했다 :'( |

**추가로** 이제 우리는 다음을 이해하게 되었습니다.

| 개념 | 핵심 요점 |
|---------|-------------|
| **모델** | 파라미터로 이루어진 바이너리 파일 — 입력을 출력으로 매핑하는 블랙박스 |
| **런타임** | 모델을 실행하고 프롬프트를 받을 수 있도록 서빙함 |
| **파라미터** | 많을수록 더 똑똑하지만 더 느려지고, 더 많은 하드웨어가 필요함 |
| **GPU** | GenAI 모델을 CPU보다 훨씬 빠르게 실행함 |
| **학습 vs 파인튜닝** | 처음부터 학습하는 것은 어렵지만, 파인튜닝은 실현 가능함 |
| **텍스트 생성** | 다음 단어 예측, 한 번에 한 단어씩(자기회귀적) |
| **환각** | 모델에 컨텍스트가 부족할 때 발생함; 더 많은 컨텍스트로 대응 |
| **컨텍스트 길이** | 프롬프트와 생성된 출력을 모두 포함함 |
</content>
