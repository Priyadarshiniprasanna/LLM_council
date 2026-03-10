"""
DocumentService — file upload, chunking, embedding, and semantic retrieval.

Uploads go to S3-compatible object storage.
Processing (chunking + pgvector embedding) is handled by the ingestion worker.
"""

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.document_schema import DocumentResponse, DocumentSearchResponse


class DocumentService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def upload_document(self, debate_id: str, file: UploadFile) -> DocumentResponse:
        """
        Persist document metadata and upload raw bytes to object storage.

        Returns immediately with status='processing'. The ingestion_worker handles
        chunking, embedding, and pgvector indexing asynchronously.
        """
        raise NotImplementedError

    async def get_document(self, document_id: str) -> DocumentResponse | None:
        """Return document metadata and processing status by ID."""
        raise NotImplementedError

    async def search(
        self, debate_id: str, query: str, top_k: int = 5
    ) -> DocumentSearchResponse:
        """
        Semantic search over embedded document chunks for a debate room.

        Embeds the query text, runs pgvector cosine similarity search,
        and returns ranked chunks with citation anchors.
        """
        raise NotImplementedError
