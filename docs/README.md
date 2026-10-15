# 🧑‍🏫📚 GenAIOps Enablement 실습 가이드 (AI501)

## 슬라이드
슬라이드는 실습 가이드와 함께 게시됩니다.

👨‍🏫 👉 [여기서 게시된 슬라이드를 볼 수 있습니다](https://rhoai-genaiops.github.io/lab-instructions/slides/ai501-index.html) 👈 🧑‍💻

## 🎯 이 실습의 목적
이 실습은 가상의 대학 "Redwood Digital University(RDU)"를 위한 교육용 AI 어시스턴트 **Canopy**를 직접 만들고 발전시켜 나가면서, GenAI 애플리케이션을 프로토타입에서 프로덕션까지 운영하는 전체 과정(**GenAIOps**)을 손으로 익히는 데 목적이 있습니다.

간단한 프롬프트 실험으로 시작해서, RAG로 지식을 연결하고, observability와 guardrails로 신뢰성과 안전성을 갖추고, 에이전트와 온프레미스 서빙, 모델 최적화, 멀티테넌트 서비스, 파인튜닝까지 — 각 모듈을 거치며 Canopy는 점점 더 프로덕션에 가까운 시스템으로 성장합니다. 모든 실습은 OpenShift와 OpenShift AI 위에서, GitOps 방식으로 배포하고 운영하는 것을 전제로 합니다.

## 🗺️ 실습 모듈 둘러보기
각 모듈 페이지에는 더 자세한 소개, 학습 목표, 사용하는 도구가 정리되어 있습니다. 아래는 전체 흐름을 파악하기 위한 요약입니다.

| # | 모듈 | 무엇을 하나요? |
|---|---|---|
| 1 | [AI 오리엔테이션](1-the-ai-orientation/README.md) | 생성형 AI/LLM의 기본 개념, 프롬프팅, 환각(hallucination)을 이해합니다. |
| 2 | [언어학](2-linguistics/README.md) | 프롬프트 엔지니어링으로 Canopy의 첫 버전을 만들고 배포합니다. |
| 3 | [스케일 준비 101](3-ready-to-scale-101/README.md) | MLflow와 백엔드 구성 요소, GitOps로 Canopy를 프로덕션 준비 상태로 만듭니다. |
| 4 | [스케일 준비 201](4-ready-to-scale-201/README.md) | 프롬프트 버전 관리, 평가 전략, Kubeflow/Tekton 파이프라인으로 품질을 끌어올립니다. |
| 5 | [도서관](5-grounded-ai/README.md) | RAG(Retrieval Augmented Generation)로 Canopy에 문서 기반 지식을 연결합니다. |
| 6 | [AI 감시자](6-observability/README.md) | 메트릭/로그/트레이싱과 피드백 루프로 Canopy의 상태를 관찰합니다. |
| 7 | [명예 규칙](7-honor-code/README.md) | Guardrails로 안전하고 책임감 있는 AI 상호작용을 보장합니다. |
| 8 | [자율 시스템 101](8-agents/README.md) | 도구(tools), MCP 서버, ReAct 패턴으로 자율적인 agent를 구축합니다. |
| 9 | [온프레미스 실습](9-on-prem-practicum/README.md) | vLLM으로 민감한 데이터를 다루는 모델을 자체 인프라에 서빙합니다. |
| 10 | [피트니스 프로그램](10-model-optimization/README.md) | 양자화(quantization)로 모델을 더 작고 빠르고 저렴하게 만듭니다. |
| 11 | [수요와 공급 101](11-maas/README.md) | MaaS(Model as a Service)로 GPU 자원을 여러 팀이 공유하도록 만듭니다. |
| 12 | [튜닝룸](12-fine-tuning/README.md) | 합성 데이터와 LoRA로 긴 시스템 프롬프트의 행동을 모델 자체에 학습시킵니다. |
| 15 | [캠퍼스 설정](15-campus-setup/README.md) | (강사용) 이 실습 전체를 위한 멀티테넌트 클러스터 환경을 구축합니다. |

## 🧰 실습 환경에서 사용하는 주요 도구
모듈마다 사용하는 도구가 조금씩 다르지만, 실습 전반에서 반복해서 만나게 되는 핵심 도구들입니다.

* **[OpenShift](https://www.redhat.com/ko/technologies/cloud-computing/openshift)** — 모든 실습 컴포넌트가 Pod/Deployment/Route로 동작하는 기반 Kubernetes 플랫폼.
* **[OpenShift AI](https://www.redhat.com/ko/technologies/cloud-computing/openshift/openshift-ai)** — 모델 서빙(vLLM), 파이프라인(Kubeflow), observability 등 AI/ML 워크플로우를 위한 OpenShift 확장.
* **[MLflow](https://mlflow.org/)** — 프롬프트와 실험을 추적하고, AI 애플리케이션을 평가·모니터링합니다.
* **[Argo CD](https://argoproj.github.io/cd/)** — Git에 커밋된 상태를 클러스터에 지속적으로 동기화하는 GitOps 컨트롤러.
* **[Helm](https://helm.sh/)** — Kubernetes 애플리케이션을 차트로 패키징하고 설치/업그레이드합니다.
* **[Llama Stack](https://github.com/meta-llama/llama-stack)** — Canopy가 모델과 상호작용하는 방식을 표준화하는 API 레이어.
* **[vLLM](https://docs.vllm.ai/)** — 온프레미스에서 LLM을 고성능으로 서빙하는 엔진.
* **Tekton / Kubeflow Pipelines** — 평가·배포 파이프라인을 자동화하는 CI/CD 도구.
* **Gitea** — 실습에서 소스 코드와 GitOps 매니페스트를 저장하는 자체 Git 서버.
* **Canopy** — 이 실습 전체에서 직접 만들고 발전시켜 나가는, RDU를 위한 예시 교육용 AI 어시스턴트 앱.

## 🦆 작성 규칙
실습을 진행하는 동안, 특히 Notebook에서 값을 바꿔야 하는 부분을 표시해두었습니다. 대부분의 `<PLACEHOLDER>` 값은 자동으로 채워집니다. 혹시 남아있는 값이 있다면 직접 실제 값으로 바꿔주세요. 예를 들어 사용자 이름이 `user1`인데 `<\USER_NAME>`이 보인다면, 아래처럼 바꾸면 됩니다:
    <div class="highlight" style="background: #f7f7f7">
    <pre><code class="language-bash">
    name: &lt;USER_NAME&gt;
    # ^ 이 부분이 아래처럼 바뀝니다
    name: user1
    </code></pre></div>

복사해서 사용할 수 있는 코드 블록이 많이 있습니다. 코드 블록 위에 마우스를 올리면 오른쪽에 ✂️ 아이콘이 나타납니다.

```bash
    echo "like this one :)"
```

**중요:** 모든 코드 블록을 복사해서 실행하는 것은 아닙니다. ✂️ 아이콘이 없는 블록은 **예상 출력 결과**입니다. 여러분의 실행 결과나 YAML을 해당 블록과 비교해 확인하는 용도로 사용하세요.

<!-- customize-section-start -->

## 🪄 가이드 내용 맞춤 설정하기
OpenShift 상에 배포된 환경이라면 Deployment의 환경변수(`user`, `password`, `openshift_cluster_ingress_domain`, `gitea_console_url`)로 이미 아래 값들이 채워져 있으므로 이 섹션은 필요하지 않습니다. 로컬에서 미리보기하거나 직접 값을 채워야 하는 경우에만 아래를 따라하세요.

페이지 상단의 입력창을 이용하면 여러분 팀의 값을 미리 채운 상태로 문서를 볼 수 있습니다. 아래 항목을 입력하고 **저장** 버튼을 누르세요:

1. **사용자 이름** — 예: `user1`. 이 값은 우리가 사용하는 네임스페이스 등의 접두사로 쓰입니다.
2. **비밀번호** — 여러분의 실습 비밀번호.
3. **클러스터 도메인** — OpenShift 도메인 중 `apps.*` 부분(아래 설명 참고).

입력한 값은 브라우저의 로컬 스토리지에 저장됩니다. 저장된 값을 모두 초기화하려면 **초기화** 버튼을 누르세요.

* 저장한 뒤에는 아래와 같이 사용자 이름과 비밀번호가 보여야 합니다:

    ```bash
    <USER_NAME>
    <PASSWORD>
    ```

* 클러스터 도메인에는 OpenShift 도메인 중 `apps.*` 부분만 입력하세요. 예를 들어 콘솔 주소가 <code class="language-yaml">https://console-openshift-console.apps.hivec.sandbox1243.opentlc.com/</code> 라면
 클러스터 도메인 입력창에는 `apps.hivec.sandbox1243.opentlc.com`을 입력하면 됩니다.

    아래와 같이 클러스터 도메인이 보여야 합니다:

    ```bash
    <CLUSTER_DOMAIN>
    ```

<!-- customize-section-end -->

자, 이제 시작해봅시다! 첫 번째 챕터로 이동해서 GenAIOps 여정을 시작하세요! 🏃💨
