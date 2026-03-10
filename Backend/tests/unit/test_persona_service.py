"""
Unit tests for PersonaService.

Tests cover persona creation, AI generation flow,
and prompt validation rules.
"""

import pytest


class TestPersonaServiceCreate:
    async def test_create_persona_stores_raw_prompt(self) -> None:
        """A manually created persona must store the provided raw_prompt."""
        pytest.skip("Not yet implemented — implement alongside PersonaService.create_persona()")

    async def test_create_persona_sets_source_mode_to_manual(self) -> None:
        """Manually created personas must have source_mode='manual'."""
        pytest.skip("Not yet implemented")


class TestPersonaServiceGenerate:
    async def test_generate_persona_sets_source_mode_to_ai_generated(self) -> None:
        """AI-generated personas must have source_mode='ai_generated'."""
        pytest.skip("Not yet implemented")

    async def test_generate_persona_validates_model_output(self) -> None:
        """Generated persona output must pass schema validation before persisting."""
        pytest.skip("Not yet implemented")


class TestPersonaServicePromptValidation:
    async def test_preview_prompt_returns_pass_for_valid_persona(self) -> None:
        """A fully valid persona must return validation.passed=True."""
        pytest.skip("Not yet implemented")

    async def test_preview_prompt_returns_fail_for_empty_prompt(self) -> None:
        """A persona with an empty compiled_prompt must fail validation."""
        pytest.skip("Not yet implemented")

    async def test_invalid_prompt_blocks_debate_start(self) -> None:
        """Attempting to start a debate with a participant whose prompt is invalid must raise."""
        pytest.skip("Not yet implemented")
