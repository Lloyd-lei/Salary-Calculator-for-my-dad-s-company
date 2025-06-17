from setuptools import setup, find_packages

setup(
    name="salary-calculator",
    version="1.0.0",
    description="工资计算器 - 支持员工管理、税率配置的专业工资计算工具",
    author="Salary Calculator Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=1.5.0", 
        "plotly>=5.15.0"
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'salary-calculator=start_app:main',
        ],
    },
    package_data={
        '': ['*.html', '*.md', '*.py'],
    },
) 