## AI501 클러스터 설정

<p class="warn">
    ⛷️ <b>참고</b> ⛷️ - cluster-admin 권한을 가진 OpenShift 4.19+ 클러스터가 필요합니다.
</p>

이 과정 전체에서 실습하는 것처럼, 우리도 클러스터 구성을 GitHub 저장소에 코드로 관리합니다: https://github.com/rhoai-genaiops/deploy-lab

이 저장소는 세 가지 주요 부분으로 구성됩니다.
- **Operators**: OpenShift AI, GitOps, Pipelines, GPU 지원 등 오퍼레이터를 배포하는 Helm 차트
- **Toolings**: MinIO, 관측성(observability) 스택, 워크벤치 템플릿 같은 공유 인프라를 구성하는 Helm 차트
- **Student Content**: ArgoCD 인스턴스와 Data Science 프로젝트를 포함한 학생별 환경을 위한 Helm 차트

## 사전 준비 사항

시작하기 전에 다음이 준비되어 있는지 확인하세요.

- cluster-admin 권한을 가진 OpenShift 4.19+ 클러스터
- Helm 3.x 설치
- `oc` CLI 설정 및 인증 완료
- (선택) GPU 머신 프로비저닝을 위한 AWS 자격 증명

### GPU 요구 사항

이 실습에는 특정 taint가 적용된 **GPU 노드 3개**가 필요합니다.

| 구성 요소 | GPU 개수 | 인스턴스 타입 | Taint |
|-----------|-----------|---------------|-------|
| Docling Serve | 1 | g4dn (T4) | `nvidia.com/gpu=g4dn` |
| Llama 3.2 (cloud-model) | 1 | g5 (A10G) | `nvidia.com/gpu=g5` |
| Llama 3.2 FP8 (quantized-model) | 1 | g5 (A10G) | `nvidia.com/gpu=g5` |

<p class="tip">
    💡 <b>팁</b> 💡 - GPU 노드에 다른 taint가 설정되어 있다면, <code>student-content/templates/</code> 디렉토리에서 배포 톨러레이션(toleration)을 업데이트하세요.
</p>

## 빠른 설치

가장 빠르게 시작하는 방법은 자동화된 설치 스크립트를 사용하는 것입니다.

1. **저장소 클론**

    ```bash
    git clone https://github.com/rhoai-genaiops/deploy-lab.git
    cd deploy-lab
    ```

2. **배포 구성**

    설치를 실행하기 전에 `student-content/values.yaml`을 편집하세요.

    ```yaml
    cluster_domain: apps.your-cluster.example.com  # Your OpenShift apps domain
    attendees: 20                                   # Number of students to create
    ```

    클러스터 도메인을 확인하려면:
    ```bash
    oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'
    ```

3. **설치 실행**

    ```bash
    ./install.sh
    ```

    이 스크립트는 다음을 수행합니다.
    - 필요한 오퍼레이터 설치 (RHOAI, Pipelines, GitOps, GPU Operator)
    - 공유 툴링 인프라 배포
    - 학생 환경 생성
    - HTPasswd를 이용한 OAuth 인증 구성
    - 멀티테넌시를 위한 ArgoCD 설정
    - Tekton 및 사용자 워크로드 모니터링 구성

## 단계별 설치

설치 과정을 더 세밀하게 제어하고 싶다면, 각 단계를 수동으로 실행할 수 있습니다.

### 1단계: 오퍼레이터 설치

먼저 플랫폼 기능을 제공하는 기본 오퍼레이터를 설치합니다.

```bash
cd deploy-lab
helm upgrade --install ai501-base operators \
    --namespace ai501 \
    --create-namespace
```

GitOps 오퍼레이터가 준비될 때까지 기다립니다.

```bash
oc wait --for=jsonpath='{.status.availableReplicas}'=1 \
    -n openshift-gitops deployment/cluster
```

<p class="warn">
    ⏳ <b>참고</b> ⏳ - 오퍼레이터가 설치되고 reconcile되는 데 최대 15분 정도 걸릴 수 있습니다.
</p>

### 2단계: 공유 Toolings 설치

공유 인프라 구성 요소를 배포합니다.

```bash
helm upgrade --install ai501-toolings toolings \
    --namespace ai501 \
    --create-namespace
```

이 단계는 다음을 설치합니다.
- MinIO (S3 호환 스토리지)
- 관측성 스택 (Prometheus, Grafana, Tempo)
- 커스텀 워크벤치 템플릿

### 3단계: Student Content 설치

학생별 리소스를 배포합니다.

```bash
helm upgrade --install ai501-student-content student-content \
    --namespace ai501 \
    --create-namespace
```

<p class="tip">
    💡 <b>팁</b> 💡 - 이 단계를 실행하기 전에 <code>values.yaml</code>에 클러스터 도메인과 원하는 수강생 수를 설정했는지 확인하세요.
</p>

### 4단계: 인증 구성

학생을 위한 HTPasswd 인증을 설정합니다.

```bash
oc patch --type=merge OAuth/cluster -p '{
    "spec": {
        "identityProviders": [{
            "name": "Students",
            "type": "HTPasswd",
            "mappingMethod": "claim",
            "htpasswd": {
                "fileData": {
                    "name": "htpasswd-ai501"
                }
            }
        }]
    }
}'
```

### 5단계: 멀티테넌시를 위한 ArgoCD 구성

학생 네임스페이스에 대해 ArgoCD를 활성화합니다. 설치 스크립트는 수강생 수를 기준으로 네임스페이스 목록을 자동으로 계산합니다.

```bash
# Example for 5 attendees
oc -n openshift-gitops-operator patch subscriptions.operators.coreos.com/openshift-gitops-operator \
    --type=json \
    -p '[
        {
            "op": "add",
            "path": "/spec/config/env",
            "value": [{"name": "DISABLE_DEFAULT_ARGOCD_INSTANCE", "value": "true"}]
        },
        {
            "op": "add",
            "path": "/spec/config/env/1",
            "value": {"name": "ARGOCD_CLUSTER_CONFIG_NAMESPACES", "value": "user1-toolings,user2-toolings,user3-toolings,user4-toolings,user5-toolings"}
        }
    ]'
```

### 6단계: Tekton 및 모니터링 구성

비용 최적화를 위해 Tekton을 조정하고 사용자 워크로드 모니터링을 구성합니다.

```bash
# Disable affinity assistant for cost optimization
oc patch tektonconfig config --type merge -p '{"spec":{"pipeline":{"disable-affinity-assistant":true}}}'

# Configure user workload monitoring
oc -n openshift-user-workload-monitoring patch configmap user-workload-monitoring-config \
    --type=merge \
    -p '{"data": {"config.yaml": "prometheus:\n  logLevel: debug\n  retention: 15d\nalertmanager:\n  enabled: true\n  enableAlertmanagerConfig: true\n"}}'
```

## GPU 프로비저닝 (AWS)

AWS에서 실행 중이고 GPU 노드를 프로비저닝해야 한다면, 머신 프로비저닝 스크립트를 사용할 수 있습니다.

```bash
./machineset.sh
```

이 스크립트는 다양한 GPU 인스턴스 타입의 프로비저닝을 지원합니다.
- T4 (g4dn 인스턴스)
- A10G (g5 인스턴스)
- A100 (p4d 인스턴스)
- H100 (p5 인스턴스)
- L40 인스턴스

## 설치 확인

설치가 완료되면 모든 것이 정상적으로 동작하는지 확인하세요.

1. **오퍼레이터가 준비되었는지 확인**:
    ```bash
    oc get csv -n openshift-operators
    ```

2. **학생 네임스페이스 확인**:
    ```bash
    oc get namespaces | grep user
    ```

3. **메인 네임스페이스의 Pod 확인**:
    ```bash
    oc get pods -n ai501
    ```

4. **Helm 릴리스 확인**:
    ```bash
    helm list -n ai501
    ```

5. **ArgoCD 동기화 상태 모니터링**:
    ```bash
    oc get applications -A
    ```

UI를 통해 클러스터에 로그인하고, 학생 계정의 사용자명과 비밀번호로 `htpasswd` 로그인을 사용하세요. `<USER_NAME>`과 `<USER_NAME>-toolings` 네임스페이스만 보여야 합니다.

## 필요한 링크 확인하기

OpenShift 콘솔, OpenShift AI Dashboard 등 필요한 링크들은 이 페이지 오른쪽 상단의 `Quick Links`에 포함되어 있습니다.

## 문제 해결

### Helm 릴리스 문제

Helm 릴리스가 실패하면 릴리스 상태를 확인하세요.

```bash
helm list -n ai501
helm status <release-name> -n ai501
```

### ConfigMap이 이미 존재하는 경우

(Helm이 소유하지 않은) ConfigMap이 이미 존재한다는 오류가 발생하면, 먼저 이를 삭제해야 할 수 있습니다.

```bash
oc delete configmap <configmap-name> -n <namespace>
```

그런 다음 Helm 설치를 다시 실행하세요.

### GPU Pod가 스케줄링되지 않는 경우

GPU 워크로드가 스케줄링되지 않는다면 다음을 확인하세요.

1. GPU 노드가 사용 가능한지 확인:
    ```bash
    oc get nodes -l nvidia.com/gpu.present=true
    ```

2. 노드 taint가 배포 톨러레이션과 일치하는지 확인:
    ```bash
    oc describe node <gpu-node-name> | grep Taints
    ```

3. NVIDIA GPU 오퍼레이터가 실행 중인지 확인:
    ```bash
    oc get pods -n nvidia-gpu-operator
    ```
