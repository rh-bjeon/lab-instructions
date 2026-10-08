# 🧑‍🏫📚 GenAIOps Enablement 실습 가이드 (AI501)

## 슬라이드
슬라이드는 실습 가이드와 함께 게시됩니다.

👨‍🏫 👉 [여기서 게시된 슬라이드를 볼 수 있습니다](https://rhoai-genaiops.github.io/lab-instructions/slides/ai501-index.html) 👈 🧑‍💻

## 🪄 가이드 내용 맞춤 설정하기
페이지 상단의 입력창을 이용하면 여러분 팀의 값을 미리 채운 상태로 문서를 볼 수 있습니다. 아래 항목을 입력하고 **저장** 버튼을 누르세요:

1. **사용자 이름** — 예: `user1`. 이 값은 우리가 사용하는 네임스페이스 등의 접두사로 쓰입니다.
2. **비밀번호** — 여러분의 실습 비밀번호.
3. **클러스터 도메인** — OpenShift 도메인 중 `apps.*` 부분(아래 설명 참고).

입력한 값은 브라우저의 로컬 스토리지에 저장됩니다. 저장된 값을 모두 초기화하려면 **초기화** 버튼을 누르세요.

> OpenShift 상에 배포된 환경이라면, Deployment의 환경변수(`user`, `password`, `openshift_cluster_ingress_domain`, `gitea_console_url`)에 값이 미리 설정되어 있어 위 입력창이 자동으로 채워집니다. 이 경우 직접 입력할 필요 없이 그대로 사용하면 되고, 필요할 때만 값을 수정해 다시 저장하면 됩니다.

* 저장한 뒤에는 아래와 같이 사용자 이름과 비밀번호가 보여야 합니다:

    ```bash
    <USER_NAME>
    <PASSWORD>
    ```

* 클러스터 도메인에는 OpenShift 도메인 중 `apps.*` 부분만 입력하세요. 예를 들어 콘솔 주소가 <code class="language-yaml">https://console-openshift-console.apps.hivec.sandbox1243.opentlc.com/</code> 라면
 클러스터 도메인 입력창에는 `apps.hivec.sandbox1243.opentlc.com`을 입력하면 됩니다.

    아래와 같이 클러스터 도메인이 보여야 합니다:

    ```bash
    <CLUSTER_DOMAIN>
    ```

## 🦆 작성 규칙
실습을 진행하는 동안, 특히 Notebook에서 값을 바꿔야 하는 부분을 표시해두었습니다. 위에서 값을 저장했다면 대부분의 `<PLACEHOLDER>` 값은 자동으로 채워집니다. 혹시 남아있는 값이 있다면 직접 실제 값으로 바꿔주세요. 예를 들어 사용자 이름이 `user1`인데 `<\USER_NAME>`이 보인다면, 아래처럼 바꾸면 됩니다:
    <div class="highlight" style="background: #f7f7f7">
    <pre><code class="language-bash">
    name: &lt;USER_NAME&gt;
    # ^ 이 부분이 아래처럼 바뀝니다
    name: user1
    </code></pre></div>

복사해서 사용할 수 있는 코드 블록이 많이 있습니다. 코드 블록 위에 마우스를 올리면 오른쪽에 ✂️ 아이콘이 나타납니다.

```bash
    echo "like this one :)"
```

**중요:** 모든 코드 블록을 복사해서 실행하는 것은 아닙니다. ✂️ 아이콘이 없는 블록은 **예상 출력 결과**입니다. 여러분의 실행 결과나 YAML을 해당 블록과 비교해 확인하는 용도로 사용하세요.

자, 이제 시작해봅시다! 첫 번째 챕터로 이동해서 GenAIOps 여정을 시작하세요! 🏃💨
