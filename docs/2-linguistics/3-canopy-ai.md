# 🌿 Canopy란 무엇인가?

**Canopy**는 **Redwood Digital University**의 교육과 학습을 돕는 지능형 어시스턴트입니다. 텍스트 요약부터 퀴즈 생성, 과제 채점까지 다양한 교육 업무를 지원합니다.

## 🎯 이 프론트엔드가 프롬프트 엔지니어링에 중요한 이유

좋은 프롬프트가 좋은 모델 응답을 이끌어내듯, 잘 설계된 사용자 인터페이스는 사용자가 모델의 기능을 자연스럽게 탐색하도록 돕습니다.

GenAI 애플리케이션에서는 어떤 모델을 선택했는지만큼 사용자가 그 모델과 어떻게 상호작용하는지도 중요합니다.

아무리 뛰어난 LLM을 사용해도 UI가 불편하면 모델의 가치를 충분히 활용하기 어렵습니다.

**Canopy**의 이 첫 번째 버전은 다음을 지원하도록 만들어졌습니다.

- 모델의 행동을 정의하는 시스템 프롬프트 🧠

- 무엇을 물을지 정의하는 사용자 프롬프트 💬

- 각 토큰이 피어나는 모습을 볼 수 있는 실시간 스트리밍 출력 🌱

이후 모듈에서는 같은 인터페이스가 정보 검색, 지능형 학생 지원 등을 다룰 수 있도록 발전해 나갈 것입니다.

## 🚀 OpenShift에서 Canopy 시작하기

이제 여러분의 Canopy 인스턴스를 실행해 보겠습니다.

### 📦 1. OpenShift에 프론트엔드 배포하기

OpenShift에는 `<USER_NAME>-canopy`라는 실험 환경이 준비되어 있습니다. 이곳에서 Canopy를 반복해서 개선하고 새로운 기능을 추가하며 프런트엔드를 업데이트합니다.

1. [OpenShift Console](https://console-openshift-console.<CLUSTER_DOMAIN>)로 이동해서 동일한 자격 증명을 입력하세요.

    사용자: `<USER_NAME>`

    비밀번호: `<PASSWORD>`

    로그인 후에는 Projects 페이지가 보일 것입니다.

    ![openshift-console.png](./images/openshift-console.png)

2. 왼쪽 메뉴에서 `Helm` 섹션을 펼치고 `Releases`를 클릭한 다음, `<USER_NAME>-canopy` 프로젝트에 있는지 확인하세요. 그런 다음 오른쪽 상단에서 `Create Helm Release`를 선택하세요. 

    ![add-helm.png](./images/add-helm.png)

3. `Canopy Helm Charts`를 선택하고 배포할 `Canopy UI` 헬름 차트를 클릭하세요.

    ![canopy-helm](./images/canopy-helm.png)

4. `Create`를 누른 다음, `Canopy UI Helm Chart Values Schema`를 펼쳐서 다음과 같이 값을 입력하세요.

    - **MLFLOW_PROMPT_NAME:** 앞에서 레지스트리에 저장한 프롬프트의 이름입니다. 값이 `summarization`인지 확인합니다.

    - **MODEL_NAME:** `llama32`
  
    - **LLM_ENDPOINT:** `https://llama32-ai501.<CLUSTER_DOMAIN>`
    
    **(주의: 캡쳐에 보이는 것과 Value 값 순서가 다를 수 있습니다. 'MLFLOW_TRACKING_URI'가 아닌 'LLM_ENDPOINT' 값을 수정하고 있는지 다시 한번 확인하세요!)**
  
    나머지는 지금은 그대로 두세요.

    ![mlflow-helm-values.png](./images/mlflow-helm-values.png)

    ✅ 이 설정으로 다음 리소스가 생성됩니다.

      - 채팅 요청을 LLM으로 보내는 UBI9 기반 Streamlit 애플리케이션
      - 클러스터 외부에서 앱에 접근할 수 있도록 하는 안전한 OpenShift 라우트

5. 애플리케이션이 성공적으로 실행되면, 파드 오른쪽 상단에 있는 외부 링크 아이콘(↗)을 클릭해서 Canopy UI에 접근하세요 🌳🌳🌳

    ![canopy-ui-ocp.png](./images/canopy-ui-ocp.png)

    _참고: 함께 보이는 다른 파드는 GenAI 플레이그라운드에서 사용합니다._

### 🧪 2. 요약 UI 사용해보기

1. Wikipedia에서 Canopy에 대한 텍스트를 복사할 수 있습니다: https://en.wikipedia.org/wiki/Canopy_(biology). 이를 요약을 위해 애플리케이션에 붙여넣으세요. 텍스트 박스에 내용을 붙여넣고, `Send 💬`를 누른 다음 모델이 실시간으로 요약을 생성하는 모습을 지켜보세요 ✨

    ![summarize-with-canopy](./images/summarize-with-canopy.png)

### ✨ 3. 시스템 프롬프트 업데이트하기

앞에서 선택한 시스템 프롬프트를 레지스트리에 저장했습니다. 이제 Canopy 애플리케이션을 다시 빌드하지 않고 프롬프트를 바꾸어 실험하는 방법을 알아보겠습니다.

1. [OpenShift AI](https://data-science-gateway.<CLUSTER_DOMAIN>/)로 돌아가서 `<USER_NAME>-canopy` 프로젝트 아래의 `Gen AI stuido` > `Prompts` > `Summarization prompt`로 이동하세요. 그리고 `Create prompt version`을 클릭해 새 버전을 등록하세요. 응답에서 알아볼 수 있는 변화를 추가해보세요. 예를 들어 "use bullet points"나 "only respond in emojis" 같은 것을 테스트용으로 시도해볼 수 있으며, 원한다면 처음의 프롬프트로 되돌릴 수도 있습니다(새 버전을 삭제하는 방식으로요. 나중에 더 나은 롤백 방법을 다룰 것입니다). 레지스트리에 저장되어 있으니까요 :)

    ![summarization-prompt-3.png](./images/summarization-prompt-3.png)

2. 그런 다음 [Canopy UI](https://canopy-ui-<USER_NAME>-canopy.<CLUSTER_DOMAIN>)로 가서 페이지를 새로고침하세요. 이전 단계와 같은 요청을 보내고 차이를 확인해보세요!

    _Canopy가 캐시를 무효화하고 새 시스템 프롬프트를 가져오는 데 1~2분 정도 걸립니다. 기다리고 싶지 않다면 파드를 재시작하세요💀_

    코드 수정이나 재배포 없이 프롬프트가 바뀌었습니다. 새 버전이 자동으로 `latest`가 되었고 Canopy가 이 버전을 불러왔기 때문입니다. 다만 운영 환경에서 검증 없이 `latest`를 사용하는 것은 안전하지 않습니다. 다음 장에서는 내부 동작을 살펴보고, 테스트 환경과 운영 환경을 더 안정적이고 재현 가능한 방식으로 구성합니다.

    ![summarization-prompt-4.png](./images/summarization-prompt-4.png)

---

✅ 이번 실습에서 한 일

   - OpenShift에 Canopy 프론트엔드를 배포함

   - 제공된 LLM 엔드포인트에 연결함

   - 어시스턴트의 행동을 결정하는 데 사용되는 최신 시스템 프롬프트를 프롬프트 레지스트리에서 가져옴

   - 프롬프팅과 요약 스타일 사이의 관계를 이해함

</content>
