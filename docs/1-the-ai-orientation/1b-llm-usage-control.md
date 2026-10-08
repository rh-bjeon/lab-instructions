# 💭 LLM 사용 및 제어 :id=using-and-controlling-llms

## 📚 목차 :id=contents
- [💭 LLM 사용 및 제어](#using-and-controlling-llms)
  - [📚 목차](#contents)
  - [💭 프롬프팅 기법](#prompting-techniques)
  - [🚨 환각(Hallucination) 이해하기](#understanding-hallucinations)
    - [환각을 줄이는 방법](#how-can-we-reduce-hallucinations)
  - [🛡️ 가드레일 구현하기](#implementing-guardrails)
    - [🔍 실습 - LLM에는 내장된 메모리가 있을까?](#hands-on-exercises-do-llms-have-built-in-memory)
    - [🔍 실습 - LLM은 결정론적일까?](#hands-on-exercises-are-llms-deterministic)

## 💭 프롬프팅 기법 :id=prompting-techniques

모델에게 무엇을 *묻는지*는 모델이 어떻게 답하는지에 큰 영향을 미칩니다. 이것을 **프롬프팅**(prompting)이라고 부르며, 이는 모델의 동작을 유도하는 방법입니다.

대부분의 모델에서 프롬프트에는 두 가지 핵심 구성 요소가 있습니다.
- **시스템 프롬프트(System Prompt)**: 어시스턴트의 어조나 역할을 설정합니다. 예: `You are a strict grader.`
- **사용자 프롬프트(User Prompt)**: 모델을 사용하는 사람이 실제로 하는 질문이나 메시지입니다.

표현의 작은 변화만으로도 매우 다른 응답으로 이어질 수 있습니다.

좋은 프롬프팅은 필수적입니다 — 모델로부터 더 명확하고, 더 유용하고, 더 정확한 답변을 얻는 데 도움이 됩니다.

📚 더 고급 프롬프트 전략은 나중에 살펴보겠습니다. 지금은 프롬프팅이 실제로 어떻게 작동하는지 재미있는 퀴즈로 확인해 봅시다.

<!-- 💭 Prompting – what will happen? -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 퀴즈</h3>

<p style="color:#495057;font-weight:500;">
<strong>모델에 보낸 프롬프트:</strong></p>

<pre style="background:#f8f9fa;border:1px solid #ccc;border-radius:6px;padding:10px;font-size:.9em;color:#495057;font-weight:500;">
{"role":"system",
 "content":"You are a strict grader. Respond with only the single word PASS or FAIL."}

{"role":"user",
 "content":"Explain IN DETAIL how you would grade this homework."}
</pre>

<p style="color:#495057;font-weight:500;">
모델에는 temperature 관련 특별 설정이 없고 기본 샘플링을 사용합니다.<br>
<strong>모델이 생성할 가능성이 가장 높은 출력은 무엇일까요?</strong></p>

<style>
.quiz-container-prompt-out{position:relative}
.quiz-option-prompt-out{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;
  cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-prompt-out:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-prompt-out{display:none}
.quiz-radio-prompt-out:checked+.quiz-option-prompt-out[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-prompt-out:checked+.quiz-option-prompt-out:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-prompt-out{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#prompt-out-correct:checked~.feedback-prompt-out[data-feedback="correct"],
#prompt-out-wrong1:checked~.feedback-prompt-out[data-feedback="wrong1"],
#prompt-out-wrong2:checked~.feedback-prompt-out[data-feedback="wrong2"]{display:block}
.feedback-prompt-out[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-prompt-out[data-feedback="wrong1"], .feedback-prompt-out[data-feedback="wrong2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-prompt-out">
  <input type="radio" name="quiz-prompt-out" id="prompt-out-wrong1" class="quiz-radio-prompt-out">
  <label for="prompt-out-wrong1" class="quiz-option-prompt-out" data-correct="false">
    📝 여러 단락에 걸친 설명
  </label>

  <input type="radio" name="quiz-prompt-out" id="prompt-out-correct" class="quiz-radio-prompt-out">
  <label for="prompt-out-correct" class="quiz-option-prompt-out" data-correct="true">
    ✔️ 단 한 단어: <code>PASS</code> <em>또는</em> <code>FAIL</code>
  </label>

  <input type="radio" name="quiz-prompt-out" id="prompt-out-wrong2" class="quiz-radio-prompt-out">
  <label for="prompt-out-wrong2" class="quiz-option-prompt-out" data-correct="false">
    🚫 거부 메시지
  </label>

  <div class="feedback-prompt-out" data-feedback="correct">
    ✅ <strong>정확합니다.</strong> 시스템 지시문이 사용자 요청보다 우선하므로, 모델은 한 단어 형식을 그대로 지킵니다.
  </div>
  <div class="feedback-prompt-out" data-feedback="wrong1">
    ❌ 시스템 프롬프트는 출력을 한 단어로만 제한합니다. 여러 단락에 걸친 설명은 "한 단어" 제약을 어기는 것입니다.
  </div>
  <div class="feedback-prompt-out" data-feedback="wrong2">
    ❌ 모델은 거부하지 않을 것입니다 — 채점에는 유해한 요소가 전혀 없습니다. 시스템 지시문은 단지 출력 형식을 한 단어로 정의할 뿐입니다.
  </div>
</div>
</div>



---

## 🚨 환각(Hallucination) 이해하기 :id=understanding-hallucinations

때때로 언어 모델은 **사실을 지어냅니다** — 자신 있게 말하지만 실제로는 거짓이거나 심지어 완전히 허구인 답변을 내놓습니다. 이것을 **환각**(hallucination)이라고 부릅니다.

왜 이런 일이 일어날까요?
- 모델은 사실을 확인하지 않습니다 — 단지 다음에 올 가능성이 가장 높은 토큰을 추측할 뿐입니다.
- 모델은 무엇이 실제인지 모릅니다. 학습 데이터에서 *흔히 등장했던* 것만 알고 있을 뿐입니다.

👻 실제 출처를 요청해도, 모델은 그럴듯해 보이지만 실제로는 존재하지 않는 문서를 만들어낼 수 있습니다.

### 환각을 줄이는 방법 :id=how-can-we-reduce-hallucinations
- 프롬프트 안에 실제의, 정확한 사실을 제공하세요.
- 사용자에게 도달하기 전에 잘못된 주장을 걸러내는 가드레일을 추가하세요. (아래 참고)
- 신뢰할 수 있는 데이터베이스나 웹사이트에서 정보를 가져오는 "검색(retrieval)" 기능을 추가하는 도구를 사용하세요.

간단한 퀴즈로 이 내용을 살펴봅시다.

<!-- 🚨 Hallucination – realistic prevention options -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">
  <h3 style="margin:0 0 8px;color:#5a5a5a;">🚨 퀴즈</h3>
  <p style="color:#495057;font-weight:500;">
    <strong>상황:</strong> 한 교사가 "화성에서 가장 높은 산에 대한 NASA 출처를 알려줘"라고 물었습니다.<br>
    모델은 존재하지 않는 2023년 NASA 백서를 인용해 답했습니다.
  </p>

  <p style="color:#495057;font-weight:500;">
    당신은 이런 종류의 환각을 막아야 하는 엔지니어입니다. 아래 중 어떤 해결책이 가장 효과적일까요?
  </p>

  <style>
  .hall-fix-row{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;
                border:2px solid #e9ecef;color:#495057;cursor:pointer;transition:.2s}
  .hall-fix-row:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
  .hall-fix-radio{display:none}
  .hall-fix-radio:checked + .hall-fix-row[data-good="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
  .hall-fix-radio:checked + .hall-fix-row[data-good="false"]{background:#f8d7da;color:#721c24;border-color:#f5b7b1}
  .hall-fix-feedback{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
  #hall-fix-correct:checked ~ .hall-fix-feedback[data-type="good"],
  #hall-fix-w1:checked     ~ .hall-fix-feedback[data-type="bad1"],
  #hall-fix-w2:checked     ~ .hall-fix-feedback[data-type="bad2"]{display:block}
  .hall-fix-feedback[data-type="good"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
  .hall-fix-feedback[data-type="bad1"], .hall-fix-feedback[data-type="bad2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
  </style>

  <div class="quiz-container-prompt-out">
  <input type="radio" id="hall-fix-w1" name="hall-fix" class="hall-fix-radio">
  <label for="hall-fix-w1" class="hall-fix-row" data-good="false">
    🚧 밤사이에 모델을 파인튜닝한다.
  </label>

  <input type="radio" id="hall-fix-correct" name="hall-fix" class="hall-fix-radio">
  <label for="hall-fix-correct" class="hall-fix-row" data-good="true">
    📝 프롬프트를 다시 작성해서 <b>정확한 정보와 실제 URL</b>을 포함시킨다.<br>
    예: "NASA에 따르면 <em>Olympus Mons</em>가 가장 높다. 그 출처를 인용하라."
  </label>

  <input type="radio" id="hall-fix-w2" name="hall-fix" class="hall-fix-radio">
  <label for="hall-fix-w2" class="hall-fix-row" data-good="false">
    📢 프롬프트의 첫 문장에 "환각을 일으키지 마!"라고 추가한다.
  </label>

  <div class="hall-fix-feedback" data-type="good">
    ✅ 정답입니다 — 모델에게 <em>참된 사실과 실제 링크</em>를 제공하면 다음 토큰 추측이 현실에 가깝게 유도됩니다. 이를 모델을 "그라운딩(grounding)"한다고 부르며, 즉 모델의 답변을 현실에 근거하게 만드는 것입니다.
  </div>
  <div class="hall-fix-feedback" data-type="bad1">
    ❌ 파인튜닝에는 시간과 컴퓨팅 자원이 들며, 학습 데이터에 없는 최신 사실에 대한 환각을 즉시 해결해주지는 못합니다.
  </div>
  <div class="hall-fix-feedback" data-type="bad2">
    ❌ "환각을 일으키지 마!" 같은 단순한 경고는 모델에게 참조할 실제 사실을 제공하지 않습니다. 모델에게는 실제 정보를 바탕으로 한 그라운딩이 필요합니다.
  </div>
</div>
</div>

---

## 🛡️ 가드레일 구현하기 :id=implementing-guardrails

모델이 다음을 지키도록 해야 한다면 어떻게 해야 할까요?
- 유해한 발언을 하지 않도록
- 자신의 작업에만 집중하도록
- 개인정보나 의료 조언을 절대 공유하지 않도록

이때 **가드레일**(guardrail)이 필요합니다.

가드레일은 모델의 동작 주변에 설정하는 추가적인 규칙이나 검사로, 예를 들어 다음과 같습니다.
- 정확히 어떻게 답해야 하는지를 알려주는 템플릿
- 안전하지 않은 콘텐츠를 차단하는 필터
- 모델이 말한 내용을 사실 확인하는 외부 시스템

그리고 실제로 가드레일 자체가 또 다른 LLM이 되어 원래 LLM이 생성한 결과를 검사할 수도 있습니다.

가드레일은 Canopy와 같은 실제 시스템에서 중요합니다 — 특히 학교, 의료, 대중을 상대하는 애플리케이션에서 더욱 그렇습니다.

가드레일을 언제 사용해야 하고 언제 더 유연하게 접근해야 하는지를 다루는 퀴즈가 있습니다.


<!-- 🛡️ Guardrails – architectural quiz -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

  <h3 style="margin:0 0 10px;color:#5a5a5a;">🛡️ 퀴즈</h3>

  <p style="color:#495057;font-weight:500;">
    <strong>가드레일은 언제 효과를 발휘할까요?</strong><br>
    각 상황에서 표준 안전 가드레일을 추가하는 것이 더 나은 아키텍처 선택인지 판단해 보세요.
    악용 위험, 지연 시간 예산, 거짓 양성(false positive)의 비용을 고려하세요.
  </p>

  <style>
    .gtbl{border-collapse:collapse;width:100%;font-size:.94em;color:#495057}
    .gtbl th,.gtbl td{border:1px solid #d1e7dd;padding:10px}
    .gtbl th{background:#eef5ff;text-align:center}
    .grad{display:none}

    /* initial neutral cell */
    .gopt{display:block;height:32px;line-height:30px;border-radius:6px;
          background:#f8f9fa;border:2px solid #e9ecef;cursor:pointer}

    .gopt:hover{background:#fff;border-color:#dee2e6}

    /* right pick */
    .grad:checked + .gopt[data-good="yes"]{
      background:#d4edda;border-color:#c3e6cb;color:#155724}
    .grad:checked + .gopt[data-good="yes"]::after{content:"✓";font-weight:600}

    /* wrong pick + explanation */
    .grad:checked + .gopt[data-good="no"]{
      background:#f8d7da;border-color:#f5b7b1;color:#721c24}
    .grad:checked + .gopt[data-good="no"]::after{
      content:"✗  → " attr(data-msg);
      font-weight:600;
      margin-left:6px}
  </style>

  <table class="gtbl">
    <tr>
      <th style="width:45%">상황</th>
      <th>가드레일<br><small>(예)</small></th>
      <th>가드레일<br><small>(아니오)</small></th>
    </tr>

  <!-- 1 Public bot -->
  <tr>
    <td>🌐 <b>공개 Q&amp;A 봇</b></td>

  <td align="center">
    <input type="radio" id="r1y" name="r1" class="grad">
    <label for="r1y" class="gopt" data-good="yes"></label>
  </td>

  <td align="center">
    <input type="radio" id="r1n" name="r1" class="grad">
    <label for="r1n" class="gopt" data-good="no"
            data-msg="필터 없이는 안전하지 않음"></label>
  </td>
  </tr>

  <!-- 3 Medical assistant -->
  <tr>
    <td>🏥 <b>건강 조언 어시스턴트</b></td>

  <td align="center">
    <input type="radio" id="r3y" name="r3" class="grad">
    <label for="r3y" class="gopt" data-good="yes"></label>
  </td>

  <td align="center">
    <input type="radio" id="r3n" name="r3" class="grad">
    <label for="r3n" class="gopt" data-good="no"
            data-msg="유해한 조언의 위험"></label>
  </td>
  </tr>

  <!-- 4 Dev code helper -->
  <tr>
    <td>💻 <b>개발자 전용 코드 도우미</b></td>

  <td align="center">
    <input type="radio" id="r4y" name="r4" class="grad">
    <label for="r4y" class="gopt" data-good="no"
            data-msg="무해한 코드 스니펫까지 차단함"></label>
  </td>

  <td align="center">
    <input type="radio" id="r4n" name="r4" class="grad">
    <label for="r4n" class="gopt" data-good="yes"></label>
  </td>
  </tr>
  </table>

  <p style="margin-top:8px;font-size:.9em;color:#495057;">
    초록색 ✓는 아키텍처적으로 타당한 선택을 나타내고, 빨간색 ✗는 왜 다른 선택이 최선이 아닌지를 설명합니다.
  </p>
</div>



### 🔍 실습 - LLM에는 내장된 메모리가 있을까? :id=hands-on-exercises-do-llms-have-built-in-memory

모델에게 다음 질문을 보내 보세요.

```bash
What did you learn today?
```

그런 다음 다음 질문을 이어서 보내 보세요.

```bash
What did I say in the last message?
```

모델은 뭐라고 응답했나요?

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>


<!-- TODO: Uncomment this below line when we have it in Canopy -->
<!-- Now try the same thing in **Canopy** and compare. Does it remember what you said? What makes it different? -->


### 🔍 실습 - LLM은 결정론적일까? :id=hands-on-exercises-are-llms-deterministic

이번에는 모델에게 다음과 같은 간단한 질문을 해보세요.

```bash
How can I brew Turkish tea? ☕️🫖
```

응답을 기록해 두세요. 그런 다음 **정확히 같은 질문을 다시** 해보세요.

같은 답변을 받았나요, 아니면 다른 답변을 받았나요?

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>


LLM은 답변을 생성할 때 종종 약간의 무작위성을 사용합니다. 이 무작위성은 **temperature**라는 값으로 제어됩니다.
- **낮은 temperature (예: 0.1)** → 더 예측 가능하고 반복 가능한 응답
- **높은 temperature (예: 0.9)** → 더 다양하고 창의적인 응답

temperature 값을 조정해 보면서 동작이 어떻게 바뀌는지 확인해 보세요.


[🔝 목차로 돌아가기](#contents)
</content>
