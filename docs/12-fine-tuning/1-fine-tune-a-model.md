# 🎯 Fine-tuning

AI 커스터마이징 도구에는 세 가지가 있습니다: **프롬프트 엔지니어링(prompt engineering)**, **컨텍스트 엔지니어링(context engineering)**(RAG 같은 것), 그리고 **파인튜닝(fine-tuning)**입니다.  
지금까지 프롬프트 엔지니어링과 컨텍스트를 활용해서 모델 응답을 개선하고, 다른 것들과 함께 응답을 그라운딩(grounding)하는 방법을 살펴봤습니다.

그럼 파인튜닝은 어디에 쓰일까요?  
단순히 프롬프트를 개선하거나 컨텍스트를 추가하는 것보다 파인튜닝이 더 잘하는 몇 가지가 있습니다:

- 모델이 일관된 *행동(behavior)*을 보여야 할 때
- 모델이 도메인 전문 용어를 알아야 할 때
- 프롬프트가 너무 길어질 때

## 📚 소크라테스식 튜터(Socratic Tutor) 사용 사례

Canopy를 개선하기 위해, 우리는 Canopy가 소크라테스식 튜터처럼 행동해서, 학생들에게 정답을 바로 알려주지 않고 영리한 후속 질문으로 정답을 스스로 찾아가도록 유도하는 기능을 추가하고자 합니다. 이를 위해서는 꽤 긴 프롬프트가 필요하고 그만큼 깨지기 쉬워지기 때문에, 대신 이 행동을 모델에 파인튜닝하기로 결정합니다.

프롬프트는 대략 이런 모습이 될 것입니다.

```
You are a Socratic math tutor for Redwood Digital University...
CORE BEHAVIORS: Never give the final answer immediately...
FORBIDDEN BEHAVIORS: Do not solve the problem for them...
EXAMPLE INTERACTIONS: [Student]: How do I solve 2x + 5 = 13?...
```

**파인튜닝이 어떻게 도움이 될까요?**


| 문제점 | 파인튜닝이 돕는 방식 |
|-----------|----------------------|
| 800토큰짜리 시스템 프롬프트 | 약 10토큰으로 축소 |
| 탈옥(jailbreak) 취약점 | 행동이 제안이 아니라 가중치(weights)에 담김 |
| 일관되지 않은 응답 | 수백 개의 예제로부터 학습 |
| 요청당 토큰 비용 | 입력 토큰 72% 절감 |
| 지연 시간(latency) | 토큰이 적을수록 첫 토큰까지의 시간이 빨라짐 |

그래서 파인튜닝 후에는 이렇게만 말하면 됩니다.

```
You are Canopy, RDU's math tutor.
```

다시 말해, 소크라테스식 행동이 *가중치 안에* 들어있게 되는 것입니다.


## 사전 설정

시작하기 전에, 워크벤치(Workbench)에 메모리를 좀 더 할당해 줘야 합니다.

1. OpenShift AI Dashboard -> <USER_NAME>-canopy 프로젝트 -> Workbenches로 이동합니다.
![userx-project](images/userx-project.png)

2. ⋮를 클릭한 다음 `Edit workbench`를 눌러서 워크벤치를 편집합니다.
![edit-workbench](images/edit-workbench.png)

3. 마지막으로 `Deployment size`로 스크롤을 내려서 `Memory requests`와 `Memory limits`를 각각 8GB로 변경한 다음 `Update workbench`를 클릭합니다.
![set-memory](images/set-memory.png)

이제 노트북을 실행할 준비가 끝났습니다!

## 튜닝은 데이터를 먹습니다 🐟

모델 튜닝을 시작하기 전에 데이터가 필요합니다(소크라테스식 튜터를 위해서는 최소 500~1000개 이상의 예제가 필요합니다).  
안타깝게도 좋은 데이터는 구하기가 꽤 어렵고, 보통 매우 수작업이 많이 들어가는 일입니다.  
다행히 이제는 기존 데이터를 보완할 수 있는 합성 데이터 생성 기법들이 존재합니다.

이러한 접근 방식을 **합성 데이터 생성(Synthetic Data Generation)**이라고 부릅니다.

직접 시도해 보려면, 워크벤치로 가서 **`experiments/12-fine-tuning/1-synthetic-data-generation.ipynb`**를 열고 안내를 따라가세요.

## 이제 파인튜닝을 해봅시다!

합성 데이터 생성이 어떻게 동작하는지 살펴봤습니다. 이제 실제로 모델이 소크라테스식 튜터가 되도록 학습시켜 봅시다.

우리는 LoRA(Low Rank Adaptation, 저랭크 적응)를 사용해서 모델을 파인튜닝합니다. LoRA는 모델의 작은 일부분만 영리하게 업데이트하기 때문에, 전체 학습(full training)보다 훨씬 빠르고 비용 효율적이면서도 좋은 결과를 얻을 수 있습니다.

다시 워크벤치로 돌아가서 **`experiments/12-fine-tuning/2-lora-training.ipynb`**를 실행해서 작은 모델을 파인튜닝하세요!

## 평가 및 저장

Canopy를 업데이트할 때 사용하는 표준 온라인 평가도 물론 진행하지만, 여기서는 모델이 배포되기 전에 기존 모델보다 더 나은지 간단히 확인하는 차원에서 오프라인 평가도 함께 수행합니다.

다만 모델을 저장하기 전에, 워크벤치에서 클러스터에 로그인되어 있는지 먼저 확인해야 합니다.  
노트북 `4-save-model.ipynb`를 진행하기 전에 워크벤치 터미널에서 다음을 실행하세요.

  ```bash
    export CLUSTER_DOMAIN=<CLUSTER_DOMAIN>
    oc login --server=https://api.${CLUSTER_DOMAIN##apps.}:6443 -u <USER_NAME> -p <PASSWORD>
  ```

새 모델을 평가하려면 **`experiments/12-fine-tuning/3-evaluation.ipynb`** 노트북을 진행한 다음, **`experiments/12-fine-tuning/4-save-model.ipynb`**로 가서 모델을 저장하고 모델 레지스트리(model registry)에 푸시하세요.
