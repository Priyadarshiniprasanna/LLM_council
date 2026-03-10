"""
Persona API routes — template management, AI generation, and prompt compilation.

All business logic is delegated to PersonaService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.persona_schema import (
    PersonaCreateRequest,
    PersonaGenerateRequest,
    PersonaResponse,
    PromptPreviewResponse,
)
from app.services.persona_service import PersonaService

router = APIRouter(prefix="/personas")


@router.post("/", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
async def create_persona(
    payload: PersonaCreateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> PersonaResponse:
    """Create a persona from a manual definition."""
    service = PersonaService(db)
    return await service.create_persona(payload)


@router.post("/generate", response_model=PersonaResponse)
async def generate_persona(
    payload: PersonaGenerateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> PersonaResponse:
    """Generate a persona using an AI model based on a role description."""
    service = PersonaService(db)
    return await service.generate_persona(payload)


@router.get("/{persona_id}", response_model=PersonaResponse)
async def get_persona(
    persona_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> PersonaResponse:
    """Retrieve a persona by ID."""
    service = PersonaService(db)
    persona = await service.get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found")
    return persona


@router.get("/{persona_id}/prompt-preview", response_model=PromptPreviewResponse)
async def preview_prompt(
    persona_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> PromptPreviewResponse:
    """
    Compile and preview the full system prompt for a persona.

    Returns the compiled prompt and validation result before a debate starts.
    """
    service = PersonaService(db)
    return await service.preview_prompt(persona_id)
