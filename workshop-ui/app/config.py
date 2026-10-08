import os
import secrets

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
DATABASE_PATH = os.environ.get("DATABASE_PATH", "./workshop.db")

STUDENT_COOKIE_NAME = "workshop_session"
ADMIN_COOKIE_NAME = "workshop_admin_session"
