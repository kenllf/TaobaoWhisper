import os
import shutil
import yaml


def read_yaml(file, encoding="UTF-8"):
    """
    读取并解析 YAML 格式的配置文件。

    参数:
    file: 字符串，表示需要读取的 YAML 文件的路径。

    返回值:
    读取并解析后的数据，数据类型取决于 YAML 文件的内容。

    异常:
    如果遇到 YAML 解析错误，将打印错误信息。
    """
    with open(file, "r", encoding=encoding) as stream:  # 打开文件并以读取模式进行处理
        try:
            data = yaml.safe_load(stream)  # 安全地解析 YAML 格式的文件内容
            return data
        except yaml.YAMLError as exc:  # 捕获并处理 YAML 解析错误
            print(exc)


def read_common():
    """
    读取通用配置文件。

    该函数没有参数。

    返回:
        返回从通用配置文件中读取的数据。
    """
    # 获取当前工作目录
    current_dir = os.getcwd()

    # 设置config目录和文件名
    config_dir = "automation/config"
    default_filename = "common.default.yaml"
    yaml_filename = "common.yaml"

    # 构建完整的文件路径
    default_file_path = os.path.join(current_dir, config_dir, default_filename)
    yaml_file_path = os.path.join(current_dir, config_dir, yaml_filename)

    if not os.path.exists(yaml_file_path):
        # 把config/common.default.yaml 拷贝为config/common.yaml
        shutil.copy(default_file_path, yaml_file_path)
        print(f"已复制 {default_file_path} 到 {yaml_file_path}")

    return read_yaml(yaml_file_path)  # 读取并返回配置文件中的数据
