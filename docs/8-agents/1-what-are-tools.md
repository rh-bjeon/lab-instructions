# 도구(tools)란 무엇인가?

## 도구의 기본 개념

방금 플레이그라운드에서 직접 체험해 보셨습니다: 모델이 잠시 멈추고, weather 도구를 호출한 뒤, 추측 대신 실제 데이터를 반환했습니다. 그런데 이게 내부적으로 실제로는 어떻게 동작하는 걸까요?

**도구**(tool)란 LLM이 상호작용할 수 있도록 간단한 JSON 인터페이스로 감싼 모든 서비스를 말합니다 — 계산기, 데이터베이스, ERP 시스템, 날씨 API 등 무엇이든 가능합니다. LLM은 **코디네이터(coordinator)** 역할을 합니다. 즉, 어떤 도구를 호출할지와 그 결과를 어떻게 해석할지를 결정합니다. 실제 실행은 모델 자체가 아니라, 주변 애플리케이션, 런타임, 또는 백엔드 시스템이 처리합니다.

이제 그 메커니즘을 자세히 살펴봅시다.

워크벤치로 이동해서 다음 노트북을 끝까지 실행해 보세요: **`experiments/8-agents/1-intro-to-tools.ipynb`**

## MCP 서버

도구가 실제로 어떻게 동작하는지 확인했으니, 이제 규모를 키워 봅시다!

**MCP(Model Context Protocol) 서버**는 원격 또는 로컬에서 호출할 수 있는 도구들의 모음입니다. 도구를 하나씩 정의하는 대신, MCP 서버는 기능 전체 모음(suite)을 제공합니다 — 단일 도구가 아니라 하나의 도구 상자와 같은 셈이죠.

MCP 서버를 사용하기 전에, 먼저 하나를 배포해야 합니다. 바로 시작해 봅시다!

1. 이전과 마찬가지로 OpenShift UI -> Helm -> Releases로 이동해서 Create Helm Release를 클릭하세요.

    ![helm-release.png](./images/helm-release.png)


2. 왼쪽 메뉴에서 `Canopy Helm Charts`를 선택한 뒤 Canopy MCP Calendar를 클릭하세요.

    ![helm-calender.png](./images/helm-calender.png)

3. 여기서는 아무것도 변경할 필요가 없으니 바로 `Create`를 클릭하세요.

    ![helm-calender-2.png](./images/helm-calender-2.png)

4. 모든 것이 배포되고 나면, [Calendar website](https://canopy-mcp-calendar-frontend-<USER_NAME>-canopy.<CLUSTER_DOMAIN>)에 접속할 수 있습니다. 동그라미들이 모두 파란색 🔵이 되면 작은 화살표를 클릭해서 어떤 모습인지 확인해 보세요.

    ![helm-calender-3.png](./images/helm-calender-3.png)

    다음과 같은 모습을 보게 될 것입니다.

    ![calender-app.png](./images/calender-app.png)

5. 워크벤치로 이동해서 **`experiments/8-agents/2-mcp-servers.ipynb`** 노트북을 열어 MCP 서버와 그 도구들을 어떻게 사용하는지 확인하세요. 완료되면 다시 여기로 돌아오세요!

도구가 무엇인지, 어떻게 동작하는지, 그리고 어떻게 사용하는지 알게 되었으니, 이제 더욱 강력한 agent를 만드는 방법을 살펴봅시다.
