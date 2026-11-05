# 플레이그라운드에서 Agent 체험하기

LLM은 학습 데이터에 포함된 내용만 알고 있으며 스스로 외부 시스템에 접근하지 못합니다. **도구**(tool)를 연결하면 실시간 데이터를 조회하고 API를 호출하며 계산을 수행할 수 있습니다.

코드를 살펴보기 전에, 먼저 실제로 동작하는 모습을 확인해 봅시다!

1. 플레이그라운드에 **weather MCP server**(날씨 MCP 서버)를 연결해 두었습니다. 이를 통해 모델은 추측 대신 실시간 날씨 데이터를 가져올 수 있습니다.

   OpenShift AI Dashboard > Gen AI studio > AI asset endpoints > `MCP Servers`에서 이 서버가 사용 가능하게 등록되어 있는 것을 확인할 수 있습니다.

2. OpenShift AI Dashboard > Gen AI studio > Playground 으로 이동해서, 프로젝트가 `<USER_NAME>-canopy`로 선택되어 있는지 확인하세요.


3. 모델이 평소에는 정확히 답할 수 없는 질문을 해 보세요.

    ```
    What is the weather like in Raleigh right now?
    ```

    도구가 없다면, 모델은 답을 거부하거나 그냥 지어낸 내용을 말할 것입니다.

4. 이제 `MCP` 섹션에서 `Weather MCP Server` 체크박스를 선택해 활성화하세요.

    ![playground-weather-mcp.png](./images/playground-weather-mcp.png)

5. 모델이 **잠시 멈추고 생각하는** 모습을 확인할 수 있습니다. 바로 그 순간 날씨 도구에 대한 호출이 일어나고 있으며, 그 후 실제 현재 데이터를 반영한 응답을 받게 됩니다 — 환각(hallucination)이 아닙니다.

    원한다면 다른 도시들로도 몇 번 더 시도해 보세요. 모델이 도구를 사용할 *시점*과 응답을 *표현하는 방식*을 어떻게 결정하는지 살펴보세요.

    (아쉽게도 이 MCP 서버는 미국 도시에 대해서만 데이터를 가져올 수 있습니다 🙈)

핵심은 역할의 분리입니다. LLM은 어떤 도구를 언제 사용할지 결정하고, 백엔드는 실제 호출을 실행해 결과를 모델에 돌려줍니다. 모델 자체가 외부 시스템을 직접 호출하는 것은 아닙니다.

이제 이것이 실제로 어떻게 동작하는지 내부 구조를 살펴봅시다 — **What are tools?**(도구란 무엇인가?)로 계속 진행하세요.
