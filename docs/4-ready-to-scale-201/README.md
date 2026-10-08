# Module 4 - Ready to Scale 201

> 프롬프트 버전 관리, 평가 프레임워크, 자동화된 파이프라인을 통해 AI 애플리케이션을 배포 단계에서 프로덕션급 품질로 끌어올리세요.

# 🧑‍🍳 모듈 소개

이 모듈은 필수적인 프로덕션 사례들을 소개하여 여러분의 GenAI 애플리케이션을 한 단계 더 발전시킵니다. 프롬프트를 체계적으로 버전 관리하고 추적하는 방법, 자동화된 프레임워크를 사용하여 애플리케이션 품질을 평가하는 방법, 그리고 AI 시스템이 확장되더라도 신뢰성과 성능을 유지할 수 있도록 하는 CI/CD 파이프라인을 구축하는 방법을 배우게 됩니다.

# 🖼️ 전체 그림
![big-picture-evals](images/big-picture-evals.jpg)

# 🔮 학습 목표

* Git과 GitOps 사례를 사용하여 프롬프트를 코드처럼 버전 관리하는 방법 배우기
* GenAI 애플리케이션에 대한 평가 전략을 이해하고 자동화된 테스트 구현하기
* Kubeflow를 사용하여 애플리케이션 품질을 체계적으로 측정하는 평가 파이프라인 구축하기
* Tekton을 사용하여 지속적 통합 및 배포를 위한 평가 워크플로우 자동화하기

# 🔨 이 모듈에서 사용하는 도구

* [GuideLLM](https://github.com/neuralmagic/guidellm) - LLM의 처리량(throughput)과 지연 시간(latency)을 측정하기 위한 성능 테스트 도구
* [MLflow](https://mlflow.org/) - AI 애플리케이션을 디버깅, 평가, 모니터링, 최적화할 수 있는 기능을 제공

* [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/) - 머신러닝 워크플로우를 구축하고 오케스트레이션하기 위한 플랫폼
* [Tekton](https://tekton.dev/) - 빌드, 테스트, 배포 파이프라인 자동화를 위한 클라우드 네이티브 CI/CD 프레임워크
