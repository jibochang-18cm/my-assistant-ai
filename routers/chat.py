from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from rag import ask_ai_assistant_stream
from schemas import QueryRequest

router = APIRouter()


@router.post("/api/chat")
async def chat(req: QueryRequest):
    """向 AI 助教提问"""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="提问不能为空")
    return StreamingResponse(
        ask_ai_assistant_stream(req.question, req.history),
        media_type="text/event-stream"
    )
