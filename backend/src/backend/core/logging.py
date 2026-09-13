"""日志配置"""

import logging


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    # 降低三方库噪音
    logging.getLogger("httpx").setLevel(logging.WARNING)
