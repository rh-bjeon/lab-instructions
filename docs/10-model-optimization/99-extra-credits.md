<!-- 
## 왜 신경 써야 할까요?

| 이점 | 여러분에게 의미하는 것 |
|---------|----------------------|
| **메모리** | 그 14GB 모델이요? 이제 3.5GB입니다. 더 저렴한 GPU를 쓸 수 있습니다! |
| **속도** | 작은 숫자 = 더 빠른 연산 = 더 빠른 응답 |
| **비용** | 더 적은 GPU에 더 많은 모델을 올림 = 행복해하는 재무팀 |
| **정확도** | 함정: 품질을 약간 잃을 수 있습니다(하지만 생각보다 적습니다) |

질문은 양자화를 *할지 말지*가 아닙니다. 학생들이 눈치채기 전에 *얼마나* 밀어붙일 수 있는지입니다.

## 정밀도 메뉴

정밀도 형식을 커피 사이즈처럼 생각해보세요. 여러분의 지연시간, 비용, 품질 요구사항에 맞는 것을 고를 수 있습니다.

| 형식 | 비트 | FP32 대비 메모리 | 사용 시기 |
|--------|------|----------------|----------------|
| FP32 | 32 | 100% | 실전에서는 드묾; 디버깅이나 수치적으로 민감한 연산에 사용. 최신 LLM 학습의 기본값은 아님. |
| FP16/BF16 | 16 | 50% | 최신 GPU에서의 대부분의 학습 + 추론의 기본값 |
| FP8 | 8 | 25% | 최신 GPU에서 처리량(throughput) 중심의 학습/추론 |
| INT8 | 8 | 25% | 프로덕션 추론의 "안전한 선택"(즉, 좋은 품질/지연시간/메모리 트레이드오프) |
| INT4 | 4 | 12.5% | 공격적인 압축(위험하게 살기) |

대부분의 프로덕션 배포는 INT8과 INT4 사이 어딘가에 자리잡습니다. 실제로 우리가 압축하는 대상이 무엇인지 이해해봅시다.

-->

## 무엇을 양자화할 수 있는가?

LLM에는 압축할 수 있는 세 가지 요소가 있으며, 각각 고유한 위험/보상이 있습니다:

### 1. 가중치 양자화 (쉬운 쪽)
가중치(weight)는 모델이 학습한 파라미터로—모델이 아는 모든 것을 인코딩한, 디스크/VRAM에 저장된 수십억 개의 숫자입니다. 추론 시점에는 고정되어 있고, 예측 가능하며, 대체로 양자화가 잘 됩니다.

- **가장 흔하고 가장 안전한** 접근법
- 한 번만 수행하면 영구적으로 이득을 봄
- 예: W8A16은 8비트 가중치, 16비트 활성값(activation)을 의미

### 2. 활성값 양자화 (까다로운 쪽)
활성값(activation)은 프롬프트/토큰을 처리하는 동안 생성되는 중간 값들입니다. 동적이고, 입력에 따라 달라지며, 이상치(outlier)로 급격히 튈 수 있습니다. 그래서 양자화에 더 민감합니다.

- **더 어려움**—활성값은 예상치 못하게 급등할 수 있음
- 제대로 하려면 캘리브레이션(calibration) 데이터가 필요함
- 예: W8A8은 가중치와 활성값 둘 다 양자화됨을 의미

### 3. KV 캐시 양자화 (메모리 먹는 하마)
어텐션(attention)은 모델이 이전 토큰을 "돌아보고" 다음 토큰에서 무엇이 중요한지 판단하게 해주는 메커니즘입니다. 학생들이 에세이를 쓰거나 후속 질문을 할 때, 모델은 재계산할 필요가 없도록 어텐션 상태를 KV 캐시라는 캐시에 저장하는 경우가 많습니다.
긴 대화의 경우, 이 KV 캐시는 모델 자체보다 더 많은 메모리를 먹을 수 있습니다.

- 챗봇(Canopy처럼!)에 특히 유용함
- 긴 대화에서 메모리를 줄여줌
- 자주 간과되지만 게임 체인저가 될 수 있음

<!-- 🧠 Quiz 2: KV Cache scenario -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 시나리오 확인</h3>

<p style="color:#495057;font-weight:500;">
Canopy를 배포하는 중이고 학생들이 후속 질문이 있는 <strong>긴 대화</strong>를 나누고 있습니다. 각 채팅 세션 내내 메모리 사용량이 계속 늘어납니다.<br><br>
<strong>어떤 양자화 대상이 가장 도움이 될까요?</strong>
</p>

<style>
.quiz-container-kv-cache{position:relative}
.quiz-option-kv-cache{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;
  cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-kv-cache:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-kv-cache{display:none}
.quiz-radio-kv-cache:checked+.quiz-option-kv-cache[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-kv-cache:checked+.quiz-option-kv-cache:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-kv-cache{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#kv-cache-correct:checked~.feedback-kv-cache[data-feedback="correct"],
#kv-cache-wrong1:checked~.feedback-kv-cache[data-feedback="wrong1"],
#kv-cache-wrong2:checked~.feedback-kv-cache[data-feedback="wrong2"]{display:block}
.feedback-kv-cache[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-kv-cache[data-feedback="wrong1"], .feedback-kv-cache[data-feedback="wrong2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-kv-cache">
  <input type="radio" name="quiz-kv-cache" id="kv-cache-wrong1" class="quiz-radio-kv-cache">
  <label for="kv-cache-wrong1" class="quiz-option-kv-cache" data-correct="false">
    🏋️ 가중치 양자화
  </label>

  <input type="radio" name="quiz-kv-cache" id="kv-cache-wrong2" class="quiz-radio-kv-cache">
  <label for="kv-cache-wrong2" class="quiz-option-kv-cache" data-correct="false">
    ⚡ 활성값 양자화
  </label>

  <input type="radio" name="quiz-kv-cache" id="kv-cache-correct" class="quiz-radio-kv-cache">
  <label for="kv-cache-correct" class="quiz-option-kv-cache" data-correct="true">
    💾 KV 캐시 양자화
  </label>

  <div class="feedback-kv-cache" data-feedback="correct">
    ✅ <strong>정답입니다!</strong> KV 캐시는 전체 대화의 어텐션 상태를 저장하며 메시지마다 커집니다. 긴 대화의 경우, 모델의 가중치 메모리를 초과할 수 있습니다. 이를 양자화하면 늘어나는 메모리 문제를 직접적으로 해결할 수 있습니다.
  </div>
  <div class="feedback-kv-cache" data-feedback="wrong1">
    ❌ 가중치는 한 번 로드되면 고정됩니다. 대화 길이에 따라 커지지 않습니다—여러분의 문제는 대화가 진행되면서 쌓이는 무언가입니다.
  </div>
  <div class="feedback-kv-cache" data-feedback="wrong2">
    ❌ 활성값은 토큰마다 계산되지만 대화 전체에 걸쳐 축적되지 않습니다. 늘어나는 메모리는 어텐션 상태를 저장하는 데서 발생합니다.
  </div>
</div>
</div>

## 양자화 기법

### 대칭(Symmetric) vs. 비대칭(Asymmetric)

온도계처럼 생각해보세요:

- **대칭**(Symmetric)은 0°C를 중심으로 하는 온도계와 같습니다—양방향(-50°에서 +50°)을 동일하게 측정합니다. 모델 가중치처럼 데이터가 0을 중심으로 균형을 이룰 때 적합합니다.

- **비대칭**(Asymmetric)은 체온을 재는 온도계(35°C에서 42°C)와 같습니다—오프셋(제로 포인트, zero-point)을 두어 데이터가 실제로 존재하는 곳에 정밀도를 집중시킵니다. 모두 양수이거나 한쪽으로 치우친 활성값에 더 적합합니다.

| 방식 | 방법 | 수식 | 가장 적합한 대상 |
|----------|--------|---------|----------|
| **대칭** | 스케일만 사용 | `q = round(x / scale)` | 가중치 (0을 중심으로 분포) |
| **비대칭** | 스케일 + 제로 포인트 | `q = round(x / scale) + zero_point` | 활성값 (중심이 0이 아님) |

양자화는 원본 부동소수점 값 `x`(예: FP32)를 작은 정수 `q`(예: INT8/INT4)로 매핑해서 모델을 더 빠르고 메모리를 덜 쓰게 만듭니다. `scale`은 단계 크기(step size)를 설정하고, `zero_point`는 0이 중앙에 있지 않을 때 범위를 이동시킵니다.

**각각 언제 사용할까:**
- 대칭은 더 단순하고 빠름
- 비대칭은 0을 중심으로 하지 않는 분포를 더 잘 처리함
- 대부분의 가중치 양자화는 대칭을 사용함
- 활성값 양자화는 비대칭이 필요한 경우가 많음

<!-- ⚖️ Quiz 3: Symmetric vs Asymmetric -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 간단 확인</h3>

<p style="color:#495057;font-weight:500;">
모델 <strong>가중치</strong>는 일반적으로 0을 중심으로 분포합니다: <code>[-0.5, 0.3, -0.1, 0.4]</code><br>
ReLU 이후의 <strong>활성값</strong>은 항상 양수입니다: <code>[0.0, 0.7, 0.2, 1.3]</code><br>
<i>ReLU는 많은 신경망에서 사용하는 기본 규칙입니다: 숫자가 음수면 0으로 바꾸고, 양수면 그대로 둡니다.
그래서 "ReLU 이후의" 활성값은 항상 0 이상입니다. 예: [-0.8, 0.7, -0.1, 1.3] → [0.0, 0.7, 0.0, 1.3]</i><br><br>
<strong>어떤 설명이 맞을까요?</strong>
</p>

<style>
.quiz-container-sym-asym{position:relative}
.quiz-option-sym-asym{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;
  cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-sym-asym:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-sym-asym{display:none}
.quiz-radio-sym-asym:checked+.quiz-option-sym-asym[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-sym-asym:checked+.quiz-option-sym-asym:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-sym-asym{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#sym-asym-correct:checked~.feedback-sym-asym[data-feedback="correct"],
#sym-asym-wrong1:checked~.feedback-sym-asym[data-feedback="wrong1"],
#sym-asym-wrong2:checked~.feedback-sym-asym[data-feedback="wrong2"]{display:block}
.feedback-sym-asym[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-sym-asym[data-feedback="wrong1"], .feedback-sym-asym[data-feedback="wrong2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-sym-asym">
  <input type="radio" name="quiz-sym-asym" id="sym-asym-correct" class="quiz-radio-sym-asym">
  <label for="sym-asym-correct" class="quiz-option-sym-asym" data-correct="true">
    ⚖️ 가중치는 대칭, 활성값은 비대칭을 사용한다
  </label>

  <input type="radio" name="quiz-sym-asym" id="sym-asym-wrong1" class="quiz-radio-sym-asym">
  <label for="sym-asym-wrong1" class="quiz-option-sym-asym" data-correct="false">
    🔄 둘 다 비대칭을 사용한다
  </label>

  <input type="radio" name="quiz-sym-asym" id="sym-asym-wrong2" class="quiz-radio-sym-asym">
  <label for="sym-asym-wrong2" class="quiz-option-sym-asym" data-correct="false">
    ➡️ 둘 다 대칭을 사용한다
  </label>

  <div class="feedback-sym-asym" data-feedback="correct">
    ✅ <strong>정답입니다!</strong> 대칭은 0을 중심으로 하는 데이터(가중치)에 잘 맞습니다. 비대칭은 제로 포인트 오프셋을 사용해 데이터가 실제로 존재하는 곳에 정밀도를 집중시킴으로써, 중심이 0이 아닌 분포(ReLU 활성값은 항상 0 이상)를 처리합니다.
  </div>
  <div class="feedback-sym-asym" data-feedback="wrong1">
    ❌ 비대칭은 오버헤드(제로 포인트 저장)를 추가합니다. 데이터가 이미 0을 중심으로 분포한다면 필요하지 않습니다—대칭이 더 빠르고 가중치에 매우 적합합니다.
  </div>
  <div class="feedback-sym-asym" data-feedback="wrong2">
    ❌ 대칭은 항상 양수인 데이터에 정밀도를 낭비합니다. 범위의 절반(음수 값)이 사용되지 않기 때문입니다. ReLU 활성값의 경우, 비대칭을 사용하면 모든 비트를 양수 범위에 집중시킬 수 있습니다.
  </div>
</div>
</div>

### 세분성(Granularity)

여러 가지를 측정한다고 상상해보세요:

* 일부는 **아주 작습니다** (클립처럼)
* 일부는 **아주 큽니다** (테이블처럼)

모두가 큰 눈금을 가진 **같은 자**(예를 들어 센티미터 단위만 있는)를 사용해야 한다면, 작은 것을 측정할 때 세부 정보를 잃게 됩니다.

양자화에서도 같은 일이 벌어집니다:

* **정수 `q`**는 허용된 작은 숫자 집합(예: INT4의 경우 0–15)만 사용해서 측정값을 기록하는 것과 같습니다.
* **스케일**(scale)은 "1단계"가 무엇을 의미하는지 말해주는 자입니다(예: "1단계 = 1cm" 또는 "1단계 = 1mm").

#### 세분성은 어떻게 영향을 미치는가?

신경망 내부에는 가중치와 같은 정보가 "텐서(Tensor)"(숫자들의 다차원 리스트/배열) 안에 저장됩니다.

신경망을 이러한 텐서들이 여러 개 모여 있는 것으로 시각화할 수 있습니다:

![neural-network.png](images/neural-network.png)

그리고 각 텐서는 더 작은 부분으로 나뉠 수 있습니다:

![per-channel.png](images/per-channel.png)

세분성은 단순히: **몇 개의 값이 같은 자(스케일)를 공유하는가**입니다.

* **텐서 단위(Per-tensor):** *모든 것에 하나의 자*

  클립과 테이블을 같은 "센티미터 전용" 자로 측정하는 것과 같습니다 → 빠르지만 작은 세부 정보를 잃습니다.

* **채널 단위(Per-channel):** *채널마다 하나의 자*

  각 그룹(클립 vs 테이블)에게 각자의 자를 주는 것과 같습니다 → 훨씬 더 정확합니다.

* **그룹 단위(g128/g64/g32):** *채널 내부의 작은 묶음마다 하나의 자*

  더 세밀하게 나누는 것입니다(각 서랍마다 자신만의 자를 갖는 것) → 가장 잘 맞지만, 이제 많은 자(오버헤드/메타데이터)를 추적해야 합니다.

#### 더 작은 그룹이 왜 도움이 되는가 (품질 면에서 g32 > g64 > g128)

그룹이 작을수록 = 하나의 자를 공유해야 하는 항목이 줄어들어, 각 자가 자신이 담당하는 묶음에 더 "잘 맞게" 됩니다 → **반올림 오차가 줄어듭니다**.

**그룹 양자화**(예: group_size=128)는 INT4의 최적점입니다:
- `g128`: 좋은 압축률, 수용 가능한 정확도
- `g64`: 더 나은 정확도, 약간 더 큰 크기
- `g32`: 최고의 정확도, 가장 큰 오버헤드

### 양자화 데이터는 어떻게 저장되는가

양자화된 모델은 양자화된(저정밀) 가중치만 저장하는 것이 아닙니다. 추론 중에 원본 값을 재구성하기 위해 필요한 메타데이터도 저장합니다.

**저장되는 내용:**
- **양자화된 가중치**: 실제 INT4/INT8 값
- **스케일(Scales)**: 텐서, 채널, 또는 그룹마다 하나씩(세분성에 따라 다름)
- **제로 포인트(Zero-points)**: 비대칭 양자화에만 해당
- **양자화 설정(config)**: 사용된 알고리즘, 그룹 크기, 양자화된 레이어

**예시 구조** (단순화됨):
```
model.safetensors
├── model.layers.0.self_attn.q_proj.weight      # INT4 packed weights
├── model.layers.0.self_attn.q_proj.weight_scale # FP16 scales (one per group)
├── model.layers.0.self_attn.q_proj.weight_zp   # Zero-points (if asymmetric)
└── ...
```

**오버헤드 트레이드오프:**
- 더 세밀한 세분성(더 작은 그룹) = 저장할 스케일이 더 많음 = 더 큰 파일
- 7B 모델에 g128을 적용한 INT4: 약 3.5GB 가중치 + 약 50MB 스케일
- g64를 적용한 INT4: 스케일 값이 2배 더 많아 약간 더 큼

이것이 그룹 크기가 정확도 *그리고* 최종 모델 크기 모두에 영향을 미치는 이유입니다.

## 문제가 생길 때

양자화는 마법이 아닙니다 🪄 때로는 뭔가를 망가뜨립니다. 🫣 흔히 벌어지는 문제들입니다:

### 이상치(Outlier) 문제

커브를 적용해서 채점하는데 한 학생이 10,000%를 받았다고 상상해보세요. 이제 다른 모든 학생이 0점을 받은 것처럼 보입니다. 이상치 활성값이 양자화에 하는 일이 바로 이것입니다.

```
Normal activations: [-1.0, 0.5, -0.3, 0.8, ...]
That one outlier:       [..., 127.5, ...]  ← Ruins everything!
```

**해결 방법:**

적용할 수 있는 몇 가지 기법/방법이 있습니다:

* **SmoothQuant:** 극단적인 범위의 일부를 가중치 쪽으로 옮겨서 *활성값을 덜 "뾰족하게"* 만들어, 활성값을 양자화하기 더 쉽게 만듭니다.
* **AWQ:** 가장 중요한 부분(출력에 강하게 영향을 미치는 "바쁜" feature)을 *특별히 신경 써서* 더 부드럽게 양자화합니다.
* **혼합 정밀도(Mixed precision):** *모든 것을 양자화하지 않습니다* — 민감한 부분은 FP16으로 유지하고 나머지만 양자화합니다.

<!-- 📊 Quiz 4: Outlier Problem -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 생각해보기</h3>

<p style="color:#495057;font-weight:500;">
여러분의 INT8 모델에는 때때로 <strong>500</strong>까지 튀는 내부 값이 하나 있고, 거의 모든 다른 내부 값은 <strong>-2에서 2</strong> 사이에 머무릅니다.<br><br>
<strong>양자화할 때 정상적인 값들에는 무슨 일이 생길까요?</strong>
</p>

<style>
.quiz-container-outlier{position:relative}
.quiz-option-outlier{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;
  cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-outlier:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.quiz-radio-outlier{display:none}
.quiz-radio-outlier:checked+.quiz-option-outlier[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-outlier:checked+.quiz-option-outlier:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-outlier{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#outlier-correct:checked~.feedback-outlier[data-feedback="correct"],
#outlier-wrong1:checked~.feedback-outlier[data-feedback="wrong1"],
#outlier-wrong2:checked~.feedback-outlier[data-feedback="wrong2"]{display:block}
.feedback-outlier[data-feedback="correct"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.feedback-outlier[data-feedback="wrong1"], .feedback-outlier[data-feedback="wrong2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div class="quiz-container-outlier">
  <input type="radio" name="quiz-outlier" id="outlier-wrong1" class="quiz-radio-outlier">
  <label for="outlier-wrong1" class="quiz-option-outlier" data-correct="false">
    ✨ 더 정밀해진다
  </label>

  <input type="radio" name="quiz-outlier" id="outlier-correct" class="quiz-radio-outlier">
  <label for="outlier-correct" class="quiz-option-outlier" data-correct="true">
    📉 스케일이 늘어나면서 정밀도를 잃는다
  </label>

  <input type="radio" name="quiz-outlier" id="outlier-wrong2" class="quiz-radio-outlier">
  <label for="outlier-wrong2" class="quiz-option-outlier" data-correct="false">
    🤷 아무 일도 없다, INT8이 이를 잘 처리한다
  </label>

  <div class="feedback-outlier" data-feedback="correct">
    ✅ <strong>정답입니다!</strong> 스케일이 이상치(500)를 포용해야 하므로, 1.5와 1.7 같은 값들이 같은 정수로 반올림될 수 있습니다. 정상 범위 내의 작은 차이를 구별하는 능력을 잃게 됩니다. 이것이 SmoothQuant 같은 알고리즘이 존재하는 이유입니다—양자화 전에 이상치를 다스리기 위함입니다.
  </div>
  <div class="feedback-outlier" data-feedback="wrong1">
    ❌ 실제로는 그 반대입니다. 이상치를 포용하기 위해 스케일이 넓어지면, 양자화된 값들 사이의 "단계 크기(step size)"가 커져서 정상 값들이 덜 정밀해집니다.
  </div>
  <div class="feedback-outlier" data-feedback="wrong2">
    ❌ INT8은 가능한 값이 256개뿐입니다. 이상치를 담기 위해 스케일이 -500에서 +500까지 늘어나면, 각 "단계"는 약 4 단위 너비가 됩니다. 0.5와 1.5 같은 값들이 모두 0이 됩니다. 이것은 문제입니다!
  </div>
</div>
</div>

### 포화(Saturation) (클리핑 문제)

값이 우리 형식이 표현할 수 있는 범위를 초과하면 잘려나갑니다. 기린을 공중전화 부스에 넣으려는 것과 같습니다.

```
INT8 can hold: [-128, 127]
Your value:    150 → gets squished to 127 (oops)
```

**해결 방법:**
* **실제 데이터로 캘리브레이션하기:** 이상한 극단 사례가 아니라 현실적인 값 범위를 기반으로 스케일을 선택합니다.
* **클리핑을 최소화하는 스케일 선택하기:** 대부분의 값이 [-128, 127] 안에 들어가는 매핑을 선택합니다.
* **더 세밀한 세분성(더 작은 그룹):** 모델의 각 부분마다 전형적인 범위가 다를 수 있습니다. 각 그룹에 자체 스케일을 부여하면 "넓은 범위" 그룹이 "좁은 범위" 그룹에 같은 스케일을 강제하지 않게 됩니다.


## 결정 트리

무엇을 골라야 할지 모르겠나요? 다음은 치트 시트입니다:

| 다음과 같은 상황이라면…                 | 이것을 선택하세요…          |
| ------------------------------------------------- | --------------------- |
| "정확도를 높게 유지하고 싶다"                              | INT8 (W8A16)          |
| "균형 잡힌 중간 지점을 원한다"                | INT4 with g128        |
| "더 많은 압축이 필요하고, 정확도는 타협 가능하다" | INT4 with a larger group g256 | 
| "긴 대화가 GPU 메모리를 잡아먹고 있다"                | KV cache quantization |



# 🔧 LLM-Compressor

## 왜 LLM-Compressor인가?

| 특징 | 왜 중요한가 |
|---------|--------------|
| **프로덕션에서 검증됨** | vLLM 팀이 만들었습니다. 그들이 직접 사용합니다 |
| **HuggingFace 네이티브** | 어떤 Transformers 모델이든 로드, 압축, 저장 가능 |
| **모든 알고리즘** | GPTQ, AWQ, SmoothQuant, SparseGPT가 한곳에 |
| **vLLM 준비 완료** | 출력된 모델이 여러분의 서빙 스택에서 바로 동작함 |

## PTQ 워크플로우 (훈련 후 양자화, Post-Training Quantization)

훈련 후 양자화(PTQ)는 모델이 훈련을 *마친 후에* 압축합니다. 비용이 많이 드는 재훈련이 필요하지 않습니다. 양복을 맞춰 입는 것과 비슷합니다: 원단(지식)은 이미 있고, 더 잘 맞도록 만드는 것뿐입니다.

내부적으로 벌어지는 일은 다음과 같습니다:

1. **모델 로드하기** — FP16/FP32 모델로 시작합니다
2. **캘리브레이션 데이터 입력하기** — 모델에게 대표적인 입력을 보여줍니다
3. **범위 학습하기** — 알고리즘이 일반적인 활성값 범위를 파악합니다
4. **보상하며 압축하기** — 오차를 최소화하면서 가중치를 양자화합니다
5. **결과 저장하기** — 번쩍이는 압축된 모델을 내보냅니다

**캘리브레이션이 중요한 이유:** 사진에 무엇이 담겨 있는지 모른 채 압축한다고 상상해보세요. 중요한 세부 정보를 뭉개버릴 수 있습니다. 캘리브레이션 데이터는 알고리즘에게 "정상"이 어떻게 보이는지 가르쳐줘서, 무엇을 보존해야 하는지 알게 합니다.

<!-- 🧮 Quiz 1: Calibration Understanding -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">
<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 간단 확인: 캘리브레이션은 왜 필요한가?</h3>
<p style="margin:0 0 12px;color:#666;">여러분의 팀이 Canopy용 모델을 양자화하고 있습니다. 누군가가 시간을 절약하기 위해 캘리브레이션 데이터를 건너뛰자고 제안합니다. 이것이 왜 나쁜 생각일까요?</p>
<style>
.quiz-container-calib{position:relative}
.quiz-option-calib{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-calib:hover{background:#e9ecef}
.quiz-radio-calib{display:none}
.quiz-radio-calib:checked+.quiz-option-calib[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-calib:checked+.quiz-option-calib:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-calib{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#calib-correct:checked~.feedback-calib[data-feedback="correct"]{display:block;background:#d4edda;color:#155724}
#calib-wrong1:checked~.feedback-calib[data-feedback="wrong1"],#calib-wrong2:checked~.feedback-calib[data-feedback="wrong2"],#calib-wrong3:checked~.feedback-calib[data-feedback="wrong3"]{display:block;background:#f8d7da;color:#721c24}
</style>
<div class="quiz-container-calib">
<input type="radio" name="quiz-calib" id="calib-wrong1" class="quiz-radio-calib">
<label for="calib-wrong1" class="quiz-option-calib" data-correct="false">📊 캘리브레이션 없이는 모델이 더 커진다</label>
<input type="radio" name="quiz-calib" id="calib-wrong2" class="quiz-radio-calib">
<label for="calib-wrong2" class="quiz-option-calib" data-correct="false">⏱️ 추론이 더 느려진다</label>
<input type="radio" name="quiz-calib" id="calib-correct" class="quiz-radio-calib">
<label for="calib-correct" class="quiz-option-calib" data-correct="true">🎯 알고리즘이 어떤 값을 보존해야 할지 몰라 중요한 세부 정보를 뭉개버린다</label>
<input type="radio" name="quiz-calib" id="calib-wrong3" class="quiz-radio-calib">
<label for="calib-wrong3" class="quiz-option-calib" data-correct="false">🔒 보안 취약점이 생긴다</label>
<div class="feedback-calib" data-feedback="correct">✅ <strong>정답입니다!</strong> 캘리브레이션 데이터는 알고리즘에게 "정상"이 어떻게 보이는지 가르쳐줍니다. 이것이 없으면, 알고리즘이 가장 중요한 값들을 뭉개버릴 수 있습니다—사진을 보지도 않고 압축하는 것과 같습니다.</div>
<div class="feedback-calib" data-feedback="wrong1">❌ 모델 크기는 목표 정밀도(INT4, INT8)에 의해 결정되며, 캘리브레이션과는 무관합니다. 캘리브레이션은 <em>품질</em>에 영향을 주지, <em>크기</em>에는 영향을 주지 않습니다.</div>
<div class="feedback-calib" data-feedback="wrong2">❌ 추론 속도는 양자화 방식과 하드웨어에 따라 결정되며, 캘리브레이션 사용 여부와는 무관합니다.</div>
<div class="feedback-calib" data-feedback="wrong3">❌ 캘리브레이션은 정확도 보존에 관한 것이지 보안과는 무관합니다. 실제 위험은 중요한 정보를 뭉개버리는 것입니다.</div>
</div>
</div>

## 알고리즘 선택하기

모든 압축 알고리즘이 똑같지는 않습니다. 각자 고유한 개성을 가진 주요 후보들을 소개합니다.

### GPTQ: 완벽주의자 🎯

GPTQ는 GPT Quantization의 줄임말로, GPT 모델을 위해 설계된 양자화 방식입니다. INT4 가중치 양자화의 표준으로 통합니다. 정확도가 최우선이라면 여기서 시작하세요.

모든 것이 완벽하게 들어가야 하는 여행 가방을 싼다고 상상해보세요. 아무렇게나 싸면 그냥 모든 것을 짓누르게 됩니다. 그래서 일부 물건이 손상됩니다. GPTQ는 한 물건을 압축한 후, 보상하기 위해 주변 물건들을 조심스럽게 재배치하는 숙련된 짐꾼과 같습니다. 결과는? 모든 것이 들어가고, 아무것도 망가지지 않습니다.

**내부적으로:**
- 가중치를 레이어별로 처리합니다
- 수학(헤시안 행렬, Hessian matrices)을 사용해 어떤 가중치가 가장 중요한지 파악합니다 🧠
- 각 가중치를 양자화한 후, 보상을 위해 나머지 가중치를 조정합니다
- 더 느리지만, 품질을 위해서는 그만한 가치가 있습니다

**사용 시기:** 정확도를 절대 타협할 수 없을 때!

### AWQ: 스피드 데몬 🏎️

AWQ(Activation-aware Weight Quantization)는 GPTQ보다 빠르면서도 거의 비슷한 정확도를 보입니다. MLSys 2024 최우수 논문상을 수상했습니다. 빠르기만 한 게 아니라 똑똑합니다!

석양 사진을 편집한다고 상상해보세요. 모든 곳에 같은 설정을 적용하면, 태양이 날아가거나 풍경을 잃게 됩니다. AWQ는 "강조해야 할" 채널—활성값 패턴에 기반해 가장 중요한 가중치—을 식별하고, 압축 중에 이를 보호합니다.

**내부적으로:**
- 활성값의 크기를 살펴보며 "중요한(salient)" 채널을 찾습니다
- 양자화 전에 중요한 가중치를 스케일업합니다(보호합니다)
- 균형을 맞추기 위해 활성값을 스케일다운합니다
- 비용이 많이 드는 역전파(backpropagation)가 필요하지 않습니다

**사용 시기:** 내일이 아니라 오늘 결과가 필요할 때

### SmoothQuant: 균형자 ⚖️

가중치*와* 활성값 *둘 다*를 INT8로 양자화합니다. 이것이 진짜 W8A8을 얻는 방법입니다.

**문제:** 가중치는 다루기 쉽고 압축하기 쉽습니다. 활성값은 제멋대로입니다—모든 것을 망치는 이상치를 가지고 있습니다.

시소에 앉은 두 사람을 그려보세요: 한 명은 무겁고(이상치가 있는 어려운 활성값), 한 명은 가볍습니다(쉬운 가중치). SmoothQuant는 무거운 쪽에서 가벼운 쪽으로 무게를 일부 옮겨서, 둘 다 동등하게 다룰 수 있도록 시소의 균형을 맞춥니다.

**내부적으로:**
- 수학적으로 양자화의 어려움을 활성값에서 가중치로 옮깁니다
- 활성값에 평활화 인자(smoothing factor)를 곱합니다(이상치를 다스립니다)
- 가중치는 같은 인자로 나눕니다(가중치가 이를 흡수할 수 있습니다)

**사용 시기:** INT8 하드웨어에서 최대 처리량을 위해 W8A8이 필요할 때

### SparseGPT: 마리 콘도 🗑️

압축만 할 수 있는데 왜 삭제도 안 할까요? SparseGPT는 정확도에 기여하지 않는 가중치 전체를 제거하여, 남은 부분을 GPTQ로 압축할 수 있게 합니다.

소설을 편집하는 것과 비슷합니다: 먼저 채우기용 문단을 완전히 잘라내고(가지치기, pruning), 그다음 문장을 다듬습니다(양자화). 결과는 더 짧으면서도 더 나은 결과물입니다.

**내부적으로:**
- 정확도를 해치지 않고 0으로 만들 수 있는 가중치를 식별합니다
- GPTQ 방식의 보상을 사용해 품질을 유지합니다
- 극단적인 압축을 위해 희소성(sparsity)과 양자화를 결합할 수 있습니다

**사용 시기:** 최대 압축을 목표로 하고, 튜닝할 인내심이 있을 때

<!-- 🧮 Quiz 3: Algorithm Matching -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">
<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 간단 확인: 이상치 문제</h3>
<p style="margin:0 0 12px;color:#666;">여러분의 모델에는 양자화 문제를 일으키는 활성값 이상치가 있습니다. 가중치와 활성값 사이의 어려움을 "평활화"함으로써 이를 특별히 해결하는 알고리즘은 무엇일까요?</p>
<style>
.quiz-container-outlier{position:relative}
.quiz-option-outlier{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-outlier:hover{background:#e9ecef}
.quiz-radio-outlier{display:none}
.quiz-radio-outlier:checked+.quiz-option-outlier[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-outlier:checked+.quiz-option-outlier:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-outlier{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#outlier-correct:checked~.feedback-outlier[data-feedback="correct"]{display:block;background:#d4edda;color:#155724}
#outlier-wrong1:checked~.feedback-outlier[data-feedback="wrong1"],#outlier-wrong2:checked~.feedback-outlier[data-feedback="wrong2"],#outlier-wrong3:checked~.feedback-outlier[data-feedback="wrong3"]{display:block;background:#f8d7da;color:#721c24}
</style>
<div class="quiz-container-outlier">
<input type="radio" name="quiz-outlier" id="outlier-wrong1" class="quiz-radio-outlier">
<label for="outlier-wrong1" class="quiz-option-outlier" data-correct="false">🎯 GPTQ</label>
<input type="radio" name="quiz-outlier" id="outlier-wrong2" class="quiz-radio-outlier">
<label for="outlier-wrong2" class="quiz-option-outlier" data-correct="false">🏎️ AWQ</label>
<input type="radio" name="quiz-outlier" id="outlier-correct" class="quiz-radio-outlier">
<label for="outlier-correct" class="quiz-option-outlier" data-correct="true">⚖️ SmoothQuant</label>
<input type="radio" name="quiz-outlier" id="outlier-wrong3" class="quiz-radio-outlier">
<label for="outlier-wrong3" class="quiz-option-outlier" data-correct="false">🗑️ SparseGPT</label>
<div class="feedback-outlier" data-feedback="correct">✅ <strong>정답입니다!</strong> SmoothQuant는 양자화의 어려움을 활성값(이상치가 있는)에서 가중치(다루기 쉬운)로 옮깁니다. 시소의 균형을 맞추는 것과 같습니다!</div>
<div class="feedback-outlier" data-feedback="wrong1">❌ GPTQ는 정확도에는 훌륭하지만 가중치만 양자화합니다. 활성값 이상치를 직접적으로 다루지는 않습니다.</div>
<div class="feedback-outlier" data-feedback="wrong2">❌ AWQ는 "중요한" 채널을 보호하지만 가중치 전용 방법입니다. 활성값 이상치를 다루는 것은 SmoothQuant입니다.</div>
<div class="feedback-outlier" data-feedback="wrong3">❌ SparseGPT는 가중치를 완전히 제거합니다(가지치기)만, 활성값 이상치 문제는 다루지 않습니다.</div>
</div>
</div>

## 치트 시트

아직 확신이 안 드시나요? 다음은 빠른 결정 가이드입니다:

| 여러분의 상황 | 알고리즘 | 이유 |
|----------------|-----------|-----|
| "가능한 최고의 정확도가 필요하다" | GPTQ (g128) | 표준적인 오차 보상 방식 |
| "어제까지 끝내야 했다" | AWQ | 충분히 빠르고 충분히 좋음 |
| "최대 처리량을 위해 W8A8을 원한다" | SmoothQuant | 활성값 양자화에서는 유일한 선택 |
| "최대한 압축하고 싶다" | SparseGPT + GPTQ | 가지치기 + 양자화 조합 |
| "그냥 뭘 써야 할지 알려달라" | GPTQ or AWQ | 실전에서 검증됨, vLLM이 선호함 |

<!-- 🧮 Quiz 2: Pick the Right Algorithm -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">
<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 간단 확인: 알고리즘 선택</h3>
<p style="margin:0 0 12px;color:#666;">기말고사 주간이라 Canopy에 요청이 쏟아지고 있습니다. GPU당 가능한 많은 학생을 서빙하려면 처리량을 최대화해야 합니다. 어떤 접근 방식을 사용해야 할까요?</p>
<style>
.quiz-container-throughput{position:relative}
.quiz-option-throughput{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-throughput:hover{background:#e9ecef}
.quiz-radio-throughput{display:none}
.quiz-radio-throughput:checked+.quiz-option-throughput[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-throughput:checked+.quiz-option-throughput:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-throughput{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#throughput-correct:checked~.feedback-throughput[data-feedback="correct"]{display:block;background:#d4edda;color:#155724}
#throughput-wrong1:checked~.feedback-throughput[data-feedback="wrong1"],#throughput-wrong2:checked~.feedback-throughput[data-feedback="wrong2"],#throughput-wrong3:checked~.feedback-throughput[data-feedback="wrong3"]{display:block;background:#f8d7da;color:#721c24}
</style>
<div class="quiz-container-throughput">
<input type="radio" name="quiz-throughput" id="throughput-wrong1" class="quiz-radio-throughput">
<label for="throughput-wrong1" class="quiz-option-throughput" data-correct="false">🎯 GPTQ with W4A16</label>
<input type="radio" name="quiz-throughput" id="throughput-wrong2" class="quiz-radio-throughput">
<label for="throughput-wrong2" class="quiz-option-throughput" data-correct="false">🏎️ AWQ</label>
<input type="radio" name="quiz-throughput" id="throughput-correct" class="quiz-radio-throughput">
<label for="throughput-correct" class="quiz-option-throughput" data-correct="true">⚖️ SmoothQuant with W8A8</label>
<input type="radio" name="quiz-throughput" id="throughput-wrong3" class="quiz-radio-throughput">
<label for="throughput-wrong3" class="quiz-option-throughput" data-correct="false">🗑️ SparseGPT</label>
<div class="feedback-throughput" data-feedback="correct">✅ <strong>정답입니다!</strong> W8A8(가중치와 활성값 모두 INT8)은 최신 하드웨어에서 INT8 연산이 매우 빠르기 때문에 최대 처리량을 제공합니다. SmoothQuant가 W8A8을 얻는 방법입니다. GPU당 더 많은 학생을 서빙할 수 있습니다!</div>
<div class="feedback-throughput" data-feedback="wrong1">❌ W4A16을 적용한 GPTQ는 메모리 절약과 지연시간에는 훌륭하지만, 최대 처리량을 위해서는 W8A8이 필요합니다. 가중치 전용 양자화는 실제 연산 속도를 그만큼 높이지 못합니다.</div>
<div class="feedback-throughput" data-feedback="wrong2">❌ AWQ는 <em>실행</em>(압축 과정)이 빠르지만, GPTQ처럼 가중치 전용입니다. 최대 서빙 처리량을 위해서는 W8A8이 필요합니다.</div>
<div class="feedback-throughput" data-feedback="wrong3">❌ SparseGPT는 훌륭한 압축률을 제공하지만, 희소성 지원은 하드웨어에 따라 다릅니다. 안정적인 고처리량 서빙을 위해서는 SmoothQuant를 통한 W8A8이 검증된 선택입니다.</div>
</div>
</div>

# ⚡ 고급 양자화: 배포 플레이북

모델을 압축했습니다. 이제 진짜 질문이 등장합니다: *여러분의* 상황에는 *어떤* 압축이 맞을까요?

여기서부터 양자화는 전략적인 영역이 됩니다. 올바른 선택은 하드웨어, 트래픽 패턴, 그리고 얼마나 정확도를 희생할 수 있는지에 따라 달라집니다.

## 표기법 해독하기

"W4A16" 같은 표기법을 어디서나 보게 될 것입니다. 해독 방법은 다음과 같습니다:

**WxAy** = x비트 **가중치(Weights)**, y비트 **활성값(Activations)**

| 방식 | 의미 | 크기 감소 | 최적 지점 |
|--------|-------------|----------------|------------|
| W8A16 | 8비트 가중치, 16비트 활성값 | 약 2배 작아짐 | 안전한 선택, 균형적 |
| W4A16 | 4비트 가중치, 16비트 활성값 | 약 3.5배 작아짐 | 엣지 디바이스, 지연시간이 중요한 경우 |
| W8A8 | 모두 8비트 | 약 2배 작아짐 | 고처리량 서버 |

## 가중치 전용 양자화 vs. 전체 양자화

여기서부터 재미있어집니다. 두 가지 철학이 있습니다:

### "가중치만 압축하자" 접근법 (W4A16 / W8A16)

가중치는 INT4/INT8로 저장하지만, 연산은 FP16으로 수행합니다. 사진을 압축된 JPEG로 저장하지만 RAW로 편집하는 것과 비슷합니다.

**동작하는 이유:**
- 가중치는 정적입니다—한 번 압축하면 영구적으로 이득을 봅니다
- 활성값은 정밀하게 유지됩니다—연산 오차로 인한 정확도 손실이 없습니다
- 메모리 절약으로 더 큰 KV 캐시를 사용할 수 있게 되어 = 더 많은 병렬 요청이 가능해집니다

**수치:** 모델과 GPU에 따라 최대 약 1.5–2.5배. "한 번에 한 학생" 시나리오에 적합합니다.

### "모든 것을 압축하자" 접근법 (W8A8)

가중치*와* 활성값 모두 INT8로. 이것이 처리량을 위한 전략입니다.

**동작하는 이유:**
- INT8 연산은 최신 하드웨어에서 *빠릅니다*
- 피크 시간대에 GPU당 더 많은 학생을 처리할 수 있습니다
- INT8 모델은 FP16 대비 약 1.8–2배의 처리량을 제공하는 경우가 많아, 더 적은 GPU로 큰 모델을 실행할 수 있게 해줍니다.

**함정:** 활성값 이상치를 다스리기 위해 SmoothQuant가 필요합니다.

### 언제 어떤 것을 써야 할까?

의사결정 프레임워크는 다음과 같습니다:

| 트래픽 패턴 | 최선의 선택 | 이유 |
|-----------------|-------------|-----|
| 학생 1명, 빠른 응답이 필요함 | W4A16 | 메모리에 제약이 있음, 지연시간이 우선 |
| 많은 학생, 피크 시간대 | W8A8 | 연산에 제약이 있음, 처리량이 우선 |
| "아직 잘 모르겠다" | W8A16 | 안전한 기본값, 좋은 균형 |

**교차점:** 배치 크기가 작을 때는 가중치 전용이 유리합니다. 배치 크기가 클 때는 W8A8이 유리합니다. 하드웨어에 따라 결과는 달라집니다.

## Group Size: 정밀도 다이얼

원본 값을 재구성하는 데 도움을 주는 작은 숫자들, 스케일에 대해 이야기했던 것을 기억하시나요? Group size는 몇 개의 가중치가 하나의 스케일을 공유하는지를 결정합니다.

**그룹이 작을수록 = 스케일이 더 많아짐 = 정확도가 더 좋아짐 = 파일이 더 커짐**

이미지의 해상도처럼 생각해보세요:

| Group Size | 품질 | 오버헤드 | 사용 시기 |
|------------|---------|----------|-------------|
| 32 | 🏆 최고 | 가장 높음 | 거의 필요하지 않음 |
| 64 | ⭐ 더 좋음 | 더 높음 | 수학 중심 태스크, 코드 생성 |
| **128** | ✅ 좋음 | 균형적 | **여기서 시작하세요 (기본값)** |
| 1024 | 🔽 더 낮음 | 최소 | 속도가 다른 모든 것보다 중요할 때 |

**연구 결과:** 더 작은 그룹(예: 채널 단위 또는 g32)이 최고의 정확도를 제공합니다. g128이 표준적인 균형점입니다.
g1024 같은 더 큰 그룹은 메타데이터를 줄이지만, 모델에 따라 일반적으로 perplexity를 약 0.1–0.3 정도 증가시킵니다.

**원칙:** g128로 시작하세요. 수학이나 코드 태스크에서 벤치마크가 아우성칠 때만 g64로 넘어가세요.

## 출력 형식: 이 모델은 어디에 살게 될까?

모델을 압축했습니다. 이제: 어떤 파일 형식을 쓸까요?

단순히 파일 확장자의 문제가 아닙니다—모델을 *어디서*, *어떻게* 서빙할 것인가의 문제입니다.

### SafeTensors: GPU 표준 🖥️

HuggingFace가 프로덕션 GPU 서빙을 위해 만들었습니다. vLLM이 기대하는 형식입니다.

| 좋은 이유 | 세부 내용 |
|---------------|-------------|
| **안전함** | 취약점이 없습니다(보안팀이 고마워할 것입니다) |
| **빠른 로딩** | 지연 로딩(lazy-loading)과 메모리 매핑 |
| **생태계** | HuggingFace, vLLM, TensorRT-LLM이 모두 이 형식을 사용합니다 |

**사용 대상:** 클러스터의 GPU에서 실행되는 모든 것.

### GGUF: 엣지 형식 📱

Georgi Gerganov가 llama.cpp를 위해 만들었습니다. 노트북, 휴대폰, 그리고 구석에 있는 그 Raspberry Pi에서 모델을 실행하는 방법입니다.

| 좋은 이유 | 세부 내용 |
|---------------|-------------|
| **CPU에 최적화됨** | GPU 없이 추론하기 위해 만들어짐 |
| **유연한 양자화** | Q4_K_M, Q5_K_M, Q8_0—다양한 옵션 |
| **단일 파일** | 하나의 파일 = 배포가 쉬움 |

**사용 대상:** Ollama, llama.cpp, 엣지 디바이스, 오프라인 배포.

### 빠른 참고표

| 모델이 어디로 가나요? | 형식 |
|--------------------------|--------|
| Kubernetes의 vLLM | SafeTensors |
| TensorRT-LLM | SafeTensors |
| Ollama / llama.cpp | GGUF |
| 엣지 디바이스 (CPU) | GGUF |
| 추후 파인튜닝 | SafeTensors |

**워크플로우:** llm-compressor로 압축 → GPU용 SafeTensors. CPU/엣지에 배포할 때만 GGUF로 변환하세요.

<!-- 📦 Quiz: Output Format Selection -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">
<h3 style="margin:0 0 8px;color:#5a5a5a;">📝 간단 확인: 형식 선택</h3>
<p style="margin:0 0 12px;color:#666;">여러분의 팀이 Canopy용 모델을 양자화했습니다. 한 개발자가 "단일 파일이라 관리가 더 쉽다"는 이유로 GGUF를 사용하고 싶어 합니다. 하지만 Canopy는 Kubernetes 클러스터에서 vLLM으로 실행됩니다. 그에게 무엇을 말해줘야 할까요?</p>
<style>
.quiz-container-format{position:relative}
.quiz-option-format{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;transition:.2s;border:2px solid #e9ecef;color:#495057}
.quiz-option-format:hover{background:#e9ecef}
.quiz-radio-format{display:none}
.quiz-radio-format:checked+.quiz-option-format[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.quiz-radio-format:checked+.quiz-option-format:not([data-correct="true"]){background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.feedback-format{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#format-correct:checked~.feedback-format[data-feedback="correct"]{display:block;background:#d4edda;color:#155724}
#format-wrong1:checked~.feedback-format[data-feedback="wrong1"],#format-wrong2:checked~.feedback-format[data-feedback="wrong2"],#format-wrong3:checked~.feedback-format[data-feedback="wrong3"]{display:block;background:#f8d7da;color:#721c24}
</style>
<div class="quiz-container-format">
<input type="radio" name="quiz-format" id="format-wrong1" class="quiz-radio-format">
<label for="format-wrong1" class="quiz-option-format" data-correct="false">📱 GGUF도 괜찮다—단일 파일이 배포하기 더 쉽다</label>
<input type="radio" name="quiz-format" id="format-correct" class="quiz-radio-format">
<label for="format-correct" class="quiz-option-format" data-correct="true">🖥️ SafeTensors를 사용하라—GPU 서빙에서 vLLM이 기대하는 형식이다</label>
<input type="radio" name="quiz-format" id="format-wrong2" class="quiz-radio-format">
<label for="format-wrong2" class="quiz-option-format" data-correct="false">🤷 둘 다 괜찮다, 그냥 하나 고르면 된다</label>
<input type="radio" name="quiz-format" id="format-wrong3" class="quiz-radio-format">
<label for="format-wrong3" class="quiz-option-format" data-correct="false">📦 둘 다로 변환해서 vLLM이 선택하게 하라</label>
<div class="feedback-format" data-feedback="correct">✅ <strong>정확합니다!</strong> GGUF는 CPU 추론(llama.cpp, Ollama)에 최적화되어 있습니다. Kubernetes의 vLLM은 SafeTensors를 기대합니다. 잘못된 형식을 사용하면 로드가 되지 않거나 성능상의 이점을 잃게 됩니다.</div>
<div class="feedback-format" data-feedback="wrong1">❌ GGUF는 llama.cpp와 Ollama에는 훌륭하지만, vLLM은 SafeTensors를 기대합니다. GPU 최적화를 잃거나 로드 자체가 실패할 수 있습니다.</div>
<div class="feedback-format" data-feedback="wrong2">❌ 형식은 중요합니다! GGUF는 CPU에 최적화되어 있고, SafeTensors는 GPU에 최적화되어 있습니다. 잘못된 선택 = 잘못된 성능 또는 호환성 문제입니다.</div>
<div class="feedback-format" data-feedback="wrong3">❌ vLLM은 자동으로 선택하지 않습니다—SafeTensors를 기대합니다. 여분의 형식은 저장 공간만 낭비합니다.</div>
</div>
</div>