#!/bin/bash

# 启用错误检测
set -e

# 默认虚拟环境名称
DEFAULT_VENV_NAME="myenv"

# 显示帮助信息
show_help() {
    echo "Usage: $0 [-n VENV_NAME]"
    echo
    echo "Options:"
    echo "  -n    指定虚拟环境名称 (默认: $DEFAULT_VENV_NAME)"
    echo "  -h    显示此帮助信息"
}

# 解析命令行参数
while getopts ":n:h" opt; do
  case ${opt} in
    n )
      VENV_NAME=$OPTARG
      ;;
    h )
      show_help
      exit 0
      ;;
    \? )
      echo "Invalid Option: -$OPTARG" 1>&2
      show_help
      exit 1
      ;;
    : )
      echo "Invalid Option: -$OPTARG requires an argument" 1>&2
      show_help
      exit 1
      ;;
  esac
done

# 如果未指定虚拟环境名称，使用默认值
VENV_NAME=${VENV_NAME:-$DEFAULT_VENV_NAME}

# 检查是否已经在虚拟环境中
if [ -n "$VIRTUAL_ENV" ]; then
    echo "当前已经激活虚拟环境: $(basename $VIRTUAL_ENV)"
    exit 0
fi

# 检查 Python 是否安装
if ! command -v python &> /dev/null
then
    echo "未安装 Python，请先安装以继续。"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "$VENV_NAME" ]; then
    # 创建虚拟环境
    python -m venv $VENV_NAME
    echo "虚拟环境已创建: $VENV_NAME"
fi

# 检查虚拟环境目录是否存在
if [ ! -d "$VENV_NAME" ]; then
    echo "创建虚拟环境失败。请检查您的 Python 安装。"
    exit 1
fi

# 激活虚拟环境
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows 环境 (Git Bash)
    source "$VENV_NAME/Scripts/activate"
else
    # Unix-like 环境
    source "$VENV_NAME/bin/activate"
fi

echo "虚拟环境 '$VENV_NAME' 已激活。"

# 检查 requirements.txt 是否存在
if [ ! -f "requirements.txt" ]; then
    echo "未找到 requirements.txt，正在创建一个空文件。"
    touch requirements.txt
fi

# 升级 pip
echo "升级 pip..."
python -m pip install --upgrade pip

# 安装依赖包
echo "安装依赖包..."
if pip install -r requirements.txt; then
    echo "所有依赖包已成功安装。"
else
    echo "安装依赖包时出错。请检查 requirements.txt 文件。"
    deactivate
    exit 1
fi

echo "虚拟环境 '$VENV_NAME' 已创建并激活，依赖包已安装完成。"
echo "要退出虚拟环境，请输入 'deactivate'。"