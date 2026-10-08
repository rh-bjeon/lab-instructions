# Module 11 - 수요와 공급 101

> 모든 사람에게 GPU를 주는 것은 모든 사람에게 각자의 발전소를 주는 것과 같습니다. 그냥... 전기를 나눠 쓰면 어떨까요? ⚡

# 🧑‍🍳 모듈 소개

Canopy가 어떻게 시작됐는지 기억하시나요? Module 2에서의 간단한 챗봇 실험이었습니다. GitOps 배포, RAG 기반 문서 인텔리전스, 학업 윤리를 위한 가드레일, 에이전틱 기능들을 거쳐... 이제는 Redwood Digital University의 모든 사람이 Canopy 같은 애플리케이션을 원하고 있습니다.

---

# 👥 페르소나 소개

이 모듈이 특별한 이유는 사람마다 MaaS의 다른 측면에 관심을 갖기 때문입니다. 네 가지 시각으로 이를 탐구해보겠습니다:

| 페르소나 | 이모지 | 관심사... | 주요 레슨 |
|---------|-------|-------------------|-----------------|
| **오너(Owner)** | 🎩 | 비용, 효율성, ROI, "왜 우리가 GPU에 이렇게 많이 쓰고 있지?" | 1, 5 |
| **AI 엔지니어** | 🔧 | 인프라, 배포, "이걸 어떻게 제대로 구축하지?" | 2 |
| **서비스 관리자** | 👩‍💼 | 사용자 관리, 설정, "누가 무엇에 접근해야 하지?" | 3, 5 |
| **소비자(Consumer)** | 👤 | API 접근, 앱 구축, "그냥 엔드포인트만 줘!" | 4, 6 |

각 레슨을 진행하면서 "여러 모자를 바꿔 쓰며" MaaS를 다양한 관점에서 이해하게 됩니다. 끝날 때쯔음에는 각 역할이 왜 중요한지 이해하게 될 것이고—어쩌면 어떤 모자가 자신에게 가장 잘 맞는지도 깨닫게 될 것입니다! 🎭

---

# 🖼️ 큰 그림

![big-picture-complete.jpg](./images/big-picture-maas.jpg)

목표는 다음과 같습니다:

![Before and After MaaS comparison showing resource consolidation](images/before-after-maas.svg)

---

# 🔮 학습 목표

이 모듈을 마치면 다음을 할 수 있게 됩니다:

* **설명하기** — 조직에서 AI 도입을 확장하는 데 왜 MaaS가 필수적인지
* **배포하기** — GitOps 원칙을 사용해 OpenShift에 LiteMaaS를 배포하기
* **설정하기** — 서비스 관리자로서 사용자 역할, 모델 접근, 예산을 설정하기
* **사용하기** — API 키와 OpenAI 호환 인터페이스를 통해 AI 모델을 사용하기
* **모니터링하기** — 사용량을 모니터링하고, 비용을 추적하며, 차지백(chargeback) 모델을 구현하기
* **통합하기** — 기존 애플리케이션(Canopy처럼!)을 MaaS 백엔드와 통합하기

---

# 🔨 이 모듈에서 사용하는 도구

* **LiteMaaS** — 경량의 오픈소스 Models-as-a-Service 개념 증명(proof-of-concept) 애플리케이션
  * 아름답고 접근성이 좋은 UI를 위한 React + PatternFly 6 프론트엔드
  * 견고한 API 관리를 위한 Fastify + PostgreSQL 백엔드
  * OpenAI 호환 API 프록시를 위한 LiteLLM 통합
  * OpenShift 통합을 지원하는 OAuth2/JWT 인증

* **LiteLLM** — 여러 모델 백엔드에 걸쳐 통일된 API를 제공하는 OpenAI 호환 프록시

* **PostgreSQL** — 사용자, API 키, 사용량 데이터, 감사 로그를 저장하는 데이터베이스

* **OpenShift OAuth** — 원활한 사용자 온보딩을 위한 엔터프라이즈 인증 통합

* **여러분이 좋아하는 HTTP 클라이언트** — API 호출을 하기 위한 curl, Postman, 또는 Python requests
