# Agentic Frameworks: Llama Stack & LangGraph

## 밑바닥부터 프로덕션까지

방금 여러분은 수동 파싱, 루프 관리, 상태 처리, 오류 복구까지 모두 직접 구현한 ReAct agent를 밑바닥부터 만들어 보았습니다. 어려운 방식이고 보일러플레이트 코드도 많습니다! 하지만 이제는 agent가 내부적으로 *어떻게* 동작하는지 이해하게 되었습니다.

프로덕션 환경에서는 아무도 agent를 밑바닥부터 만들지 않습니다. 대신, 그 모든 복잡함을 대신 처리해주는 **agentic frameworks**(에이전틱 프레임워크)를 사용합니다.
Agentic framework는 복잡한 부분을 추상화해주기 때문에, agent가 **어떻게(how)** 동작하는지가 아니라 **무엇(what)**을 해야 하는지에 집중할 수 있습니다.

## 널리 사용되는 Agentic Framework

사용 가능한 agentic framework는 여러 가지가 있으며, 그중 대표적인 것들은 다음과 같습니다.

- **LangGraph**: LangChain이 만든 프로덕션급 그래프 기반 agent framework
- **CrewAI**: 다중 agent 협업 framework
- **AutoGen**: Microsoft의 다중 agent 대화 framework
- **Haystack**: 엔드투엔드 LLM 오케스트레이션

오늘은 **LangGraph**를 사용하겠습니다. 강력하면서도 접근하기 쉽고, OpenAI 호환 엔드포인트를 통해 Llama Stack과도 깔끔하게 통합되기 때문입니다.

## 사용 사례

다음과 같은 기능을 할 수 있는 **지식 기반 챗봇(knowledge-based chatbot)**을 만들어 보겠습니다.
1. 문서에서 정보를 검색합니다 (RAG)
2. 질문에 답할 수 없을 경우 교수님과의 미팅을 예약합니다

이를 위해서는 agent가 "검색해야 할 때"와 "예약해야 할 때"를 추론할 수 있어야 하는데, 이는 LangGraph의 단순함을 보여주기에 완벽한 예시입니다!

## LlamaStack에서 MCP 활성화하기

시작하기 전에, Llama Stack 인스턴스에서 MCP 지원을 활성화해야 합니다.

1. **OpenShift Console** → **Helm** → **Releases**로 이동하세요

    ![helm-release-2.png](images/helm-release-2.png)

2. `llama-stack-operator-instance`를 찾고, **세 개의 점(three dots)** → **Upgrade**를 클릭하세요

    ![upgrade-lls](images/upgrade-lls.png)

3. Form view에서 **MCP section**을 열고 **`enabled`**를 선택한 다음 **Upgrade**를 클릭하세요

    ![enable-mcp](images/enable-mcp.png)

이렇게 하면 LangGraph가 사용할 MCP Calendar 도구가 활성화됩니다.

## 왜 Llama Stack인가?

Llama Stack은 여기서 결정적인 차이를 만드는 세 가지 역할을 합니다: 모델을 서빙하고, RAG 벡터 스토어를 관리하며, ✨무엇보다 중요하게도✨ 표준 Chat Completions를 넘어서는 **Responses API**를 제공합니다. 표준 Chat Completions를 사용한다면, MCP 서버가 노출하는 도구마다 Python 래퍼 함수를 작성해야 합니다 (ReAct agent를 밑바닥부터 만들 때 사용했던 것과 동일한 수동 방식입니다). Responses API는 이 모든 과정을 생략합니다: MCP 서버 바인딩을 전달하기만 하면, 사용 가능한 도구들을 자동으로 발견하고 실행까지 처리해줍니다. Llama Stack이 calendar 서버를 알고 있는 이유는, 방금 수행한 Helm upgrade가 시작 시점에 이를 `tool_group`으로 등록했기 때문입니다.

LangGraph는 자체적인 MCP 지원 기능을 가지고 있어서 Llama Stack 없이도 모델에 직접 연결할 수 있습니다. 그런데도 여기서 이 구조를 사용하는 이유는, 모델, 벡터 스토어, MCP 연결 등 모든 것의 기반이 이미 이 플랫폼이기 때문입니다. 그래서 인프라 관련 관심사가 애플리케이션 코드 전체에 흩어지지 않고 한 곳에 모이게 됩니다. 모델이나 MCP 서버를 교체하는 작업도 코드 변경이 아니라 설정(config) 변경만으로 가능해집니다.

## 직접 만들어 봅시다!

훨씬 쉬워지는 걸 직접 확인할 준비가 되셨나요? 똑같은 agentic 기능을 **~70% 더 적은 코드**로 구현하게 될 것입니다. 깔끔하고 선언적인 agent 정의만 남게 됩니다.
워크벤치로 이동해서 **`experiments/8-agents/4-agentic-llamas.ipynb`**를 열어보세요
