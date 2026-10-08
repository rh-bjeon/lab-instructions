## GenAIOps Enablement Instructions Repo

The repo holds the content for the GenAIOps Enablement.

`docs` - contains the student and teacher guides for the technical exercises as well as the classroom
activities. 
The `slides/content` are written in markdown and automatically published to the site when pushed to main.

### 🏃‍♀️ Running the docs & slides site locally

To launch the slides, ensure you have NodeJS installed or run it in a NodeJS container if you prefer.

```shell
npm i -g docsify-cli@4.4.3
docsify serve ./docs
```

* Open the browser to http://localhost:3000 to view the tech exercise.
* Open the browser to http://localhost:3000/slides to view the slides.

### ☁️ Deploying to OpenShift

The site deploys as a Deployment on OpenShift without building a custom image: an `initContainer` (`quay.io/rhpds/git-cloner:v1.1.5`) clones this repo's `docs/` content into a shared volume, and a stock `registry.access.redhat.com/ubi9/nginx-124` container serves it. One cluster is shared by many students, so each student gets their own `<username>-labguide` namespace, provisioned by an Ansible playbook that runs **once per cluster** (not once per student).

Run from the bastion host as the account whose `~/.kube/config` already holds a valid, authenticated OpenShift context (the playbook uses that ambient kubeconfig as-is — no `host`/`api_key`/`username`/`password` are passed in):

```shell
# Deploy user1..userN (e.g. student_count=30 -> user1-labguide .. user30-labguide)
ansible-playbook ansible/deploy-labguide.yml \
  -e student_count=30 \
  -e openshift_cluster_ingress_domain=apps.example.com \
  -e default_password='ABC' \
  -e password_overrides='{"user7":"special-pass"}'

# Tear down the same set of students
ansible-playbook ansible/destroy-labguide.yml -e student_count=30
```

- `student_count` and `openshift_cluster_ingress_domain` are the only variables you normally need to pass. `gitea_console_url` defaults to `gitea-gitea.<openshift_cluster_ingress_domain>` and only needs an explicit `-e gitea_console_url=...` when a cluster's Gitea doesn't follow that convention. See `ansible/defaults.yml` for every default.
- `default_password` applies to all students; `password_overrides` (a JSON map of username to password) overrides specific students only.

These Ansible variables map to container env vars, which map to the placeholders substituted into the docs (see `docs/index.html`):

| Ansible variable | Container env var | Doc placeholder |
|---|---|---|
| per-student username (`user<N>`) | `user` | `<USER_NAME>` |
| `default_password` / `password_overrides` | `password` | `<PASSWORD>` |
| `openshift_cluster_ingress_domain` | `openshift_cluster_ingress_domain` | `<CLUSTER_DOMAIN>` |
| `gitea_console_url` | `gitea_console_url` | `<GIT_SERVER>` |

## 🎃 Contribution

Pull requests welcome 🎃. Please 🙏, review 👀 the [Contribution Guide](./CONTRIBUTING.md) to become a contributor.

Changes approved and pushed to main will automatically be published to the docs site.
