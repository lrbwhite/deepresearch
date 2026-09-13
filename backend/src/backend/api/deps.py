"""依赖注入"""

from fastapi import Request

from backend.services.chat import ChatService


def get_chat_service(request: Request) -> ChatService:
    """从 app.state 获取 ChatService（在应用 lifespan 中初始化）"""
    return request.app.state.chat_service
