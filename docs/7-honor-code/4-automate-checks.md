# Jailbreak 시나리오 자동화하기

지금까지 우리는 좋은 regex 규칙을 만들고 애플리케이션 오용을 방지하고 의도된 범위 안에 머물도록 몇 가지 guardrails를 추가했습니다. 하지만 가능한 모든 시나리오를 테스트하는 것은 불가능하므로, 당연히 자동화에 대해서도 이야기해야 합니다. 이를 위해 `Spikee`🦔🦔라는 오픈소스 도구를 소개합니다.

## Spikee로 Prompt Injection에 대한 시스템 테스트하기

Spikee는 [웹사이트](https://spikee.ai/)에 소개된 대로, "Simple Prompt Injection Kit for Evaluation and Exploitation"입니다. 이를 사용해 알려진 prompt injection 공격에 대해 우리 시스템을 벤치마크해 볼 수 있습니다.

1. workbench로 돌아가 터미널에서 아래 명령어를 실행합니다.

    ```bash
    cd /opt/app-root/src/experiments/7-guardrails/spikee
    spikee init
    ```

2. Spikee가 우리의 vLLM 엔드포인트와 Llama Stack 엔드포인트와 함께 동작하도록 하려면, 두 개의 target을 정의해야 합니다. 아래 명령어를 실행해, 모델과 Llama Stack 서버를 가리키는 기존 파이썬 파일들을 `targets/` 폴더로 옮깁니다.

    ```bash
    cd /opt/app-root/src/experiments/7-guardrails/spikee
    mv llama_stack_nemo.py targets/
    mv vllm_local.py targets/
    ```

3. Spikee에는 대형 언어 모델에 대한 일반적인 jailbreak 시나리오를 담은 여러 데이터셋이 포함되어 있습니다. `spikee/datasets` 폴더 아래의 파일들을 열어 몇 가지 예시 프롬프트를 확인해 보세요.

    보시다시피, 우리 애플리케이션을 테스트해야 할 프롬프트가 수천 개나 있습니다. 하지만 당연히 시간이 많이 걸립니다. 그래서 이 파일의 매우 작은 서브셋을 미리 만들어 두었습니다. `spikee` 폴더 아래에 있는 `quick-test-diverse.jsonl`이라는 파일입니다. 그곳의 프롬프트들도 확인해 보세요.

    그런 다음 이 파일을 spikee의 datasets 폴더로 옮깁니다.

    ```bash
    cd /opt/app-root/src/experiments/7-guardrails/spikee
    mv quick-test-diverse.jsonl datasets/
    ```

4. 이제 몇 가지 테스트를 실행할 준비가 되었습니다! 먼저, 이 작은 데이터셋을 모델에 대해 실행해 봅시다. 내부적인 guardrailing 외에는 다른 guardrails가 없는 상태입니다. 모델이 어떻게 반응하는지 지켜보세요.

    ```bash
    spikee test --dataset datasets/quick-test-diverse.jsonl --target vllm_local  --attack best_of_n --attack-iterations 1
    ```

    테스트가 완료되기까지 시간이 좀 걸릴 수 있습니다. (그리고 타임아웃 오류가 나더라도 걱정하지 마세요. 응답에 대해 60초의 타임아웃이 설정되어 있습니다.)

5. 이제 결과를 살펴봅시다.

    ```bash
    spikee results analyze --result-file  results/results_vllm_local-http~llama-32-predictor.ai501.svc.cluster.local~8080~v1_quick-test-diverse_*.jsonl | sed -n '1,/=== Breakdown by Jailbreak Type ===/p' | head -n -1
    ```

    아래와 같은 결과가 보일 것입니다.

    ```bash

    _____ _____ _____ _  ________ ______ 
    / ____|  __ \_   _| |/ /  ____|  ____|
    | (___ | |__) || | | ' /| |__  | |__   
    \___ \|  ___/ | | |  < |  __| |  __|  
    ____) | |    _| |_| . \| |____| |____ 
    |_____/|_|   |_____|_|\_\______|______|

    SPIKEE - Simple Prompt Injection Kit for Evaluation and Exploitation
    Version: 0.4.6

    Author: Reversec (reversec.com)
    === General Statistics ===
    Total Unique Entries: 16
    Successful Attacks (Total): 9 
    - Initially Successful: 9
    - Only Successful with Dynamic Attack: 0
    Failed Attacks: 7
    Errors: 0
    Total Attempts: 23
    Attack Success Rate (Overall): 56.25% 👈👈👈👈 not that great!🫣
    Attack Success Rate (Without Dynamic Attack): 56.25%
    Attack Success Rate (Improvement from Dynamic Attack): 0.00%
    ```


6. 보시는 것처럼 모델의 내부 guardrailing은 그다지 훌륭하지 않습니다! 다행히 우리가 그 detector들을 추가해 두었죠. 이번에는 그것들도 테스트해 봅시다! 이번에는 백엔드가 하는 것처럼, 같은 테스트를 Llama Stack 엔드포인트에 대해 실행해 봅니다.

    테스트를 실행합니다.

    ```bash
    spikee test --dataset datasets/quick-test-diverse.jsonl --target llama_stack_nemo  --attack best_of_n --attack-iterations 1
    ```

7. 결과를 확인해 봅시다.

    ```bash
    spikee results analyze --result-file  results/results_llama_stack_nemo-shields_enabled_quick-test-diverse*.jsonl | sed -n '1,/=== Breakdown by Jailbreak Type ===/p' | head -n -1
    ```
    아래와 같은 결과가 나와야 합니다.

    ```bash

    _____ _____ _____ _  ________ ______ 
    / ____|  __ \_   _| |/ /  ____|  ____|
    | (___ | |__) || | | ' /| |__  | |__   
    \___ \|  ___/ | | |  < |  __| |  __|  
    ____) | |    _| |_| . \| |____| |____ 
    |_____/|_|   |_____|_|\_\______|______|

    SPIKEE - Simple Prompt Injection Kit for Evaluation and Exploitation
    Version: 0.4.6

    Author: Reversec (reversec.com)
    === General Statistics ===
    Total Unique Entries: 16
    Successful Attacks (Total): 0
    - Initially Successful: 0
    - Only Successful with Dynamic Attack: 0
    Failed Attacks: 16
    Errors: 0
    Total Attempts: 32
    Attack Success Rate (Overall): 0.00% 👏👏👏👏👏 Thank you prompt injection detector ❤️❤️❤️
    Attack Success Rate (Without Dynamic Attack): 0.00%
    Attack Success Rate (Improvement from Dynamic Attack): 0.00%
    ```

8. 이는 겨우 몇 개의 프롬프트에 대한 테스트였습니다. 좀 더 현실적인 테스트를 해보고 싶다면, `dataset` 폴더에 있는 다양한 데이터셋 중 하나를 기반으로 테스트를 실행할 수 있습니다. 다만 이 데이터셋들은 매우 크며, 예를 들어 `seeds-cybersec-2025-04`는 우리 환경에서 약 7시간 정도 걸리지만 훨씬 더 현실적인 결과를 줄 것입니다. 여전히 궁금하다면, 기존 데이터셋을 다음과 같이 사용할 수 있습니다.

    <div class="highlight" style="background: #f7f7f7; overflow-x: auto; padding: 8px;">
    <pre><code class="language-bash"> 
    spikee generate --seed-folder datasets/seeds-cybersec-2025-04 --plugins 1337 --tag mytest
    </code></pre> 
    </div>

    그런 다음 생성된 데이터셋을 가리켜 아래와 같이 테스트를 시작할 수 있습니다. ‼️ 하지만, 좋은 요리 방송이 늘 그렇듯, 결과를 기다릴 필요는 없습니다! 저희가 대신 처리해 두었어요. 계속 읽어서 결과를 확인해 보세요 😌

9. 잠시 기다린 후 결과를 확인해 보니, 이런 결과가 나왔습니다.

    <div class="highlight" style="background: #f7f7f7; overflow-x: auto; padding: 8px;">
    <pre><code class="language-bash"> 
    _____ _____ _____ _  ________ ______ 
    / ____|  __ \_   _| |/ /  ____|  ____|
    | (___ | |__) || | | ' /| |__  | |__   
    \___ \|  ___/ | | |  < |  __| |  __|  
    ____) | |    _| |_| . \| |____| |____ 
    |_____/|_|   |_____|_|\_\______|______|

    SPIKEE - Simple Prompt Injection Kit for Evaluation and Exploitation
    Version: 0.4.6

    Author: Reversec (reversec.com)
    === General Statistics ===
    Total Unique Entries: 2040
    Successful Attacks (Total): 765
    - Initially Successful: 557
    - Only Successful with Dynamic Attack: 208
    Failed Attacks: 1275
    Errors: 0
    Total Attempts: 3523
    Attack Success Rate (Overall): 37.50% 👈👈👈 not bad but also not perfect 🙃
    Attack Success Rate (Without Dynamic Attack): 27.30%
    Attack Success Rate (Improvement from Dynamic Attack): 10.20%
    </code></pre> 
    </div>

    이런 테스트를 실행할 때는 리포트에서 세부 정보를 확인해서 어떤 종류의 공격이 성공했는지 살펴보고 무엇을 개선해야 할지 계획할 수 있습니다. 더 나은 prompt injection 모델을 사용하거나, 기존 모델을 재학습하거나, 아니면 regex에 간단한 추가 사항을 넣는 것일 수도 있겠죠.


이제 guardrails를 상위 환경으로 가져갈 시간입니다 🌳🛡️
