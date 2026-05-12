# Config Loader - AI 助手指南

本文档为 AI 助手（如 Claude）提供项目的核心信息和开发指南。

## 项目概述

Config Loader 是一个轻量级的 Python 配置加载器，灵感来自 Spring Framework 的配置机制。

**核心特性**：
- YAML 配置文件加载和合并
- 环境变量替换（支持默认值）
- 基于 `active` 字段的多环境配置支持
- 自动配置文件查找

## 项目结构

```
config-loader/
├── config_loader/           # 核心包
│   ├── __init__.py         # 导出 load_yaml
│   └── loader.py           # 核心实现
├── examples/               # 使用示例
├── tests/                  # 测试文件
│   └── test_loader.py     # 单元测试
├── pyproject.toml         # 项目配置（使用 hatchling）
├── README.md              # 用户文档
└── CLAUDE.md              # 本文件
```

## 核心实现

### loader.py 关键函数

1. **`load_yaml() -> Dict[str, Any]`**
   - 入口函数，负责整个配置加载流程
   - 查找配置文件 → 加载基础配置 → 处理 active → 合并环境配置 → 替换环境变量

2. **`_find_config_dir() -> str`**
   - 在当前目录和 `configs/` 子目录查找 `config.yaml`
   - 找不到时抛出 `FileNotFoundError`

3. **`_merge_dict(base: Dict, override: Dict) -> None`**
   - 深度合并字典，override 的值会覆盖 base
   - 嵌套字典递归合并

4. **`_replace_env_vars(obj: Any) -> Any`**
   - 递归替换对象中的环境变量占位符
   - 支持 `${VAR}` 和 `${VAR:default}` 两种格式
   - 处理字符串、字典、列表

## 关键设计决策

### 1. active 字段支持环境变量

**问题**：原始实现中，`active` 字段的值在合并配置文件前没有进行环境变量替换。

**解决方案**（已修复）：
```python
# 先对active值进行环境变量替换
active = config.get("active", "")
if active:
    active = _replace_env_vars(active).strip()
```

这允许用户通过环境变量动态控制使用哪个配置文件：
```yaml
active: ${CONFIG_ENV:dev}
```

### 2. 配置文件查找顺序

1. 当前工作目录（`os.getcwd()`）
2. `configs/` 子目录

这个设计让配置文件可以放在项目根目录或专门的配置目录。

### 3. 深度合并策略

- 嵌套字典：递归合并
- 其他类型：直接覆盖

示例：
```yaml
# config.yaml
db:
  host: localhost
  port: 3306

# config.dev.yaml
db:
  host: 127.0.0.1
  # port 保持 3306（继承自基础配置）
```

## 测试策略

### 测试覆盖

1. **基础功能测试**
   - `test_load_basic_config`: 加载单个配置文件
   - `test_load_with_active_config`: 配置文件合并

2. **环境变量测试**
   - `test_env_var_replacement`: 环境变量替换
   - `test_active_with_env_var`: active 字段使用环境变量
   - `test_active_with_env_var_default`: active 使用环境变量默认值

3. **文件查找测试**
   - `test_load_config_from_configs_subdir`: 从 configs/ 子目录加载

### 测试模式

使用 `tempfile.TemporaryDirectory` 创建临时配置文件，避免依赖真实文件系统。

## 开发指南

### 运行测试

```bash
# 所有测试
pytest tests/ -v

# 单个测试
pytest tests/test_loader.py::test_active_with_env_var -v

# 带覆盖率
pytest tests/ --cov=config_loader
```

### 添加新功能

1. 在 `loader.py` 实现功能
2. 在 `tests/test_loader.py` 添加测试
3. 更新 `README.md` 文档
4. 如有需要，更新 `examples/`

### 代码规范

- 使用类型注解
- 函数和类添加 docstring
- 私有函数以 `_` 开头
- 遵循 PEP 8

## 常见任务

### 修复 Bug

1. 写一个失败的测试重现 bug
2. 修复代码使测试通过
3. 确保所有测试都通过
4. 更新文档（如有需要）

### 添加新的环境变量格式

当前支持：`${VAR}` 和 `${VAR:default}`

如需添加新格式（如 `#{VAR}`）：
1. 修改 `_replace_env_vars` 中的正则表达式
2. 添加对应测试
3. 更新文档说明

### 支持新的配置格式

当前仅支持 YAML。如需支持其他格式（如 JSON、TOML）：
1. 添加对应的解析库到依赖
2. 修改 `load_yaml` 函数（或创建新函数）
3. 更新文件查找逻辑
4. 添加测试和文档

## 依赖管理

- **运行时依赖**：PyYAML>=6.0
- **开发依赖**：pytest>=7.0
- **构建系统**：hatchling

使用 `uv` 或 `pip` 管理依赖。

## API 稳定性

当前版本：0.1.0

- `load_yaml()` - 稳定 API，不应有破坏性变更
- `_` 开头的函数 - 内部 API，可能变更

## 已知限制

1. **配置文件名固定**：必须是 `config.yaml` 和 `config.{active}.yaml`
2. **单层 active**：不支持多层环境嵌套（如 dev.local）
3. **无配置缓存**：每次调用 `load_yaml()` 都重新读取文件
4. **环境变量仅字符串**：不支持类型转换（如 `${PORT:8080}` 结果是字符串 "8080"）

## 快速参考

### 环境变量语法

```yaml
# 使用环境变量，不存在时为空
value: ${ENV_VAR}

# 使用环境变量，不存在时用默认值
value: ${ENV_VAR:default}

# active 字段也支持环境变量
active: ${CONFIG_ENV:dev}
```

### 配置合并示例

```yaml
# config.yaml
app:
  name: MyApp
  debug: false
  version: 1.0

# config.dev.yaml
app:
  debug: true
  # name 和 version 继承自 config.yaml

# 最终结果（当 active: dev）
app:
  name: MyApp      # 来自 config.yaml
  debug: true      # 来自 config.dev.yaml（覆盖）
  version: 1.0     # 来自 config.yaml
```

## 贡献建议

当对项目进行修改时：
1. 保持简洁性 - 这是一个轻量级库
2. 向后兼容 - 不要破坏现有 API
3. 完善测试 - 测试覆盖率应保持高水平
4. 更新文档 - 代码变更要同步文档

## 联系方式

- GitHub: https://github.com/cncws/config-loader
- Issues: https://github.com/cncws/config-loader/issues
