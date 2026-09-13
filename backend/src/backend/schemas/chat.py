"""对话接口的请求/响应模型"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """对话请求"""

    thread_id: str = Field(..., description="会话 ID，用于跨请求持久化上下文")
    message: str = Field(..., min_length=1, description="用户消息")
