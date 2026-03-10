"""
Debate API routes — room lifecycle, participants, and turn management.

All business logic is delegated to DebateService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.debate_schema import (
    DebateCreateRequest,
    DebateResponse,
    DebateSummaryResponse,
    ParticipantAddRequest,
)
from app.services.debate_service import DebateService

router = APIRouter(prefix="/debates")


@router.post("/", response_model=DebateResponse, status_code=status.HTTP_201_CREATED)
async def create_debate(
    payload: DebateCreateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> DebateResponse:
    """Create a new debate room from a problem statement."""
    service = DebateService(db)
    return await service.create_debate(payload)


@router.get("/{debate_id}", response_model=DebateResponse)
async def get_debate(
    debate_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> DebateResponse:
    """Retrieve a debate by ID."""
    service = DebateService(db)
    debate = await service.get_debate(debate_id)
    if not debate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debate not found")
    return debate


@router.post("/{debate_id}/participants", response_model=DebateResponse)
async def add_participant(
    debate_id: str,
    payload: ParticipantAddRequest,
    db: AsyncSession = Depends(get_db_session),
) -> DebateResponse:
    """Add a participant (role + model mapping) to an existing debate."""
    service = DebateService(db)
    return await service.add_participant(debate_id, payload)


@router.post("/{debate_id}/start", response_model=DebateResponse)
async def start_debate(
    debate_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> DebateResponse:
    """Start a debate — triggers Temporal workflow."""
    service = DebateService(db)
    return await service.start_debate(debate_id)


@router.post("/{debate_id}/pause", response_model=DebateResponse)
async def pause_debate(
    debate_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> DebateResponse:
    """Pause an in-progress debate."""
    service = DebateService(db)
    return await service.pause_debate(debate_id)


@router.post("/{debate_id}/end", response_model=DebateResponse)
async def end_debate(
    debate_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> DebateResponse:
    """End a debate and trigger summary generation."""
    service = DebateService(db)
    return await service.end_debate(debate_id)


@router.get("/{debate_id}/summary", response_model=DebateSummaryResponse)
async def get_summary(
    debate_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> DebateSummaryResponse:
    """Retrieve the generated summary for a completed debate."""
    service = DebateService(db)
    summary = await service.get_summary(debate_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Summary not yet available"
        )
    return summary
