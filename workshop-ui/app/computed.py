"""Derive per-student URLs/commands by the same naming conventions
ansible/deploy-labguide.yml and docs/index.html already use, so this app
never needs to talk to the OpenShift API directly.
"""

from .models import Workshop, WorkshopUser


def openshift_console_url(workshop: Workshop) -> str:
    domain = workshop.cluster_ingress_domain or ""
    return f"https://console-openshift-console.{domain}" if domain else ""


def labguide_url(workshop: Workshop, user: WorkshopUser) -> str:
    domain = workshop.cluster_ingress_domain or ""
    if not domain:
        return ""
    route = workshop.labguide_route_name or "labguide"
    return f"https://{route}-{user.username}-labguide.{domain}"


def effective_password(workshop: Workshop, user: WorkshopUser) -> str:
    return user.password_override or workshop.default_user_password or ""


def oc_login_command(workshop: Workshop, user: WorkshopUser) -> str:
    domain = workshop.cluster_ingress_domain or ""
    if not domain:
        return ""
    api_host = "api." + domain[len("apps.") :] if domain.startswith("apps.") else "api." + domain
    password = effective_password(workshop, user)
    return f"oc login --username {user.username} --password {password} https://{api_host}:6443"


def user_info(workshop: Workshop, user: WorkshopUser) -> dict:
    return {
        "username": user.username,
        "assigned_email": user.assigned_email,
        "openshift_console_url": openshift_console_url(workshop),
        "labguide_url": labguide_url(workshop, user),
        "cluster_ingress_domain": workshop.cluster_ingress_domain,
        "gitea_console_url": workshop.gitea_console_url,
        "password": effective_password(workshop, user),
        "oc_login_command": oc_login_command(workshop, user),
    }
