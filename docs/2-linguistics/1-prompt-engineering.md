# 🧠 프롬프트 엔지니어링이란 무엇인가?

<div class="terminal-curl"></div>

프롬프트 엔지니어링은 언어 모델에서 유용하고 정확한 응답을 얻을 수 있도록 입력, 즉 프롬프트를 설계하는 작업입니다.

똑똑하지만 지시를 글자 그대로 해석하는 어시스턴트에게 업무를 맡긴다고 생각하면 쉽습니다. 같은 요청이라도 프롬프트를 어떻게 작성하느냐에 따라 응답의 어조와 형식, 설명의 깊이, 심지어 정확성까지 크게 달라집니다.

프롬프팅에는 일반적으로 두 가지 핵심 구성 요소가 있습니다.

* **시스템 프롬프트(System Prompt)**: 모델이 따라야 할 배경과 행동 방식을 지정합니다(예: "You are a helpful teaching assistant for computer science students.").
* **사용자 프롬프트(User Prompt)**: 모델에 전달하는 실제 질문이나 작업입니다(예: "Explain recursion to a beginner.").

두 프롬프트가 함께 모델의 행동과 응답 형식을 결정합니다.

> ℹ️ **참고:** 시스템 프롬프트와 사용자 프롬프트는 LLM에 따로따로 전송되는 것이 아니라, 하나의 프롬프트로 합쳐져서 전달됩니다.  

## 🎯 RDU의 Canopy에서 프롬프트 엔지니어링이 중요한 이유

Redwood Digital University에서는 학생마다 다른 학습 요구와 교수자의 교육 방식에 맞춰 동작하는 플랫폼 **Canopy**를 만들고 있습니다. 이를 위해서는 성능 좋은 LLM뿐 아니라 목적에 맞게 잘 다듬은 프롬프트도 필요합니다.

프롬프트 조건을 바꾸었을 때 LLM의 응답이 어떻게 달라지는지 살펴보겠습니다.


## 🧪 실습: Gen AI Playground

Red Hat OpenShift AI는 여러 프롬프팅 전략을 손쉽게 비교할 수 있는 플레이그라운드를 제공합니다. 이번 실습에서는 그중 `Prompt` 기능에 집중합니다.

이제 플레이그라운드를 만들어 보겠습니다.

1. [OpenShift AI](https://data-science-gateway.<CLUSTER_DOMAIN>/)에 로그인합니다. `Projects` 목록에서 `<USER_NAME>-canopy`를 찾습니다. 이 프로젝트가 여러분의 실험 환경이며, 테스트와 운영 단계로 넘어가기 전에 아이디어를 검증하는 공간입니다. 💪

    사용자: `<USER_NAME>`

    비밀번호: `<PASSWORD>`

   ![openshift-ai.png](./images/openshift-ai.png)

   OpenShift AI에 오신 것을 환영합니다! 👋🤖

2. 왼쪽 메뉴에서 `Gen AI studio` > `Playground`를 선택합니다. 드롭다운 메뉴에서 `<USER_NAME>-canopy` 네임스페이스를 선택했는지 확인하세요. `Create playground`를 클릭합니다.

	![genai-playground.png](./images/genai-playground.png)

3. 프롬프트가 적용된 모델을 선택하고 `Create`를 클릭합니다.

	![genai-playground-2.png](./images/genai-playground-2.png)

4. 플레이그라운드가 준비되면, 제대로 작동하는지 확인하기 위해 메시지를 보내보세요 😊

	![genai-playground-3.png](./images/genai-playground-3.png)

5. 이번 실습의 목표는 주어진 텍스트를 **요약**하는 데 가장 적합한 시스템 프롬프트와 설정을 찾는 것입니다.

	플레이그라운드에서 설정할 수 있는 항목은 다음과 같습니다.

	| 설정          | 하는 일                                | 예시                       |
	| ---------------- | ------------------------------------------- | ----------------------------- |
	| 🧾 시스템 프롬프트 | AI의 역할이나 행동을 설정함              | "You are a helpful tutor."     |
	| 💬 사용자 프롬프트   | 모델에 요청할 실제 작업                 | "This text is about..."        |
	| 🔥 Temperature   | 출력이 얼마나 창의적이고 다양해질지 (0 = 엄격하고 결정적, 1 = 창의적이고 무작위적) | "0.2 = 엄격, 0.8 = 창의적"  |

	Temperature 설정은 `Model` 탭에서, 시스템 프롬프트는 `Prompt` 탭에서 확인할 수 있습니다. 그리고 사용자 프롬프트는 모델에게 보내는 내용입니다 :)

	효과적인 요약 프롬프트를 생각해 보세요. 아래 텍스트를 사용자 프롬프트로 사용합니다.

	```
	차를 준비하는 과정은 가공된 차나무(Camellia sinensis) 잎에서 생리활성 화합물을 제어된 방식으로 추출하는 과정입니다. 먼저, 화합물의 용해도를 최적화하기 위해 물을 약 100°C까지 가열합니다. 세라믹 용기에 티백을 넣은 다음, 뜨거운 물을 부어 우려내는 과정을 시작합니다. 일반적으로 폴리페놀과 카페인이 충분히 확산될 수 있도록 3~5분 동안 우려냅니다. 티백을 제거한 후에는 풍미를 조절하기 위해 설탕(자당)이나 지방 기반 유화액(예: 우유)과 같은 첨가물을 선택적으로 넣을 수 있습니다. 이렇게 하면 차가 완성되어 마실 준비가 됩니다.
	```

	![images/explain-like-8.jpg](images/explain-like-8.jpg)

	Gen AI Playground를 사용해서 다음을 해보세요.

	* 서로 다른 **시스템 프롬프트**가 같은 모델의 행동을 어떻게 바꾸는지 비교해보기.
	* **temperature**를 조정해서 출력이 어떻게 달라지는지 살펴보기.
	* Canopy의 요약 기능에 잘 작동할 시스템 프롬프트 템플릿을 정해보기.

	📌 **팁**: 시스템 프롬프트의 어조와 구체성, 출력 형식을 바꾸어 응답이 어떻게 달라지는지 비교해 보세요. 다양한 방식으로 자유롭게 실험해도 좋습니다.


6. 위 텍스트를 가장 잘 요약하는 시스템 프롬프트와 설정을 찾아보세요.

	아래는 실험해 볼 수 있는 시스템 프롬프트 예시입니다. 실습에서 사용하는 LLM은 크기가 작아 한국어보다 영어로 지시했을 때 더 나은 결과를 내는 경향이 있습니다.

	```
	Write a short version of this.
	```

	```
	Summarize the text in a few sentences.
	```

	```
	Explain the given text as if I'm a 5-year-old.
	```

	```
	Explain the given text using only emojis.
	```

	중요한 정보를 잃지 않으면서도 텍스트를 더 잘 설명하는 프롬프트를 만들어낼 수 있나요?


_`Temperature`가 더 궁금하다면 지금 사용 중인 LLM에 직접 물어보세요. 꽤 자세히 설명해 줄 겁니다. 🙃_
</content>
