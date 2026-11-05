# 모듈 11 - 수요와 공급 101

> 모든 사용자에게 GPU를 따로 제공하는 것은 집집마다 발전소를 짓는 것과 같습니다. 전기를 함께 쓰듯 모델도 서비스로 공유하면 어떨까요? ⚡

# 🧑‍🍳 모듈 소개

Canopy는 모듈 2의 간단한 챗봇 실험으로 시작했습니다. 이후 GitOps 배포와 RAG 기반 문서 활용, 학업 윤리를 위한 가드레일, 에이전트 기능을 차례로 추가했습니다. 이제 Redwood Digital University의 여러 팀이 Canopy와 같은 AI 애플리케이션을 필요로 합니다.

---

# 👥 페르소나 소개

MaaS를 바라보는 관점은 역할마다 다릅니다. 다음 네 가지 역할의 시각에서 MaaS를 살펴보겠습니다.

| 페르소나 | 이모지 | 주요 관심사 | 관련 레슨 |
|---------|-------|------------|----------|
| **오너(Owner)** | 🎩 | 비용, 효율성, 투자 대비 효과 | 1, 5 |
| **AI 엔지니어** | 🔧 | 인프라와 배포 | 2 |
| **서비스 관리자** | 👩‍💼 | 사용자, 권한, 설정 | 3, 5 |
| **소비자(Consumer)** | 👤 | API 접근과 애플리케이션 개발 | 4, 6 |

각 레슨에서 역할을 바꾸어 가며 MaaS를 여러 관점에서 살펴봅니다. 모듈을 마치면 각 역할이 왜 필요한지 이해하고 자신에게 가장 가까운 역할도 찾을 수 있을 것입니다. 🎭

---

# 🖼️ 큰 그림

![big-picture-complete.jpg](./images/big-picture-maas.jpg)

MaaS를 도입하기 전과 후의 모습은 다음과 같습니다.

![Before and After MaaS comparison showing resource consolidation](images/before-after-maas.svg)

---

# 🔮 학습 목표

* **설명하기** — 조직의 AI 도입을 확장할 때 MaaS가 필요한 이유
* **배포하기** — GitOps 원칙에 따라 OpenShift에 LiteMaaS 배포하기
* **설정하기** — 서비스 관리자로서 사용자 역할과 모델 접근 권한, 예산 설정하기
* **사용하기** — API 키와 OpenAI 호환 인터페이스로 AI 모델 사용하기
* **모니터링하기** — 사용량과 비용을 추적하고 비용 배분(chargeback) 체계 구현하기
* **통합하기** — Canopy 같은 기존 애플리케이션을 MaaS 백엔드와 연결하기

---

# 🔨 이 모듈에서 사용하는 도구

* **LiteMaaS** — 경량 오픈 소스 Models-as-a-Service 개념 증명 애플리케이션
  * 접근성 높은 UI를 위한 React와 PatternFly 6 프런트엔드
  * API 관리를 위한 Fastify와 PostgreSQL 백엔드
  * OpenAI 호환 API 프록시를 위한 LiteLLM 통합
  * OpenShift 연동을 지원하는 OAuth2/JWT 인증
* **LiteLLM** — 여러 모델 백엔드에 단일 API를 제공하는 OpenAI 호환 프록시
* **PostgreSQL** — 사용자, API 키, 사용량 데이터, 감사 로그를 저장하는 데이터베이스
* **OpenShift OAuth** — 사용자 등록을 간소화하는 엔터프라이즈 인증 통합
* **HTTP 클라이언트** — API 호출에 사용하는 curl, Postman, Python `requests`
