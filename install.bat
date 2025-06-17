@echo off
chcp 65001 >nul
echo ===============================================
echo         💰 工资计算器 - Windows 安装程序
echo ===============================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python 3.7或更高版本
    echo 📥 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ 检测到Python环境
python --version

echo.
echo 🔧 正在安装依赖包...
echo.

:: 升级pip
python -m pip install --upgrade pip

:: 安装依赖
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo ✅ 安装完成！
echo.
echo 📝 使用方法:
echo    双击 "启动工资计算器.bat" 运行程序
echo    或者在命令行中运行: python start_app.py
echo.
echo 🌐 访问地址:
echo    本地访问: http://localhost:8501
echo    局域网访问: http://你的IP地址:8501
echo.
pause 