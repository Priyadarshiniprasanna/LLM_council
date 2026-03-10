"""Pydantic v2 request/response schemas for the persona domain."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PersonaCreateRequest(BaseModel):
    workspace_id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    role_description: str = Field(..., min_length=10)
    raw_prompt: str = Field(..., min_length=10)


class PersonaGenerateRequest(BaseModel):
    workspace_id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    role_description: str = Field(..., min_length=10)
    generation_model: str = Field(default="openai/gpt-4o", examples=["openai/gpt-4o"])


class PersonaResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    role_description: str
    source_mode: str
    compiled_prompt: str | None
    prompt_version: str | None
    validation_passed: bool | None
    created_at: datetime
    updated_at: datetime


class PromptValidationResult(BaseModel):
    passed: bool
    errors: list[str]
    warnings: list[str]


class PromptPreviewResponse(BaseModel):
    persona_id: UUID
    compiled_prompt: str
    prompt_version: str
    validation: PromptValidationResult
