# 📘 Workbench를 통해 모델과 상호작용하기

계속 진행하기 전에, 방금 배포한 Canopy 애플리케이션에서 사용하고 있는 주요 구성 요소들을 살펴보겠습니다.

   - **OpenAI 호환 클라이언트** — 모델에 프롬프트를 전송하기 위한 클라이언트
   - **MLflow** — 프롬프트를 관리하고 상호작용을 추적하기 위한 도구

이번 섹션에서는 Red Hat OpenShift AI에서 Workbench를 실행하여 Code Server 환경을 구성합니다. 이를 통해 브라우저 기반 IDE를 사용하여 Python 노트북을 실행하고, 모델 및 MLflow와 프로그래밍 방식으로 상호작용할 수 있습니다.

이 환경을 사용하여 다음을 수행하게 됩니다.

- OpenAI 호환 API 살펴보기
- 코드에서 직접 테스트 프롬프트 전송하기
- 모델에 연결하고, 레지스트리에서 프롬프트를 가져오며, 프런트엔드로부터의 요청을 처리하는 백엔드 구축하기

이 섹션을 마치면 모델을 자신만의 워크플로우와 애플리케이션에 통합하는 방법을 더 잘 이해하게 되고, 더 고급 사용 사례를 위한 토대를 마련하게 됩니다.

1. [OpenShift AI](https://data-science-gateway.<CLUSTER_DOMAIN>/)로 다시 이동합니다.

   ![openshift-ai.png](./images/openshift-ai.png)

2. Workbench를 생성해 봅시다!   

   `<USER_NAME>-canopy` 프로젝트를 클릭한 다음 `Create a Workbench`를 클릭합니다. OpenShift AI 대시보드가 꽤 직관적이지 않나요? :)
   
   ![create-workbench.png](./images/create-workbench.png)

3. 이름을 `<USER_NAME>-canopy` 🌳 로 지정합니다.

    **Notebook Image:** 

    - 이미지 선택: `AI501 - Custom Code Server` (목록 맨 끝에 있습니다😌)
  
    **Deployment size**
    - Hardware profile: `default-profile`

    **Environment variables**
    - 지금은 추가할 필요가 없습니다.

    **Cluster storage**
    - 최대 20 GiB로 그대로 둡니다.

    **Connections**
    - 그대로 둡니다. 지금은 별도의 연결 정의가 필요하지 않습니다.

    마지막으로 `Create workbench`를 클릭합니다.

Status가 Ready가 되면 이름을 클릭하여 열고, 자격 증명을 사용하여 접속합니다.

   ![open-workbench.png](./images/open-workbench.png)

4. 왼쪽 상단의 햄버거 메뉴를 클릭한 다음 메뉴에서 `Terminal` > `New Terminal`을 선택하여 새 터미널을 엽니다.

   ![code-server-terminal.png](./images/code-server-terminal.png)

5. 몇 가지 노트북이 포함된 Canopy 실험용 저장소를 클론하고, Llama Stack에 대해 더 알아봅시다!

   ```bash
   git clone https://<USER_NAME>:<PASSWORD>@gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/experiments.git
   ```

6. `3-ready-to-scale-101/1-intro-openai-mlflow.ipynb` 라는 노트북을 열고 안내에 따라 진행합니다. 첫 번째 코드 셀을 실행하면 커널을 선택하라는 메시지가 표시됩니다. 첫 번째 옵션을 선택합니다. 이는 이 workbench 내에서 로컬로 코드를 실행한다는 의미입니다.

   ![choose-python-env.png](./images/choose-python-env.png)

   그 다음 사용할 Python 환경을 선택하라는 메시지가 표시됩니다. `Virtual Env`를 선택합니다.

   ![choose-python-env2.png](./images/choose-python-env2.png)

   이제 자유롭게 실험해 보세요! 노트북의 셀을 읽고 실행해 보세요! 완료되면 다시 이곳으로 돌아오세요 :)

이제 이러한 실습을 위한 작업 공간을 설정하고, 모델과 상호작용하는 과정을 직접 체험해 보았습니다.
