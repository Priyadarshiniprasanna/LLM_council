"""
IngestionWorker — background document processing pipeline.

Handles:
- Fetching raw document bytes from object storage.
- Text extraction and chunking.
- Embedding generation via ModelGateway.
- Indexing chunks into pgvector with citation anchors.
- Updating document status on completion or failure.

This worker runs as a separate process and is triggered by DocumentService
after a successful file upload.
"""

from temporalio import activity, workflow

from app.config import settings

DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 64


@workflow.defn(name="DocumentIngestionWorkflow")
class DocumentIngestionWorkflow:
    """
    Temporal workflow for end-to-end document ingestion.

    Orchestrates: download → extract → chunk → embed → index.
    """

    @workflow.run
    async def run(self, document_id: str) -> str:
        """
        Run the full ingestion pipeline for a document.

        Returns the document_id on success.
        Updates document status to 'ready' or 'failed' in DB.
        """
        raise NotImplementedError


@activity.defn(name="download_document")
async def download_document(document_id: str) -> bytes:
    """
    Download document bytes from object storage.

    Inputs: document_id mapped to an S3 object key in the DB.
    Outputs: raw document bytes.
    """
    raise NotImplementedError


@activity.defn(name="chunk_document")
async def chunk_document(document_id: str, raw_bytes: bytes) -> list[dict]:
    """
    Extract text and split into overlapping chunks.

    Returns a list of chunk dicts: {text, page, char_offset, chunk_index}.
    Uses DEFAULT_CHUNK_SIZE and DEFAULT_CHUNK_OVERLAP unless overridden by doc settings.
    """
    raise NotImplementedError


@activity.defn(name="embed_chunks")
async def embed_chunks(document_id: str, chunks: list[dict]) -> list[dict]:
    """
    Generate embeddings for each chunk via ModelGateway.

    Returns chunks with an added 'embedding' field (float list).
    """
    raise NotImplementedError


@activity.defn(name="index_chunks")
async def index_chunks(document_id: str, chunks: list[dict]) -> None:
    """
    Insert embedded chunks into the pgvector index.

    Each chunk is stored with citation anchor metadata for retrieval.
    """
    raise NotImplementedError


async def start_worker() -> None:
    """Entry point for running the ingestion Temporal worker process."""
    import temporalio.client as tc
    import temporalio.worker as tw

    client = await tc.Client.connect(settings.temporal_host)
    worker = tw.Worker(
        client,
        task_queue=f"{settings.temporal_task_queue}-ingestion",
        workflows=[DocumentIngestionWorkflow],
        activities=[download_document, chunk_document, embed_chunks, index_chunks],
    )
    await worker.run()
