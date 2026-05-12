import os
import tempfile

import pytest

from config_loader import load_yaml


def test_load_basic_config():
    """测试加载基础配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, "config.yaml")
        with open(config_file, "w") as f:
            f.write("app:\n  name: TestApp\n  debug: false\n")

        cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            config = load_yaml()
        finally:
            os.chdir(cwd)

        assert config["app"]["name"] == "TestApp"
        assert config["app"]["debug"] is False


def test_load_with_active_config():
    """测试加载基础配置并合并active配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, "config.yaml")
        with open(config_file, "w") as f:
            f.write("active: dev\napp:\n  name: TestApp\n  debug: false\n")

        dev_config_file = os.path.join(tmpdir, "config.dev.yaml")
        with open(dev_config_file, "w") as f:
            f.write("app:\n  debug: true\n")

        cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            config = load_yaml()
        finally:
            os.chdir(cwd)

        assert config["app"]["name"] == "TestApp"
        assert config["app"]["debug"] is True


def test_env_var_replacement():
    """测试环境变量替换"""
    os.environ["TEST_VAR"] = "test_value"

    with tempfile.TemporaryDirectory() as tmpdir:
        config_file = os.path.join(tmpdir, "config.yaml")
        with open(config_file, "w") as f:
            f.write(
                "app:\n  value: ${TEST_VAR}\n  default: ${NONEXISTENT:default_val}\n"
            )

        cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            config = load_yaml()
        finally:
            os.chdir(cwd)

        assert config["app"]["value"] == "test_value"
        assert config["app"]["default"] == "default_val"


def test_load_config_from_configs_subdir():
    """测试从 cwd/configs 目录加载配置"""
    with tempfile.TemporaryDirectory() as tmpdir:
        configs_dir = os.path.join(tmpdir, "configs")
        os.makedirs(configs_dir, exist_ok=True)
        config_file = os.path.join(configs_dir, "config.yaml")
        with open(config_file, "w") as f:
            f.write("app:\n  name: ConfigsDirApp\n")

        cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            config = load_yaml()
        finally:
            os.chdir(cwd)

        assert config["app"]["name"] == "ConfigsDirApp"


def test_active_with_env_var():
    """测试active字段支持环境变量"""
    os.environ["CONFIG_ENV"] = "dev"

    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建基础配置文件，active使用环境变量
        config_file = os.path.join(tmpdir, "config.yaml")
        with open(config_file, "w") as f:
            f.write("active: ${CONFIG_ENV}\napp:\n  name: TestApp\n  debug: false\n")

        # 创建开发环境配置文件
        dev_config_file = os.path.join(tmpdir, "config.dev.yaml")
        with open(dev_config_file, "w") as f:
            f.write("app:\n  debug: true\n")

        cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            config = load_yaml()
        finally:
            os.chdir(cwd)
            # 清理环境变量
            del os.environ["CONFIG_ENV"]

        # 验证配置被正确合并
        assert config["app"]["name"] == "TestApp"
        assert config["app"]["debug"] is True


def test_active_with_env_var_default():
    """测试active字段支持环境变量和默认值"""
    # 不设置环境变量，使用默认值
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建基础配置文件，active使用环境变量和默认值
        config_file = os.path.join(tmpdir, "config.yaml")
        with open(config_file, "w") as f:
            f.write(
                "active: ${CONFIG_ENV:prod}\napp:\n  name: TestApp\n  debug: false\n"
            )

        # 创建生产环境配置文件
        prod_config_file = os.path.join(tmpdir, "config.prod.yaml")
        with open(prod_config_file, "w") as f:
            f.write("app:\n  debug: false\n  extra: prod_value\n")

        cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            config = load_yaml()
        finally:
            os.chdir(cwd)

        # 验证使用了默认值prod，配置被正确合并
        assert config["app"]["name"] == "TestApp"
        assert config["app"]["debug"] is False
        assert config["app"]["extra"] == "prod_value"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
