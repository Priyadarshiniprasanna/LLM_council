"""
PersonaService — persona templates, AI generation, and prompt compilation.

Supports three persona source modes: preset, AI-generated, and manual.
Compiled prompts are versioned and snapshotted per debate participant.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.persona_schema import (
    PersonaCreateRequest,
    PersonaGenerateRequest,
    PersonaResponse,
    PromptPreviewResponse,
)


class PersonaService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_persona(self, payload: PersonaCreateRequest) -> PersonaResponse:
        """Create a persona from a fully manual definition."""
        raise NotImplementedError

    async def generate_persona(self, payload: PersonaGenerateRequest) -> PersonaResponse:
        """
        Generate a persona using model_gateway.

        Calls the configured model with a generation prompt, validates the output
        against the PersonaSchema, and persists the result.
        """
        raise NotImplementedError

    async def get_persona(self, persona_id: str) -> PersonaResponse | None:
        """Return a persona by ID, or None if not found."""
        raise NotImplementedError

    async def preview_prompt(self, persona_id: str) -> PromptPreviewResponse:
        """
        Compile and validate the full system prompt for a persona.

        Runs all validation rules (length, required fields, forbidden patterns).
        Returns the compiled text plus a pass/fail validation result.
        Invalid prompts will block debate start.
        """
        raise NotImplementedError
