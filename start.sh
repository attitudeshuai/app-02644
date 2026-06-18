#!/bin/bash
#
# 科学计算器一键启动脚本
# 自动安装 Python 3.11 + tkinter (兼容性最佳)
#

set -e

echo "========================================"
echo "  科学计算器 - 一键启动"
echo "========================================"
echo

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Darwin*)  echo "macos" ;;
        Linux*)   echo "linux" ;;
        *)        echo "unknown" ;;
    esac
}

OS=$(detect_os)
echo "[信息] 检测到操作系统: $OS"

# macOS: 确保使用 Python 3.11 (兼容性最佳)
if [ "$OS" = "macos" ]; then
    
    # 检查 Homebrew
    if ! command -v brew &> /dev/null; then
        echo "[信息] 安装 Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # 配置 PATH
        if [ -f "/opt/homebrew/bin/brew" ]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        elif [ -f "/usr/local/bin/brew" ]; then
            eval "$(/usr/local/bin/brew shellenv)"
        fi
    fi
    echo "[OK] Homebrew 已安装"
    
    # 确定 brew 路径
    if [ -d "/opt/homebrew" ]; then
        BREW_PREFIX="/opt/homebrew"
    else
        BREW_PREFIX="/usr/local"
    fi
    
    PYTHON="$BREW_PREFIX/bin/python3.11"
    
    # 检查 Python 3.11
    if [ ! -x "$PYTHON" ]; then
        echo "[信息] 安装 Python 3.11..."
        brew install python@3.11
    fi
    echo "[OK] Python 3.11: $($PYTHON --version)"
    
    # 检查 tkinter
    if ! $PYTHON -c "import tkinter" &> /dev/null; then
        echo "[信息] 安装 python-tk@3.11..."
        brew install python-tk@3.11
    fi
    
    # 验证 tkinter
    if ! $PYTHON -c "import tkinter; root=tkinter.Tk(); root.destroy()" &> /dev/null; then
        echo "[错误] tkinter 无法正常工作"
        echo "请尝试: brew reinstall python@3.11 python-tk@3.11"
        exit 1
    fi
    echo "[OK] tkinter 可用"

# Linux
elif [ "$OS" = "linux" ]; then
    PYTHON="python3"
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo "[信息] 安装 Python..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-tk
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-tkinter
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-tkinter
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python tk
        fi
    fi
    echo "[OK] Python: $(python3 --version)"
    
    # 检查 tkinter
    if ! python3 -c "import tkinter" &> /dev/null; then
        echo "[信息] 安装 tkinter..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-tk
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-tkinter
        fi
    fi
    echo "[OK] tkinter 可用"

else
    echo "[错误] 不支持的操作系统"
    exit 1
fi

# 切换到脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/calculator"

# 启动 GUI
echo ""
echo "========================================"
echo "[信息] 启动计算器 GUI..."
echo "========================================"
$PYTHON main.py
