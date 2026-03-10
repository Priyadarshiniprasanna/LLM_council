"""
DebateService — room lifecycle, participant management, and turn policy.

Owns all state transitions for a debate: created → active → paused → ended.
Triggers Temporal workflows for turn progression and summary generation.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.debate_schema import (
    DebateCreateRequest,
    DebateResponse,
    DebateSummaryResponse,
    ParticipantAddRequest,
)


class DebateService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_debate(self, payload: DebateCreateRequest) -> DebateResponse:
        """
        Create a new debate room.

        Persists the debate record and returns initial state.
        Does not start the Temporal workflow — call start_debate() separately.
        """
        raise NotImplementedError

    async def get_debate(self, debate_id: str) -> DebateResponse | None:
        """Return debate state by ID, or None if not found."""
        raise NotImplementedError

    async def add_participant(
        self, debate_id: str, payload: ParticipantAddRequest
    ) -> DebateResponse:
        """
        Add a participant to an existing debate.

        Each participant requires a role name and a model identifier (for model_gateway routing).
        Debate must be in 'created' status — participants cannot be added once started.
        """
        raise NotImplementedError

    async def start_debate(self, debate_id: str) -> DebateResponse:
        """
        Start a debate.

        Validates all participants have valid compiled prompts, then triggers the
        Temporal debate workflow for deterministic turn/state progression.
        """
        raise NotImplementedError

    async def pause_debate(self, debate_id: str) -> DebateResponse:
        """Send a pause signal to the running Temporal workflow."""
        raise NotImplementedError

    async def end_debate(self, debate_id: str) -> DebateResponse:
        """
        End a debate and trigger async summary generation.

        Terminates the Temporal workflow and queues the ingestion worker
        to produce executive summary, minutes, action items, and dissent/risk.
        """
        raise NotImplementedError

    async def get_summary(self, debate_id: str) -> DebateSummaryResponse | None:
        """Return the generated summary, or None if not yet available."""
        raise NotImplementedError
