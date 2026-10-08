# LLM 기본 개념 :id=llm-fundamentals

## 📚 목차 :id=contents
- [LLM 기본 개념](#llm-fundamentals)
  - [📚 목차](#contents)
  - [🔍 토큰이란 무엇인가?](#what-is-a-token)
  - [🔄 다음 토큰 예측](#next-token-prediction)
  - [🧠 컨텍스트 길이와 윈도우](#context-length-and-window)
  - [🔮 LLM은 고정되어 있을까, 변할까?](#are-llms-fixed-or-do-they-change)

## 🔍 토큰이란 무엇인가? :id=what-is-a-token

AI 모델이 텍스트를 이해하거나 생성하기 전에, 먼저 모든 것을 **토큰(token)**이라고 불리는 작은 조각으로 쪼갭니다.

토큰은 완전한 단어와 똑같지는 않습니다. 다음과 같을 수 있습니다.
- 짧은 단어 전체: `"The"` → 1개의 토큰
- 긴 단어의 일부: `"unbelievable"` → 3개의 토큰 (`"un"`, `"believ"`, `"able"`)
- 구두점: `","` 또는 `"."`는 각각 1개의 토큰일 수 있음

이것이 모델이 보는 기본 단위입니다. 모델은 인간처럼 텍스트를 이해하지 않습니다. 단지 토큰의 흐름을 보고, 그것이 나타나는 패턴을 학습할 뿐입니다.

"왜 그냥 단어나 글자를 그대로 입력하지 않나요?"라고 물을 수도 있습니다.
토큰을 사용하는 데는 두 가지 주요 이유가 있습니다.
- 무엇을 사용하든 결국 숫자로 변환해야 합니다. 컴퓨터는 궁극적으로 숫자만 이해하기 때문입니다 🔢. 그리고 모든 단어에 각각 숫자를 부여하기에는 단어의 수가 너무 많습니다.
- 토큰은 가능한 한 크면서도 재사용 가능하도록 설계되어, LLM에 보내는 입력의 **개수**를 최소화합니다. 예를 들어 `unbelievable`이라는 단어를 글자 단위로 보내면 12개의 입력이 되지만, 토큰 단위로는 3개의 토큰에 불과합니다. 입력의 개수가 왜 중요한지는... 지금부터 설명하겠습니다 👇

LLM을 다루기 시작하면 사람들이 토큰 수를 세는 모습을 자주 보게 될 것입니다. 이는 단순히 재미로 하는 것이 아니라, 토큰의 수가 바로 LLM에 들어가는 입력의 크기를 나타내기 때문입니다.
LLM은 한 번의 요청에서 입력하고 출력할 수 있는 토큰 수에 제한이 있습니다(한 번에 볼 수 있는 컨텍스트/정보의 양이라고 생각하면 됩니다).
그뿐만 아니라 입력이 많아질수록 모든 입력과 출력을 추적하기 위해 더 많은 메모리(특히 GPU 메모리)가 필요합니다(출력이 다음 단계에서 입력으로 바뀐다는 점을 기억하세요).

![input-output.png](images/input-output.png)

여기에서 문장이 어떻게 토큰으로 변환되는지 직접 체험해볼 수 있습니다.
<iframe
	src="https://agents-course-the-tokenizer-playground.static.hf.space"
	frameborder="0"
	width="500"
	height="750"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
></iframe>

*이 앱은 [HuggingFace Learning Course](https://agents-course-the-tokenizer-playground.static.hf.space)에서 제공합니다*

간단한 퀴즈로 이해도를 확인해 봅시다!

<!-- 🔍 Token‐capacity calculation (typed answer) -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">
  <h3 style="margin:0 0 8px;color:#5a5a5a;">🔤 퀴즈</h3>
  <p style="color:#495057; font-weight:500;">
    당신은 수천 줄에 달하는 대형 코드베이스 작업을 하고 있는데, 한 줄 한 줄 읽고 싶지는 않습니다. <br>
    그래서 대신 가장 좋아하는 LLM에게 도움을 받기로 합니다 🤖<br>
    먼저 다음과 같은 지시문을 작성합니다.

    “이 코드가 무엇을 하는지 단계별로, 쉬운 말로 설명해줘...”
  <p style="color:#495057; font-weight:500;">
    이 지시문은 전체 96개의 토큰을 차지합니다.<br>
    그런 다음 코드를 한 줄씩 입력하기 시작하는데, 한 줄당 약 12개의 토큰을 차지합니다.<br>
    그리고 이 모델은 한 번에 최대 4096개의 토큰까지만 처리할 수 있다는 것을 알고 있습니다.<br>
  </p>
  <p style="color:#495057; font-weight:500;">
    👉 <strong>한 번에 LLM에 보낼 수 있는 <em>완전한</em> 코드 줄 수는 몇 줄일까요?</strong>
  </p>

  <style>
    /* hide the native number-input arrows */
    #cap-input::-webkit-inner-spin-button,
    #cap-input::-webkit-outer-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
    #cap-input {
      -moz-appearance: textfield;
    }
    /* your existing valid/invalid styling… */
    #cap-input { margin:6px 0 4px; padding:6px 10px; border:2px solid #e9ecef; border-radius:6px; width:120px; font-size:1em; }
    #cap-input:focus { outline:none; border-color:#6ea8fe; }
    #cap-input:valid { background:#d4edda; border-color:#28a745; color:#155724; }
    #cap-input:invalid:not(:placeholder-shown) { background:#f8d7da; border-color:#dc3545; color:#721c24; }
    .feedback-cap { display:none; margin:4px 0; padding:8px 16px; border-radius:6px; }
    #cap-input:valid + .feedback-cap[data-feedback="correct"],
    #cap-input:invalid:not(:placeholder-shown) + .feedback-cap[data-feedback="wrong"] {
      display:block;
    }
    .feedback-cap[data-feedback="correct"] { background:#d1f2eb; color:#0c5d56; border:1px solid #a3d9cc; }
    .feedback-cap[data-feedback="wrong"]   { background:#fce8e6; color:#58151c; border:1px solid #f5b7b1; }
  </style>

  <input
    id="cap-input"
    type="number"
    placeholder="---"
    min="333"
    max="333"
    step="1"
    required>

  <div class="feedback-cap" data-feedback="correct">✅ 정답입니다! 333줄입니다.</div>
  <div class="feedback-cap" data-feedback="wrong">❌ 아쉽지만 정답이 아닙니다.</div>
</div>

<script>
  // prevent Up/Down arrows from jumping to 333 when empty
  document.getElementById('cap-input')
    .addEventListener('keydown', function(e) {
      if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && this.value === '') {
        e.preventDefault();
      }
    });
</script>

## 🔄 다음 토큰 예측 :id=next-token-prediction

대형 언어 모델(LLM)이 근본적으로 하는 일은 놀랍도록 단순합니다.
바로 **다음 토큰**을 추측하는 것입니다.

텍스트 문자열을 주면, 모델은 가장 가능성이 높은 다음 조각을 예측하여 그 텍스트를 이어갑니다. 그리고 이 작업을 또 하고, 또 하고, 계속 반복합니다.

이것은 매우 빠른 자동완성과 비슷하지만, 책, 웹사이트, 대화 등 방대한 텍스트 모음으로 학습된 것입니다.

예를 들어:
> 입력: “Photosynthesis is the process by which plants”  
> 모델의 예측: `“ convert sunlight into energy”`

이렇게 한 단계씩 추측해 나가는 과정을 **추론(inference)**이라고 부릅니다.

모델은 *보통* 다음에 무엇이 오는지를 예측하려고 하기 때문에, 프롬프트 속의 단서와 패턴에 민감합니다. 그래서 작은 변화가 아주 다른 결과로 이어지기도 합니다.

특정 맥락에서 모델이 얼마나 잘 추측하는지 살펴봅시다.


<!-- 🔄 Next token – tricky semantic cue -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 퀴즈 1</h3>
<p style="color:#495057; font-weight:500;">
LLM에 보낸 프롬프트가 정확히 다음과 같다고 상상해 보세요.
</p>

<p style="color:#495057; font-weight:500;">
"It rains like cats and..."
</p>

<p style="color:#495057; font-weight:500;">모델이 다음으로 생성할 가능성이 가장 높은 <em>단일 토큰</em>은 무엇일까요?</p>

<style>
.quiz-container-next-easy{position:relative}
.quiz-option-next-easy{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-next-easy:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-next-easy{display:none}
.quiz-radio-next-easy:checked+.quiz-option-next-easy[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-next-easy:checked+.quiz-option-next-easy:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-next-easy{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#next-easy-correct:checked~.feedback-next-easy[data-feedback="correct"],
#next-easy-wrong1:checked~.feedback-next-easy[data-feedback="wrong1"],
#next-easy-wrong2:checked~.feedback-next-easy[data-feedback="wrong2"]{display:block}
.feedback-next-easy[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-next-easy[data-feedback="wrong1"], .feedback-next-easy[data-feedback="wrong2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-next-easy">
  <input type="radio" name="quiz-next-easy" id="next-easy-wrong1" class="quiz-radio-next-easy">
  <label for="next-easy-wrong1" class="quiz-option-next-easy" data-correct="false">🐸 frogs</label>

  <input type="radio" name="quiz-next-easy" id="next-easy-correct" class="quiz-radio-next-easy">
  <label for="next-easy-correct" class="quiz-option-next-easy" data-correct="true">🐶 dogs</label>

  <input type="radio" name="quiz-next-easy" id="next-easy-wrong2" class="quiz-radio-next-easy">
  <label for="next-easy-wrong2" class="quiz-option-next-easy" data-correct="false">🐭 mice</label>

  <div class="feedback-next-easy" data-feedback="correct">✅ 정답입니다!</div>
  <div class="feedback-next-easy" data-feedback="wrong1">❌ "Frogs"는 조금 어색합니다. 다만 기술적으로는 다른 선택지보다 개구리가 비처럼 내릴 가능성이 더 높긴 하겠지만요...</div>
  <div class="feedback-next-easy" data-feedback="wrong2">❌ "비처럼 고양이와 쥐가 쏟아진다"라니, 아마 톰과 제리에 그런 에피소드가 있을 법도 하지만, 우리가 찾는 관용구는 아닙니다.</div>
</div>
</div>



LLM은 다음에 올 가능성이 가장 높은 토큰을 예측하고, 각 토큰에 확률을 부여합니다.
확률이 높을수록 선택될 가능성도 높아집니다.

<details>
<summary> 🕵️ 스포일러! 퀴즈를 마친 후 눌러보세요.</summary>  
<br>

![images/cats-and-dogs.png](images/cats-and-dogs.png)

<br>

</details>

위 퀴즈처럼 어떤 경우에는 모델이 무엇을 예측할지 꽤 분명합니다.
하지만 다른 경우에는 아래 예시처럼 그렇게 명확하지 않을 수 있습니다.



<!-- 🔄 Next token – tricky semantic cue -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 퀴즈 2</h3>
<p style="color:#495057; font-weight:500;">
LLM에 보낸 프롬프트가 정확히 다음과 같다고 상상해 보세요.
</p>

<p style="color:#495057; font-weight:500;">
"John carefully packed his bag with essentials for the desert hike: water, sunscreen, and a wide-brimmed hat. He double-checked everything twice. When he arrived, the blazing sun made him immediately grateful he'd remembered his..."
</p>

<p style="color:#495057; font-weight:500;">모델이 다음으로 생성할 가능성이 가장 높은 <em>단일 토큰</em>은 무엇일까요?</p>

<style>
.quiz-container-next-tricky{position:relative}
.quiz-option-next-tricky{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-next-tricky:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-next-tricky{display:none}
.quiz-radio-next-tricky:checked+.quiz-option-next-tricky[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-next-tricky:checked+.quiz-option-next-tricky:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-next-tricky{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#next-tricky-correct:checked~.feedback-next-tricky[data-feedback="correct"],
#next-tricky-wrong1:checked~.feedback-next-tricky[data-feedback="wrong1"],
#next-tricky-wrong2:checked~.feedback-next-tricky[data-feedback="wrong2"],
#next-tricky-wrong3:checked~.feedback-next-tricky[data-feedback="wrong3"]{display:block}
.feedback-next-tricky[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-next-tricky[data-feedback="wrong1"], .feedback-next-tricky[data-feedback="wrong2"], .feedback-next-tricky[data-feedback="wrong3"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-next-tricky">
  <input type="radio" name="quiz-next-tricky" id="next-tricky-wrong1" class="quiz-radio-next-tricky">
  <label for="next-tricky-wrong1" class="quiz-option-next-tricky" data-correct="false">🥤 water</label>

  <input type="radio" name="quiz-next-tricky" id="next-tricky-correct" class="quiz-radio-next-tricky">
  <label for="next-tricky-correct" class="quiz-option-next-tricky" data-correct="true">🎩 hat</label>

  <input type="radio" name="quiz-next-tricky" id="next-tricky-wrong2" class="quiz-radio-next-tricky">
  <label for="next-tricky-wrong2" class="quiz-option-next-tricky" data-correct="false">🧴 sunscreen</label>

  <input type="radio" name="quiz-next-tricky" id="next-tricky-wrong3" class="quiz-radio-next-tricky">
  <label for="next-tricky-wrong3" class="quiz-option-next-tricky" data-correct="false">🕶️ sunglasses</label>

  <div class="feedback-next-tricky" data-feedback="correct">✅ 정답입니다! 맥락상 "blazing sun"(타는 듯한 햇살)이 강하게 암시되므로, "hat"이 가장 논리적인 다음 단어입니다.</div>
  <div class="feedback-next-tricky" data-feedback="wrong1">❌ 물은 사막 하이킹에 필수적이지만, "blazing sun"이라는 표현은 특히 자외선 차단이 필요함을 강조합니다.</div>
  <div class="feedback-next-tricky" data-feedback="wrong2">❌ 선크림은 자외선으로부터 피부를 보호하지만, 맥락에서 "blazing sun"이라는 표현은 즉각적인 물리적 보호를 암시합니다.</div>
  <div class="feedback-next-tricky" data-feedback="wrong3">❌ 선글라스는 짐 목록에 언급되지 않았으므로, 모델은 이미 맥락에서 등장한 물건으로 문장을 완성할 가능성이 더 높습니다.</div>
</div>
</div>

<details>
<summary> 🕵️ 스포일러! 퀴즈를 마친 후 눌러보세요.</summary>  
<br>

![images/bring-to-beach.png](images/bring-to-beach.png)


</details>

## 🧠 컨텍스트 길이와 윈도우 :id=context-length-and-window

  LLM은 입력의 길이에 제한이 없을 수 없습니다. 메시지를 보내면 모델은 다음을 위한 공간이 필요합니다.

  - 프롬프트를 읽는 것
  - 그것을 바탕으로 추론하는 것
  - 응답을 생성하는 것

  이 모든 과정은 **컨텍스트 윈도우(context window)**(때로는 **최대 모델 길이(max model length)** 등 비슷한 용어로도 불림)라는 고정된 공간 안에서 일어납니다.

  화이트보드를 떠올려 보세요. 질문이든, 기대하는 답변이든 너무 많은 내용을 쓰면 보드의 공간이 부족해집니다. 모델은 포기하거나 내용을 중간에 잘라버릴 수 있습니다.

  일반적인 컨텍스트 윈도우 크기:

  - 소형 모델: 2,000~4,000 토큰
  - 대형 모델: 8,000~128,000 토큰
  - 일부 최신 모델: 그보다 훨씬 더 많음!

  그래서 매우 긴 프롬프트를 보내거나 매우 긴 답변을 요청하면 모델의 한계에 부딫힐 수 있습니다.

  또한 직접 제어할 수 있는 `max_tokens`(또는 *max completion tokens*)라는 값도 있습니다. 이는 모델에게 "답변에서 이 토큰 수까지만 줘"라고 알려주는 역할을 합니다.

  모델에게 글쓰기 분량 제한을 주는 것과 비슷합니다. 한번 시도해 봅시다.

  모델에게 `I need a Spanish tortilla recipe.`라고 물어보고, 맛있는 레시피가 나올 때까지 `max_token` 값을 조정해 보세요 🇪🇸

  _참고: 실습을 더 잘 보기 위해 필요하다면 상단의 ㈢ 버튼을 클릭해 왼쪽 메뉴를 닫을 수 있습니다_

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/context?embed"
	frameborder="0"
	width="400"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>


  만족스러운 숫자는 얼마였나요?

  하지만 기억하세요 — 모델의 전체 용량 자체는 변하지 않습니다. 컨텍스트 윈도우는 고정되어 있으며, 다음 두 가지를 모두 포함합니다.

  - 입력(당신의 프롬프트)
  - 출력(모델의 응답, 최대 max_tokens까지)

  따라서 `max_tokens`를 너무 높게 설정했는데 입력이 이미 길다면, 모델에게 충분한 공간이 남지 않아 오류가 발생할 수 있습니다.

  그러니 조금 더 세심하게, 더 많은 세부 사항을 담아 모델에게 물어보고 싶을 수도 있습니다. 다음 내용을 보내고 어떤 일이 일어나는지 확인해 보세요.

  ```
  I'm interested in learning how to make an authentic Spanish tortilla de patatas, also known as a Spanish omelette. 
  Could you please provide a step-by-step recipe, including ingredients, preparation tips, and cooking techniques that reflect the traditional way it's made in Spain?
  ```

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/max-length?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

 이런. 아마 오류 메시지를 받았을 것입니다. 왜 그럴까요?

  모델은 한정된 메모리 공간, 즉 요청당 처리할 수 있는 고정된 토큰 수를 가지고 있습니다. 그 공간에는 다음 두 가지가 모두 들어가야 합니다.

  - 당신의 프롬프트(질문이나 지시문), 그리고

  - 모델이 생성할 답변

  이 경우, 더 길어진 질문이 이미 그 공간의 많은 부분을 차지했습니다. 게다가 모델은 길고 상세한 레시피를 생성하라는 요청까지 받았으니, 둘 다 수행할 공간이 충분하지 않았습니다. 그래서 모델은 포기하고 오류를 반환한 것입니다.

  다시 말해, 이 공간 제한을 최대 컨텍스트 길이(maximum context length)라고 부릅니다. 이는 모델이 시작될 때 설정되는 값으로, 모델이 한 번에 처리할 수 있는 입력과 출력의 총량에 영향을 줍니다.

  이 값을 너무 높게 설정하면 메모리가 낭비될 수 있고, 너무 낮게 설정하면 출력이 잘리거나 긴 프롬프트를 처리하지 못할 수 있습니다.


<!-- 🧠 Context window – chunking strategy -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🧠 퀴즈</h3>

<p style="color:#495057;font-weight:500;">
누군가 당신에게 90페이지 분량의 계약서를 바탕으로 Q&amp;A를 만들어달라는 업무를 맡겼습니다.<br>
당연히 당신은 LLM을 사용해 이를 Q&amp;A 형태로 요약하기로 했습니다(요즘 누가 다 읽겠어요?).
그런데 그 90페이지는 약 45,000 토큰에 달하는 반면, 당신의 모델은 8,000 토큰의 컨텍스트 윈도우만 가지고 있습니다.
</p>

<p style="color:#495057;font-weight:500;">
<em>가장 현실적인</em> 접근 방식은 무엇일까요?</p>

<style>
.ctxOpt{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;
       border:2px solid #e9ecef;color:#495057;transition:.2s}
.ctxOpt:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.ctxRadio{display:none}
.ctxRadio:checked + .ctxOpt[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.ctxRadio:checked + .ctxOpt[data-correct="false"]{background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.ctxFeed{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#ctx-good:checked ~ .ctxFeed[data-type="good"],
#ctx-w1:checked  ~ .ctxFeed[data-type="bad1"],
#ctx-w2:checked  ~ .ctxFeed[data-type="bad2"]{display:block}
.ctxFeed[data-type="good"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.ctxFeed[data-type="bad1"], .ctxFeed[data-type="bad2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div>
  <input type="radio" id="ctx-w1" name="ctx" class="ctxRadio">
  <label for="ctx-w1" class="ctxOpt" data-correct="false">
    📚 계약서 전체를 통째로 집어넣어 밤새 새 모델을 파인튜닝한다.
  </label>

  <input type="radio" id="ctx-good" name="ctx" class="ctxRadio">
  <label for="ctx-good" class="ctxOpt" data-correct="true">
    🔍 계약서를 약 1000 토큰 단위의 청크(chunk)로 나누고,  
    각 질문과 관련된 청크만 삽입한다.
  </label>

  <input type="radio" id="ctx-w2" name="ctx" class="ctxRadio">
  <label for="ctx-w2" class="ctxOpt" data-correct="false">
    ⛓️ 하나의 요청 안에서 6K 토큰짜리 프롬프트 여러 개를 연결한다. 백엔드가 자동으로 이어붙여줄 것이다.
  </label>

  <div class="ctxFeed" data-type="good">
    ✅ 맞습니다 — 1K 청크 여러 개를 필요에 따라 불러오는 방식은 8K 한도를 지키면서, 청크 외부에도 추가 컨텍스트를 넣을 여유를 남깁니다.
  </div>
  <div class="ctxFeed" data-type="bad1">
    ❌ 파인튜닝에는 학습 데이터, 상당한 컴퓨팅 자원, 그리고 시간이 필요합니다.
  </div>
  <div class="ctxFeed" data-type="bad2">
    ❌ 6K 프롬프트를 여러 개 연결하면 프롬프트마다 컨텍스트가 초기화되어, Q&A에 필요한 일관된 이해를 잃게 됩니다.
  </div>
</div>
</div>




## 🔮 LLM은 고정되어 있을까, 변할까? :id=are-llms-fixed-or-do-they-change

대형 언어 모델은 한 번 학습되고 나면 **고정(frozen)**됩니다 — 당신과 대화한다고 해서 새로운 것을 배우지는 않습니다. 메시지를 보낼 때마다(이것을 **프롬프트(prompt)**라고 부름), 모델은 이미 알고 있는 것을 바탕으로 다음 요소들만 사용해 응답합니다.
- 원래의 학습 데이터
- 현재 프롬프트의 내용
- 생성 과정에서의 무작위성

오늘 모델에게 새로운 것을 알려주더라도, 프롬프트에서 계속 그것을 언급하지 않는 한 모델은 내일 그것을 "기억"하지 못합니다.

그렇다면 시스템은 대화와 대화 사이에 어떻게 사실을 "기억"할까요?

다음 퀴즈를 통해 알아낼 수 있는지 확인해 봅시다.

<!-- 🔮 Frozen-model memory dilemma (harder) -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🧠 퀴즈</h3>
<p style="color:#495057; font-weight:500;">
당신은 회사의 HR 팀을 위한 유용한 AI 어시스턴트를 만들고 있습니다.<br>
오늘 대화 중에 팀원들이 새로 입사한 직원들의 이름, 예를 들어 Emily Zhang, Jasper Müller, Amina Idris 등을 입력합니다.<br>
어시스턴트는 그 대화 안에서는 문제없이 잘 따라갑니다.<br>
하지만 내일, 완전히 새로운 세션으로 대화가 다시 시작되어도 어시스턴트는 이 모든 이름을 여전히 기억해야 합니다.
<p style="color:#495057; font-weight:500;">이를 달성하기 위한 <em>가장 현실적인</em> 방법은 무엇일까요.</p>

<style>
.quiz-container-sku{position:relative}
.quiz-option-sku{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-sku:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-sku{display:none}
.quiz-radio-sku:checked+.quiz-option-sku[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-sku:checked+.quiz-option-sku:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-sku{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#sku-correct:checked~.feedback-sku[data-feedback="correct"],
#sku-wrong1:checked~.feedback-sku[data-feedback="wrong1"],
#sku-wrong2:checked~.feedback-sku[data-feedback="wrong2"],
#sku-wrong3:checked~.feedback-sku[data-feedback="wrong3"]{display:block}
.feedback-sku[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-sku[data-feedback="wrong1"], .feedback-sku[data-feedback="wrong2"], .feedback-sku[data-feedback="wrong3"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-sku">
  <input type="radio" name="quiz-sku" id="sku-wrong1" class="quiz-radio-sku">
  <label for="sku-wrong1" class="quiz-option-sku" data-correct="false">🔖 오늘 프롬프트의 맨 끝에 "이것들을 영원히 기억해"라고 덧붙인다</label>

  <input type="radio" name="quiz-sku" id="sku-wrong2" class="quiz-radio-sku">
  <label for="sku-wrong2" class="quiz-option-sku" data-correct="false">🧹 모델의 컨텍스트 윈도우를 늘려서 <em>오늘</em>의 대화가 내일의 프롬프트에 그대로 들어가게 한다</label>

  <input type="radio" name="quiz-sku" id="sku-wrong3" class="quiz-radio-sku">
  <label for="sku-wrong3" class="quiz-option-sku" data-correct="false">🔧 밤사이에 새 직원 정보로 모델을 재학습시킨다</label>

  <input type="radio" name="quiz-sku" id="sku-correct" class="quiz-radio-sku">
  <label for="sku-correct" class="quiz-option-sku" data-correct="true">📦 이름들을 데이터베이스에 저장하고 내일 프롬프트에 자동으로 삽입한다</label>

  <div class="feedback-sku" data-feedback="correct">✅ 정답입니다! 고정된 가중치는 밤사이에 새로운 것을 배울 수 없으므로, 어제의 직원 이름을 다시 입력해 주어야 합니다(데이터베이스에서 가져오는 것이 가장 빠르고 저렴합니다).</div>
  <div class="feedback-sku" data-feedback="wrong1">❌ "이것들을 영원히 기억해"와 같은 단순한 지시문은 모델의 가중치를 바꾸지 않습니다. 모델은 여전히 현재 프롬프트에 있는 내용만 알 수 있습니다.</div>
  <div class="feedback-sku" data-feedback="wrong2">❌ 컨텍스트 윈도우를 늘리는 것은 비용이 많이 들고 확장성이 좋지 않습니다. 모든 대화마다 거대한 컨텍스트가 필요해져서, 오래된 대화 기록에 자원을 낭비하게 됩니다.</div>
  <div class="feedback-sku" data-feedback="wrong3">❌ 재학습은 느리고 비용이 많이 들며, 신입 직원 이름처럼 자주 바뀌는 데이터에는 과도한 방법입니다.</div>
</div>
</div>

</content>
