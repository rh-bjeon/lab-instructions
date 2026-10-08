# Agentic Workflows

## 도구에서 agent로

LLM이 도구를 사용하는 방법을 보셨습니다 - 요청을 이해하고, 도구 호출을 구성하고, 결과를 해석합니다. 그런데 LLM이 여러 도구를 *연속으로* 사용해야 한다면 어떨까요? 또는 어떤 도구를 사용할지 *추론(reason)*해야 한다면요?

바로 이때 **agentic workflows**(에이전틱 워크플로)가 등장합니다.

"도구 A를 호출한 다음 도구 B를 호출하라"고 하드코딩하는 대신, LLM이 올바른 작업 순서를 스스로 파악할 수 있는 자율성을 부여합니다.

## ReAct: Reasoning + Acting (추론 + 행동)

가장 흔한 agentic 패턴은 **ReAct**(Reasoning and Acting)입니다. 단순하지만 강력합니다.

1. **Thought(사고)**: LLM이 자신이 생각하고 있는 바를 설명합니다
2. **Action(행동)**: LLM이 도구를 호출합니다
3. **Observation(관찰)**: 도구가 결과를 반환합니다
4. **Repeat(반복)**: 작업이 완료될 때까지 반복합니다

이 패턴은 LLM이 행동하기 전에 "소리 내어 생각하게" 만들면 의사결정이 개선된다는 연구 결과에서 비롯되었습니다. 모델이 자신의 추론 과정을 명확히 표현하도록 강제하면, 더 나은 도구 선택을 하게 되고 스스로의 실수도 포착하게 됩니다.

실제로 어떻게 동작하는지 확인해 봅시다!

워크벤치로 이동해서 **`experiments/8-agents/3-agentic-workflows.ipynb`**를 열고, 해당 실습을 마친 후 다시 여기로 돌아오세요.


<!-- ## Beyond ReAct

ReAct is just the beginning. Other agentic patterns include:

- **Plan-and-Execute**: Create a full plan upfront, then execute each step
- **Tree of Thoughts**: Explore multiple reasoning paths in parallel
- **Reflection**: Agent critiques its own work and improves
- **Multi-Agent Systems**: Multiple specialized agents collaborate

These patterns are covered in the lecture slides, but the core principles remain the same: give LLMs tools, autonomy, and a reasoning framework. -->
