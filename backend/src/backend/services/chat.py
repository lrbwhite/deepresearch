"""会话服务：组装图与 checkpointer，对外提供流式执行入口"""

from pathlib import Path

import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from backend.core.config import settings
from backend.graphs.search_agent import build_search_agent


class ChatService:
    def __init__(self) -> None:
        self._conn: aiosqlite.Connection | None = None
        self._checkpointer: AsyncSqliteSaver | None = None
        self._graph = None

    async def startup(self) -> None:
        """创建数据库连接并构建图（应用启动时调用）"""
        db_path = Path(settings.sqlite_db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        self._conn = await aiosqlite.connect(db_path)
        self._checkpointer = AsyncSqliteSaver(self._conn)
        await self._checkpointer.setup()  # 建表（幂等）
        self._graph = build_search_agent(checkpointer=self._checkpointer)

    async def shutdown(self) -> None:
        if self._conn:
            await self._conn.close()

    async def stream_chat(self, thread_id: str, message: str):
        """流式执行对话图，逐个产出图事件（astream_events v2）"""
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [("user", message)]}
        async for event in self._graph.astream_events(inputs, config):
            yield event
