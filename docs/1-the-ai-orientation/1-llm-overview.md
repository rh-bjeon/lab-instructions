# LLM 이해하기: 심층 분석

Canopy에서는 어시스턴트가 빠르고 자연스럽게 느껴지지만, 그 뒤에서는 실제로 무슨 일이 일어나고 있을까요? 이 가이드는 여러분이 대화를 나누는 동안 대형 언어 모델(LLM)이 작동하도록 만드는 핵심 메커니즘을 자세히 설명합니다.

실제 배포 환경에서 가장 중요한 개념들을 중심으로 다루겠습니다.

아래 목차를 이용해 특정 주제를 살펴보거나 다시 복습하고 싶은 부분을 찾아보세요.

## 가이드 구성

이 가이드는 네 개의 주요 섹션으로 구성되어 있습니다.

1. [🧱 LLM 기본 개념](1-the-ai-orientation/1a-llm-fundamentals.md)
   - 토큰(token) 이해하기
   - LLM이 상태를 유지하는 방법
   - 다음 토큰 예측 과정
  
2. [💭 LLM 사용 및 제어](1-the-ai-orientation/1b-llm-usage-control.md)
   - 프롬프팅 기법
   - 환각(hallucination) 다루기
   - 가드레일(guardrail) 구현

3. [🧠 메모리와 처리 과정](1-the-ai-orientation/1c-llm-memory-processing.md)
   - 어텐션(attention) 메커니즘
   - 컨텍스트 윈도우(context window)
   - KV 캐시 최적화

4. [📊 성능과 하드웨어](1-the-ai-orientation/1d-llm-performance.md)
   - 주요 성능 지표
   - 모델 크기와 요구 사항
   - 하드웨어 고려 사항


## 🎯 학습 목표

이 가이드를 모두 마치면 다음을 이해하게 됩니다.

- LLM이 텍스트를 처리하고 생성하는 방법
- LLM 성능에 영향을 주는 주요 요인
- 배포 시 고려해야 할 하드웨어 사항
</content>
