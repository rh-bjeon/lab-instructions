# WIP 

# 👤 사용자 경험

> 👤 **페르소나 포커스: 소비자(Consumer)** — 인프라는 잊으세요. 예산도 잊으세요. OAuth 설정도 잊으세요. 여러분은 그냥 AI 모델을 호출하고 싶은 개발자입니다. "엔드포인트와 API 키만 주면, 멋진 걸 만들 수 있어요!"

---

## 🎯 배울 내용

이 레슨에서는 사용자의 관점에서 LiteMaaS를 경험하게 됩니다:

* 🔑 API 키 생성 및 관리하기
* 🚀 첫 API 호출 해보기 (AI의 "Hello World"!)
* 💬 챗봇 플레이그라운드 탐색하기
* 📊 개인 사용량 추적하기

---

## 🌟 셀프서비스 경험

예전 방식을 기억하시나요?

```
Old Way (pre-MaaS):
1. Submit a ticket requesting GPU access
2. Wait 3-5 business days
3. Get access to spin up your own model
4. Figure out how to deploy vLLM
5. Debug why it won't start
6. Finally make an API call
7. Forget about it for 6 months (still consuming GPU)
```

The MaaS way:

```
MaaS Way:
1. Log in
2. Create API key
3. Make API call
4. Build your app
5. Check usage whenever you want
```

[Image: Side-by-side comparison meme:
LEFT: "Deploying my own model" - person climbing a mountain with heavy backpack
RIGHT: "Using MaaS" - person relaxing in a hammock with laptop, calling an API]

---

## 🔐 1단계: 로그인하기

1. 브라우저를 열고 다음 주소로 이동합니다:
   ```
   https://litemaas-<USER_NAME>-maas.apps.<CLUSTER_DOMAIN>
   ```

2. **"Login with OpenShift"**를 클릭합니다
3. OpenShift 자격 증명을 입력합니다
4. 로그인 완료! 🎉

일반 사용자로서, 간소화된 대시보드를 보게 됩니다:

[Image: User dashboard showing:
- Welcome message with username
- Quick stats cards: API Keys (1 active), This Month's Usage ($12.50), Remaining Budget ($87.50)
- Quick actions: "Create API Key", "Open Playground"
- Recent activity feed]

---

## 🔑 2단계: 첫 API 키 만들기

API 키는 AI로 가는 여러분의 티켓입니다. 각 키는:

* 🎫 요청을 인증합니다
* 🤖 특정 모델로 범위를 제한할 수 있습니다
* 💰 자체 예산을 가질 수 있습니다(선택 사항)
* 📊 사용량을 별도로 추적합니다

### 키 만들기

1. 사이드바에서 **"API Keys"**(또는 빠른 작업 버튼)를 클릭합니다
2. **"Create New Key"**를 클릭합니다
3. 세부 정보를 입력합니다:

| 필드 | 값 | 이유 |
|-------|-------|-----|
| **Name** | `my-first-key` | 설명적인 이름은 여러 키를 관리하는 데 도움이 됨 |
| **Description** | `Testing the MaaS platform` | 선택 사항이지만 도움이 됨 |
| **Models** | `granite-8b` 선택 | 이 키가 접근할 수 있는 모델 |
| **Budget** | `$10` (선택 사항) | 키당 지출 한도 |

4. **Create**를 클릭합니다

[Image: Create API Key modal showing:
- Name input field
- Description textarea
- Models multi-select dropdown (checkboxes)
- Budget input with currency symbol
- Create/Cancel buttons]

### ⚠️ 키를 저장하세요!

생성 후, API 키는 **정확히 한 번만** 보게 됩니다:

```
sk-litemaas-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

[Image: Success modal showing:
- Green checkmark
- "API Key Created Successfully!"
- Key displayed in monospace font with copy button
- Warning: "This key will only be shown once. Copy it now!"
- "I've copied my key" button to dismiss]

> 🔒 **보안 참고:** LiteMaaS는 키를 평문으로 저장하지 않습니다. 키를 잃어버리면, 새로 만들어야 합니다.

---

## 🚀 3단계: AI의 "Hello World"

진실의 순간입니다 — 첫 API 호출!

### curl 사용하기

터미널을 열고 다음을 실행하세요:

```bash
curl https://litemaas-<USER_NAME>-maas.apps.<CLUSTER_DOMAIN>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-litemaas-YOUR-KEY-HERE" \
  -d '{
    "model": "granite-8b",
    "messages": [
      {"role": "user", "content": "Hello! What is 2+2?"}
    ]
  }'
```

### 응답

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1699876543,
  "model": "granite-8b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! 2 + 2 equals 4. Is there anything else you'd like to know?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 18,
    "total_tokens": 30
  }
}
```

🎉 **축하합니다!** 방금 첫 MaaS API 호출을 했습니다!

[Image: Celebratory "Achievement Unlocked" style graphic with:
- 🏆 "First API Call!"
- "You're now officially an AI developer"
- Confetti effects]

### Python 사용하기

```python
import requests

url = "https://litemaas-<USER_NAME>-maas.apps.<CLUSTER_DOMAIN>/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-litemaas-YOUR-KEY-HERE"
}
data = {
    "model": "granite-8b",
    "messages": [
        {"role": "user", "content": "Write a haiku about cloud computing"}
    ]
}

response = requests.post(url, json=data, headers=headers)
print(response.json()["choices"][0]["message"]["content"])
```

출력:
```
Servers in the sky,
Data flows like morning mist—
Infinite, yet near.
```

### OpenAI Python SDK 사용하기

LiteMaaS가 OpenAI 호환이므로, 공식 OpenAI SDK를 사용할 수 있습니다:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://litemaas-<USER_NAME>-maas.apps.<CLUSTER_DOMAIN>/v1",
    api_key="sk-litemaas-YOUR-KEY-HERE"
)

response = client.chat.completions.create(
    model="granite-8b",
    messages=[
        {"role": "user", "content": "What's the meaning of life?"}
    ]
)

print(response.choices[0].message.content)
```

> 💡 **이것이 강력한 이유!** OpenAI용으로 만들어진 모든 애플리케이션이 여러분의 프라이빗 MaaS와 함께 동작할 수 있습니다 — `base_url`만 바꾸면 됩니다.

---

## 💬 4단계: 챗봇 플레이그라운드

코드를 작성하고 싶지 않으신가요? 내장된 플레이그라운드를 사용하세요!

1. 사이드바에서 **Playground**로 이동합니다
2. 드롭다운에서 모델을 선택합니다
3. 채팅을 시작합니다!

[Image: Playground interface showing:
- Model selector dropdown (granite-8b selected)
- Chat window with sample conversation
- Message input at bottom
- Settings panel on right: Temperature slider, Max tokens, System prompt
- Token counter showing current session usage]

### 플레이그라운드 기능

| 기능 | 설명 |
|---------|-------------|
| **Model Switching** | 대화 중간에 다른 모델을 시도해보기 |
| **System Prompt** | AI의 성격/행동 설정하기 |
| **Temperature** | 창의성 조절(0 = 집중, 1 = 창의적) |
| **Max Tokens** | 응답 길이 제한하기 |
| **Token Counter** | 실시간 사용량 추적 |
| **Export** | 대화를 JSON으로 다운로드 |

### 실습: 모델 비교하기

여러 모델을 사용할 수 있다면:

1. `granite-8b`에 같은 질문을 합니다
2. 다른 모델로 전환합니다
3. 같은 질문을 다시 합니다
4. 응답을 비교해보세요!

이는 여러분의 사용 사례에 어떤 모델이 가장 잘 맞는지 평가하는 좋은 방법입니다.

---

## 📊 5단계: 사용량 추적하기

책임감 있는 개발자(그리고 예산에 신경 쓰는 사람)로서, 얼마나 사용하고 있는지 알고 싶을 것입니다.

### 개인 대시보드

**Dashboard**로 이동하면 다음을 볼 수 있습니다:

[Image: Personal usage dashboard showing:
- This Month card: $12.50 spent of $100 budget (progress bar at 12.5%)
- Usage Trend: Line graph showing daily usage over past 30 days
- Top Models: Pie chart showing usage by model
- Recent Requests: Table with last 10 API calls]

### 상세 사용량 보기

더 자세한 정보를 보려면 사이드바에서 **Usage**를 클릭하세요:

| 보기 | 보여주는 것 |
|------|-------|
| **By Day** | 일별 토큰 소비량 |
| **By Model** | 가장 많이 사용하는 모델 |
| **By API Key** | 키별 사용량(여러 키를 가지고 있을 때 유용함) |
| **By Application** | 메타데이터로 요청에 태그를 붙인 경우 |

### 토큰 사용량 이해하기

```
Your usage breakdown:
├── Input tokens: 15,234 (prompts you send)
├── Output tokens: 42,891 (responses you receive)
└── Total: 58,125 tokens

Estimated cost: $12.47
├── Input: 15,234 × $0.0005/1K = $7.62
└── Output: 42,891 × $0.0015/1K = $64.34... wait, that's wrong!

Actually:
├── Input: 15.234K × $0.0005 = $0.0076
└── Output: 42.891K × $0.0015 = $0.0643
└── Total: ~$0.07

(Tokens are cheap! The budget is generous for learning.)
```

> 💡 **꿀팁:** 출력 토큰은 생성이 연산적으로 더 비용이 많이 들기 때문에 입력 토큰보다 보통 2-3배 더 비쌉니다.

---

## 🔑 여러 API 키 관리하기

더 많은 애플리케이션을 만들면서, 각각을 위한 별도의 키를 원하게 될 것입니다:

| 키 이름 | 목적 | 예산 |
|----------|---------|--------|
| `dev-testing` | 로컬 개발 및 실험 | $5 |
| `canopy-backend` | 프로덕션 Canopy 애플리케이션 | $50 |
| `jupyter-notebooks` | 데이터 과학 실험 | $20 |

### 모범 사례

1. **애플리케이션당 하나의 키** — 사용량 추적과 필요시 취소가 더 쉬움
2. **설명적인 이름** — 미래의 여러분이 지금의 여러분에게 감사할 것임
3. **개발/프로덕션 키 분리** — 테스트에 프로덕션 키를 사용하지 말 것
4. **정기적인 교체** — 보안을 위해 주기적으로 키를 재생성할 것

### 키 보기

**API Keys**로 이동하면 모든 키를 볼 수 있습니다:

[Image: API Keys list showing:
- Table with columns: Name, Created, Last Used, Models, Budget Used, Status
- Example rows with different keys
- "Create New Key" button
- Actions: View Details, Regenerate, Delete]

> ⚠️ **참고:** 실제 키 값은 볼 수 없습니다 — 메타데이터만 볼 수 있습니다. 키 값이 필요하다면, 새로 만들어야 합니다.

---

## 🎮 실습

### 실습 1: 전용 키 만들기

1. `poetry-generator`라는 새 API 키를 만듭니다
2. 모델 하나에만 접근 권한을 줍니다
3. 예산을 $2로 설정합니다
4. 이를 사용해서 시 5개를 생성합니다

### 실습 2: 플레이그라운드 탐색하기

1. 플레이그라운드를 엽니다
2. 시스템 프롬프트를 설정합니다: "You are a helpful assistant who only responds in rhymes."
3. 날씨에 대해 물어봅니다
4. temperature를 바꿔보고 응답이 어떻게 달라지는지 확인합니다

### 실습 3: 사용량 추적하기

1. 다른 프롬프트로 API 호출을 10번 합니다
2. Usage로 이동해서 오늘의 사용량을 찾습니다
3. 요청당 평균 토큰 수를 계산합니다
4. 어떤 요청이 가장 많은 토큰을 사용했는지 파악합니다

---

## 🧪 지식 확인

<details>
<summary>❓ 왜 애플리케이션마다 별도의 API 키를 만들어야 할까요?</summary>

✅ **답:** 별도의 키는 다음을 제공합니다:
- 더 나은 사용량 추적(어떤 앱이 무엇을 사용하는지 알 수 있음)
- 더 쉬운 취소(한 앱의 키가 유출되어도 다른 앱은 영향받지 않음)
- 애플리케이션별 예산(프로젝트별 비용 통제)
- 더 깔끔한 감사 기록
</details>

<details>
<summary>❓ LiteMaaS를 "OpenAI 호환"으로 만드는 것은 무엇인가요?</summary>

✅ **답:** LiteMaaS는 OpenAI와 동일한 API 형식(`/v1/chat/completions`, 동일한 요청/응답 구조)을 사용합니다. 이는 OpenAI용으로 작성된 모든 애플리케이션이 base URL과 API 키만 바꾸면 LiteMaaS와 함께 동작할 수 있다는 의미입니다.
</details>

<details>
<summary>❓ 왜 출력 토큰이 입력 토큰보다 보통 더 비쌀까요?</summary>

✅ **답:** 출력 토큰은 생성이 필요합니다 — 모델이 "생각"하고 새로운 텍스트를 만들어내야 합니다. 입력 토큰은 그냥 처리되고 이해되기만 하면 됩니다. 생성은 연산적으로 더 비용이 많이 들기 때문에 더 비쌉니다.
</details>

---

## 🎯 달성한 것

소비자로서, 이제 여러분은:

* ✅ 첫 API 키를 만들었습니다
* ✅ AI의 "Hello World" — 첫 API 호출을 했습니다!
* ✅ 챗봇 플레이그라운드를 탐색했습니다
* ✅ 개인 사용량을 추적하는 방법을 배웠습니다

[Image: Achievement badge with "👤 AI Developer" text and subtitle "You're now building with AI — no GPU knowledge required!"]

---

## 🎯 다음 단계

이제 소비자로서 MaaS를 사용하는 방법을 알게 되었습니다. 하지만 큰 그림은 어떨까요? 조직은 *모든 사람*에 걸친 사용량을 어떻게 추적할까요?

📊 **오너/회계 담당자** 모자를 다시 써봅시다 — observability와 차지백에 대해 깊이 알아볼 시간입니다!

**[Usage & Observability](./5-usage-observability.md)로 계속하기** →
