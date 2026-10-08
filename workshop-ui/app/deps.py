from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import config, security
from .db import get_db
from .models import WorkshopUser

__all__ = ["get_db"]


def get_current_student(
    db: Session = Depends(get_db),
    session_cookie: str | None = Cookie(default=None, alias=config.STUDENT_COOKIE_NAME),
) -> WorkshopUser:
    username = security.read_student_session(session_cookie)
    if not username:
        raise HTTPException(status.HTTP_303_SEE_OTHER, headers={"Location": "/"})
    user = db.get(WorkshopUser, username)
    if not user or not user.assigned_email:
        raise HTTPException(status.HTTP_303_SEE_OTHER, headers={"Location": "/"})
    return user


def require_admin(
    admin_cookie: str | None = Cookie(default=None, alias=config.ADMIN_COOKIE_NAME),
) -> None:
    if not security.read_admin_session(admin_cookie):
        raise HTTPException(status.HTTP_303_SEE_OTHER, headers={"Location": "/admin/login"})
