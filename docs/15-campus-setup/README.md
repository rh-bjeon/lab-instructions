# Exercise 12 - Campus Setup

## 👨‍🏫 실습 소개

이번 실습에서는 GenAIOps 랩 환경을 구축하는 데 필요한 단계를 살펴봅니다. 이는 다른 모든 실습을 위해 클러스터를 준비하는, 강사가 수행하는 뒷단 준비 작업입니다.

## 🖼️ 전체 그림

이 설정 과정은 OpenShift 위에 완전한 멀티테넌트 AI/ML 학습 환경을 배포하여, 학생들이 대규모 언어 모델(LLM), 프롬프트 엔지니어링, 모델 최적화, AI 거버넌스를 직접 실습해 볼 수 있도록 합니다.

![big-picture-campus-setup](./images/big-picture-campus-setup.jpg)

## 🔮 학습 목표

- [ ] Helm을 이용해 GenAIOps 랩 인프라를 배포할 수 있다
- [ ] 랩 환경을 구성하는 요소들을 이해한다
- [ ] 학생 환경과 인증을 구성할 수 있다
- [ ] 모델 서빙을 위한 GPU 노드를 프로비저닝할 수 있다

## 🔨 이 실습에서 사용하는 도구!

* OpenShift 4.19+
* <span style="color:blue;">[Helm](https://helm.sh/)</span> - Kubernetes 애플리케이션을 정의, 설치, 업그레이드하는 데 도움을 주는 도구
* <span style="color:blue;">[oc CLI](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)</span> - OpenShift 명령줄 도구
