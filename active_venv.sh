#!/bin/bash

# 启用错误检测
set -e

# 默认虚拟环境名称
DEFAULT_VENV_NAME="myenv"

# 显示帮助信息
show_help() {
    echo "Usage: source $0 [-n VENV_NAME]"
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
      return 0
      ;;
    \? )
      echo "Invalid Option: -$OPTARG" 1>&2
      show_help
      return 1
      ;;
    : )
      echo "Invalid Option: -$OPTARG requires an argument" 1>&2
      show_help
      return 1
      ;;
  esac
done

# 如果未指定虚拟环境名称，使用默认值
VENV_NAME=${VENV_NAME:-$DEFAULT_VENV_NAME}

# 检查是否已经在虚拟环境中
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Already in virtual environment: $(basename "$VIRTUAL_ENV")"
    return 0
fi

# 检测可用的 Python 命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Python is not installed. Please install Python3."
    return 1
fi

echo "Using Python command: $PYTHON_CMD"

# 检查虚拟环境目录是否存在
if [ ! -d "$VENV_NAME" ]; then
    echo "Virtual environment '$VENV_NAME' does not exist. Please run setup_venv.sh first."
    return 1
fi

# 激活虚拟环境
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows 环境 (Git Bash)
    ACTIVATE_SCRIPT="$VENV_NAME/Scripts/activate"
else
    # Unix-like 环境
    ACTIVATE_SCRIPT="$VENV_NAME/bin/activate"
fi

# 检查激活脚本是否存在
if [ ! -f "$ACTIVATE_SCRIPT" ]; then
    echo "Activation script '$ACTIVATE_SCRIPT' not found."
    return 1
fi

echo "Activating virtual environment using '$ACTIVATE_SCRIPT'..."
source "$ACTIVATE_SCRIPT"

# 检查是否成功激活
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual environment '$VENV_NAME' has been activated."
    echo "To deactivate the virtual environment, type 'deactivate'."
    # 显示当前 Python 版本以确认激活
    "$PYTHON_CMD" --version
    # 显示当前 Python 路径
    which "$PYTHON_CMD"
else
    echo "Failed to activate virtual environment. Please check your installation."
    return 1
fi
