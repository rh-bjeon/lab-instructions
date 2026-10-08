# 🧠 LLM의 메모리와 처리 과정 :id=memory-and-processing-in-llms

## 📚 목차 :id=contents
- [🧠 LLM의 메모리와 처리 과정](#memory-and-processing-in-llms)
  - [📚 목차](#contents)
  - [👀 어텐션(Attention) 메커니즘](#attention-mechanism)
  - [⚡ KV 캐시와 성능](#kv-cache-and-performance)

## 👀 어텐션(Attention) 메커니즘 :id=attention-mechanism

언어 모델은 문장에서 어느 부분이 가장 중요한지 어떻게 알까요? 바로 여기서 **어텐션**(attention)이 등장합니다.

어텐션은 스포트라이트와 같습니다 — 응답을 생성할 때 모델이 가장 중요한 단어에 집중할 수 있도록 도와줍니다.

예시:
> "When the student finished the exam, they felt relieved."

"they"를 이해하기 위해, 모델은 "the student"에 주의를 기울입니다.

모델은 단순히 마지막 단어만 보는 것이 아니라, 뒤를 돌아보며 어떤 단어가 가장 맥락에 맞는지 파악합니다.

이것이 바로 LLM이 똑똑하게 느껴지는 이유입니다. 긴 텍스트에 걸쳐 의미를 계속 추적할 수 있기 때문입니다.

<img src="https://huggingface.co/datasets/agents-course/course-images/resolve/main/en/unit1/AttentionSceneFinal.gif" alt="어텐션을 보여주는 시각적 GIF" width="60%">

이것이 어떻게 작동하는지 퀴즈로 확인해 봅시다.

<!-- 👀 Attention – who gets the weight? -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">👀 퀴즈</h3>

<p style="color:#495057;font-weight:500;">
모델이 <em>밑줄 친</em> 단어를 생성하려는 상황입니다.<br>
"<u>surprised</u> the crowd with a thunderous drum roll."<br>
지금까지의 프롬프트:
</p>

<p style="border-left:3px solid #bbb;padding-left:10px;margin:8px 0;color:#444;">
"The <b>drummer</b> practiced quietly backstage while the <b>singer</b> warmed up.  
Just before the <b>finale</b>, the <b>drummer</b> nodded and then..."
</p>

<p style="color:#495057;font-weight:500;">
"surprised"를 예측할 때, 어텐션 메커니즘이 이전 토큰 중 <b>가장 높은 가중치</b>를 부여할 토큰은 무엇일까요?</p>

<style>
.attnOpt{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;
        border:2px solid #e9ecef;color:#495057;transition:.2s}
.attnOpt:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.attnRadio{display:none}
.attnRadio:checked + .attnOpt[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.attnRadio:checked + .attnOpt[data-correct="false"]{background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.attnFeed{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#attn-good:checked ~ .attnFeed[data-type="good"],
#attn-w1:checked  ~ .attnFeed[data-type="bad1"],
#attn-w2:checked  ~ .attnFeed[data-type="bad2"]{display:block}
.attnFeed[data-type="good"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.attnFeed[data-type="bad1"], .attnFeed[data-type="bad2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div>
  <input type="radio" id="attn-w1" name="attn" class="attnRadio">
  <label for="attn-w1" class="attnOpt" data-correct="false">
    🎤 "singer"
  </label>

  <input type="radio" id="attn-good" name="attn" class="attnRadio">
  <label for="attn-good" class="attnOpt" data-correct="true">
    🥁 "drummer"
  </label>

  <input type="radio" id="attn-w2" name="attn" class="attnRadio">
  <label for="attn-w2" class="attnOpt" data-correct="false">
    🏟️ "crowd"
  </label>

  <div class="attnFeed" data-type="good">
    ✅ 정답입니다 — 어텐션은 문장을 일관되게 만드는 토큰에 집중합니다. 깜짝 놀라게 한 주체는 바로 <b>drummer</b>입니다.
  </div>
  <div class="attnFeed" data-type="bad1">
    ❌ "singer"는 앞서 언급되었지만, 이 맥락에서 능동적인 주체는 아닙니다.
  </div>
  <div class="attnFeed" data-type="bad2">
    ❌ "crowd"는 문장 뒤쪽에 등장하며, 행위의 주체가 아닙니다.
  </div>
</div>
</div>

---

## ⚡ KV 캐시와 성능 :id=kv-cache-and-performance

답변을 생성하는 데는 시간이 걸릴 수 있습니다 — 특히 긴 응답일 경우에는 더욱 그렇습니다. 그렇다면 LLM은 어떻게 빠른 속도를 유지할까요?

바로 **KV 캐시(KV cache)**, 즉 *Key-Value cache*라는 것을 사용합니다.

모델은 생성하는 단어마다 처음부터 다시 계산하는 대신, 이미 계산한 것("지금까지의 사고 과정")을 저장해두고 재사용합니다. 메모장에 메모를 남겨두는 것과 비슷합니다.

이렇게 하면 엄청난 시간을 절약할 수 있습니다.

![KV 캐시 자기회귀(autoregression) 다이어그램](https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/kv-cache/autoregression.png)

이점:

- 더 빠른 응답
- 중복 작업 감소
- 채팅 앱에서 더 부드러운 경험
- 스트리밍 출력 가능(텍스트를 단어 단위로 보여주는 방식 등)

하지만 이러한 이점에는 더 많은 GPU 메모리가 필요하다는 대가가 따릅니다. 이제 이 모든 계산 결과를 어딘가에 저장해야 하기 때문입니다.

하지만 KV 캐시에 필요한 추가 메모리가 얼마나 되는지 계산하는 일은 다소 까다로울 수 있습니다.
다행히 특정 모델에 대해 이를 계산해주는 도구들이 있습니다. 예를 들어 다음 도구를 한번 사용해 보세요: [https://lmcache.ai/kv_cache_calculator.html](https://lmcache.ai/kv_cache_calculator.html)

<!-- ⚡ KV cache – concept focus -->
<div style="background:linear-gradient(135deg,#e8f2ff 0%,#f5e6ff 100%);
            padding:20px;border-radius:10px;margin:20px 0;border:1px solid #d1e7dd;">

<h3 style="margin:0 0 8px;color:#5a5a5a;">⚡ 퀴즈</h3>

<p style="color:#495057;font-weight:500;">
KV 캐시를 켠 상태에서는 1,000 토큰이 2초 만에 스트리밍됩니다.  
캐시를 끄면 → 6초가 걸립니다.<br>
<strong>실제로 캐시된 것은 무엇이며, 왜 속도가 빨라질까요?</strong>
</p>

<style>
.kvOpt{display:block;margin:4px 0;padding:8px 16px;background:#f8f9fa;border-radius:6px;cursor:pointer;
       border:2px solid #e9ecef;color:#495057;transition:.2s}
.kvOpt:hover{background:#fff;transform:translateY(-1px);border-color:#dee2e6}
.kvRadio{display:none}
.kvRadio:checked + .kvOpt[data-correct="true"]{background:#d4edda;color:#155724;border-color:#c3e6cb}
.kvRadio:checked + .kvOpt[data-correct="false"]{background:#f8d7da;color:#721c24;border-color:#f5b7b1}
.kvFeed{display:none;margin:4px 0;padding:8px 16px;border-radius:6px}
#kv-good:checked ~ .kvFeed[data-type="good"],
#kv-w1:checked  ~ .kvFeed[data-type="bad1"],
#kv-w2:checked  ~ .kvFeed[data-type="bad2"]{display:block}
.kvFeed[data-type="good"]{background:#d1f2eb;color:#0c5d56;border:1px solid #a3d9cc}
.kvFeed[data-type="bad1"], .kvFeed[data-type="bad2"]{background:#fce8e6;color:#58151c;border:1px solid #f5b7b1}
</style>

<div>
  <input type="radio" id="kv-w1" name="kv" class="kvRadio">
  <label for="kv-w1" class="kvOpt" data-correct="false">
    📝 모든 출력 토큰의 복사본을 저장해 다시 생성할 필요가 없도록 한다.
  </label>

  <input type="radio" id="kv-good" name="kv" class="kvRadio">
  <label for="kv-good" class="kvOpt" data-correct="true">
    🔑 이전 토큰들에 대한 어텐션 계산 결과를 저장해, 매번 다시 계산하지 않고 재사용한다.
  </label>

  <input type="radio" id="kv-w2" name="kv" class="kvRadio">
  <label for="kv-w2" class="kvOpt" data-correct="false">
    📉 토큰 임베딩을 압축해 메모리만 줄이고, 연산량은 줄이지 않는다.
  </label>

  <div class="kvFeed" data-type="good">
    ✅ 정확합니다. KV 캐시는 모델의 모든 내부 구성 요소에 대한 어텐션 계산 결과를 담은 "커닝지"를 유지합니다. 이것이 있으면 새 토큰 하나를 생성하는 데 거의 비용이 들지 않지만, 없으면 모델은 <em>이전의 모든</em> 토큰에 대해 무거운 연산을 다시 수행해야 합니다.
  </div>
  <div class="kvFeed" data-type="bad1">
    ❌ 가능한 모든 토큰의 조합을 저장하고 그중에서 고르는 것은 그냥 생성하는 것보다 오히려 더 비용이 많이 들어 보입니다 😩
  </div>
  <div class="kvFeed" data-type="bad2">
    ❌ KV 캐시가 메모리를 사용하긴 하지만, 가장 큰 이점은 메모리 효율이 아니라 연산 속도입니다.
  </div>
</div>
</div>

[🔝 목차로 돌아가기](#contents)</content>
