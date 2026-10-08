# Module 8 - Autonomous Systems 101

> LLM 혼자서는 요리법을 설명할 줄만 알고 실제로는 요리를 할 수 없는 셰프와 같습니다. 거기에 도구(tools)와 자율성(agency)을 부여하면, 갑자기 검색하고, 일정을 잡고, 계산하고, 실제로 일을 해낼 수 있게 됩니다. AI agent의 세계로 환영합니다!

# 🧑‍🍳 모듈 소개

이 모듈은 LLM을 단순한 텍스트 생성기로 이해하는 단계에서, 추론하고 계획하고 행동할 수 있는 자율적인 agent를 구축하는 단계로 여러분을 안내합니다. 도구(tools)가 대화를 넘어 LLM의 역량을 어떻게 확장하는지, MCP 서버가 어떻게 확장 가능한 도구 생태계를 제공하는지, 그리고 ReAct와 같은 agentic workflow가 어떻게 정교한 다단계 추론을 가능하게 하는지 알아보게 됩니다.

RDU에서는 Canopy를 단순한 스마트 챗봇에서 진정한 student assistant(학생 비서)로 발전시키고 있습니다. 이 assistant는 지식 기반(knowledge base)을 검색하고, 교수님과의 미팅을 예약하며, 학생들이 학업 여정을 자율적으로 탐색하도록 도울 수 있습니다. 이 모듈을 마칠 때면, RAG, 도구 호출(tool calling), 그리고 지능적인 의사결정을 결합한 agent를 배포하게 될 것입니다.

# 🖼️ 큰 그림
![big-picture-agents](images/big-picture-agents.jpg)

# 🔮 학습 목표

* 도구(tools)가 무엇이며, 텍스트 생성을 넘어 LLM의 역량을 어떻게 확장하는지 이해합니다
* 확장 가능한 도구 모음을 제공하는 MCP(Model Context Protocol) 서버를 배포하고 사용합니다
* 자율적인 agent를 구축하기 위한 ReAct(Reasoning and Acting) 패턴을 학습합니다
* Llama Stack과 통합된 LangGraph를 사용해 agent를 구축합니다
* GitOps 파이프라인을 통해 agentic 기능을 test 및 production 환경에 배포합니다
* RAG 지식과 도구 기반 행동을 결합한 지능형 assistant를 만듭니다

# 🔨 이 모듈에서 사용하는 도구

* **LLM Tools**: LLM이 계산기, 데이터베이스, API와 같은 외부 서비스와 상호작용할 수 있게 해주는 JSON 기반 인터페이스
* **MCP (Model Context Protocol) Servers**: LLM이 사용할 수 있는 도구 모음을 제공하는 표준화된 서버
* **ReAct Framework**: LLM이 반복적인 루프 안에서 사고, 행동, 관찰을 수행할 수 있게 해주는 Reasoning and Acting 패턴
* **LangGraph**: 복잡한 agentic workflow를 구축하기 위한 프로덕션급 그래프 기반 agent framework
* **Llama Stack Agent APIs**: AI agent를 구축하고 오케스트레이션하기 위한 통합 레이어
* **Calendar MCP Server**: 일정 관리 및 캘린더 관리 기능을 제공하는 예시 도구 서버
* **OpenShift & Helm Charts**: 개발 및 프로덕션 환경에 agent 인프라와 MCP 서버를 배포하기 위한 도구
