# Guardrails란 무엇인가?

대형 언어 모델(LLM)의 맥락에서 guardrails(가드레일)는 다음을 보장하기 위한 안전 메커니즘입니다.

* LLM이 애플리케이션의 의도된 범위 안에서만 질문에 답합니다.
* LLM이 정확하고 애플리케이션의 의도된 범위에서 벗어나지 않는 답변을 제공합니다.
  
몇 가지 예시는 다음과 같습니다.

* Canopy에서 사용될 때, LLM이 학생이 시험이나 과제에서 부정행위를 하도록 돕는 것을 거부하도록 보장합니다.
* 학생 지원이나 동료 멘토링을 도울 때 LLM이 존중을 담아, 편향 없이 응답하도록 보장합니다.

## 일반적인 Guardrails

### Prompt-Level Guardrails (경량이며 적용이 빠름)

> Welcome to Fight Club. The first rule of Fight Club is: you do not talk about Fight Club. The second rule of Fight Club is: you DO NOT talk about Fight Club!

![fight-club.jpg](./images/fight-club.jpg)

1. 이미 여러 번 경험했듯이, 시스템 프롬프트는 LLM이 어떻게 행동해야 하는지를 정의합니다. 우리가 할 수 있는 최소한의 일은 시스템 프롬프트를 설정하는 것입니다. OpenShift AI Dashboard의 GenAI Playground로 이동해, Fight Club에 대해 이야기하지 **말라고** 지시하는 시스템 프롬프트와 함께 모델에 직접 메시지를 보내보세요.

우리가 할 수 있는 최소한의 일은 시스템 프롬프트를 설정하는 것입니다. workbench에서 터미널을 열고, Fight Club에 대해 이야기하지 **말라고** 지시하는 시스템 프롬프트와 함께 모델에 직접 메시지를 보내보세요.

  ![fight-club-2.png](./images/fight-club-2.png)

1. 효과가 있는 시스템 프롬프트를 찾았다면, 이번에는 그것을 우회해서 모델이 어쨌든 Fight Club에 대해 이야기하게 만들 방법을 생각해 보세요. 시간을 측정해 보세요. 얼마나 걸리나요?

  ![fight-club-3.png](./images/fight-club-3.png)

시스템 프롬프트는 모델의 컨텍스트에 포함된 지시일 뿐 강제력이 있는 보안 정책은 아닙니다. 프롬프트 인젝션과 난독화, 긴 대화를 이용하면 모델이 지시를 무시하도록 유도할 수 있습니다. LLM은 확률적으로 동작하고 문구와 컨텍스트의 순서에 민감하므로 잘 작성한 시스템 프롬프트도 입력이나 모델 버전에 따라 일관되지 않을 수 있습니다.

신뢰할 수 있는 가드레일을 만들려면 모델 **외부**에 여러 보안 계층을 적용해야 합니다. 입출력 필터와 분류기, 정책 엔진, 허용·차단 목록으로 허용되지 않은 동작과 데이터 유출을 차단합니다.

그러니 이제 본격적으로 들어가 봅시다. 이를 위해 흥미로운 도구 하나를 소개합니다. **NeMo Guardrails**입니다! 🛡️
