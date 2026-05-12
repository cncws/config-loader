"""
配置加载器使用示例

cd examples && uv run usage.py
"""

import json
import os

from config_loader import load_yaml


def main():
    # 直接加载配置
    config = load_yaml()

    print("=" * 50)
    print("完整配置:")
    print("=" * 50)

    print(json.dumps(config, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # 设置一些环境变量示例
    os.environ["RUN_ENV"] = "development"
    os.environ["DB_PASSWORD"] = "my_secure_pass"
    os.environ["REDIS_HOST"] = "redis.example.com"
    os.environ["SERVER_PORT"] = "9000"

    main()
