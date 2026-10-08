import hmac
import time
from collections import defaultdict

import bcrypt
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from . import config

_student_serializer = URLSafeTimedSerializer(config.SECRET_KEY, salt="student-session")
_admin_serializer = URLSafeTimedSerializer(config.SECRET_KEY, salt="admin-session")

SESSION_MAX_AGE = 60 * 60 * 12  # 12 hours


def hash_password(raw: str) -> str:
    return bcrypt.hashpw(raw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(raw: str, hashed: str) -> bool:
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(raw.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def constant_time_eq(a: str, b: str) -> bool:
    return hmac.compare_digest(a or "", b or "")


def sign_student_session(username: str) -> str:
    return _student_serializer.dumps({"username": username})


def read_student_session(token: str | None) -> str | None:
    if not token:
        return None
    try:
        data = _student_serializer.loads(token, max_age=SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None
    return data.get("username")


def sign_admin_session() -> str:
    return _admin_serializer.dumps({"admin": True})


def read_admin_session(token: str | None) -> bool:
    if not token:
        return False
    try:
        data = _admin_serializer.loads(token, max_age=SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return False
    return bool(data.get("admin"))


# Best-effort in-memory throttling (single replica; resets on pod restart).
_FAILED_ATTEMPTS: dict[str, list[float]] = defaultdict(list)
MAX_ATTEMPTS = 10
WINDOW_SECONDS = 300


def is_rate_limited(key: str) -> bool:
    now = time.monotonic()
    attempts = [t for t in _FAILED_ATTEMPTS[key] if now - t < WINDOW_SECONDS]
    _FAILED_ATTEMPTS[key] = attempts
    return len(attempts) >= MAX_ATTEMPTS


def record_failed_attempt(key: str) -> None:
    _FAILED_ATTEMPTS[key].append(time.monotonic())


def clear_failed_attempts(key: str) -> None:
    _FAILED_ATTEMPTS.pop(key, None)
