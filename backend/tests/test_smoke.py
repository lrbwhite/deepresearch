"""骨架 smoke 测试：应用与图均可正常构建导入"""


def test_import_app():
    from backend.main import app

    assert app.title == "DeepResearch Agent API"


def test_import_search_agent_builder():
    from backend.graphs.search_agent import build_search_agent

    assert callable(build_search_agent)
