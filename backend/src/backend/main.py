"""FastAPI 应用入口"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.routes import chat
from backend.core.logging import setup_logging
from backend.services.chat import ChatService


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    service = ChatService()
    await service.startup()
    app.state.chat_service = service
    yield
    await service.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(title="DeepResearch Agent API", lifespan=lifespan)
    app.include_router(chat.router, prefix="/api")
    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
