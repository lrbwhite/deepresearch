"""搜索 agent：ReAct 模式（LLM + web 搜索工具循环）"""

from re import search

# from backend.src.backend.prompts import search_agent
from backend.prompts import search_agent
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from backend.core.config import settings
from backend.prompts.search_agent import SEARCH_AGENT_SYSTEM_PROMPT
from backend.tools.search import get_web_search


def build_search_agent(checkpointer=None):
    """构建搜索 agent 图

    Args:
        checkpointer: LangGraph checkpointer，传入 AsyncSqliteSaver 实现会话持久化
    """
    llm = ChatOpenAI(
        model=settings.qwen_model,
        api_key=settings.dashscope_api_key,
        base_url=settings.dashscope_base_url,
        temperature=0,
    )
    return create_react_agent(
        model=llm,
        tools=[get_web_search()],
        prompt=SEARCH_AGENT_SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

if __name__=="__main__":

    from dotenv import load_dotenv
    load_dotenv()
    search_agent=build_search_agent()
    print(search_agent.invoke("帮我查询2026中国法定节假日放假安排"))
