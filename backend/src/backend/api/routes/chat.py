"""对话路由：SSE 流式接口"""

import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from backend.api.deps import get_chat_service
from backend.schemas.chat import ChatRequest
from backend.services.chat import ChatService

router = APIRouter(tags=["chat"])


@router.post("/chat")
async def chat(
    req: ChatRequest,
    service: ChatService = Depends(get_chat_service),
) -> StreamingResponse:
    """SSE 流式对话

    事件格式（data: {json}）：
      {"type": "token", "content": "..."}   模型增量输出
      {"type": "done"}                       本轮回答结束
    """

    async def event_stream():
        async for event in service.stream_chat(req.thread_id, req.message):
            if event["event"] == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    payload = json.dumps(
                        {"type": "token", "content": content},
                        ensure_ascii=False,
                    )
                    yield f"data: {payload}\n\n"
        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
