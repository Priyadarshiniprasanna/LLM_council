"""
Unit tests for DebateService.

Tests cover state machine transitions, participant validation,
and policy enforcement — not DB or Temporal integration.
"""

import pytest


class TestDebateServiceCreate:
    async def test_create_debate_returns_created_status(self) -> None:
        """A new debate must start in 'created' status."""
        pytest.skip("Not yet implemented — implement alongside DebateService.create_debate()")

    async def test_create_debate_requires_problem_statement(self) -> None:
        """Creating a debate without a problem statement must raise a validation error."""
        pytest.skip("Not yet implemented")


class TestDebateServiceParticipants:
    async def test_add_participant_succeeds_when_debate_is_created(self) -> None:
        """Adding a participant to a 'created' debate must succeed."""
        pytest.skip("Not yet implemented")

    async def test_add_participant_blocked_when_debate_is_active(self) -> None:
        """Adding a participant after debate starts must raise an error."""
        pytest.skip("Not yet implemented")


class TestDebateServiceTransitions:
    async def test_start_debate_triggers_temporal_workflow(self) -> None:
        """Starting a debate must set status to 'active' and record a workflow ID."""
        pytest.skip("Not yet implemented")

    async def test_start_debate_blocked_without_participants(self) -> None:
        """Debate with zero participants must not be startable."""
        pytest.skip("Not yet implemented")

    async def test_pause_debate_transitions_to_paused(self) -> None:
        """Pausing an active debate must set status to 'paused'."""
        pytest.skip("Not yet implemented")

    async def test_end_debate_transitions_to_ended(self) -> None:
        """Ending a debate must set status to 'ended'."""
        pytest.skip("Not yet implemented")
