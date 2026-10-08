# Module 3 - Ready to Scale 101

> 확장 가능한 아키텍처, MLflow, GitOps 사례를 도입하여 AI 어시스턴트를 프로덕션 준비 상태로 만들어 보세요.

# 🧑‍🍳 모듈 소개

이 모듈에서는 Canopy가 OpenAI 호환 API를 사용하여 모델과 상호작용하는 방식을 더 깊이 다루고, 프롬프트 관리를 위한 MLflow를 소개합니다. 이와 함께 백엔드 구성 요소와 GitOps 사례를 도입하여, 우리가 구축하는 모든 것이 신뢰할 수 있고 반복 가능하며 실제 사용자를 맞이할 준비가 되도록 합니다.

# 🖼️ 전체 그림
![big-picture-gitops](./images/big-picture-gitops.jpg)

# 🔮 학습 목표
* OpenAI 호환 API를 사용하여 모델과 상호작용하는 방법 이해하기
* MLflow를 사용하여 프롬프트를 관리하고 모델 상호작용을 추적하기
* LLM과의 구조화된 상호작용을 지원하는 백엔드 구성 요소 추가하기
* 일관성과 확장성을 위해 GitOps를 사용하여 전체 시스템을 테스트 및 프로덕션 환경에 배포하기

# 🔨 이 모듈에서 사용하는 도구
* [OpenAI Python SDK](https://github.com/openai/openai-python) - OpenAI 호환 모델 엔드포인트와 상호작용하기 위한 표준 클라이언트
* [MLflow](https://mlflow.org/) - AI 애플리케이션을 디버깅, 평가, 모니터링, 최적화할 수 있는 기능을 제공
* [Helm](https://helm.sh/) - Kubernetes 애플리케이션을 정의, 설치, 업그레이드할 수 있도록 도와줌
* [Argo CD](https://argoproj.github.io/cd/) - 애플리케이션을 지속적으로 모니터링하고 현재 상태를 원하는 상태와 비교하는 컨트롤러
