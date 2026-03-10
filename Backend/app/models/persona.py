"""SQLAlchemy ORM models for the persona domain."""

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class PersonaSourceMode(str, Enum):
    PRESET = "preset"
    AI_GENERATED = "ai_generated"
    MANUAL = "manual"


class Persona(Base):
    __tablename__ = "personas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role_description: Mapped[str] = mapped_column(Text, nullable=False)
    source_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    raw_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    compiled_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    validation_passed: Mapped[bool | None] = mapped_column(nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
