from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.openai_service import stream_chat

router = APIRouter()


@router.post("/chat")
def chat_stream(request: ChatRequest) -> StreamingResponse:

    return StreamingResponse(
        stream_chat(request.message),
        media_type="text/plain",
    )