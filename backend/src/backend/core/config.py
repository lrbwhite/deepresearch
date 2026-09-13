"""全局配置：从 .env 读取"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM（百炼 OpenAI 兼容接口）
    dashscope_api_key: str = ""
    qwen_model: str = "qwen-plus"
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # 搜索工具
    tavily_api_key: str = ""

    # 会话持久化
    sqlite_db_path: str = "./data/checkpoints.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
