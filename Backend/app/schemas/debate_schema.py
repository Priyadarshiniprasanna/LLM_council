"""Pydantic v2 request/response schemas for the debate domain."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ParticipantAddRequest(BaseModel):
    role_name: str = Field(..., min_length=1, max_length=100, examples=["Devil's Advocate"])
    model_id: str = Field(..., examples=["openai/gpt-4o"])
    persona_id: UUID | None = None
    turn_order: int = Field(..., ge=1)


class ParticipantResponse(BaseModel):
    id: UUID
    debate_id: UUID
    role_name: str
    model_id: str
    persona_id: UUID | None
    compiled_prompt_version: str | None
    turn_order: int
    created_at: datetime


class DebateCreateRequest(BaseModel):
    workspace_id: UUID
    title: str = Field(..., min_length=1, max_length=255)
    problem_statement: str = Field(..., min_length=10)


class DebateResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    title: str
    problem_statement: str
    status: str
    temporal_workflow_id: str | None
    participants: list[ParticipantResponse]
    created_at: datetime
    updated_at: datetime


class DebateSummaryResponse(BaseModel):
    debate_id: UUID
    executive_summary: str | None
    minutes: str | None
    action_items: str | None
    dissent_and_risk: str | None
    generated_at: datetime | None
