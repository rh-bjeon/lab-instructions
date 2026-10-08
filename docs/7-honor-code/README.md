# Module 7 - The Honor Code

> 신뢰할 수 있는 AI를 만든다는 것은 경계를 설정하는 것을 의미합니다. 훌륭한 선생님이 교실 규칙을 세우는 것처럼, guardrails는 AI가 도움이 되고, 해롭지 않고, 정직한 상태를 유지하도록 보장합니다 🛡️

# 🧑‍🍳 Module Intro

이 모듈에서는 AI 애플리케이션을 위한 안전 guardrails를 구현하는 핵심적인 실천 방법을 소개합니다. 교육용 AI 어시스턴트를 오용으로부터 보호하고, 책임감 있는 상호작용을 보장하며, 단순한 prompt engineering을 넘어서는 레이어드(layered) 보안을 구축하는 방법을 배웁니다. 기본적인 시스템 프롬프트부터 정교한 탐지 시스템까지, AI의 능력과 안전성 및 컴플라이언스 사이의 균형을 맞추는 방법을 알아봅니다.

RDU에서는 Canopy를 신뢰할 수 있는 교육 도구로 구축하는 데 전념하고 있습니다. Guardrails는 강력한 언어 모델을 학생과 교육자가 학업 윤리, 편향, 유해 콘텐츠에 대한 걱정 없이 믿고 사용할 수 있는 책임감 있는 어시스턴트로 바꿔주는 핵심 요소입니다.

# 🖼️ Big Picture
![big-picture-guardrails.png](images/big-picture-guardrails.jpg)

# 🔮 Learning Outcomes

* guardrails가 무엇인지, 그리고 프로덕션 AI 애플리케이션에 왜 필수적인지 이해합니다.
* prompt-level guardrails의 한계와 왜 외부 강제(enforcement)가 필요한지 배웁니다.
* Helm chart를 사용해 다층적인 안전성을 위한 NeMo Guardrails를 배포하고 구성합니다.
* 서로 다른 detector들이 각기 다른 유형의 문제가 되는 콘텐츠를 어떻게 잡아내는지 체험합니다.
* 안전 조치를 우회하려는 창의적인 시도에 대해 AI 애플리케이션을 테스트하고 강화합니다.

# 🔨 Tools used in this module

* **NeMo Guardrails**: Colang으로 정의된 안전 rail을 적용하는 외부 정책 계층
* **Regex Rules**: 특정 콘텐츠 패턴을 차단하거나 플래그하기 위한 패턴 기반 필터
* **HAP Detector**: 혐오 발언, 욕설, 비속어를 탐지하는 분류기(Granite Guardian)
* **Prompt Injection Detector**: AI의 동작을 조작하려는 시도를 식별하는 보안 계층(DeBERTa)
* **Language Detector**: 응답이 영어로 유지되도록 보장(Lingua)
* **Spikee**: guardrails를 벤치마킹하기 위한 오픈소스 자동화된 prompt injection 테스트 도구
* **OpenShift & Helm Charts**: 개발 및 프로덕션 환경에 NeMo Guardrails 인프라를 배포하기 위한 도구
