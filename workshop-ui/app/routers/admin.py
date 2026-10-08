from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .. import computed, config, crud, security
from ..db import get_db
from ..deps import require_admin
from ..models import WorkshopUser
from ..templating import templates

router = APIRouter(prefix="/admin")


@router.get("/login")
def admin_login_page(request: Request):
    return templates.TemplateResponse(request, "admin_login.html", {})


@router.post("/login")
def admin_login(request: Request, password: str = Form(...)):
    throttle_key = "admin-login"

    def error(message: str):
        return templates.TemplateResponse(request, "admin_login.html", {"error": message}, status_code=400)

    if security.is_rate_limited(throttle_key):
        return error("너무 많이 시도했습니다. 잠시 후 다시 시도해주세요.")

    if not config.ADMIN_PASSWORD or not security.constant_time_eq(password, config.ADMIN_PASSWORD):
        security.record_failed_attempt(throttle_key)
        return error("비밀번호가 올바르지 않습니다.")

    security.clear_failed_attempts(throttle_key)
    response = RedirectResponse("/admin", status_code=303)
    response.set_cookie(
        config.ADMIN_COOKIE_NAME,
        security.sign_admin_session(),
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/logout")
def admin_logout():
    response = RedirectResponse("/admin/login", status_code=303)
    response.delete_cookie(config.ADMIN_COOKIE_NAME)
    return response


def _dashboard_context(request: Request, db: Session, **extra):
    workshop = crud.get_workshop(db)
    crud.ensure_user_pool(db, workshop)
    users = crud.list_users(db)
    assigned, total = crud.assigned_count(db)
    user_infos = {u.username: computed.user_info(workshop, u) for u in users}
    context = {
        "workshop": workshop,
        "users": users,
        "user_infos": user_infos,
        "assigned_count": assigned,
        "total_count": total,
    }
    context.update(extra)
    return context


@router.get("", dependencies=[Depends(require_admin)])
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request, "admin_dashboard.html", _dashboard_context(request, db))


@router.post("/workshop", dependencies=[Depends(require_admin)])
def update_workshop(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(""),
    password: str = Form(""),
    redirect_enabled: bool = Form(False),
    registration_mode: str = Form("open"),
    student_count: int = Form(0),
    cluster_ingress_domain: str = Form(""),
    gitea_console_url: str = Form(""),
    default_user_password: str = Form(""),
):
    workshop = crud.get_workshop(db)
    workshop.title = title.strip()
    workshop.description = description.strip()
    if password.strip():
        workshop.password_hash = security.hash_password(password.strip())
    workshop.redirect_enabled = redirect_enabled
    workshop.registration_mode = "pre_registration" if registration_mode == "pre_registration" else "open"
    workshop.student_count = max(0, student_count)
    workshop.cluster_ingress_domain = cluster_ingress_domain.strip()
    workshop.gitea_console_url = gitea_console_url.strip()
    workshop.default_user_password = default_user_password.strip()
    db.commit()
    crud.ensure_user_pool(db, workshop)

    return templates.TemplateResponse(
        request, "admin_dashboard.html", _dashboard_context(request, db, notice="저장되었습니다.")
    )


@router.post("/users/{username}/assign", dependencies=[Depends(require_admin)])
def assign_user(
    request: Request,
    username: str,
    db: Session = Depends(get_db),
    email: str = Form(""),
    password_override: str = Form(""),
):
    user = db.get(WorkshopUser, username)
    if user is None:
        return templates.TemplateResponse(
            request, "admin_dashboard.html", _dashboard_context(request, db, error="존재하지 않는 사용자입니다."), status_code=404
        )

    email = email.strip().lower()
    if email:
        conflict = crud.find_by_email(db, email)
        if conflict and conflict.username != username:
            return templates.TemplateResponse(
                request,
                "admin_dashboard.html",
                _dashboard_context(request, db, error=f"{email}은(는) 이미 {conflict.username}에 할당되어 있습니다."),
                status_code=400,
            )
        user.assign(email)
    else:
        user.unassign()
    user.password_override = password_override.strip() or None
    db.commit()

    return templates.TemplateResponse(request, "admin_dashboard.html", _dashboard_context(request, db, notice=f"{username} 저장됨."))


@router.post("/users/{username}/unassign", dependencies=[Depends(require_admin)])
def unassign_user(request: Request, username: str, db: Session = Depends(get_db)):
    user = db.get(WorkshopUser, username)
    if user:
        user.unassign()
        db.commit()
    return templates.TemplateResponse(request, "admin_dashboard.html", _dashboard_context(request, db, notice=f"{username} 할당 해제됨."))


@router.post("/users/bulk-assign", dependencies=[Depends(require_admin)])
def bulk_assign(request: Request, db: Session = Depends(get_db), emails: str = Form("")):
    pending = [line.strip().lower() for line in emails.splitlines() if line.strip()]
    assigned_emails = []
    skipped = []
    for email in pending:
        existing = crud.find_by_email(db, email)
        if existing:
            skipped.append(email)
            continue
        slot = crud.next_free_slot(db)
        if slot is None:
            skipped.append(email)
            continue
        slot.assign(email)
        assigned_emails.append(email)
    db.commit()

    notice = f"{len(assigned_emails)}명 할당됨."
    if skipped:
        notice += f" ({len(skipped)}명 건너뜀: 이미 할당되었거나 빈 슬롯 없음)"
    return templates.TemplateResponse(request, "admin_dashboard.html", _dashboard_context(request, db, notice=notice))
