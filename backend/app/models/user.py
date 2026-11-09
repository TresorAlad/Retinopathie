from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False, default="doctor")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
