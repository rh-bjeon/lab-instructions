# Module 9 - On-Prem Practicum

> 학생들의 성적과 개인정보가 대화에 등장하는 순간, 클라우드는 컴플라이언스의 지뢰밭이 됩니다. 때로는 모든 것을 사내(in-house)에 두는 것이 가장 안전한 길입니다. LLM을 on-prem으로 가져와 봅시다 🏠

# 🧑‍🍳 모듈 소개

RDU는 성적, 학업 기록, 개인화된 튜터링 상호작용 등 학생 관련 기밀 데이터를 처리할 수 있도록 Canopy를 확장하고 있습니다. FERPA와 같은 규제와 기관의 보안 정책을 고려하면, 이 데이터를 외부 클라우드 제공업체와 공유하는 것은 선택지가 아닙니다. 해결책은? 자체적으로 LLM을 on-prem으로 운영하는 것입니다.

이 모듈에서는 vLLM을 사용해 OpenShift 클러스터에 직접 모델을 배포하는 방법을 안내합니다. 하드웨어 제약 조건에 따라 모델을 평가하는 방법, 모델을 로컬에서 서빙하는 방법, 그리고 이러한 self-hosted 엔드포인트를 사용하도록 Llama Stack과 Canopy 설정을 업데이트하는 방법을 배우게 됩니다. 이 모듈을 마칠 때면, 민감한 데이터를 정확히 있어야 할 곳 - 바로 여러분 자신의 인프라 - 에 그대로 유지하는 완전히 동작하는 on-prem AI 스택을 갖추게 될 것입니다.

# 🖼️ 큰 그림
![big-picture-onprem.jpg](images/big-picture-onprem.jpg)

# 🔮 학습 목표

* 클라우드 엔드포인트 대신 언제, 왜 LLM을 on-premise로 배포해야 하는지 이해합니다
* model card를 읽는 방법과 특정 하드웨어 제약 조건에 맞춰 모델을 평가하는 방법을 학습합니다
* Red Hat OpenShift AI에서 vLLM 서빙 런타임을 사용해 LLM을 배포합니다
* 로컬에 호스팅된 모델 엔드포인트를 사용하도록 Llama Stack을 구성합니다
* on-prem 모델과 상호작용하도록 Canopy를 업데이트합니다
* 성능 특성을 비교합니다

# 🔨 이 모듈에서 사용하는 도구

* **[vLLM](https://docs.vllm.ai/en/latest/)**: CPU와 GPU 배포를 모두 지원하는 고처리량(high-throughput) LLM 서빙 엔진
* **[KServe](https://kserve.github.io/website/)**: OpenShift AI와 통합된 Kubernetes 네이티브 모델 서빙 플랫폼
* **[TinyLlama](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)**: CPU 추론에 최적화된 1.1B 파라미터 소형 모델
* **[Llama 3.2 3B](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)**: 더 큰 모델의 역량과 비교하기 위한 instruction-tuned 모델
* **OpenShift AI Model Serving**: 모델 엔드포인트를 배포하고 관리하기 위한 엔터프라이즈 플랫폼
  