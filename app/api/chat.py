from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.llm.mock import MockLLM
from app.llm.hf_llm import HuggingFaceLLM

router = APIRouter()

llm = HuggingFaceLLM()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await llm.generate(
        prompt=request.prompt,
        user_id=request.user_id
    )
    return ChatResponse(response=response)

