## GenAIOps Enablement Instructions Repo

이 repo는 GenAIOps Enablement를 위한 콘텐츠를 담고 있습니다.

`docs` - 기술 실습을 위한 학생/강사 가이드와 교실 활동 자료가 들어 있습니다.
`slides/content`는 markdown으로 작성되며, main에 push되면 자동으로 사이트에 게시됩니다.

### 🏃‍♀️ docs & slides 사이트를 로컬에서 실행하기

슬라이드를 띄우려면 NodeJS가 설치되어 있어야 하며, 원한다면 NodeJS 컨테이너에서 실행해도 됩니다.

```shell
npm i -g docsify-cli@4.4.3
docsify serve ./docs
```

* 브라우저에서 http://localhost:3000 으로 접속하면 실습 내용을 볼 수 있습니다.
* 브라우저에서 http://localhost:3000/slides 으로 접속하면 슬라이드를 볼 수 있습니다.

### ☁️ OpenShift에 배포하기

이 사이트는 커스텀 이미지를 빌드하지 않고 OpenShift의 Deployment로 배포됩니다: `initContainer`(`quay.io/rhpds/git-cloner:v1.1.5`)가 이 repo의 `docs/` 콘텐츠를 공유 볼륨으로 clone하고, 그대로 가져온 `registry.access.redhat.com/ubi9/nginx-124` 컨테이너가 이를 서빙합니다. 하나의 클러스터를 여러 학생이 공유하므로, 각 학생은 자신만의 `<username>-labguide` 네임스페이스를 받게 되며, 이는 Ansible playbook을 통해 **클러스터당 한 번만**(학생 한 명당 한 번이 아니라) 실행되어 프로비저닝됩니다.

이 playbook은 bastion 호스트에서, 이미 유효하게 인증된 OpenShift 컨텍스트를 가진 `~/.kube/config`를 가진 계정으로 실행합니다(playbook은 이 ambient kubeconfig를 그대로 사용합니다 — `host`/`api_key`/`username`/`password`는 전달하지 않습니다).

#### Ansible 사전 요구사항

`ansible-core` 자체는 이미 설치되어 있다고 가정하며, 이 playbook들은 `ansible.builtin.*` 모듈과, 모든 OpenShift 오브젝트(Namespace/ConfigMap/Secret/Deployment/Service/Route)에 쓰이는 `kubernetes.core.k8s`만 사용합니다. 이 collection은 Python `kubernetes` 클라이언트 라이브러리와 `jsonpatch`가 필요한데 — PATH 상에서 `python3`/`pip3`가 가리키는 아무 인터프리터가 아니라, **`ansible-core`가 실제로 실행되는 바로 그 Python 인터프리터**에 설치해야 합니다. RHEL에서는 OS의 기본 스트림 `python3`와 `ansible-core`가 의존하는 인터프리터가 서로 다른 버전일 수 있기 때문에(예: 기본 스트림 Python 3.9와, `ansible-core`가 실제로 사용하는 AppStream Python 3.11/3.12가 공존하는 경우) 이 점이 중요합니다. 단순히 `dnf install python3 python3-pip && pip3 install ...`을 실행하면 모르는 사이에 잘못된 인터프리터에 설치될 수 있습니다:

```shell
# ansible-core가 실제로 실행되는 정확한 python3 인터프리터를 찾습니다
ANSIBLE_PYTHON=$(head -1 "$(command -v ansible-playbook)" | sed 's/^#!//')
PYVER=$("$ANSIBLE_PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

# 해당 인터프리터 버전에 맞는 pip (RHEL은 python stream별로 pip 패키지를 분리합니다,
# 예: python3.12-pip, python3.11-pip, 또는 기본 스트림이면 그냥 python3-pip)
sudo dnf install -y "python${PYVER}-pip"

# kubernetes.core collection에 필요한 Python 라이브러리를, 바로 그 인터프리터에 설치합니다
sudo "$ANSIBLE_PYTHON" -m pip install -r ansible/requirements.txt

# Ansible collection 자체(kubernetes.core.k8s) -- python 버전에 민감하지 않습니다
ansible-galaxy collection install -r ansible/requirements.yml
```

`ansible/defaults.yml`에서도 `ansible_python_interpreter`를 `{{ ansible_playbook_python }}`으로 고정해두었습니다. 이를 통해 Ansible이 자체 auto-discovery로 인터프리터를 추측하지 않고, 항상 이와 동일한 인터프리터로 모듈을 실행하도록 합니다.

```shell
# user1..userN 배포 (예: student_count=30 -> user1-labguide .. user30-labguide)
ansible-playbook ansible/deploy-labguide.yml \
  -e student_count=30 \
  -e openshift_cluster_ingress_domain=apps.example.com \
  -e default_password='ABC' \
  -e password_overrides='{"user7":"special-pass"}'

# 동일한 학생 집합을 제거(teardown)
ansible-playbook ansible/destroy-labguide.yml -e student_count=30
```

- 보통 전달해야 하는 변수는 `student_count`와 `openshift_cluster_ingress_domain` 뿐입니다. `gitea_console_url`은 기본적으로 `gitea-gitea.<openshift_cluster_ingress_domain>`로 설정되며, 클러스터의 Gitea가 이 규칙을 따르지 않는 경우에만 `-e gitea_console_url=...`로 명시하면 됩니다. 모든 기본값은 `ansible/defaults.yml`을 참고하세요.
- `default_password`는 모든 학생에게 적용되며, `password_overrides`(사용자명 → 비밀번호의 JSON map)는 특정 학생에게만 다른 값을 적용합니다.

이 Ansible 변수들은 컨테이너 env var로 매핑되고, 이는 다시 문서(`docs/index.html` 참고)에 치환되는 placeholder로 매핑됩니다:

| Ansible 변수 | 컨테이너 env var | 문서 placeholder |
|---|---|---|
| 학생별 사용자명(`user<N>`) | `user` | `<USER_NAME>` |
| `default_password` / `password_overrides` | `password` | `<PASSWORD>` |
| `openshift_cluster_ingress_domain` | `openshift_cluster_ingress_domain` | `<CLUSTER_DOMAIN>` |
| `gitea_console_url` | `gitea_console_url` | `<GIT_SERVER>` |

#### 워크샵 디렉터리/로그인 앱 (`workshop-ui/`)

실습자가 OpenShift 사용자 이름을 미리 알 필요 없이, 이메일 + 공용 워크샵 비밀번호만 입력하면 `ansible/deploy-labguide.yml`이 이미 프로비저닝한 `user1`..`userN` 중 하나에 자동으로 매칭되는 작은 디렉터리/로그인 앱입니다. 관리자(admin) 모드에서 워크샵 제목/설명/비밀번호/등록 방식(open 또는 pre-registration)/리다이렉트 여부를 설정하고, 이메일↔사용자 할당 현황을 확인·관리할 수 있습니다. 자세한 내용은 [`workshop-ui/README.md`](./workshop-ui/README.md) 참고.

랩 가이드 사이트와 동일하게 커스텀 이미지 빌드 없이 배포됩니다(`git-cloner` initContainer + 범용 `registry.access.redhat.com/ubi9/python-312` 이미지, 시작 시 `pip install`). 다만 랩 가이드와 달리 **학생 1명당 1개가 아니라 워크샵/클러스터당 1개**만 배포하며, 할당 데이터(SQLite)를 Pod 재시작 후에도 보존하기 위해 `emptyDir`이 아니라 PVC를 사용합니다. 이 앱은 Ansible을 직접 트리거하지 않습니다 — `ansible/deploy-labguide.yml`로 이미 프로비저닝된 것과 동일한 `student_count`/`cluster_ingress_domain`/`default_user_password`를 admin 대시보드에 입력해두면, 명명 규칙에 따라 각 사용자의 콘솔/랩가이드 URL을 계산해서 보여줄 뿐입니다.

```shell
ansible-playbook ansible/deploy-workshop-ui.yml -e workshop_ui_admin_password='some-strong-password'

# 제거 (PVC까지 함께 삭제되어 할당 데이터도 사라집니다)
ansible-playbook ansible/destroy-workshop-ui.yml
```

- `workshop_ui_admin_password`는 **필수**이며 안전하지 않은 기본값이 없습니다(미전달 시 플레이북이 즉시 실패).
- `workshop_ui_secret_key`(세션 서명 키)는 전달하지 않으면 실행마다 무작위로 생성됩니다 — 재배포 간 세션을 유지하려면 직접 값을 지정하세요.
- 워크샵 제목/설명/비밀번호/등록 방식 등 나머지 설정은 Ansible 변수가 아니라, 배포 후 admin 대시보드(`/admin`)에서 직접 입력합니다.

## 🎃 Contribution

Pull Request를 환영합니다 🎃. 컨트리뷰터가 되려면 [Contribution Guide](./CONTRIBUTING.md)를 🙏 검토 👀 해주세요.

승인되어 main에 push된 변경사항은 자동으로 docs 사이트에 게시됩니다.
