# 📊 평가(Evaluation): 동작한다는 것을 증명하기

모델을 압축했습니다. 감으로는 괜찮아 보입니다.

하지만 프로덕션에서는 "감"이 통하지 않습니다. 숫자가 필요합니다. 벤치마크가 필요합니다. *증거*가 필요합니다.

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)가 등장합니다—HuggingFace의 Open LLM Leaderboard를 구동하는 바로 그 도구입니다. NVIDIA와 Cohere에게 충분히 좋은 도구라면, 우리에게도 충분히 좋을 것입니다.

## 2단계 테스트 철학

양자화된 모델에 대해 알아둘 점이 있습니다: 표준화된 테스트는 우수한 성적으로 통과하면서도, 여러분의 애플리케이션을 이상한 방식으로 망가뜨릴 수 있습니다. 그래서 우리는 두 번 테스트합니다.

| 단계 | 테스트하는 것 | 방법 |
|-------|---------------------|-----|
| **1단계** | 모델이 여전히 *지식*을 가지고 있는가? | 벤치마크(이 섹션) |
| **2단계** | *여러분의* 애플리케이션에서 동작하는가? | Canopy 흐름 테스트(다음 섹션) |

이 섹션에서는 1단계를 다룹니다. 2단계는 Canopy가 양자화된 모델을 사용하도록 업데이트할 때 진행합니다.

## 1단계: 모델이 여전히 지식을 가지고 있는가? 📚

먼저, 압축 과정에서 모델이 "정신"을 잃지 않았는지 확인합니다.

| 테스트할 것 | 왜 중요한가 | 테스트 방법 |
|--------------|----------------|-------------|
| Perplexity(혼잡도) | 기본적인 언어 능력 | lm-evaluation-harness |
| 태스크 벤치마크 | 지식 보존 여부 | MMLU, HellaSwag, GSM8K |
| 여러분의 도메인 | *여러분의* 데이터에 대한 성능 | 커스텀 평가 세트 |

### Perplexity: 기초 건강검진

Perplexity(혼잡도)는 모델이 텍스트에 얼마나 "놀라는지"를 측정합니다. 일련의 단어가 주어졌을 때, 다음에 올 내용을 얼마나 잘 예측하는가입니다.

- **Perplexity가 낮을수록 더 좋은 모델입니다** (실제 텍스트에 덜 놀랍니다)
- **동작 방식:** 모델이 텍스트를 보고 각 단어를 예측합니다. 정답 단어에 높은 확률을 부여하면 perplexity가 낮아집니다.
- **잡아내는 것:** 심각한 압축 손상입니다. 양자화 후 perplexity가 급등하면 뭔가 근본적으로 망가진 것입니다.

독해력 기초 테스트라고 생각하면 됩니다—모델이 흔한 단어 시퀀스를 예측하지 못한다면, 질문에도 제대로 답하지 못할 가능성이 큽니다.

### 벤치마크 메뉴

Open LLM Leaderboard에서 사용되는 것과 동일한, 중요한 테스트들입니다:

| 벤치마크 | 테스트하는 것 | 양자화에서 왜 중요한가 |
|-----------|---------------|--------------------------------|
| **MMLU** | 57개 학문 분야 | 모델이 배운 것을 잊었는가? |
| **HellaSwag** | 상식 추론 | 인간은 거의 다 맞추지만(~95%), 모델은 어려워함 |
| **ARC-Challenge** | 초등학교 수준 과학 | 압축 상태에서도 추론이 가능한가? |
| **Winogrande** | 대명사 해석 | 기본적인 언어 이해가 온전한가? |
| **GSM8K** | 수학 서술형 문제 | 양자화에 가장 민감함 |
| **TruthfulQA** | 사실적 정확성 | 여전히 환각(hallucination)을 피하는가? |
| **HumanEval** | Python 코딩 문제 | 코드 생성 |
| **MBPP** | 기본적인 Python 프로그래밍 과제 | 코드 생성 |

#### 벤치마크는 실제로 어떻게 동작하는가

**객관식(multiple-choice)** 벤치마크의 경우, 모델이 "A, B, C, D 중 고르는" 방식이 아닙니다. 대신 가능한 각 완성(completion)을 모델에 입력하고, 어떤 것이 가장 낮은 perplexity를 갖는지 측정합니다. 모델은 본질적으로 질문에 비해 각 답변이 얼마나 자연스러운지를 평가하는 셈입니다.

**생성형(generative)** 벤치마크(GSM8K 등)의 경우, 모델이 답을 생성하고, 보통 최종 숫자를 추출하는 파싱을 거쳐 정답과 일치하는지 확인합니다.

**코딩(coding)** 벤치마크(HumanEval 등)의 경우, 모델이 함수 본문을 생성하고, 테스트 하네스가 이를 테스트 케이스에 대해 실행합니다. 코드가 올바르게 실행되고 올바른 출력을 생성하면 통과합니다.

### 어떤 태스크가 고통을 느끼는가?

양자화 민감도 측면에서 모든 벤치마크가 똑같이 취급되지는 않습니다:

| 민감도 | 벤치마크 | 이유 |
|-------------|------------|-----|
| 🔴 **높음** | GSM8K, 수학 태스크 | 수치 정밀도가 중요함—압축이 타격을 줌 |
| 🟡 **중간** | MMLU, ARC | 지식 검색—일부 저하 발생 |
| 🟢 **낮음** | HellaSwag, Winogrande | 패턴 매칭—상당히 견고함 |

**경고:** Canopy로 수학 튜터링을 한다면 GSM8K를 매처럼 지켜보세요. 보통 가장 먼저 금이 가는 부분입니다.

## 연구는 실제로 뭐라고 말하는가

좋은 소식이 있습니다: 대규모 연구들에 따르면 양자화는 여러분이 걱정하는 것보다 더 잘 동작합니다.

### 핵심 요약

모든 양자화 방식이 OpenLLM Leaderboard 벤치마크에서 기준 정확도의 **99% 이상**을 회복합니다. 세부 내용은 다음과 같습니다:

| 정밀도 | 예상되는 결과 |
|-----------|----------------|
| **INT8** | 거의 손실 없음—0.5% 미만의 하락 |
| **INT4** | 1-3%의 저하가 일반적 |
| **70B 이상 모델** | 더 견고함(클수록 더 여유가 있음) |
| **8B 모델** | 변동성이 더 크지만 여전히 사용 가능 |

### 반전: 답이 뒤집히는 현상

밤잠을 설치게 할 만한 사실이 있습니다. 전체 정확도가 기준 대비 1% 이내로 유지되더라도:

- 일부 정답이 *오답*으로 바뀝니다
- 일부 오답이 *정답*으로 바뀝니다
- 수학 태스크에서는 12-30%의 답이 "뒤집힙니다"

**이것이 의미하는 바:** 평균은 괜찮아 보이지만, 개별 질문들은 다르게 동작합니다. 요약 점수만 확인하지 말고, 실제 사용 사례를 테스트하세요.

### 어떤 알고리즘이 더 나은가?

| 알고리즘 | 정확도 보존 | 결론 |
|-----------|-------------------|-------------|
| AWQ | 더 높음 | 여러 태스크에서 더 안정적 |
| GPTQ | 약간 더 낮음 | GSM8K, ARC에서 변동성이 더 큼 |
| Q5_K_M (GGUF) | 최적점 | 대부분의 사용 사례에서 최고의 트레이드오프 |
| Q3_K_M (GGUF) | 위험함 | 상당한 저하—주의해서 사용 |

### "새로 나타나는 능력(Emergent Abilities)"에 대하여

좋은 소식: 연구에 따르면 인-컨텍스트 학습(in-context learning), chain-of-thought 추론, 지시 수행(instruction following) 같은 핵심 능력들은 INT4 양자화에서도 온전히 유지됩니다.

나쁜 소식: 2비트에서는 이러한 능력들이 심각하게 저하됩니다. 4비트 이하는 의미 있는 워크로드에 적합하지 않습니다.

## 직접 평가 실행하기

### 🧪 이제 직접 해볼 시간

이론은 충분합니다—실제로 양자화된 모델을 기준 모델과 비교해봅시다.

워크벤치로 이동해서 **`experiments/10-model-optimization/4-evaluation.ipynb`**를 엽니다.

이 실습에서는 `lm-evaluation-harness`를 사용해 배포된 두 모델에 대해 동일한 벤치마크를 실행하고 결과를 비교합니다.

**진행할 내용:**

1. **엔드포인트 구성하기** — lm_eval이 양자화되지 않은 모델과 FP8 양자화된 Llama 모델 모두를 가리키도록 설정합니다
2. **MMLU 벤치마크 실행하기** — 동일한 학문 문제로 두 모델을 테스트합니다
3. **결과 비교하기** — 실제 정확도 차이를 나란히 확인합니다
4. **영향 해석하기** — 이 숫자들이 배포 결정에 어떤 의미를 갖는지 이해합니다

**배울 내용:**

- `lm_eval`이 원격 OpenAI 호환 API(vLLM 등)와 어떻게 동작하는지
- 여러 사용자가 엔드포인트를 공유할 때 동시성(concurrency)을 제한하는 이유
- 벤치마크 결과를 읽고 정확도 차이를 계산하는 방법

완료되면 다시 돌아와서 배포 결정 프레임워크를 다루겠습니다.

### 배포된 모델 테스트하기

lm-evaluation-harness는 모델의 API 엔드포인트를 직접 호출할 수 있습니다:

```bash
lm_eval --model local-completions \
        --model_args base_url=https://llama32-fp8-ai501.<CLUSTER_DOMAIN> \
        --tasks hellaswag,winogrande,arc_easy \
        --limit 100
```

### 시간이 부족하다면? tinyBenchmarks를 사용하세요

전체 벤치마크는 수만 개의 질문으로 구성됩니다. tinyBenchmarks는 가장 정보량이 많은 질문들만 골라냅니다:

| 벤치마크 | 전체 크기 | tinyBenchmarks |
|-----------|-----------|----------------|
| MMLU | 14,000개 이상의 질문 | 약 100개 질문 |
| 6개 벤치마크 전체 | 50,000개 이상의 질문 | 전체의 3% 미만 |

동일한 정확도 추정치를, 훨씬 적은 시간으로. 개발 중 빠른 검증에 적합합니다.

## 의사결정 프레임워크

### 일반적인 기준치

언제 배포해야 할까요? 다음은 기본 원칙입니다:

| 정확도 하락 | 결론 | 할 일 |
|---------------|---------|------------|
| 1% 미만 | ✅ **배포하세요** | 자신 있게 배포합니다 |
| 1-3% | ⚠️ **허용 가능** | 배포하되 긴밀히 모니터링합니다 |
| 3-5% | 🔍 **애매함** | 실제 사용자와 A/B 테스트를 합니다 |
| 5% 초과 | ❌ **과도함** | INT8 또는 더 작은 group size를 시도합니다 |

### 태스크별 기준치

Canopy가 특정 태스크를 돕고 있다면 더 엄격한 기준을 적용하세요:

| Canopy가 하는 일 | 허용 가능한 최대 하락 |
|------------------|---------------------|
| 수학 튜터링 | GSM8K에서 2% 미만 |
| 코드 도움 | HumanEval에서 2% 미만 |
| 일반 채팅 | 평균 5% 미만 |
| 요약 | MMLU에서 3% 미만 |

<!-- 📊 Quiz: Ship or Not? -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">
<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 간단 확인: 배포할까요, 말까요?</h3>
<p style="margin:0 0 12px;color:#666;">여러분의 팀이 모델을 INT4로 양자화했습니다. 벤치마크 결과는 다음과 같습니다: GSM8K에서 4% 하락, MMLU에서 1% 하락, HellaSwag에서 1% 하락. Canopy는 수학 튜터링 어시스턴트로 사용되고 있습니다. 이 모델을 배포해야 할까요?</p>
<style>
.quiz-container-ship{position:relative}
.quiz-option-ship{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-ship:hover{background:#e9ecef}
.quiz-radio-ship{display:none}
.quiz-radio-ship:checked+.quiz-option-ship[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-ship:checked+.quiz-option-ship:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-ship{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#ship-correct:checked~.feedback-ship[data-feedback="correct"]{display:block;background:#d4edda;color:#155724}
#ship-wrong1:checked~.feedback-ship[data-feedback="wrong1"],#ship-wrong2:checked~.feedback-ship[data-feedback="wrong2"],#ship-wrong3:checked~.feedback-ship[data-feedback="wrong3"]{display:block;background:#f8d7da;color:#721c24}
</style>
<div class="quiz-container-ship">
<input type="radio" name="quiz-ship" id="ship-wrong1" class="quiz-radio-ship">
<label for="ship-wrong1" class="quiz-option-ship" data-correct="false">✅ 배포하세요—평균 하락은 약 2%로 허용 가능한 수준입니다</label>
<input type="radio" name="quiz-ship" id="ship-wrong2" class="quiz-radio-ship">
<label for="ship-wrong2" class="quiz-option-ship" data-correct="false">⚠️ 배포하고 모니터링하세요—전체적으로 1-3%는 허용 범위 내입니다</label>
<input type="radio" name="quiz-ship" id="ship-correct" class="quiz-radio-ship">
<label for="ship-correct" class="quiz-option-ship" data-correct="true">❌ 배포하지 마세요—GSM8K에서의 4% 하락은 수학 튜터링의 2% 기준치를 초과합니다</label>
<input type="radio" name="quiz-ship" id="ship-wrong3" class="quiz-radio-ship">
<label for="ship-wrong3" class="quiz-option-ship" data-correct="false">🔍 결정하기 전에 더 많은 벤치마크를 실행하세요</label>
<div class="feedback-ship" data-feedback="correct">✅ <strong>정답입니다!</strong> 태스크별 기준치가 평균보다 더 중요합니다. 수학 튜터링의 경우 GSM8K가 핵심 벤치마크이며—4%는 2% 기준치를 초과합니다. 수학 태스크의 정확도를 회복하려면 INT8이나 더 작은 group size(g64)를 시도해보세요.</div>
<div class="feedback-ship" data-feedback="wrong1">❌ 평균을 내면 문제가 숨겨집니다! 수학 튜터링의 경우 GSM8K가 중요한 벤치마크이며—4%는 허용 기준치의 두 배입니다.</div>
<div class="feedback-ship" data-feedback="wrong2">❌ 일반적인 기준치는 여기에 적용되지 않습니다. Canopy가 특별히 수학 튜터링용이기 때문에, GSM8K의 4% 하락은 태스크별 2% 제한을 초과합니다.</div>
<div class="feedback-ship" data-feedback="wrong3">❌ 이미 필요한 데이터를 가지고 있습니다. GSM8K는 수학 튜터링에 맞는 올바른 벤치마크이며—명백히 기준치를 초과했습니다. 벤치마크를 더 돌려도 결정은 바뀌지 않습니다.</div>
</div>
</div>

## 의사결정 매트릭스

모든 것을 비교 표로 정리해봅시다:

| 모델 변형 | 크기 | GSM8K | MMLU | HellaSwag | 평균 하락 | 배포할까요? |
|---------------|------|-------|------|-----------|----------|----------|
| FP16 (기준) | 6.4 GB | 0.412 | 0.654 | 0.762 | — | 기준값 |
| INT8 | 3.2 GB | 0.405 | 0.651 | 0.759 | -0.8% | ✅ 예 |
| INT4 g128 | 1.8 GB | 0.389 | 0.640 | 0.751 | -2.5% | ⚠️ 모니터링 |
| INT4 g64 | 2.0 GB | 0.398 | 0.647 | 0.755 | -1.5% | ✅ 예 |

## 하지만 잠깐—1단계로는 충분하지 않습니다

<!-- 🧪 Quiz: The Testing Trap -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">
<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 간단 확인: 테스트의 함정</h3>
<p style="margin:0 0 12px;color:#666;">여러분의 양자화된 모델이 MMLU에서 98%를 기록하며 모든 표준 벤치마크를 통과했습니다. 이를 프로덕션에 배포합니다. 일주일 후, 학생들이 Canopy가 프롬프트를 무시하고 잘못된 형식의 JSON을 반환한다고 불만을 제기합니다. 무엇이 잘못됐을까요?</p>
<style>
.quiz-container-testing{position:relative}
.quiz-option-testing{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-testing:hover{background:#e9ecef}
.quiz-radio-testing{display:none}
.quiz-radio-testing:checked+.quiz-option-testing[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-testing:checked+.quiz-option-testing:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-testing{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#testing-correct:checked~.feedback-testing[data-feedback="correct"]{display:block;background:#d4edda;color:#155724}
#testing-wrong1:checked~.feedback-testing[data-feedback="wrong1"],#testing-wrong2:checked~.feedback-testing[data-feedback="wrong2"],#testing-wrong3:checked~.feedback-testing[data-feedback="wrong3"]{display:block;background:#f8d7da;color:#721c24}
</style>
<div class="quiz-container-testing">
<input type="radio" name="quiz-testing" id="testing-wrong1" class="quiz-radio-testing">
<label for="testing-wrong1" class="quiz-option-testing" data-correct="false">📊 벤치마크가 너무 쉬웠습니다—더 어려운 테스트를 사용해야 했습니다</label>
<input type="radio" name="quiz-testing" id="testing-correct" class="quiz-radio-testing">
<label for="testing-correct" class="quiz-option-testing" data-correct="true">🧪 1단계(지식)만 테스트하고 2단계(애플리케이션 흐름)는 건너뛰었습니다</label>
<input type="radio" name="quiz-testing" id="testing-wrong2" class="quiz-radio-testing">
<label for="testing-wrong2" class="quiz-option-testing" data-correct="false">🔢 모델에 더 작은 group size가 필요했습니다</label>
<input type="radio" name="quiz-testing" id="testing-wrong3" class="quiz-radio-testing">
<label for="testing-wrong3" class="quiz-option-testing" data-correct="false">⏱️ 너무 빨리 배포했습니다—더 오래 기다려야 했습니다</label>
<div class="feedback-testing" data-feedback="correct">✅ <strong>정확합니다!</strong> 벤치마크 점수는 지식 보존 여부를 테스트하지만, 양자화는 벤치마크가 잡아내지 못하는 방식으로 지시 수행(instruction-following)과 출력 형식을 망가뜨릴 수 있습니다. 배포 전에는 항상 실제 애플리케이션 흐름—시스템 프롬프트, 도구 호출(tool calling), JSON 출력—을 테스트하세요.</div>
<div class="feedback-testing" data-feedback="wrong1">❌ MMLU는 이미 충분히 어렵습니다. 문제는 테스트 난이도가 아니라—벤치마크가 애플리케이션 동작과는 다른 것을 측정한다는 점입니다.</div>
<div class="feedback-testing" data-feedback="wrong2">❌ Group size는 정확도에 영향을 주지만, 여기서 문제는 <em>어떻게</em> 양자화했는지가 아니라 <em>무엇을</em> 테스트했는지입니다.</div>
<div class="feedback-testing" data-feedback="wrong3">❌ 타이밍은 문제가 아닙니다. 1년을 기다려도 벤치마크 테스트만 실행한다면 여전히 이 문제를 겪게 됩니다.</div>
</div>
</div>

**핵심 요점:** 벤치마크는 모델이 여전히 *지식*을 가지고 있는지를 검증합니다. 하지만 여러분의 애플리케이션에서 여전히 *잘 동작하는지*도 검증해야 합니다. 이것이 2단계이며—Canopy가 양자화된 모델을 사용하도록 업데이트할 때 다음 섹션에서 진행하게 됩니다.
