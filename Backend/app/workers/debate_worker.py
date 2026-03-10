"""
DebateWorker — Temporal activities and workflow for debate turn progression.

Handles:
- Deterministic turn ordering and state machine transitions.
- Per-turn model calls via ModelGateway (with SSE streaming).
- Pause/resume signals from the API.
- Retry and timeout policies for each turn.
- End-of-debate summary trigger.

Workflow name: "DebateWorkflow"
Task queue: configured via settings.temporal_task_queue
"""

from temporalio import activity, workflow
from temporalio.common import RetryPolicy

from app.config import settings

DEFAULT_TURN_TIMEOUT_SECONDS = 120
DEFAULT_RETRY_POLICY = RetryPolicy(maximum_attempts=3)


@workflow.defn(name="DebateWorkflow")
class DebateWorkflow:
    """
    Temporal workflow for a single debate session.

    Drives turn-by-turn agent responses until the debate is ended or the
    maximum turn count is reached. Supports pause/resume via signals.
    """

    @workflow.run
    async def run(self, debate_id: str) -> str:
        """
        Main workflow loop.

        Returns the debate_id when the workflow completes.
        """
        raise NotImplementedError

    @workflow.signal
    async def pause(self) -> None:
        """Signal the workflow to pause after the current turn completes."""
        raise NotImplementedError

    @workflow.signal
    async def resume(self) -> None:
        """Signal the workflow to resume from a paused state."""
        raise NotImplementedError

    @workflow.signal
    async def end(self) -> None:
        """Signal the workflow to terminate cleanly after the current turn."""
        raise NotImplementedError


@activity.defn(name="execute_turn")
async def execute_turn(debate_id: str, turn_number: int, participant_id: str) -> dict:
    """
    Execute a single agent turn.

    Fetches debate context, calls ModelGateway with the participant's compiled prompt,
    persists the turn result, and returns the response payload.

    Inputs:
        debate_id: the debate this turn belongs to.
        turn_number: 1-indexed position in the turn order.
        participant_id: the agent taking this turn.
    Side effects:
        Writes turn result to DB and publishes event to Redis pub/sub for SSE fan-out.
    """
    raise NotImplementedError


@activity.defn(name="generate_summary")
async def generate_summary(debate_id: str) -> dict:
    """
    Generate end-of-debate outputs: executive summary, minutes, action items, dissent/risk.

    Called once after the workflow ends.
    Side effects: Writes summary record to DB.
    """
    raise NotImplementedError


async def start_worker() -> None:
    """
    Entry point for running the Temporal worker process.

    Connects to the Temporal server and polls for debate workflow/activity tasks.
    """
    import temporalio.client as tc
    import temporalio.worker as tw

    client = await tc.Client.connect(settings.temporal_host)
    worker = tw.Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[DebateWorkflow],
        activities=[execute_turn, generate_summary],
    )
    await worker.run()
