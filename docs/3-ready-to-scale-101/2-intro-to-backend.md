# Canopy Backend

LLM 비즈니스 로직을 프런트엔드에서 분리하여 별도의 백엔드로 구성함으로써, 각각을 독립적으로 반복 개발할 수 있도록 하겠습니다.

1. 다른 구성 요소들을 배포했던 것과 동일한 방식으로 개발 환경에 백엔드를 배포하겠습니다. `<USER_NAME>-canopy` 프로젝트에서 OpenShift Console > `Helm` > `Releases`로 다시 이동합니다.
   
   ![canopy-be-helm-releases.png](./images/canopy-be-helm-releases.png)

2.  `Chart Repositories`에서 `Canopy Helm Charts`를 선택하고 `Canopy Backend` > `Create`를 클릭합니다.

    ![canopy-be-helm.png](./images/canopy-be-helm.png)

3. `YAML view`를 엽니다. 여기에는 많은 기본 변수들이 있습니다. 지금은 신경 쓰지 말고, 아래에 제공된 값으로 덮어쓰기만 하면 됩니다.

    앞서 설명했듯이, 백엔드는 모델 및 레지스트리 등과 통신하는 역할을 담당합니다. 따라서 올바른 연결 정보를 제공해야 합니다.

    또한 선택한 System Prompt도 제공해야 합니다. 노트북에서 했던 것처럼, 모델을 호출할 때 system prompt를 포함해야 합니다.

    상자의 내용을 삭제하고 아래 YAML 스니펫을 그대로 복사해 넣으세요 🙏

    ```yaml
    summarization:
      enabled: true
      model: llama32
      endpoint: 'http://llama-32-predictor.ai501.svc.cluster.local:8080/v1'
      mlflow_prompt_version: latest
      mlflow_prompt: summarization # 👈 your prompt registry entry 
    ```

    ![canopy-be-values.png](./images/canopy-be-values.png)
 
    ..나머지는 기본값으로 두고 `Create`를 클릭합니다.

4. OpenShift Console에서 정상적으로 실행되고 있는지 확인합니다.
   
   ![canopy-be-ocp.png](./images/canopy-be-ocp.png)


## Canopy Frontend 업데이트

1. 이제 Canopy UI가 LLM에 직접 요청을 보내는 대신 백엔드와 통신하도록 할 차례입니다. 이를 위해서는 helm chart의 일부 값을 업데이트해야 합니다. `Workloads` > `Topology` 뷰에서 `canopy-ui`라는 이름의 프런트엔드를 찾고, 그 아래의 세 개의 점을 클릭한 다음 `Upgrade`를 클릭합니다.

    ![update-canopy-ui.png](./images/update-canopy-ui.png)

2. values에서 `Form view`를 열고 `BACKEND_ENDPOINT` 키를 찾아 아래 값을 추가합니다.
   
    ```bash
    http://canopy-backend:8000
    ```

    ![update-canopy-ui-2.png](./images/update-canopy-ui-2.png)

3. 그 다음 조금 아래로 내려가 `image` 값을 펼치고 태그를 더 새로운 버전으로 업데이트합니다.
   
   - tag: **0.12** (`simple-0.5`를 `0.12`로 교체합니다.)
  
  ..그리고 이제 `Upgrade`를 클릭합니다!

    ![update-canopy-ui-3.png](./images/update-canopy-ui-3.png)

1. 작은 화살표를 클릭하고 UI에 접속하여 Canopy UI가 여전히 예상대로 동작하는지 확인합니다.
   
   ![update-canopy-ui-4.png](./images/update-canopy-ui-4.png)

2. 다시 한 번 텍스트 요약을 요청해 보세요!

    ```
    Tea preparation involves the controlled extraction of bioactive compounds from processed Camellia sinensis leaves. Begin by heating water to near 100°C to optimize solubility. Introduce a tea bag to a ceramic vessel, then infuse with hot water to initiate steeping—typically 3–5 minutes to allow for the diffusion of polyphenols and caffeine. Upon removal of the bag, optional additives like sucrose or lipid-based emulsions may be introduced to alter flavor profiles. The infusion is then ready for consumption.
    ```
   
   ![canopy-ui-after-backend.png](./images/canopy-ui-after-backend.png)

Canopy 학생 도우미의 첫 번째 반복 버전에 만족했으니, 이제 실제 사용자들의 손에 전달할 차례입니다. 이를 위해서는 지금까지 구축한 모든 것을 테스트 환경, 그리고 궁극적으로는 프로덕션 환경에 배포해야 합니다. 하지만 이번에는 더 견고하고, 일관되며, 반복 가능한 방식으로 진행하겠습니다. 그래서 우리는 이제 GitOps 🐙 의 세계로 들어가게 됩니다.

조기에 릴리스함으로써 더 빠르게 피드백을 받을 수 있고, 너무 많은 투자를 하기 전에 방향을 수정할 수 있습니다. 

그리고 자동화와 GitOps에 투자함으로써 더 자주 릴리스할 수 있습니다! 

  ![keep-calm.png](./images/keep-calm.png ':size=300 :class=center')
