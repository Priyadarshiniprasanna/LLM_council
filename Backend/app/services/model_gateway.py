"""
ModelGateway — single point of entry for all LLM calls.

Enforces:
- All model calls go exclusively through OpenRouter.
- OpenRouter API key is added at runtime (never logged or leaked).
- Per-org policy checks: allowed model list, max spend/day.
- Metering: token counts recorded per request for billing service.
- Retry logic with exponential backoff on transient errors.
"""

from app.config import settings


class ModelGateway:
    """
    Mediates all interactions with OpenRouter.

    Key inputs: model identifier, messages, org policy context.
    Key outputs: streamed or batched completion response.
    Side effects: records token usage to billing_metering_service.
    """

    def __init__(self) -> None:
        self._base_url = str(settings.openrouter_base_url)

    async def complete(
        self,
        model: str,
        messages: list[dict[str, str]],
        org_id: str,
        stream: bool = False,
    ) -> dict | None:
        """
        Send a completion request to OpenRouter.

        Applies org-level policy (allowed models, spend limits) before dispatch.
        If stream=True, returns an async generator of token chunks via SSE.
        """
        raise NotImplementedError

    async def _check_org_policy(self, org_id: str, model: str) -> None:
        """
        Enforce org-level model access policy.

        Raises PermissionError if the model is not in the org's allowed list
        or the daily spend budget has been reached.
        """
        raise NotImplementedError

    async def _record_usage(self, org_id: str, model: str, tokens_used: int) -> None:
        """Forward token consumption to the billing_metering_service."""
        raise NotImplementedError
