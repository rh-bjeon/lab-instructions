# 🐙 Argo CD - GitOps 컨트롤러 

GitOps는 개발 워크플로우와 모델 및 애플리케이션 배포를 관리하는 일관되고 자동화된 방법을 제공하여, 모든 것이 버전 관리되고 추적 가능하며 재현 가능하도록 보장하기 때문에 중요합니다. Git을 단일 진실 공급원(single source of truth)으로 사용함으로써, 팀은 변경 사항을 쉽게 추적하고 구성을 관리하며 모델과 애플리케이션이 항상 올바른 상태로 배포되도록 보장할 수 있습니다.

GitOps를 실제로 적용하기 위해 Argo CD를 GitOps 엔진으로 사용하겠습니다.

## Argo CD Applications
Argo CD는 가장 널리 사용되는 GitOps 도구 중 하나입니다. 이는 OpenShift 애플리케이션의 상태를 git 저장소와 동기화된 상태로 유지합니다. 즉, git 저장소에 저장된 내용(원하는 상태)과 클러스터에 실제로 배포된 내용(실제 상태)을 조정(reconcile)하는 컨트롤러입니다. 

GenAIOps의 맥락에서, 우리는 Argo CD를 활용하여 애플리케이션, 도구, 모델을 반복 가능하고 재현 가능한 방식으로 배포할 것입니다. 구성 정의를 Git에 저장함으로써 Argo CD는 해당 정의를 자동으로 적용하여 배포 프로세스를 더욱 효율적이고 일관되게 만들어 줍니다. 즉, 우리는 YAML 파일을 다루게 될 것입니다 :)

GitOps 시스템의 기반을 설정하고, 지금까지 사용해 온 모든 구성 요소를 Argo CD를 통해 `<USER_NAME>-test` 및 `<USER_NAME>-prod` 환경에 배포해 봅시다.

1. 먼저 GitOps와 Argo CD에 익숙해져 봅시다. Argo CD 인스턴스는 이미 `<USER_NAME>-toolings` 환경에 설치되어 있습니다. 위의 `Quick Links` 타일에서 URL을 가져오거나, 단순히 workbench의 터미널에서 아래 명령을 실행하여 얻을 수 있습니다.
   
   * 참고: 본인의 워크스테이션에 이미 `oc` CLI가 로컬로 설치되어 있다면 그것을 사용해도 됩니다. 하지만 이러한 명령을 확실하게 실행할 수 있는 쉬운 방법이 필요하다면, 앞서 생성했던 VSCode Workbench로 돌아가는 것을 권장합니다 (기억하신다면, 그곳에서 터미널을 열어 `git clone`을 실행했습니다). 웹 브라우저와 컨테이너의 장점 덕분에, 로컬 워크스테이션이 어떻게 구성되어 있든 상관없이 동작하는 것을 보장할 수 있는 방법입니다. 감사 인사는 넣어두세요!)

## 클러스터에 로그인하기

명령줄을 통해 OpenShift와 상호작용하려면 클러스터에 로그인해야 합니다. Visual Studio Code의 터미널 창을 사용하세요. 

  ```bash
    export CLUSTER_DOMAIN=<CLUSTER_DOMAIN>
    oc login --server=https://api.${CLUSTER_DOMAIN##apps.}:6443 -u <USER_NAME> -p <PASSWORD>
  ```

  그런 다음 URL을 가져오고 (또는 우측 상단의 `Quick Links`를 사용할 수도 있습니다) Argo CD에 접속합니다.

  ```bash
    echo https://$(oc get route argocd-server --template='{{ .spec.host }}' -n <USER_NAME>-toolings)
  ```

2. `Log in via OpenShift`를 클릭하여 Argo CD에 로그인하고, 제공된 OpenShift 자격 증명을 사용합니다.

  ![argocd-login.png](./images/argocd-login.png)

3. 처음 로그인할 때는 `Allow selected permissions`를 선택합니다.

4. 방금 Argo CD에 로그인했습니다 👏👏👏! UI를 통해 샘플 애플리케이션을 배포해 봅시다. 이것은 우리가 GenAIOps 목적으로 Argo CD를 사용하기에 앞서, 그 마법 같은 기능을 미리 맛보기 위한 것입니다. Argo CD에서 `CREATE APPLICATION`을 클릭합니다. 빈 양식이 보일 것입니다. 다음과 같이 입력해 봅시다.

   * "GENERAL" 상자에서
      * Application Name: `token-visualizer` 
      * Project Name: `default`
      * Sync Policy: `Automatic`
   * "SOURCE" 상자에서
      * Repository URL: `https://rhoai-genaiops.github.io/genaiops-helmcharts/`
      * 우측 GIT/HELM 드롭다운 메뉴에서 `Helm` 선택
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

5. `Create`를 클릭하면 `token-visualizer` 애플리케이션이 생성되어 `<USER_NAME>-toolings` 네임스페이스에 배포되기 시작하는 것을 볼 수 있습니다.

  ![argocd-token-visualizer-1.png](./images/argocd-token-visualizer-1.png)

6. 애플리케이션을 드릴다운하면 생성된 모든 OpenShift 리소스에 대한 Argo CD의 놀라운 뷰를 볼 수 있습니다. 이러한 리소스들은 여러분이 선택한 Helm chart에 정의되어 있습니다.

  ![argocd-token-visualizer-2.png](./images/argocd-token-visualizer-2.png)

7. 작은 token-visualizer 애플리케이션이 예상대로 실행되고 동작하는지, URL로 이동하여 확인할 수 있습니다.  
   Token visualizer는 다음 URL에 있습니다. [https://token-visualizer-<USER_NAME>-toolings.<CLUSTER_DOMAIN>/](https://token-visualizer-<USER_NAME>-toolings.<CLUSTER_DOMAIN>/)
  
  또는 터미널에서 다음 명령을 실행하여 동일한 URL을 얻을 수도 있습니다.

    ```bash
    echo https://$(oc get route/token-visualizer -n <USER_NAME>-toolings --template='{{.spec.host}}')
    ```
  
  우리가 사용하고 있는 LLM의 URL을 입력하고 Enter를 누른 다음, 교육 시작 이후 지금까지 보내고 생성한 토큰 수를 시각화해 보세요 :)

  ```bash
  https://llama32-ai501.<CLUSTER_DOMAIN>
  ```

  ![token-visualizer.png](./images/token-visualizer.png)
  
🪄🪄 마법 같죠! 이제 GitOps 컨트롤러인 Argo CD를 갖게 되었고, 이를 사용해 애플리케이션을 수동으로 배포해 보았습니다. 다음으로, Argo CD가 Canopy🌳를 `test` 및 `prod` 환경에 배포하도록 만들어 보겠습니다 🪄🪄


## ApplicationSets

### GitOps를 위한 Gitea 준비

> 이 실습에서는 Argo CD(GitOps 컨트롤러)를 Git 저장소에 연결하여 GitOps 워크플로우를 활성화합니다. 도구 및 애플리케이션 배포에 대한 정의는 `genaiops-gitops` 저장소에 저장하고, Argo CD가 해당 저장소를 인식하도록 설정합니다.

Gitea는 팀이 저장소를 관리하고, 이슈를 추적하며, 코드를 효율적으로 협업할 수 있도록 지원하는 경량의 자체 호스팅 Git 서버입니다. 오픈소스이며 배포가 쉽고 다양한 버전 관리 작업을 지원합니다. 이 워크샵에서 Gitea는 `genaiops-gitops` 구성이 저장되어 Argo CD와 원활하게 통합되는 중앙 저장소 역할을 합니다.

1. 자격 증명으로 Gitea에 로그인합니다. Gitea URL은 다음과 같습니다.

    ```bash
    https://gitea-gitea.<CLUSTER_DOMAIN>
    ```

    이미 생성되어 있는 `genaiops-gitops` 저장소를 볼 수 있습니다. 이것은 우리가 **GIT**Ops 목적으로 사용할 git 저장소입니다. 이 저장소는 도구 구성과 애플리케이션 배포 정의를 모두 담는 모노레포(mono-repo) 역할을 합니다. 실제 환경에서는 이를 별도의 저장소로 분리하는 것이 좋을 수도 있습니다! 어쨌든, 시작해 봅시다!

2. `code-server` workbench 터미널로 돌아가서 저장소를 클론합니다.

    ```bash
    cd /opt/app-root/src
    git clone https://<USER_NAME>:<PASSWORD>@gitea-gitea.<CLUSTER_DOMAIN>/<USER_NAME>/genaiops-gitops.git
    ```

   git 프로젝트를 클론했으니, 이제 GitOps 여정을 시작해 봅시다 🧙‍♀️🦄!

3. 이 `genaiops-gitops` 저장소에는 여기서 정의하는 모든 애플리케이션을 생성하기 위한 Argo CD `ApplicationSet` 정의가 포함되어 있습니다. `ApplicationSet`은 여러 Argo CD 애플리케이션을 동적으로 생성하고 관리할 수 있게 해주는 리소스입니다. 우리에게는 세 개의 `ApplicationSet` 정의가 있습니다. 하나는 도구용, 하나는 test 환경용, 하나는 production 환경용입니다.

  먼저 도구(tooling)부터 시작해 봅시다. IDE에서 `genaiops-gitops/appset-toolings.yaml` 파일을 엽니다. `CLUSTER_DOMAIN`과 `USER_NAME` 플레이스홀더를 본인의 값으로 업데이트합니다. 그런 다음 `toolings/bootstrap/config.yaml` 파일에서도 동일하게 수행합니다. 또는, 아래 명령을 실행하여 변경 사항을 자동으로 적용할 수도 있습니다.

    ```bash
      sed -i -e 's/CLUSTER_DOMAIN/<CLUSTER_DOMAIN>/g' /opt/app-root/src/genaiops-gitops/appset-toolings.yaml
      sed -i -e 's/USER_NAME/<USER_NAME>/g' /opt/app-root/src/genaiops-gitops/appset-toolings.yaml
      sed -i -e 's/USER_NAME/<USER_NAME>/g' /opt/app-root/src/genaiops-gitops/toolings/bootstrap/config.yaml
    ```

4. 이것이 바로 GITOPS입니다. 가장 먼저 커밋을 해야 합니다! 구성을 git에 반영해 봅시다 👇

    ```bash
    cd /opt/app-root/src/genaiops-gitops
    git config --global user.email "<USER_NAME>@genaiops-wizard.com"
    git config --global user.name "<USER_NAME>"
    git add .
    git commit -m  "🦆 ADD - ApplicationSet definition 🦆"
    git push
    ```

5. 이 `appset-toolings.yaml` 파일은 자동화, 관찰성(observability), 보안 등을 지원하기 위해 필요한 모든 정의가 담긴 `toolings` 폴더를 참조합니다. 지금은 두 개의 애플리케이션으로 작게 시작하겠습니다. `toolings` 폴더 안에는 두 개의 하위 폴더가 있습니다. 하나는 필요한 네임스페이스와 권한으로 클러스터를 부트스트랩하는 역할을 하는 `bootstrap`(처음에는 `test`와 `prod`), 다른 하나는 스토리지 환경을 정의하는 `minio`입니다. 즉, 스토리지와 환경 정의 모두를 Git에 저장하고 있는 것입니다. 앞서 설명했듯이 이것이 바로 GitOps이며, 따라서 우리가 원하는 상태는 반드시 ✨Git✨에 저장되어야 합니다. 

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

8. Argo CD의 기본 동기화 주기는 약 3분 정도인데, 이는 우리에게는 너무 느립니다. 우리는 변경 사항이 git 저장소에 반영되는 즉시 ArgoCD가 동기화하기를 원합니다. Argo CD를 `genaiops-gitops` 및 `backend` 프로젝트에 연결하는 웹훅을 추가해 봅시다. 다음 명령으로 Argo CD 웹훅 URL을 가져옵니다.
  
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

🪄🪄 마법 같죠! 이제 `ApplicationSet`을 배포하여 (git을 통해!) 반복 가능하고 감사 가능한 방식으로 도구와 프로젝트의 뼈대를 구성했습니다. 이제 Canopy도 같은 방식으로 배포해 봅시다! 🪄🪄
