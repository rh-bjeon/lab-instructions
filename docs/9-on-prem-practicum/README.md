# 모듈 9 - 온프레미스 실습

> 학생의 성적과 개인 정보가 대화에 포함되면 클라우드 사용에는 복잡한 규정 준수 문제가 따릅니다. 이런 경우에는 데이터를 조직 내부에 두는 것이 가장 안전할 수 있습니다. LLM을 온프레미스 환경에 배포해 보겠습니다. 🏠

# 🧑‍🍳 모듈 소개

RDU는 성적과 학업 기록, 개인화된 학습 상담처럼 학생과 관련된 민감한 데이터를 처리하도록 Canopy를 확장하고 있습니다. FERPA 같은 규정과 기관의 보안 정책 때문에 이러한 데이터를 외부 클라우드 사업자와 공유할 수 없는 경우가 있습니다. 이때 자체 인프라에서 LLM을 운영하는 온프레미스 배포가 해법이 될 수 있습니다.

이 모듈에서는 vLLM을 사용해 OpenShift 클러스터에 모델을 직접 배포합니다. 하드웨어 제약을 고려해 모델을 선택하고 로컬에서 서빙하며, 자체 호스팅 엔드포인트를 사용하도록 Llama Stack과 Canopy를 구성합니다. 모듈을 마치면 민감한 데이터를 조직의 인프라 안에 유지하는 온프레미스 AI 스택을 구축하게 됩니다.

# 🖼️ 큰 그림

![big-picture-onprem.jpg](images/big-picture-onprem.jpg)

# 🔮 학습 목표

* 클라우드 엔드포인트 대신 LLM을 온프레미스로 배포해야 하는 시점과 이유를 이해합니다.
* 모델 카드(model card)를 읽고 하드웨어 제약에 맞는 모델을 평가하는 방법을 배웁니다.
* Red Hat OpenShift AI에서 vLLM 서빙 런타임으로 LLM을 배포합니다.
* 로컬 모델 엔드포인트를 사용하도록 Llama Stack을 구성합니다.
* 온프레미스 모델과 연동하도록 Canopy를 업데이트합니다.
* 모델별 성능 특성을 비교합니다.

# 🔨 이 모듈에서 사용하는 도구

* **[vLLM](https://docs.vllm.ai/en/latest/)**: CPU와 GPU 배포를 지원하는 고처리량 LLM 서빙 엔진
* **[KServe](https://kserve.github.io/website/)**: OpenShift AI와 통합된 Kubernetes 네이티브 모델 서빙 플랫폼
* **[TinyLlama](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)**: CPU 추론에 적합한 1.1B 파라미터 소형 모델
* **[Llama 3.2 3B](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)**: 대형 모델의 능력과 비교하기 위한 지시 튜닝 모델
* **OpenShift AI Model Serving**: 모델 엔드포인트를 배포하고 관리하는 엔터프라이즈 플랫폼

