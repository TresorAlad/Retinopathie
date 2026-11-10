from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

class Screening(Base):
    __tablename__ = "screenings"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="RESTRICT"), index=True, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    image_filename: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    image_format: Mapped[str] = mapped_column(String(10), nullable=False)
    image_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    ai_status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    ai_stage: Mapped[str | None] = mapped_column(String(30), nullable=True)
    ai_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    image_quality: Mapped[str | None] = mapped_column(String(30), nullable=True)
    retinal_image_valid: Mapped[bool | None] = mapped_column(nullable=True)
    diagnosis: Mapped[str | None] = mapped_column(String(30), nullable=True)
    diagnosis_status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending_review")
    diagnosis_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    blockchain_status: Mapped[str] = mapped_column(String(64), nullable=False, default="not_configured")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    patient = relationship("Patient", back_populates="screenings")
