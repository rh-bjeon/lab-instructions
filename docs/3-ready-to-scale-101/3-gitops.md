# 🐙 Argo CD - GitOps 컨트롤러 

GitOps는 개발 워크플로와 모델·애플리케이션 배포를 일관된 방식으로 자동화합니다. 모든 구성을 버전으로 관리하므로 변경 이력을 추적할 수 있고 같은 환경을 다시 만들기도 쉽습니다. Git을 단일 기준 정보원(single source of truth)으로 삼으면 팀은 변경 사항과 구성을 한곳에서 관리하고, 모델과 애플리케이션이 선언한 상태로 배포되도록 유지할 수 있습니다.

이번 실습에서는 Argo CD를 GitOps 엔진으로 사용합니다.

## Argo CD Application
Argo CD는 널리 사용되는 GitOps 도구입니다. Git 저장소에 선언된 상태와 OpenShift 클러스터의 실제 상태를 지속적으로 비교하고, 두 상태가 일치하도록 조정(reconcile)합니다.

GenAIOps에서는 Argo CD로 애플리케이션과 도구, 모델을 반복 가능하게 배포합니다. 배포 구성을 Git에 YAML 파일로 저장하면 Argo CD가 이를 자동으로 클러스터에 적용하므로 배포 과정이 더 효율적이고 일관됩니다. :)

이제 GitOps 기반을 구성하고, 지금까지 사용한 구성 요소를 Argo CD를 통해 `<USER_NAME>-test`와 `<USER_NAME>-prod` 환경에 배포하겠습니다.

1. 먼저 GitOps와 Argo CD의 기본 사용법을 익혀보겠습니다. Argo CD 인스턴스는 `<USER_NAME>-toolings` 환경에 이미 설치되어 있습니다. 오른쪽 상단의 `바로가기`에서 `GitOps`를 선택하거나 Workbench 터미널에서 아래 명령을 실행해 접속 주소를 확인합니다.
   
   * 참고: 로컬 시스템에 `oc` CLI가 설치되어 있다면 사용해도 됩니다. 환경 차이로 생기는 문제를 피하려면 앞에서 만든 VS Code Workbench의 터미널을 사용하는 편이 가장 간단합니다. 브라우저 기반 컨테이너 환경이므로 로컬 시스템의 구성과 관계없이 같은 명령을 실행할 수 있습니다.

## 클러스터에 로그인하기

명령줄을 통해 OpenShift와 상호작용하려면 클러스터에 로그인해야 합니다. Visual Studio Code의 터미널 창을 사용하세요. 

  ```bash
    export CLUSTER_DOMAIN=<CLUSTER_DOMAIN>
    oc login --server=https://api.${CLUSTER_DOMAIN##apps.}:6443 -u <USER_NAME> -p <PASSWORD>
  ```

  다음 명령으로 URL을 확인하여 Argo CD에 접속합니다. 현재 가이드 오른쪽 상단의 `바로가기`를 사용해도 됩니다.

  ```bash
    echo https://$(oc get route argocd-server --template='{{ .spec.host }}' -n <USER_NAME>-toolings)
  ```

2. `Log in via OpenShift`를 클릭하여 Argo CD에 로그인하고, 제공된 OpenShift 자격 증명을 사용합니다. (우측 상단의 `내 정보 복사` 버튼을 활용하면 사용자 이름과 비밀번호를 바로 복사해서 사용할 수 있습니다!)

  ![argocd-login.png](./images/argocd-login.png)

3. 처음 로그인할 때는 `Allow selected permissions`를 선택합니다.

4. Argo CD 로그인이 완료되었습니다. 👏👏👏 GenAIOps 배포를 구성하기 전에 UI에서 샘플 애플리케이션을 직접 배포해 보겠습니다. `CREATE APPLICATION`을 클릭하고 아래 값을 입력합니다. 일부 항목은 입력란을 클릭하면 선택 목록이 나타납니다.

   * "GENERAL" 상자에서
      * Application Name: `token-visualizer` 
      * Project Name: `default`
      * Sync Policy: `Automatic`
   * "SOURCE" 상자에서
      * Repository URL: `https://rhoai-genaiops.github.io/genaiops-helmcharts/`
      * 우측 GIT/HELM 드롭다운 메뉴에서 `Helm` 선택 (바로 변경되지 않으면 잠시 기다리거나, URL 칸을 마우스로 한번 클릭하고 기다려보세요)
      * Chart: `token-visualizer`
      * Version: `1.0.2`
   * "DESTINATION" 상자에서
      * Cluster URL: `https://kubernetes.default.svc`
      * Namespace: `<USER_NAME>-toolings`
   * `Directory` 드롭다운을 `Helm`으로 변경하고 다음을 설정
      * Values Files: `values.yaml`
        
        참고: 드롭다운 메뉴 항목이 이미 `Helm`으로 선택되어 있을 수도 있습니다.   

    양식은 다음과 같아야 합니다.
    
    ![argocd-create-application](images/argocd-create-application.png)

5. 화면 위쪽의 `Create`를 클릭하면 `token-visualizer` 애플리케이션이 생성되어 `<USER_NAME>-toolings` 네임스페이스에 배포되기 시작하는 것을 볼 수 있습니다.

  ![argocd-token-visualizer-1.png](./images/argocd-token-visualizer-1.png)

6. 애플리케이션을 클릭하면 선택한 Helm 차트로 생성된 OpenShift 리소스와 각 리소스의 상태를 한눈에 확인할 수 있습니다.

  ![argocd-token-visualizer-2.png](./images/argocd-token-visualizer-2.png)

7. 작은 token-visualizer 애플리케이션이 예상대로 실행되고 동작하는지, URL로 이동하여 확인할 수 있습니다.  
   Token visualizer는 다음 URL에 있습니다. [https://token-visualizer-<USER_NAME>-toolings.<CLUSTER_DOMAIN>/](https://token-visualizer-<USER_NAME>-toolings.<CLUSTER_DOMAIN>/)
  
  또는 터미널에서 다음 명령을 실행하여 동일한 URL을 얻을 수도 있습니다.

    ```bash
    echo https://$(oc get route/token-visualizer -n <USER_NAME>-toolings --template='{{.spec.host}}')
    ```
  
  token-visualizer 웹페이지의 `Server URL:`에 실습에서 사용하는 LLM URL을 입력하고 Enter를 누릅니다. 교육을 시작한 뒤 지금까지 입력하고 생성한 토큰 수를 시각화해 보세요. :)

  ```bash
  https://llama32-ai501.<CLUSTER_DOMAIN>
  ```

  ![token-visualizer.png](./images/token-visualizer.png)
  
Argo CD UI에서 애플리케이션을 직접 배포해 보았습니다. 다음 단계에서는 Argo CD가 Canopy🌳를 `test`와 `prod` 환경에 자동으로 배포하도록 구성합니다. 🪄🪄


## ApplicationSets

### GitOps를 위한 Gitea 준비

> 이 실습에서는 GitOps 컨트롤러인 Argo CD를 Git 저장소에 연결합니다. 도구와 애플리케이션의 배포 구성을 `genaiops-gitops` 저장소에 저장하고 Argo CD가 이 저장소를 감시하도록 설정합니다.

Gitea는 코드 저장소와 이슈, 협업 기능을 제공하는 가벼운 오픈 소스 Git 서버입니다. 이번 워크숍에서는 도구와 애플리케이션의 배포 구성을 `genaiops-gitops` 저장소에 보관하고, Gitea를 Argo CD와 연동하는 중앙 저장소로 사용합니다.

1. Gitea에 로그인합니다. 사용자 이름과 비밀번호는 OpenShift 계정과 같습니다. 오른쪽 상단의 `내 정보 복사`를 사용하면 편리합니다. 아래 URL을 열거나 `바로가기`에서 `Git 서버`를 선택합니다.

    ```bash
    https://gitea-gitea.<CLUSTER_DOMAIN>
    ```

    미리 생성된 `genaiops-gitops` 저장소가 보입니다. 이 GitOps 저장소는 도구 구성과 애플리케이션 배포 정의를 함께 보관하는 모노레포입니다. 실제 환경에서는 조직의 운영 방식에 따라 저장소를 분리할 수도 있습니다.

2. `code-server` workbench 터미널로 돌아가서 저장소를 클론합니다.

    ```bash
    cd /opt/app-root/src
    git clone https://<USER_NAME>:<PASSWORD>@gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/genaiops-gitops.git
    ```

   Git 프로젝트를 클론했으니, 이제 GitOps 여정을 시작해 봅시다 🧙‍♀️🦄!

3. `genaiops-gitops` 저장소에는 실습에서 사용할 Argo CD `ApplicationSet` 정의가 들어 있습니다. `ApplicationSet`은 여러 Argo CD Application을 동적으로 생성하고 관리하는 리소스입니다. 여기서는 도구용, 테스트 환경용, 운영 환경용으로 모두 세 개의 `ApplicationSet`을 사용합니다.

  먼저 도구(tooling)부터 시작해 봅시다. IDE에서 `genaiops-gitops/appset-toolings.yaml` 파일을 엽니다. `CLUSTER_DOMAIN`과 `USER_NAME` 플레이스홀더를 본인의 값으로 업데이트합니다. 그런 다음 `toolings/bootstrap/config.yaml` 파일에서도 동일하게 수행합니다. 또는, 아래 명령을 실행하여 변경 사항을 자동으로 적용할 수도 있습니다.

    ```bash
      sed -i -e 's/CLUSTER_DOMAIN/<CLUSTER_DOMAIN>/g' /opt/app-root/src/genaiops-gitops/appset-toolings.yaml
      sed -i -e 's/USER_NAME/<USER_NAME>/g' /opt/app-root/src/genaiops-gitops/appset-toolings.yaml
      sed -i -e 's/USER_NAME/<USER_NAME>/g' /opt/app-root/src/genaiops-gitops/toolings/bootstrap/config.yaml
    ```

4. 이것이 바로 GitOps입니다. 가장 먼저 커밋을 해야 합니다! 구성을 git에 반영해 봅시다 👇

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git config --global user.email "<USER_NAME>@genaiops-wizard.com"
    git config --global user.name "<USER_NAME>"
    git add .
    git commit -m  "🦆 ADD - ApplicationSet definition 🦆"
    git push
    ```

5. `appset-toolings.yaml`은 자동화와 관측성(observability), 보안 도구의 정의가 들어 있는 `toolings` 폴더를 참조합니다. 우선 두 개의 애플리케이션부터 배포합니다. `bootstrap`은 `test`와 `prod` 네임스페이스와 필요한 권한을 만들고, `minio`는 스토리지를 구성합니다. 환경과 스토리지의 원하는 상태가 모두 ✨Git✨에 저장되며, 이것이 GitOps의 핵심입니다.

  우리가 해야 할 일은 ApplicationSet 객체를 생성하는 것뿐이며, 나머지는 Argo CD가 처리해 줍니다.

    ```bash
      oc apply -f /opt/app-root/src/genaiops-gitops/appset-toolings.yaml -n <USER_NAME>-toolings
    ```
6. 이제 UI의 Argo CD Application 뷰를 확인하여, ApplicationSet이 `toolings` 아래의 하위 폴더들을 인식하고 애플리케이션을 배포했는지 확인합니다!

7. Argo CD가 리소스를 동기화함에 따라 클러스터에서도 해당 리소스들을 확인할 수 있습니다. workbench에서 다음을 실행합니다.

    ```bash
    oc get projects | grep <USER_NAME>
    ```

  모든 것이 잘 진행되었다면 다음과 같은 결과가 표시될 것입니다.

    <div class="highlight" style="background: #f7f7f7; overflow-x: auto; padding: 8px;">
    <pre><code class="language-bash"> 
      $ oc get projects | grep <USER_NAME>
      <USER_NAME>-canopy     <USER_NAME>-canopy     Active
      <USER_NAME>-prod       <USER_NAME>-prod       Active
      <USER_NAME>-test       <USER_NAME>-test       Active
      <USER_NAME>-toolings   <USER_NAME>-toolings   Active
    </code></pre>
    </div>

  `<USER_NAME>-toolings` 네임스페이스에서 실행 중인 파드도 확인할 수 있습니다.

  ```bash
  oc get pods -n <USER_NAME>-toolings
  ```

8. Argo CD는 기본적으로 약 3분마다 저장소를 동기화합니다. Git에 변경 사항이 반영되는 즉시 동기화되도록 `genaiops-gitops`와 `backend` 저장소에 웹훅을 추가하겠습니다. 다음 명령으로 Argo CD 웹훅 URL을 확인합니다.
  
  ```bash
  echo https://$(oc get route argocd-server --template='{{ .spec.host }}'/api/webhook  -n <USER_NAME>-toolings)
  ```

  또는 다음 값을 그대로 복사해도 됩니다.

  ```bash
  https://argocd-server-<USER_NAME>-toolings.<CLUSTER_DOMAIN>/api/webhook
  ```

9. Gitea > `genaiops-gitops` > Settings > Webhooks > Add Gitea type webhook으로 이동합니다.

  _링크는 Quick Links에서 찾을 수 있습니다._

  ![gitops-webhook.](./images/gitops-webhook.png)

10. 해당 값을 `Target URL`에 붙여넣고 `Add Webhook`을 클릭합니다.

  ![gitops-webhook-2.png](./images/gitops-webhook-2.png)

🪄🪄 이제 `ApplicationSet`을 통해 도구와 프로젝트의 기본 구조를 반복 가능하고 감사 가능한 방식으로 배포했습니다. 다음은 Canopy를 같은 방식으로 배포할 차례입니다. 🪄🪄
