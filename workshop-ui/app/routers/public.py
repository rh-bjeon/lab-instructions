from fastapi import APIRouter, Cookie, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .. import computed, config, crud, security
from ..db import get_db
from ..models import WorkshopUser
from ..templating import templates

router = APIRouter()


@router.get("/healthz")
def healthz():
    return {"status": "ok"}


@router.get("/")
def login_page(
    request: Request,
    db: Session = Depends(get_db),
    session_cookie: str | None = Cookie(default=None, alias=config.STUDENT_COOKIE_NAME),
):
    workshop = crud.get_workshop(db)
    username = security.read_student_session(session_cookie)
    if username:
        user = db.get(WorkshopUser, username)
        if user and user.assigned_email:
            return _post_login_redirect(workshop, user)
    return templates.TemplateResponse(request, "login.html", {"workshop": workshop})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    workshop = crud.get_workshop(db)
    email = email.strip().lower()
    throttle_key = f"login:{email}"

    def error(message: str):
        return templates.TemplateResponse(
            request, "login.html", {"workshop": workshop, "error": message, "email": email}, status_code=400
        )

    if security.is_rate_limited(throttle_key):
        return error("너무 많이 시도했습니다. 잠시 후 다시 시도해주세요.")

    if not security.verify_password(password, workshop.password_hash):
        security.record_failed_attempt(throttle_key)
        return error("이메일 또는 워크샵 비밀번호가 올바르지 않습니다.")

    security.clear_failed_attempts(throttle_key)

    user = crud.find_by_email(db, email)
    if user is None:
        if workshop.registration_mode == "pre_registration":
            return error("등록되지 않은 이메일입니다. 관리자에게 문의하세요.")
        user = crud.next_free_slot(db)
        if user is None:
            return error("할당 가능한 사용자 슬롯이 없습니다. 관리자에게 문의하세요.")
        user.assign(email)
        db.commit()

    response = _post_login_redirect(workshop, user)
    response.set_cookie(
        config.STUDENT_COOKIE_NAME,
        security.sign_student_session(user.username),
        httponly=True,
        samesite="lax",
    )
    return response


def _post_login_redirect(workshop, user: WorkshopUser) -> RedirectResponse:
    if workshop.redirect_enabled:
        target = computed.labguide_url(workshop, user)
        if target:
            return RedirectResponse(target, status_code=303)
    return RedirectResponse("/workshop", status_code=303)


@router.get("/workshop")
def workshop_page(
    request: Request,
    db: Session = Depends(get_db),
    session_cookie: str | None = Cookie(default=None, alias=config.STUDENT_COOKIE_NAME),
):
    workshop = crud.get_workshop(db)
    username = security.read_student_session(session_cookie)
    user = db.get(WorkshopUser, username) if username else None
    if not user or not user.assigned_email:
        return RedirectResponse("/", status_code=303)
    info = computed.user_info(workshop, user)
    return templates.TemplateResponse(request, "workshop.html", {"workshop": workshop, "info": info})


@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(config.STUDENT_COOKIE_NAME)
    return response
