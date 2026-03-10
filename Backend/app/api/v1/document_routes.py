"""
Document API routes — file upload, processing, and citation retrieval.

All business logic is delegated to DocumentService.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.document_schema import DocumentResponse, DocumentSearchResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents")


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    debate_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session),
) -> DocumentResponse:
    """
    Upload a document for a debate room.

    Triggers async ingestion: chunking, embedding, and indexing in pgvector.
    Returns immediately with a processing status; poll GET /{document_id} for completion.
    """
    service = DocumentService(db)
    return await service.upload_document(debate_id=debate_id, file=file)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> DocumentResponse:
    """Retrieve document metadata and processing status."""
    service = DocumentService(db)
    document = await service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document


@router.get("/search", response_model=DocumentSearchResponse)
async def search_documents(
    debate_id: str,
    query: str,
    top_k: int = 5,
    db: AsyncSession = Depends(get_db_session),
) -> DocumentSearchResponse:
    """
    Semantic search over documents for a debate room.

    Returns ranked chunks with citation anchors for use in model context.
    """
    service = DocumentService(db)
    return await service.search(debate_id=debate_id, query=query, top_k=top_k)
