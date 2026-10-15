"""Derive per-student URLs/commands by the same naming conventions
ansible/deploy-labguide.yml and docs/index.html already use, so this app
never needs to talk to the OpenShift API directly.
"""

from .models import InfoLink, Workshop, WorkshopUser


def _substitute(template: str, workshop: Workshop, user: WorkshopUser) -> str:
    return (
        template.replace("{username}", user.username)
        .replace("{clusterdomain}", workshop.cluster_ingress_domain or "")
        .replace("{password}", effective_password(workshop, user))
    )


def openshift_console_url(workshop: Workshop) -> str:
    domain = workshop.cluster_ingress_domain or ""
    return f"https://console-openshift-console.{domain}" if domain else ""


def labguide_url(workshop: Workshop, user: WorkshopUser) -> str:
    if not workshop.cluster_ingress_domain:
        return ""
    template = workshop.labguide_url_template or "https://labguide-{username}-labguide.{clusterdomain}"
    return _substitute(template, workshop, user)


def custom_links(workshop: Workshop, user: WorkshopUser, links: list[InfoLink]) -> list[dict]:
    return [{"label": link.label, "url": _substitute(link.url_template, workshop, user)} for link in links]


def effective_password(workshop: Workshop, user: WorkshopUser) -> str:
    return user.password_override or workshop.default_user_password or ""


def oc_login_command(workshop: Workshop, user: WorkshopUser) -> str:
    domain = workshop.cluster_ingress_domain or ""
    if not domain:
        return ""
    api_host = "api." + domain[len("apps.") :] if domain.startswith("apps.") else "api." + domain
    password = effective_password(workshop, user)
    return f"oc login --username {user.username} --password {password} https://{api_host}:6443"


def user_info(workshop: Workshop, user: WorkshopUser, links: list[InfoLink] | None = None) -> dict:
    return {
        "username": user.username,
        "assigned_email": user.assigned_email,
        "openshift_console_url": openshift_console_url(workshop),
        "labguide_url": labguide_url(workshop, user),
        "cluster_ingress_domain": workshop.cluster_ingress_domain,
        "password": effective_password(workshop, user),
        "oc_login_command": oc_login_command(workshop, user),
        "custom_links": custom_links(workshop, user, links or []),
    }
