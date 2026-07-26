from fastapi import APIRouter
from openai import OpenAI

from app.core.config import OPENAI_API_KEY
from app.schemas.chat import ChatRequest, ChatResponse
from app.prompts.auction_prompt import SYSTEM_PROMPT

router = APIRouter()

client = OpenAI(api_key=OPENAI_API_KEY)

@router.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:

    response = client.responses.create(
        model="gpt-5.5",
        instructions=SYSTEM_PROMPT,
        input=request.message,
    )

    return ChatResponse(
        response=response.output_text
    )