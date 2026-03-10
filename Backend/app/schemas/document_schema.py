"""Pydantic v2 request/response schemas for the document domain."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    id: UUID
    debate_id: UUID
    filename: str
    mime_type: str
    status: str
    error_message: str | None
    uploaded_at: datetime
    processed_at: datetime | None


class DocumentChunkResult(BaseModel):
    chunk_id: UUID
    document_id: UUID
    filename: str
    text: str
    page: int | None
    char_offset: int | None
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    citation_anchor: str


class DocumentSearchResponse(BaseModel):
    debate_id: UUID
    query: str
    results: list[DocumentChunkResult]
