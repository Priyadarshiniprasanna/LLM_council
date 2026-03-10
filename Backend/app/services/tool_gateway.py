"""
ToolGateway — controlled execution of registered tools and MCP adapters.

Tool calling is DISABLED by default.
All tool calls must be registered in the tool registry with a risk tier (T0–T3).
Higher-tier tools require explicit approval before execution.
MCP server calls are restricted to an org-level allowlist.

See doc 13-tool-registry-and-mcp-policy-matrix.md for full policy matrix.
"""


class ToolGateway:
    """
    Mediates all agent tool executions.

    Key inputs: tool name, inputs, agent ID, org policy context.
    Key outputs: tool execution result.
    Side effects: audit log with inputs, outputs, and approval record.
    """

    async def execute(
        self,
        tool_name: str,
        inputs: dict,
        agent_id: str,
        debate_id: str,
        org_id: str,
    ) -> dict:
        """
        Execute a registered tool on behalf of an agent.

        Enforces: tool registration check, risk tier policy, spend budget, approval flow.
        Raises PermissionError for unregistered tools or policy violations.
        """
        raise NotImplementedError

    async def _check_registration(self, tool_name: str) -> dict:
        """
        Look up the tool in the registry.

        Raises PermissionError if the tool is not registered.
        Returns tool metadata including risk tier and allowed orgs.
        """
        raise NotImplementedError

    async def _require_approval(
        self, tool_name: str, risk_tier: str, org_id: str, inputs: dict
    ) -> bool:
        """
        Determine if human approval is required for this tool call.

        T0/T1: auto-approved. T2: org-policy dependent. T3: always requires approval.
        """
        raise NotImplementedError

    async def _audit_log(
        self,
        tool_name: str,
        inputs: dict,
        result: dict,
        agent_id: str,
        approved_by: str | None,
    ) -> None:
        """Persist tool call record with provenance for audit."""
        raise NotImplementedError
