# NeMo Guardrails

NeMo Guardrails는 모델을 감싸는 외부 정책 계층(policy layer)을 제공합니다. LLM이 규칙을 따르기를 바라는 대신, NeMo는 규칙을 **강제**합니다. 모든 요청이 LLM에 도달하기 전에, 그리고 모든 응답이 사용자에게 전달되기 전에 이를 가로채어 구성 가능한 rail들을 거치게 합니다.

Canopy를 위해 구성한 rail들은 다음과 같습니다.

| Rail | 무엇을 잡아내는가 |
|------|----------------|
| **Regex** | 알려진 금지 패턴(Fight Club 🥊 외 다수) |
| **HAP Detector** | 혐오 발언, 욕설, 비속어(Hate speech, Abuse, Profanity) |
| **Prompt Injection Detector** | 모델을 탈취하거나 조작하려는 시도 |
| **Language Detector** | 영어가 아닌 입력 |
| **PII Detection** | 이메일, 전화번호, 신용카드 번호, 주민등록번호(SSN) 등 |
| **LLM-as-Judge** | 다른 레이어를 통과한 모호한 내용 전부 |

규칙 자체는 입력과 출력 흐름을 정의하는 간단한 도메인 특화 언어인 **Colang**으로 작성됩니다. 이 모듈에서 Colang을 깊이 알 필요는 없지만, 이제 배포할 Helm chart 안에 Colang이 들어 있다는 것은 알아두면 좋습니다.

## NeMo Guardrails 배포하기

1. `<USER_NAME>-canopy` 환경에서 **Helm > Releases > Create Helm Release**로 이동해 `GenAIOps Helm Charts`를 선택한 다음 `NeMo Guardrails Orchestrator` 차트를 찾습니다.

    ![nemo-guardrails-helm.png](./images/nemo-guardrails-helm.png)

    값을 변경할 필요는 없습니다. 그냥 **Create**를 누르세요!

2. NeMo 서비스가 올라오기를 기다립니다. HAP detector(Granite Guardian), prompt injection detector(DeBERTa), Lingua language detector는 이미 배포되어 있습니다. Topology 뷰를 확인하세요. 모든 것이 초록색이어야 합니다 💚

## Guardrails 체험하기

이제 rail들이 실제로 동작하는 모습을 살펴봅시다. workbench로 이동해 다음을 엽니다.

```
experiments/7-guardrails/1-intro-to-guardrails.ipynb
```

이 노트북은 다양한 종류의 프롬프트를 NeMo 엔드포인트로 보내보고 서로 다른 rail들이 어떻게 작동하는지 살펴보도록 안내합니다. 끝나면 여기로 돌아와서 Canopy에 연결해 봅시다!
