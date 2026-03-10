"""
Identity API routes — org/workspace membership, RBAC, and SSO.

All business logic is delegated to IdentityService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.identity_schema import (
    TokenResponse,
    UserLoginRequest,
    UserResponse,
    WorkspaceCreateRequest,
    WorkspaceResponse,
)
from app.services.identity_service import IdentityService

router = APIRouter(prefix="/identity")


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: UserLoginRequest,
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """Authenticate a user and return a JWT access token."""
    service = IdentityService(db)
    token = await service.login(payload)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    """Return the currently authenticated user profile."""
    service = IdentityService(db)
    return await service.get_current_user()


@router.post("/workspaces", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    payload: WorkspaceCreateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> WorkspaceResponse:
    """Create a new workspace under the authenticated org."""
    service = IdentityService(db)
    return await service.create_workspace(payload)


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> WorkspaceResponse:
    """Retrieve workspace details including member roles."""
    service = IdentityService(db)
    workspace = await service.get_workspace(workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return workspace
