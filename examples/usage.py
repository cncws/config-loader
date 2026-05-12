"""
配置加载器使用示例
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_loader import load_yaml


def main():
    # 直接加载配置
    config = load_yaml()

    print("=" * 50)
    print("完整配置:")
    print("=" * 50)
    import json

    print(json.dumps(config, indent=2, ensure_ascii=False))

    print("\n" + "=" * 50)
    print("获取单个配置值:")
    print("=" * 50)
    app = config.get("app", {})
    db = config.get("db", {})
    server = config.get("server", {})

    print(f"app.name: {app.get('name')}")
    print(f"app.debug: {app.get('debug')}")
    print(f"db.host: {db.get('host')}")
    print(f"db.database: {db.get('database')}")
    print(f"server.port: {server.get('port')}")
    print(f"server.env: {server.get('env')}")
    print(
        f"不存在的配置 (有默认值): {config.get('unknown', {}).get('key', 'default_value')}"
    )


if __name__ == "__main__":
    # 设置一些环境变量示例
    os.environ["RUN_ENV"] = "development"
    os.environ["DB_PASSWORD"] = "my_secure_pass"
    os.environ["REDIS_HOST"] = "redis.example.com"
    os.environ["SERVER_PORT"] = "9000"

    main()
