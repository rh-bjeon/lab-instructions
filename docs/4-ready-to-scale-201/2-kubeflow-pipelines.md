# 파이프라인을 이용한 평가 자동화

평가가 어떻게 동작하는지 알았으니, 이제 파이프라인을 사용하여 이를 자동화해 봅시다! 🎢  

## Kubeflow 파이프라인

평가를 실행하기 위한 파이프라인 프레임워크로 Kubeflow Pipelines를 사용하겠습니다.  
Kubeflow 파이프라인은 Python 기반이며, OpenShift AI 대시보드 내에서 파이프라인 실행을 표시해 주어 OpenShift AI와 잘 연동되기 때문에 데이터 과학/AI 엔지니어링 작업에 편리합니다.


### Kubeflow Pipelines를 위한 환경 설정

항상 그래왔듯, 실험 환경에서 먼저 시작하여 이 자동화를 개발하겠습니다. 하지만 Kubeflow Pipelines를 사용하기 전에, Data Science Pipeline Server와 파이프라인 아티팩트를 저장할 경량 스토리지 옵션인 MinIO를 Canopy 환경에 설치해야 합니다. 이번에도 역시 Helm chart를 사용하겠습니다.

1. `<USER_NAME>-canopy` 프로젝트를 선택합니다.

2. OpenShift Console > `Helm` > `Releases` > `Create Helm Release`로 이동합니다.

    ![dspa-helm-1.png](./images/dspa-helm-1.png)

3. 저장소 목록에서 `GenAIOps Helm Charts`를 선택하고 `Minio`를 선택합니다. 

    ![minio-helm.png](./images/minio-helm.png)

4. `Create`를 클릭한 후, 값을 그대로 두고 다시 `Create`를 클릭합니다.

    ![minio-helm-2.png](./images/minio-helm-2.png)

5. 이제 `Dspa` helm chart에 대해서도 동일하게 수행합니다.

    ![dspa-helm-2.png](./images/dspa-helm-2.png)

6. `Create`를 클릭하고 파이프라인 서버가 준비될 때까지 기다립니다!

    ![dspa-helm-3.png](./images/dspa-helm-3.png)

7. 모두 파란색으로 표시되면 계속 진행해도 좋습니다!
    ![dspa-minio.png](./images/dspa-minio.png)

    > 참고: 브라우저 탭을 닫고 다시 여는 것으로는 충분하지 않으므로, workbench를 정지한 후 다시 시작하여 재시작해 주세요. DataSciencePipelineApplication(```dspa```)이 생성되면 Workbench 구성 내부에 일부 변수가 주입되는데, 이 변수들은 런타임 중에는 적용되지 않기 때문에 완전한 재시작이 필요합니다.

### 평가 파이프라인 설정하기

이제 실험 네임스페이스에서 파이프라인을 실행할 수 있도록 모든 준비가 끝났으니, 코드를 살펴보고 실행해 봅시다!  
평가 파이프라인은 `evals`라는 저장소 안에 있으며, 평가 테스트와 파이프라인 정의가 함께 저장되어 있습니다. 

1. 이를 살펴보려면 workbench로 돌아가서 저장소를 클론하세요.

   ```bash
   cd /opt/app-root/src/
   git clone https://<USER_NAME>:<PASSWORD>@gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/evals.git
   ```

2. 그 안에는 몇 개의 폴더가 있는데, 하나는 `evals-pipeline`이고, 나머지는 평가를 실행하고자 하는 각 사용 사례별 폴더입니다. 지금 우리에게 관련 있는 것은 `summarization` 뿐이며, 나머지는 다가올 모듈들에 대한 약간의 스포일러입니다 🤫  

    `evals/summarization/summary_tests.yaml`을 열어서 어떤 테스트를 실행할지 살펴보세요. 여러분만의 예제도 몇 가지 추가해 보세요 ✍️

    ![summary_test.png](images/summary_tests.png)

    예를 들면:

    ```yaml
      - inputs:
          messages:
              - role: "user"
                content: "The Forest Canopy Structure course at Redwood Digital University covers the vertical layering of forest ecosystems, including the emergent, canopy, understory, and forest floor layers. Each layer supports distinct plant and animal communities adapted to the varying light, temperature, and humidity conditions found at different heights."
          session_id: "test-session-004"
        expectations:
          expected_result: "The course covers forest ecosystem layers - emergent, canopy, understory, and forest floor - each with distinct communities adapted to their light, temperature, and humidity conditions."

    ```

    _**이전에 혼이 난 경험이 있는 사람으로서 경고 한마디:** YAML은 스페이스바를 숭배하는 종교입니다. 자신만의 평가를 추가할 때는 공백에 주의하세요. 🥲_

3. 이러한 평가를 실행하는 Kubeflow 파이프라인의 코드는 `evals-pipeline/mlflow_pipeline.py` 안에 있습니다. 이를 열어서 살펴보세요. 파일 상단 근처(19번째 줄 부근)에서, `repo_url` 인자에 필요한 변수들을 다음과 같이 수정합니다.
    ```python
    # 🚨 replace with your own user details and repo URL
    USER_NAME="Your user name"
    PASSWORD="Your password"
    GIT_SERVER="Your Gitea host"  # Without the https://
    ```
    ⚠️ 이 변수들은 파일 하단에서 `repo_url` 인자를 구성하는 데 사용되며, 이는 파이프라인이 `evals` 저장소를 클론하고 방금 보았던 테스트를 실행하기 위해 필요합니다. 반드시 본인의 값으로 교체하세요!


4. 변경 사항을 push 합시다.

    ```bash
    cd /opt/app-root/src/evals
    git add .
    git commit -m  "🧑‍⚖️ Update evals pipeline 🧑‍⚖️"
    git push origin main
    ```

5. 이제 파이프라인을 실행할 수 있습니다! 🙌  

    터미널에서 다음을 실행하세요.

    ```bash
    cd /opt/app-root/src/evals
    python evals-pipeline/mlflow_pipeline.py
    ```
    다음과 같은 출력이 보일 것입니다.

    ![trigger-kfp.png](./images/trigger-kfp.png)

    그리고 OpenShift AI 대시보드 > `Develop & train` > `Pipelines` > `Runs`로 이동합니다.

    ![running-kfp-pipeline](images/running-kfp-pipeline.png)

6.  실행이 완료되면, `<USER_NAME>-canopy` 작업 공간의 Experiments (MLFlow)에서, `summarization` 실험의 왼쪽 메뉴 `Evaluation runs` 아래에서 결과를 확인할 수 있습니다.

![summary_eval](./images/summary_eval.png)

다음 섹션에서는 system prompt와 같은 변경 사항이 발생했을 때 이 파이프라인을 자동으로 트리거하는 방법을 살펴보겠습니다. 

그리고 GuideLLM 테스트도 잊지 말아야겠죠!
