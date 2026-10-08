# 📝 GenAI 102: 프롬프팅 원칙

## 📚 목차
- [🎯 프롬프팅이 왜 중요할까?](#why-is-prompting-important)
- [🔍 프롬프트가 중요한 이유](#prompt-matters)
- [🧩 프롬프트의 구성 요소](#composition-of-a-prompt)
- [🔧 시스템 프롬프트](#system-prompt)
- [🧪 컨텍스트](#context)
- [📏 모델이 받아들일 수 있는 입력에는 한계가 있다](#the-model-can-only-take-so-much-input)
- [✅ 요약](#recap)

## 🎯 프롬프팅이 왜 중요할까? :id=why-is-prompting-important

프롬프팅은 모델이 답을 내놓게 만드는 방법입니다.

<!-- 🍿 Pop Quiz – Prompting definition -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">프롬프팅은 모델이 답을 내놓게 만드는 방법입니다.</p>

<style>
.quiz-container-prompting-def{position:relative}
.quiz-option-prompting-def{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-prompting-def:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-prompting-def{display:none}
.quiz-radio-prompting-def:checked+.quiz-option-prompting-def[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-prompting-def:checked+.quiz-option-prompting-def:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-prompting-def{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#prompting-def-correct:checked~.feedback-prompting-def[data-feedback="correct"],
#prompting-def-wrong1:checked~.feedback-prompting-def[data-feedback="wrong1"]{display:block}
.feedback-prompting-def[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-prompting-def[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-prompting-def">
  <input type="radio" name="quiz-prompting-def" id="prompting-def-correct" class="quiz-radio-prompting-def">
  <label for="prompting-def-correct" class="quiz-option-prompting-def" data-correct="true">✅ TRUE</label>

  <input type="radio" name="quiz-prompting-def" id="prompting-def-wrong1" class="quiz-radio-prompting-def">
  <label for="prompting-def-wrong1" class="quiz-option-prompting-def" data-correct="false">❌ FALSE</label>

  <div class="feedback-prompting-def" data-feedback="correct">✅ 정답입니다! 진실 1번을 기억하세요: 모델은 말을 걸어야만 답합니다. 프롬프팅은 모델에게 텍스트를 보내 응답을 만들어내게 하는 방법입니다.</div>
  <div class="feedback-prompting-def" data-feedback="wrong1">❌ 사실 이것은 TRUE입니다! 프롬프트가 없으면 모델은 아무것도 만들어내지 않습니다. 프롬프팅은 말 그대로 모델에게 텍스트 입력을 보내 응답을 유도하는 행위입니다.</div>
</div>
</div>

LLM은 **오직** 텍스트만을 입력으로 받기 때문에, 전체 출력은 **당신이 보내는 텍스트**에 전적으로 달려 있습니다.

다시 말해, 프롬프트를 올바르게 표현하면 LLM이 원하는 어떤 말이든 하게 만들 수 있습니다 😈😈


## 🔍 프롬프트가 중요한 이유 :id=prompt-matters

프롬프트가 무엇이든, 일반적으로 모델이 정중하고, 도움이 되며, 유해하지 않기를 원할 것입니다. 적어도 특정한 방식으로 행동하길 바랄 것입니다.

### 🔍 실습: 프롬프팅이 출력을 어떻게 바꾸는지 확인하기

다음 두 프롬프트를 각각 보내보고 응답을 비교해 보세요.

**프롬프트 1:**
```
You are a helpful tutor. What is 5+5?
```

**프롬프트 2:**
```
You only speak in lies. What is 5+5?
```

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

<!-- 🍿 Pop Quiz – Prompt changes output -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">프롬프트를 바꾸면 출력이 크게 달라질 수 있습니다.</p>

<style>
.quiz-container-prompt-change{position:relative}
.quiz-option-prompt-change{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-prompt-change:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-prompt-change{display:none}
.quiz-radio-prompt-change:checked+.quiz-option-prompt-change[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-prompt-change:checked+.quiz-option-prompt-change:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-prompt-change{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#prompt-change-correct:checked~.feedback-prompt-change[data-feedback="correct"],
#prompt-change-wrong1:checked~.feedback-prompt-change[data-feedback="wrong1"]{display:block}
.feedback-prompt-change[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-prompt-change[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-prompt-change">
  <input type="radio" name="quiz-prompt-change" id="prompt-change-correct" class="quiz-radio-prompt-change">
  <label for="prompt-change-correct" class="quiz-option-prompt-change" data-correct="true">✅ TRUE</label>

  <input type="radio" name="quiz-prompt-change" id="prompt-change-wrong1" class="quiz-radio-prompt-change">
  <label for="prompt-change-wrong1" class="quiz-option-prompt-change" data-correct="false">❌ FALSE</label>

  <div class="feedback-prompt-change" data-feedback="correct">✅ 정확합니다! 프롬프트는 모델이 받는 유일한 입력입니다. 지시문이 다르면 완전히 다른 동작으로 이어집니다 — 같은 질문이라도 전혀 다른 답이 나올 수 있습니다.</div>
  <div class="feedback-prompt-change" data-feedback="wrong1">❌ 사실 방금 보았듯이, 프롬프트를 바꾸면 응답이 완전히 달라질 수 있습니다. 모델의 동작은 전적으로 받는 텍스트에 의해 결정됩니다.</div>
</div>
</div>

---

## 🧩 프롬프트의 구성 요소 :id=composition-of-a-prompt

초기 연구자들은 프롬프트를 두 부분으로 나누었습니다.

- **시스템 프롬프트(System Prompt)** — 모델이 어떻게 행동하길 원하는지
- **사용자 프롬프트(User Prompt)** — 답을 얻고자 하는 질문

예를 들어 `"You are a helpful tutor. What is 5+5?"`라는 프롬프트는 다음과 같이 나눌 수 있습니다.

| 구성 요소 | 내용 |
|------|---------|
| **시스템 프롬프트** | "You are a helpful tutor." |
| **사용자 프롬프트** | "What is 5+5?" |

> 모델은 **사용자 프롬프트보다 시스템 프롬프트를 더 따르는** 경향이 있습니다. 단순히 모델이 그렇게 학습되었기 때문입니다.

### 시스템 프롬프트는 모델에 대한 별도의 입력이 아니다

시스템 프롬프트와 사용자 프롬프트는 다음과 같이 서로 다른 섹션에 주석을 붙여 하나의 전체 입력 프롬프트로 합쳐집니다.

```
[System] You are a helpful and patient tutor. Guide the user towards the correct answer without giving it straight up.

[User] What is 5+5?
```

이 전체가 모델에 전달되는 **단 하나의 입력 프롬프트**가 됩니다.


## 🔧 시스템 프롬프트 :id=system-prompt

모델의 행동을 어떻게 유도할 수 있을까요? 바로 여기서 등장하는 것이... **시스템 프롬프트**입니다!

- 시스템 프롬프트는 모델의 **전반적인 행동**을 설정합니다
  - **애플리케이션 소유자(Application Owners)**가 설계하고 구현합니다
- 입력 프롬프트의 일부로 자동으로 첨부됩니다
- **최종 사용자가 보거나 변경할 수 없는** 부분입니다

### 🔍 실습: 시스템 프롬프트 vs 사용자 프롬프트

둘이 충돌할 때 어느 쪽이 이기는지 확인해 봅시다.

1. 설정을 열고 시스템 프롬프트를 다음과 같이 설정하세요: `"You only speak in lies."`
2. 그런 다음 다음과 같이 물어보세요: `"You are a helpful tutor. What is 5+5?"`

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

무슨 일이 일어났나요? 시스템 프롬프트가 이겼나요, 아니면 사용자 프롬프트가 이겼나요?

<!-- 🍿 Pop Quiz – System vs User prompt -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">사용자 프롬프트가 시스템 프롬프트를 덮어썼습니다.</p>

<style>
.quiz-container-sys-vs-user{position:relative}
.quiz-option-sys-vs-user{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-sys-vs-user:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-sys-vs-user{display:none}
.quiz-radio-sys-vs-user:checked+.quiz-option-sys-vs-user[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-sys-vs-user:checked+.quiz-option-sys-vs-user:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-sys-vs-user{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#sys-vs-user-correct:checked~.feedback-sys-vs-user[data-feedback="correct"],
#sys-vs-user-wrong1:checked~.feedback-sys-vs-user[data-feedback="wrong1"]{display:block}
.feedback-sys-vs-user[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-sys-vs-user[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-sys-vs-user">
  <input type="radio" name="quiz-sys-vs-user" id="sys-vs-user-wrong1" class="quiz-radio-sys-vs-user">
  <label for="sys-vs-user-wrong1" class="quiz-option-sys-vs-user" data-correct="false">✅ TRUE — 사용자 프롬프트가 주도권을 가져갔다</label>

  <input type="radio" name="quiz-sys-vs-user" id="sys-vs-user-correct" class="quiz-radio-sys-vs-user">
  <label for="sys-vs-user-correct" class="quiz-option-sys-vs-user" data-correct="true">❌ FALSE — 시스템 프롬프트가 여전히 우세했다</label>

  <div class="feedback-sys-vs-user" data-feedback="correct">✅ 정답입니다! 시스템 프롬프트가 일반적으로 우선권을 가집니다. 모델은 사용자 수준의 지시보다 시스템 수준의 지시를 더 충실히 따르도록 학습되었습니다.</div>
  <div class="feedback-sys-vs-user" data-feedback="wrong1">❌ 그렇지 않습니다! 시스템 프롬프트가 일반적으로 이깁니다. 모델은 사용자 수준의 지시보다 시스템 수준의 지시를 우선하도록 학습되었습니다.</div>
</div>
</div>


## 🧪 컨텍스트 :id=context

모델은 당신의 이름을 몰랐었죠? 하지만 모델이 무언가를 모른다면, **우리가 필요한 것을 줄 수 있습니다!**

### 🔍 실습: 모델에게 컨텍스트 제공하기

당신의 이름을 알려주고 **같은 프롬프트 안에서** 이름을 아는지 물어보세요.

```
Hello! My name is Rob. What is my name?
```

<iframe
	src="https://ai-orientation-app-ai501.<CLUSTER_DOMAIN>/chat?embed"
	frameborder="0"
	width="500"
	height="600"
	style="border: 1px solid #ccc; border-radius: 8px;"
	loading="lazy">
</iframe>

이번에는 모델이 당신의 이름을 *알고* 있었습니다! 하지만 그것을 **학습**한 것은 아닙니다 — 당신이 프롬프트의 일부로 제공한 것입니다.

이것을 **컨텍스트(context)**라고 부릅니다.
- 프롬프트에 정보를 명시적으로 추가함으로써, 모델이 그 정보를 바탕으로 답하게 만들 수 있습니다
- 본질적으로, 우리는 프롬프트를 통해 **정보를 주입(inject)**하고 있는 것입니다

### 예시: 컨텍스트가 쌓이는 방식

모델의 응답이 다음 메시지가 처리되기 전에 **입력에 다시 추가**되는 것을 확인해 보세요.

**모델이 받는 입력:**
```
[System] You are a helpful and patient tutor. Guide the user towards the correct answer without giving it straight up.

[User] What is 5+5?
```

**모델의 응답:**
> Try and see if you can do 2+2 and how that works, then 3+3, then 4+4, and finally 5+5. What do you get?

이제 사용자가 답을 합니다. 하지만 모델이 실제로 받는 것을 보세요 — **지금까지의 모든 내용에 새 메시지가 더해진 것**입니다.

```
[System] You are a helpful and patient tutor. Guide the user towards the correct answer without giving it straight up.

[User] What is 5+5?

[Tutor] Try and see if you can do 2+2 and how that works, then 3+3, then 4+4, and finally 5+5. What do you get?

[User] I got 2+2=5
```

**모델의 응답:**
> Hmm okay that's not quite right, how did you get it to be 5?

무슨 일이 일어났는지 보이나요? 모델의 이전 응답이 **입력의 일부**가 되었습니다. 컨텍스트는 대화를 주고받을 때마다 **계속 커집니다**. 모델은 항상 지금까지의 전체 대화를 보고 있으며, 이것이 바로 같은 세션 안에서 앞서 말한 내용을 "기억"하는 방식입니다.


## 📏 모델이 받아들일 수 있는 입력에는 한계가 있다 :id=the-model-can-only-take-so-much-input

인터넷 전체를 컨텍스트로 추가해서 모델을 전지전능하게 만들 수 있을까요?

<!-- 🍿 Pop Quiz – Context limits -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">🍿 깜짝 퀴즈</h3>
<p style="color:#495057; font-weight:500;">인터넷 전체를 컨텍스트로 추가하면 모델이 모든 것을 알게 될 것이다.</p>

<style>
.quiz-container-context-limit{position:relative}
.quiz-option-context-limit{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-context-limit:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-context-limit{display:none}
.quiz-radio-context-limit:checked+.quiz-option-context-limit[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-context-limit:checked+.quiz-option-context-limit:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5c6cb}
.feedback-context-limit{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#context-limit-correct:checked~.feedback-context-limit[data-feedback="correct"],
#context-limit-wrong1:checked~.feedback-context-limit[data-feedback="wrong1"]{display:block}
.feedback-context-limit[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-context-limit[data-feedback="wrong1"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-context-limit">
  <input type="radio" name="quiz-context-limit" id="context-limit-wrong1" class="quiz-radio-context-limit">
  <label for="context-limit-wrong1" class="quiz-option-context-limit" data-correct="false">✅ TRUE</label>

  <input type="radio" name="quiz-context-limit" id="context-limit-correct" class="quiz-radio-context-limit">
  <label for="context-limit-correct" class="quiz-option-context-limit" data-correct="true">❌ FALSE</label>

  <div class="feedback-context-limit" data-feedback="correct">✅ 정답입니다! 모델이 받아들일 수 있는 입력에는 최대치가 있습니다. 그보다 더 많은 단어를 추가하면 오류가 발생합니다. 어떤 컨텍스트를 제공할지 전략적으로 선택해야 합니다.</div>
  <div class="feedback-context-limit" data-feedback="wrong1">❌ 아닙니다! 모델에는 최대 컨텍스트 길이가 있습니다. 모든 것을 그냥 쏟아부을 수는 없습니다! 모델이 한 번에 처리할 수 있는 텍스트의 양에는 엄격한 한계가 있습니다.</div>
</div>
</div>

> 모델이 받아들일 수 있는 **최대 입력량**이 있습니다. 그보다 더 많은 단어를 추가하면 오류가 발생합니다. 다음 섹션에서 이에 대해 더 자세히 살펴보겠습니다.

---

## ✅ 요약 :id=recap

프롬프팅에 대해 배운 내용:

| 개념 | 핵심 요점 |
|---------|-------------|
| **프롬프팅** | 모델과 상호작용하는 유일한 방법: 텍스트 입력, 텍스트 출력 |
| **시스템 프롬프트** | 모델의 행동을 설정하며, 애플리케이션 소유자가 작성하고, 우선권을 가짐 |
| **사용자 프롬프트** | 사용자가 실제로 하는 질문이나 요청 |
| **컨텍스트** | 모델의 답변을 유도하기 위해 프롬프트에 주입하는 정보 |
| **컨텍스트 한계** | 모델에는 최대 입력 크기가 있으며, 모든 것을 추가할 수는 없음 |

</content>
