#!/usr/bin/env python3
"""
工资计算器 - 启动脚本 (Streamlit版)
支持局域网访问，确保手机等设备可以使用
"""

import subprocess
import sys
import os

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'streamlit', 'pandas', 'plotly'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def start_streamlit():
    """启动Streamlit版本"""
    print("🚀 启动 Streamlit 工资计算器...")
    print("📱 支持局域网访问 - 手机和其他设备可以使用")
    print("=" * 50)
    
    try:
        # 启动streamlit，绑定到所有网络接口，确保局域网可访问
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "salary_calculator_streamlit.py",
            "--server.address=0.0.0.0",  # 绑定所有网络接口
            "--server.port=8501",
            "--server.headless=true",    # 无头模式
            "--browser.serverAddress=0.0.0.0",  # 浏览器服务器地址
            "--server.enableCORS=false", # 禁用CORS以支持跨域访问
            "--server.enableXsrfProtection=false"  # 禁用XSRF保护以支持局域网访问
        ]
        
        print("🌐 本地访问地址: http://localhost:8501")
        print("📱 局域网访问地址: http://[您的IP地址]:8501")
        print("💡 提示: 请确保防火墙允许8501端口")
        print("⏹️  按 Ctrl+C 停止服务")
        print("=" * 50)
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    print("💰 工资计算器")
    print("=" * 30)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查文件是否存在
    if not os.path.exists("salary_calculator_streamlit.py"):
        print("❌ 找不到 salary_calculator_streamlit.py 文件")
        return
    
    if not os.path.exists("salary_calculator_core.py"):
        print("❌ 找不到 salary_calculator_core.py 文件")
        return
    
    start_streamlit()

if __name__ == "__main__":
    main() 