import os
import re
from typing import Any, Dict, List

import yaml

DEFAULT_CONFIG_NAME = "config.yaml"


def _get_config_search_paths() -> List[str]:
    cwd = os.getcwd()
    return [cwd, os.path.join(cwd, "configs")]


def _find_config_dir() -> str:
    for path in _get_config_search_paths():
        config_file = os.path.join(path, DEFAULT_CONFIG_NAME)
        if os.path.exists(config_file):
            return path
    raise FileNotFoundError(
        f"配置文件不存在: {DEFAULT_CONFIG_NAME} in {', '.join(_get_config_search_paths())}"
    )


def load_yaml() -> Dict[str, Any]:
    config_dir = _find_config_dir()
    config_file = os.path.join(config_dir, DEFAULT_CONFIG_NAME)

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    active = config.get("active", "").strip()
    if active:
        active_config_file = os.path.join(config_dir, f"config.{active}.yaml")
        if os.path.exists(active_config_file):
            with open(active_config_file, "r", encoding="utf-8") as f:
                active_config = yaml.safe_load(f) or {}
            _merge_dict(config, active_config)

    return _replace_env_vars(config)


def _merge_dict(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _merge_dict(base[key], value)
        else:
            base[key] = value


def _replace_env_vars(obj: Any) -> Any:
    if isinstance(obj, str):
        pattern = r"\$\{([^}:]+)(?::([^}]*))?\}"

        def replace(match):
            var_name = match.group(1)
            default_value = match.group(2) or ""
            return os.environ.get(var_name, default_value)

        return re.sub(pattern, replace, obj)
    elif isinstance(obj, dict):
        return {k: _replace_env_vars(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_replace_env_vars(item) for item in obj]
    else:
        return obj
