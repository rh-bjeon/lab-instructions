# 🧠 프롬프트 엔지니어링이란 무엇인가?

<div class="terminal-curl"></div>

프롬프트 엔지니어링은 언어 모델로부터 유용하고, 관련성 있고, 정확한 출력을 이끌어내기 위해 효과적인 입력(프롬프트)을 설계하는 작업입니다.

매우 똑똑하지만 매우 문자 그대로 받아들이는 어시스턴트에게 지시문을 작성하는 것이라고 생각하면 됩니다. 프롬프트를 어떻게 표현하는지에 따라 모델 응답의 어조, 형식, 깊이, 심지어 정확성까지도 크게 달라질 수 있습니다.

프롬프팅에는 일반적으로 두 가지 핵심 구성 요소가 있습니다.

* **시스템 프롬프트(System Prompt)**: 모델의 맥락이나 행동을 설정합니다. 모델이 *어떻게* 행동해야 하는지를 정의합니다(예: "You are a helpful teaching assistant for computer science students.").
* **사용자 프롬프트(User Prompt)**: 모델에게 실제로 주는 질문이나 작업입니다(예: "Explain recursion to a beginner.").

이 둘이 함께 모델의 행동을 유도하고 응답의 형태를 결정합니다.

> ℹ️ **참고:** 시스템 프롬프트와 사용자 프롬프트는 LLM에 따로따로 전송되는 것이 아니라, 하나의 프롬프트로 합쳐져서 전달됩니다.  

## 🎯 RDU의 Canopy에서 프롬프트 엔지니어링이 중요한 이유

Redwood Digital University에서는 다양한 학생들의 필요와 교수 스타일에 맞춰 적응하도록 설계된 플랫폼인 **Canopy**를 구축하고 있습니다. 이는 좋은 LLM뿐만 아니라 프롬프트를 다듬는 작업도 필요하다는 뜻입니다.

서로 다른 프롬프팅 조건에서 우리 LLM이 어떻게 동작하는지 살펴봅시다.


## 🧪 실습: Gen AI Playground

Red Hat OpenShift AI는 다양한 프롬프팅 전략을 실험해볼 수 있는 플레이그라운드를 만들 수 있는 기능을 제공하며, 그 외에도 다양한 실험 기능을 제공합니다. 지금은 그중 `Prompt` 부분에 집중해보겠습니다.

플레이그라운드를 만들어 봅시다!

1. [OpenShift AI](https://data-science-gateway.<CLUSTER_DOMAIN>/)에 로그인하세요. 몇 개의 `Projects`가 보일 것입니다. `<USER_NAME>-canopy`라고 불리는 것이 바로 당신의 실험 환경입니다! 이곳에서 우리는 테스트와 운영 단계로 넘어가기 전에 아이디어를 검증합니다 💪

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

5. 당신의 목표는 주어진 텍스트를 **요약**하기 위한 최적의 시스템 프롬프트와 설정을 찾는 것입니다. 

	플레이그라운드에서 설정할 수 있는 항목은 다음과 같습니다.

	| 설정          | 하는 일                                | 예시                       |
	| ---------------- | ------------------------------------------- | ----------------------------- |
	| 🧾 시스템 프롬프트 | AI의 역할이나 행동을 설정함              | "You are a helpful tutor."     |
	| 💬 사용자 프롬프트   | 부여하는 작업                           | "This text is about..."        |
	| 🔥 Temperature   | 출력이 얼마나 창의적이고 다양해질지 (0 = 엄격하고 결정적, 1 = 창의적이고 무작위적) | "0.2 = 엄격, 0.8 = 창의적"  |

	Temperature 설정은 `Model` 탭에서, 시스템 프롬프트는 `Prompt` 탭에서 확인할 수 있습니다. 그리고 사용자 프롬프트는 모델에게 보내는 내용입니다 :)

	좋은 요약 프롬프트를 생각해 보세요. 그리고 여기 요약을 요청할 텍스트가 있습니다(다시 말해, 사용자 프롬프트에 보낼 텍스트입니다).

	```
	Tea preparation involves the controlled extraction of bioactive compounds from processed Camellia sinensis leaves. Begin by heating water to near 100°C to optimize solubility. Introduce a tea bag to a ceramic vessel, then infuse with hot water to initiate steeping—typically 3–5 minutes to allow for the diffusion of polyphenols and caffeine. Upon removal of the bag, optional additives like sucrose or lipid-based emulsions may be introduced to alter flavor profiles. The infusion is then ready for consumption.
	```

	![images/explain-like-8.jpg](images/explain-like-8.jpg)

	Gen AI Playground를 사용해서 다음을 해보세요.

	* 서로 다른 **시스템 프롬프트**가 같은 모델의 행동을 어떻게 바꾸는지 비교해보기.
	* **temperature**를 조정해서 출력이 어떻게 달라지는지 살펴보기.
	* Canopy의 요약 기능에 잘 작동할 시스템 프롬프트 템플릿을 정해보기.

	📌 **팁**: 시스템 프롬프트의 어조, 구체성, 형식을 바꿔보면서 출력이 얼마나 달라지는지 확인해 보세요. 창의적으로 시도해 보는 것을 두려워하지 마세요!


6. 위 텍스트를 요약하는 데 당신이 찾을 수 있는 최선의 시스템 프롬프트와 설정은 무엇인가요?

	시도해볼 수 있는 몇 가지 예시 시스템 프롬프트입니다.

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


_`Temperature`에 대해 더 알고 싶으신가요? 당신에게는 꽤 많이 아는 대형 언어 모델에 접근할 수 있잖아요? 편하게 물어보세요 🙃_
</content>
