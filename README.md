# Config Loader

一个简洁的Python配置加载器，支持环境变量替换和配置文件合并，设计灵感来自Spring Framework的配置加载机制。

## 功能特性

- 📋 **默认配置加载** - 自动读取 `config.yaml` 基础配置文件
- 🔀 **环境配置合并** - 通过 `active` 参数决定合并的配置文件（如 `config.dev.yaml`）
- 🌍 **环境变量支持** - 支持 `${VAR_NAME:default_value}` 格式的环境变量替换
- 🎯 **灵活的active配置** - `active` 字段本身也支持环境变量，如 `active: ${ENV:dev}`
- 🔍 **自动查找配置** - 自动在当前目录和 `configs/` 子目录中查找配置文件

## 安装

### 使用 uv（推荐）

```bash
uv pip install config-loader
```

### 使用 pip

```bash
pip install config-loader
```

### 从源码安装

```bash
git clone https://github.com/cncws/config-loader.git
cd config-loader
pip install -e .
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
from config_loader import load_yaml
import os

# 设置环境变量
os.environ["DB_PASSWORD"] = "my_secure_pass"
os.environ["SERVER_PORT"] = "9000"

# 加载配置
config = load_yaml()

# 访问配置值
db_host = config["db"]["host"]  # "127.0.0.1" (来自config.dev.yaml)
db_port = config["db"]["port"]  # 3306
db_password = config["db"]["password"]  # "my_secure_pass"
server_port = config["server"]["port"]  # "9000"
```

## 配置加载流程

1. **查找配置文件** - 在当前目录或 `configs/` 子目录中查找 `config.yaml`
2. **加载基础配置** - 读取 `config.yaml` 文件
3. **处理active字段** - 获取并替换 `active` 字段中的环境变量
4. **合并环境配置** - 如果 `active: dev`，则加载并合并 `config.dev.yaml`
5. **替换环境变量** - 将所有 `${VAR_NAME:default}` 替换为实际值

## 高级用法

### active 字段支持环境变量

`active` 字段本身支持环境变量，这样可以通过环境变量动态切换配置环境：

```yaml
# config.yaml
active: ${CONFIG_ENV:dev}

app:
  name: MyApp
```

```python
import os
from config_loader import load_yaml

# 通过环境变量控制使用哪个配置文件
os.environ["CONFIG_ENV"] = "prod"

config = load_yaml()  # 会加载并合并 config.prod.yaml
```

### 环境变量格式

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

### 配置文件查找路径

配置加载器会按以下顺序查找 `config.yaml`：

1. 当前工作目录（`os.getcwd()`）
2. 当前工作目录下的 `configs/` 子目录

## API 文档

### load_yaml() -> Dict[str, Any]

加载并返回配置字典。

**返回值**：
- `Dict[str, Any]` - 合并后的配置字典，所有环境变量已被替换

**异常**：
- `FileNotFoundError` - 如果找不到 `config.yaml` 文件

**示例**：

```python
from config_loader import load_yaml

config = load_yaml()
print(config["app"]["name"])
```

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
├── pyproject.toml           # 项目配置
├── README.md                # 项目文档
└── .gitignore               # Git忽略配置
```

## 与Spring配置加载的对比

| 功能 | Spring | Config Loader |
|-----|--------|---------------|
| 默认配置文件 | application.properties | config.yaml |
| 环境配置 | application-{active}.properties | config.{active}.yaml |
| 环境变量 | ${ENV_VAR:default} | ${ENV_VAR:default} |
| 配置格式 | properties/yaml | yaml |
| active字段支持环境变量 | ✅ | ✅ |

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
