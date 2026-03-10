"""Pydantic v2 request/response schemas for the identity domain."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: UUID
    org_id: UUID
    email: str
    display_name: str
    created_at: datetime


class WorkspaceCreateRequest(BaseModel):
    org_id: UUID
    name: str = Field(..., min_length=1, max_length=255)


class WorkspaceMemberResponse(BaseModel):
    user_id: UUID
    email: str
    display_name: str
    role: str


class WorkspaceResponse(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    members: list[WorkspaceMemberResponse]
    created_at: datetime
