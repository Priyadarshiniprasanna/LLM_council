"""
ResearchGateway — policy-controlled internet verification for debate agents.

Internet access is DISABLED by default.
When enabled per-agent, all requests are mediated here:
- domain allowlist enforcement,
- per-session request/token/time budgets,
- approval mode (auto vs human-in-the-loop),
- full audit logging with source linking.

Agents never browse directly — all external calls are proxied through this gateway.
"""

from app.config import settings


class ResearchGateway:
    """
    Mediates policy-controlled internet access for debate agents.

    Key inputs: agent ID, debate ID, query, org policy context.
    Key outputs: source-linked research results.
    Side effects: audit log entry for every request/result.
    """

    async def fetch(
        self,
        agent_id: str,
        debate_id: str,
        query: str,
        org_id: str,
    ) -> dict:
        """
        Execute a research query on behalf of an agent.

        Enforces: gateway_enabled flag, domain allowlist, budget limits.
        Raises PermissionError if research is disabled or policy is violated.
        Returns results with source URLs and relevance scores.
        """
        if not settings.research_gateway_enabled:
            raise PermissionError("Research gateway is disabled. Enable per-org policy to use.")
        raise NotImplementedError

    async def _check_budget(self, agent_id: str, debate_id: str) -> None:
        """
        Check whether the agent has remaining request budget for this session.

        Raises BudgetExceededError if the session limit has been reached.
        """
        raise NotImplementedError

    async def _enforce_domain_allowlist(self, url: str, org_id: str) -> None:
        """Raise PermissionError if the target domain is not in the org's allowlist."""
        raise NotImplementedError

    async def _audit_log(
        self, agent_id: str, debate_id: str, query: str, result: dict
    ) -> None:
        """Persist a research request/result record for audit purposes."""
        raise NotImplementedError
