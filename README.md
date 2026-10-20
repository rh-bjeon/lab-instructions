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

```shell
sudo dnf install -y ansible-core python3.12-pip
pip3.12 install -r ansible/requirements.txt
ansible-galaxy collection install -r ansible/requirements.yml
```

```shell
# user1..userN 배포 (예: student_count=30 -> user1-labguide .. user30-labguide)
ansible-playbook ansible/deploy-labguide.yml \
  -e student_count=30 \
  -e openshift_cluster_ingress_domain='apps로시작하는클러스터도메인주소' \
  -e default_password='유저공통패스워드' \
  -e content_git_repo_ref=ko-openshift-labguide


# 랩가이드를 제거하는 경우(teardown)
ansible-playbook ansible/destroy-labguide.yml -e student_count=30
```

- 보통 전달해야 하는 변수는 `student_count`와 `openshift_cluster_ingress_domain` 뿐입니다. 모든 기본값은 `ansible/defaults.yml`을 참고하세요.
- 콘텐츠는 `content_git_repo_url`(기본값: 이 repo)의 `content_git_repo_ref`(기본값: `main`) 브랜치를 clone해옵니다. 아직 `main`에 merge되지 않은 브랜치의 내용을 배포하려면 `-e content_git_repo_ref=<브랜치명>`을 함께 전달하세요. 이 두 변수는 `deploy-labguide.yml`과 `deploy-workshop-ui.yml` 모두에 동일하게 적용됩니다.

이 Ansible 변수들은 컨테이너 env var로 매핑되고, 이는 다시 문서(`docs/index.html` 참고)에 치환되는 placeholder로 매핑됩니다. 임시 클러스터 환경이라는 점을 고려해 이 값들은 모두 일반 ConfigMap(`labguide-values`)으로만 관리하며(`password` 포함, 별도 Secret 없음), 페이지 상단의 수동 입력 폼은 이 값들이 env var로 이미 채워져 있을 때는 자동으로 숨겨집니다:

| Ansible 변수 | 컨테이너 env var | 문서 placeholder |
|---|---|---|
| 학생별 사용자명(`user<N>`) | `user` | `<USER_NAME>` |
| `default_password` / `password_overrides` | `password` | `<PASSWORD>` |
| `openshift_cluster_ingress_domain` | `openshift_cluster_ingress_domain` | `<CLUSTER_DOMAIN>` |
| `gitea_console_url` | `gitea_console_url` | `<GIT_SERVER>` |

#### 워크샵 디렉터리/로그인 앱 (`workshop-ui/`)

실습자가 OpenShift 사용자 이름을 미리 알 필요 없이, 이메일 + 공용 워크샵 비밀번호만 입력하면 `ansible/deploy-labguide.yml`이 이미 프로비저닝한 `user1`..`userN` 중 하나에 자동으로 매칭되는 작은 디렉터리/로그인 앱입니다. 관리자(admin) 모드에서 워크샵 제목/설명/비밀번호(현재 값도 그대로 확인 가능)/등록 방식(open 또는 pre-registration)/리다이렉트 여부/랩가이드 URL 템플릿(`{username}`, `{clusterdomain}`, `{password}` 치환 가능)을 설정하고, 이메일↔사용자 할당 현황 및 사용자 정보 페이지에 추가로 보여줄 커스텀 링크(label + URL 템플릿)를 확인·관리할 수 있습니다. 자세한 내용은 [`workshop-ui/README.md`](./workshop-ui/README.md) 참고.

```shell
ansible-playbook ansible/deploy-workshop-ui.yml \
  -e workshop_ui_admin_password='워크샵배정UI어드민패스워드' \
  -e content_git_repo_ref=ko-openshift-labguide

# 제거 (PVC까지 함께 삭제되어 할당 데이터도 사라집니다)
ansible-playbook ansible/destroy-workshop-ui.yml
```

- `workshop_ui_admin_password`는 **필수**이며 안전하지 않은 기본값이 없습니다(미전달 시 플레이북이 즉시 실패).
- `workshop_ui_secret_key`(세션 서명 키)는 전달하지 않으면 실행마다 무작위로 생성됩니다 — 재배포 간 세션을 유지하려면 직접 값을 지정하세요.
- 워크샵 제목/설명/비밀번호/등록 방식 등 나머지 설정은 Ansible 변수가 아니라, 배포 후 admin 대시보드(`/admin`)에서 직접 입력합니다.
