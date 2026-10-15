import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import InfoLink, Workshop, WorkshopUser

WORKSHOP_ID = 1


def _sort_key(username: str):
    # "user2" sorts before "user10" -- plain lexicographic order would not.
    match = re.search(r"(\d+)$", username)
    return (int(match.group(1)) if match else 0, username)


def get_workshop(db: Session) -> Workshop:
    workshop = db.get(Workshop, WORKSHOP_ID)
    if workshop is None:
        workshop = Workshop(id=WORKSHOP_ID, password="changeme")
        db.add(workshop)
        db.commit()
        db.refresh(workshop)
    return workshop


def ensure_user_pool(db: Session, workshop: Workshop) -> None:
    """Create any missing user1..user{student_count} rows. Never deletes rows,
    so shrinking student_count just stops offering the extra slots -- it
    doesn't touch existing assignments."""
    existing = {u.username for u in db.scalars(select(WorkshopUser))}
    for i in range(1, workshop.student_count + 1):
        username = f"{workshop.username_prefix}{i}"
        if username not in existing:
            db.add(WorkshopUser(username=username))
    db.commit()


def list_users(db: Session) -> list[WorkshopUser]:
    users = list(db.scalars(select(WorkshopUser)))
    users.sort(key=lambda u: _sort_key(u.username))
    return users


def find_by_email(db: Session, email: str) -> WorkshopUser | None:
    return db.scalar(select(WorkshopUser).where(WorkshopUser.assigned_email == email))


def next_free_slot(db: Session) -> WorkshopUser | None:
    free = [u for u in list_users(db) if not u.assigned_email]
    return free[0] if free else None


def assigned_count(db: Session) -> tuple[int, int]:
    users = list_users(db)
    assigned = sum(1 for u in users if u.assigned_email)
    return assigned, len(users)


def list_links(db: Session) -> list[InfoLink]:
    return list(db.scalars(select(InfoLink).order_by(InfoLink.id)))


def add_link(db: Session, label: str, url_template: str) -> None:
    db.add(InfoLink(label=label, url_template=url_template))
    db.commit()


def delete_link(db: Session, link_id: int) -> None:
    link = db.get(InfoLink, link_id)
    if link:
        db.delete(link)
        db.commit()
