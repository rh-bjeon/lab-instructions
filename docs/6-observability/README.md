# Module 6 - The AI Watcher

> observability 없이 프로덕션에서 AI를 운영하는 것은 눈을 가리고 어두운 교실에서 수업을 하는 것과 같습니다. 학생들이 배우고 있는지, 혼란스러워하는지, 아니면 이미 교실을 떠났는지조차 알 수 없습니다. 이제 Canopy가 건강하고 신뢰할 수 있는 상태를 유지하기 위해 필요한 바이탈 사인과 instrumentation(계측)을 갖춰줍시다 📊

# 🧑‍🍳 Module Intro

여러분은 요약(summarization)과 RAG 기능을 갖춘 Canopy를 구축했지만, 그것이 실제로 프로덕션에서 잘 동작하고 있는지 어떻게 알 수 있을까요? 이 모듈에서는 AI 애플리케이션을 블랙박스에서 신뢰할 수 있고 모니터링 가능한 투명한 시스템으로 바꿔주는 observability의 세 가지 기둥을 소개합니다.

여러분은 OpenShift AI의 내장 observability 스택을 사용하는 방법을 배웁니다. 성능을 정량화하는 metrics, 동작을 이해하는 logs, 분산 시스템을 거치는 요청을 따라가는 traces입니다. 또한 사용자 피드백으로 루프를 닫는 방법도 배웁니다. 좋아요/싫어요 신호를 수집하고, 부정적인 피드백을 평가 테스트 케이스로 전환하고, A/B 테스트를 사용해 프롬프트를 나란히 비교함으로써 데이터 기반의 프롬프트 엔지니어링 의사결정을 내릴 수 있게 됩니다. 이 모듈이 끝나면, Canopy의 상태를 한눈에 보여주는 대시보드, 피드백 기반 개선 사이클, 그리고 문제를 빠르게 디버깅할 수 있는 역량을 갖추게 됩니다.

# 🖼️ Big Picture
![big-picture-observability](images/big-picture-monitoring.jpg)

# 🔮 Learning Outcomes

* observability의 세 가지 기둥을 이해하고, 이것이 프로덕션 AI 시스템에 왜 필수적인지 설명할 수 있습니다.
* OpenTelemetry, Prometheus, MLflow를 사용해 OpenShift AI의 observability 스택을 배포 및 구성할 수 있습니다.
* PromQL을 사용해 메트릭을 조회하여 Canopy의 성능과 리소스 사용량을 모니터링할 수 있습니다.
* AI 특화 메트릭과 시스템 상태를 시각화하기 위한 커스텀 Grafana 대시보드를 생성할 수 있습니다.
* OpenShift의 로깅 스택을 사용해 로그를 분석하여 문제를 디버깅하고 사용자 상호작용을 이해할 수 있습니다.
* 요청을 추적하여 병목과 지연 원인을 파악할 수 있습니다.
* 사용자 피드백을 수집하고 부정적인 신호를 평가 데이터셋으로 내보내 프롬프트를 체계적으로 개선할 수 있습니다.
* A/B 테스트를 사용해 프롬프트 변형을 나란히 비교하고 승리한 쪽을 승격시킬 수 있습니다.

# 🔨 Tools used in this module

* **OpenTelemetry Collector (OTel)**: AI 워크로드로부터 텔레메트리 데이터를 수집하기 위한 벤더 중립적 표준
* **Prometheus**: 메트릭을 저장하고 알림을 구동하는 시계열 데이터베이스
* **Grafana**: 메트릭을 실행 가능한 대시보드로 바꿔주는 시각화 플랫폼
* **LokiStack**: OpenShift와 통합된 확장 가능한 로그 수집 시스템
* **OpenShift User Workload Monitoring**: 커스텀 애플리케이션 메트릭과 모델 성능을 추적하기 위한 사전 구성된 모니터링 스택
