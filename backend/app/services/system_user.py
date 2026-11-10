import os

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User

MOBILE_SYSTEM_EMAIL = "mobile-system@retinopathie.local"


def ensure_mobile_system_user(db: Session) -> User:
    user = db.query(User).filter(User.email == MOBILE_SYSTEM_EMAIL).first()
    if user:
        return user
    password = os.getenv("MOBILE_SYSTEM_PASSWORD", "mobile-system-not-for-production-use")
    user = User(
        email=MOBILE_SYSTEM_EMAIL,
        hashed_password=hash_password(password),
        role="system",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
