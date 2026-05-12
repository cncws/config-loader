# Config Loader

一个轻量级的 Python 配置加载器，灵感来自 Spring Framework 的配置机制。

## 功能

- YAML 配置加载和合并
- 环境变量替换（支持默认值）
- 多环境配置支持（基于 `active` 字段）
- 自动配置文件查找

## 安装

```bash
uv pip install config-loader
```

## 快速开始

**config.yaml**
```yaml
active: dev

app:
  name: MyApp
  debug: false

db:
  host: localhost
  port: 3306
  password: ${DB_PASSWORD:-default123}
```

**config.dev.yaml**
```yaml
app:
  debug: true

db:
  host: 127.0.0.1
```

**使用**
```python
from config_loader import load_yaml
import os

os.environ["DB_PASSWORD"] = "my_pass"
config = load_yaml()

print(config["app"]["debug"])      # True (来自 config.dev.yaml)
print(config["db"]["password"])    # "my_pass"
```

## 环境变量语法

- `${VAR}` - 使用环境变量，不存在时为空
- `${VAR:-default}` - 使用环境变量，不存在时用默认值（兼容 `${VAR:default}` 旧写法）

## 详细文档

参见 [CLAUDE.md](CLAUDE.md) 了解完整的开发指南。

## 高级用法

### active 字段支持环境变量

`active` 字段本身支持环境变量，这样可以通过环境变量动态切换配置环境：

```yaml
# config.yaml
active: ${CONFIG_ENV:-dev}

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
- `${VAR_NAME:-default_value}` - 读取环境变量，如果不存在则使用默认值

示例：

```yaml
# 环境变量存在
database: ${DB_HOST:-localhost}  # 如果DB_HOST=mydb.com，则为 "mydb.com"

# 环境变量不存在
database: ${DB_HOST:-localhost}  # 使用默认值 "localhost"

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
| 环境变量 | ${ENV_VAR:-default} | ${ENV_VAR:-default} |
| 配置格式 | properties/yaml | yaml |
| active字段支持环境变量 | ✅ | ✅ |

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
