#!/bin/bash

echo "==============================================="
echo "           💰 工资计算器 正在启动..."
echo "==============================================="
echo

# 确定Python命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python环境异常，请运行 ./install.sh 重新安装"
    exit 1
fi

# 启动应用
echo "🚀 正在启动工资计算器..."
echo "📱 支持局域网访问 - 手机和其他设备可以使用"
echo
echo "🌐 访问地址:"
echo "   本地: http://localhost:8501"
echo "   局域网: http://你的IP地址:8501"
echo
echo "⏹️  按 Ctrl+C 停止程序"
echo "==============================================="

$PYTHON_CMD start_app.py

echo
echo "👋 程序已停止" 