#!/bin/bash

echo "==============================================="
echo "        💰 工资计算器 - Mac/Linux 安装程序"
echo "==============================================="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ 未找到Python，请先安装Python 3.7或更高版本"
        echo "📥 Mac用户建议使用Homebrew: brew install python"
        echo "📥 Linux用户: sudo apt-get install python3 python3-pip"
        exit 1
    else
        PYTHON_CMD=python
    fi
else
    PYTHON_CMD=python3
fi

echo "✅ 检测到Python环境"
$PYTHON_CMD --version

echo
echo "🔧 正在安装依赖包..."
echo

# 升级pip
$PYTHON_CMD -m pip install --upgrade pip

# 安装依赖
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，请检查网络连接"
    exit 1
fi

# 给脚本执行权限
chmod +x 启动工资计算器.sh

echo
echo "✅ 安装完成！"
echo
echo "📝 使用方法:"
echo "   双击 '启动工资计算器.sh' 运行程序"
echo "   或者在终端中运行: $PYTHON_CMD start_app.py"
echo
echo "🌐 访问地址:"
echo "   本地访问: http://localhost:8501"
echo "   局域网访问: http://你的IP地址:8501"
echo 