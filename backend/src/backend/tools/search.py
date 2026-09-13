"""web 搜索工具（Tavily）"""

from langchain_tavily import TavilySearch


def get_web_search() -> TavilySearch:
    """创建 web 搜索工具实例（构建图时调用，避免导入期校验 API key）"""
    return TavilySearch(max_results=5)
