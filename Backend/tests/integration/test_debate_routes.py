"""
Integration tests for debate API routes.

Tests verify the full request → service → DB round-trip using
an in-memory or test Postgres database via the FastAPI test client.
"""

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


class TestCreateDebate:
    async def test_create_debate_returns_201(self, client: AsyncClient) -> None:
        """POST /api/v1/debates must return 201 with the new debate."""
        pytest.skip("Not yet implemented — requires DB fixture setup")

    async def test_create_debate_missing_problem_statement_returns_422(
        self, client: AsyncClient
    ) -> None:
        """POST /api/v1/debates without problem_statement must return 422."""
        pytest.skip("Not yet implemented")


class TestGetDebate:
    async def test_get_debate_returns_200(self, client: AsyncClient) -> None:
        """GET /api/v1/debates/{id} must return 200 for an existing debate."""
        pytest.skip("Not yet implemented")

    async def test_get_debate_returns_404_for_unknown_id(self, client: AsyncClient) -> None:
        """GET /api/v1/debates/{unknown_id} must return 404."""
        pytest.skip("Not yet implemented")


class TestDebateLifecycle:
    async def test_full_lifecycle_create_add_participant_start_end(
        self, client: AsyncClient
    ) -> None:
        """
        Full happy-path integration test:
        create → add participant → start → end.

        Each step must succeed and return the correct status transition.
        """
        pytest.skip("Not yet implemented — requires Temporal test server")
