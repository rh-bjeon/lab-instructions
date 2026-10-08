from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from .db import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Workshop(Base):
    """Singleton row (id=1) holding the workshop's configuration."""

    __tablename__ = "workshop"

    id = Column(Integer, primary_key=True, default=1)
    title = Column(String, nullable=False, default="GenAIOps Workshop")
    description = Column(String, nullable=True, default="")
    password_hash = Column(String, nullable=False)
    redirect_enabled = Column(Boolean, nullable=False, default=False)
    registration_mode = Column(String, nullable=False, default="open")  # "open" | "pre_registration"
    username_prefix = Column(String, nullable=False, default="user")
    student_count = Column(Integer, nullable=False, default=0)
    cluster_ingress_domain = Column(String, nullable=True, default="")
    gitea_console_url = Column(String, nullable=True, default="")
    labguide_route_name = Column(String, nullable=False, default="labguide")
    default_user_password = Column(String, nullable=True, default="")


class WorkshopUser(Base):
    """One row per provisioned OpenShift user slot (user1..userN)."""

    __tablename__ = "workshop_user"

    username = Column(String, primary_key=True)
    assigned_email = Column(String, nullable=True, unique=True, index=True)
    password_override = Column(String, nullable=True)
    assigned_at = Column(DateTime, nullable=True)

    def assign(self, email: str) -> None:
        self.assigned_email = email
        self.assigned_at = _utcnow()

    def unassign(self) -> None:
        self.assigned_email = None
        self.assigned_at = None
