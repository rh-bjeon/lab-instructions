# workshop-ui

A small directory/login app for the GenAIOps lab guide: students enter their
email + a shared workshop password and get matched to one of the
`user1`..`userN` OpenShift users that `ansible/deploy-labguide.yml` already
provisioned; an admin configures the workshop and manages the email↔user
assignment table. See the plan/README at the repo root ("☁️ Deploying to
OpenShift") for how this gets deployed.

This app only computes URLs/credentials by naming convention — it never talks
to the OpenShift API itself, so its `student_count` / `cluster_ingress_domain`
/ `default_user_password` (set from the admin dashboard) must match whatever
you actually passed to `ansible/deploy-labguide.yml`.

## Local development

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

DATABASE_PATH=./workshop.db ADMIN_PASSWORD=adminpass SECRET_KEY=devsecret \
  uvicorn app.main:app --reload --port 8099
```

- Student login: http://localhost:8099/
- Admin: http://localhost:8099/admin/login

`ADMIN_PASSWORD` has no default — the app rejects all admin logins until it's
set. `SECRET_KEY` is auto-generated if omitted (sessions won't survive a
restart in that case; fine for local dev, set it explicitly in deployment).
