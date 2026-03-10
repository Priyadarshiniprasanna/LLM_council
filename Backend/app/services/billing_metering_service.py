"""
BillingMeteringService — token and cost accounting per org/workspace.

Records every model call's token usage, computes cost estimates,
and enforces daily spend limits. Feeds into observability dashboards.
"""

from sqlalchemy.ext.asyncio import AsyncSession


class BillingMeteringService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def record_usage(
        self,
        org_id: str,
        workspace_id: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        debate_id: str | None = None,
    ) -> None:
        """
        Persist a token usage record for a model call.

        Called by ModelGateway after every completion request.
        Increments the org's daily spend counter.
        """
        raise NotImplementedError

    async def get_daily_spend(self, org_id: str) -> dict:
        """
        Return total token counts and estimated cost for the current UTC day.

        Used by ModelGateway's policy check to enforce spend limits.
        """
        raise NotImplementedError

    async def get_workspace_usage(
        self, workspace_id: str, start_date: str, end_date: str
    ) -> list[dict]:
        """
        Return a time-series of token usage for a workspace within a date range.

        Used for billing dashboards and export.
        """
        raise NotImplementedError
