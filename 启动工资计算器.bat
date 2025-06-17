@echo off
chcp 65001 >nul
title 工资计算器

echo ===============================================
echo            💰 工资计算器 正在启动...
echo ===============================================
echo.

:: 检查Python是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python环境异常，请运行 install.bat 重新安装
    pause
    exit /b 1
)

:: 启动应用
echo 🚀 正在启动工资计算器...
echo 📱 支持局域网访问 - 手机和其他设备可以使用
echo.
echo 🌐 访问地址:
echo    本地: http://localhost:8501
echo    局域网: http://你的IP地址:8501
echo.
echo ⏹️  按 Ctrl+C 停止程序
echo ===============================================

python start_app.py

echo.
echo 👋 程序已停止
pause 