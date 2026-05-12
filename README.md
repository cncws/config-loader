# Config Loader

一个简洁的Python配置加载器，支持环境变量替换和配置文件合并，设计灵感来自Spring Framework的配置加载机制。

## 功能特性

- 📋 **默认配置加载** - 自动读取 `config.yaml` 基础配置文件
- 🔀 **环境配置合并** - 通过 `active` 参数决定合并的配置文件（如 `config.dev.yaml`）
- 🌍 **环境变量支持** - 支持 `${VAR_NAME:default_value}` 格式的环境变量替换
- 🎯 **点号访问** - 支持 `config.get("db.host")` 这样的嵌套访问

## 安装

### 从源码安装

```bash
pip install -e .
```

### 从PyPI安装（发布后）

```bash
pip install config-loader
```

## 快速开始

### 1. 创建配置文件

**config.yaml** - 基础配置

```yaml
active: dev

app:
  name: MyApp
  debug: false

db:
  host: localhost
  port: 3306
  user: root
  password: ${DB_PASSWORD:password123}

server:
  host: 0.0.0.0
  port: ${SERVER_PORT:8080}
```

**config.dev.yaml** - 开发环境配置（会合并到基础配置中）

```yaml
app:
  debug: true

db:
  host: 127.0.0.1
  password: ${DB_PASSWORD:dev_pass}

server:
  port: 8888
```

### 2. 使用配置加载器

```python
from config_loader import ConfigLoader
import os

# 设置环境变量
os.environ["DB_PASSWORD"] = "my_secure_pass"
os.environ["SERVER_PORT"] = "9000"

# 创建加载器实例
loader = ConfigLoader(config_dir="./config")

# 加载配置
config = loader.load()

# 获取配置值
db_host = loader.get("db.host")  # "127.0.0.1" (来自config.dev.yaml)
db_port = loader.get("db.port")  # 3306
db_password = loader.get("db.password")  # "my_secure_pass"
server_port = loader.get("server.port")  # "9000"

# 获取不存在的配置，提供默认值
timeout = loader.get("db.timeout", 30)  # 30
```

## 配置加载流程

1. **加载基础配置** - 读取 `config.yaml` 文件
2. **读取active值** - 获取 `config.yaml` 中的 `active` 字段
3. **合并环境配置** - 如果 `active: dev`，则加载并合并 `config.dev.yaml`
4. **替换环境变量** - 将所有 `${VAR_NAME:default}` 替换为实际值

## 环境变量格式

支持两种格式：

- `${VAR_NAME}` - 直接读取环境变量，如果不存在则为空字符串
- `${VAR_NAME:default_value}` - 读取环境变量，如果不存在则使用默认值

示例：

```yaml
# 环境变量存在
database: ${DB_HOST:localhost}  # 如果DB_HOST=mydb.com，则为 "mydb.com"

# 环境变量不存在
database: ${DB_HOST:localhost}  # 使用默认值 "localhost"

# 不指定默认值
api_key: ${API_KEY}  # 如果API_KEY不存在，则为空字符串
```

## API 文档

### ConfigLoader

#### `__init__(config_dir: str = ".")`

初始化配置加载器

- `config_dir` - 配置文件所在目录，默认为当前目录

#### `load() -> Dict[str, Any]`

加载并返回配置字典

#### `get(key: str, default: Any = None) -> Any`

获取配置值

- `key` - 配置键，支持点号分隔的嵌套路径（如 `"db.host"`）
- `default` - 如果键不存在的默认值

## 运行示例

```bash
cd examples
python usage.py
```

## 运行测试

```bash
# 安装测试依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 带覆盖率的测试
pytest tests/ --cov=config_loader
```

## 项目结构

```
config-loader/
├── config_loader/
│   ├── __init__.py          # 包初始化
│   └── loader.py            # 核心实现
├── examples/
│   ├── config.yaml          # 基础配置示例
│   ├── config.dev.yaml      # 开发环境配置示例
│   └── usage.py             # 使用示例
├── tests/
│   └── test_loader.py       # 单元测试
├── setup.py                 # 打包配置
├── README.md                # 项目文档
└── .gitignore               # Git忽略配置
```

## 打包和发布

### 构建包

```bash
python setup.py sdist bdist_wheel
```

### 上传到PyPI（需要账号）

```bash
pip install twine
twine upload dist/*
```

## 与Spring配置加载的对比

| 功能 | Spring | Config Loader |
|-----|--------|---------------|
| 默认配置文件 | application.properties | config.yaml |
| 环境配置 | application-{active}.properties | config.{active}.yaml |
| 环境变量 | ${ENV_VAR:default} | ${ENV_VAR:default} |
| 配置访问 | @Value | get() 方法 |
| 配置格式 | properties/yaml | yaml |

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
