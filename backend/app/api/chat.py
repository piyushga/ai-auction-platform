from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat import ChatRequest
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/chat")
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    rag_service = RAGService(db)

    return StreamingResponse(
        rag_service.stream_answer(request.message),
        media_type="text/plain",
    )
