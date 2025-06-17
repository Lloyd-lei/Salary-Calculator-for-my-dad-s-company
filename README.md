# 💰 工资计算器 - 专业的企业工资管理系统

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个功能强大、易于使用的工资计算器，专为中小企业设计。支持多平台运行，局域网访问，手机端操作。

## 🎯 项目特色

### ✨ 核心功能

- **📊 专业工资计算引擎** - 支持复杂的税率计算和扣除项管理
- **👥 员工信息管理** - 完整的员工档案和工资记录
- **⚙️ 灵活配置系统** - 可自定义收入项、扣除项和税率表
- **📱 多设备支持** - 支持手机、平板、电脑访问
- **🌐 局域网访问** - 团队协作，多人同时使用
- **📈 数据可视化** - 直观的图表分析和统计

### 🚀 技术亮点

- **零配置安装** - 一键安装，开箱即用
- **跨平台支持** - Windows、Mac、Linux 全平台
- **响应式设计** - 适配各种屏幕尺寸
- **数据导出** - 支持 CSV 格式，便于进一步处理

## 📦 快速开始

### 系统要求

- Python 3.7 或更高版本
- 现代浏览器（Chrome、Firefox、Safari、Edge）
- 网络连接（首次安装时）

### 安装步骤

#### Windows 用户

```bash
# 1. 双击运行安装脚本
install.bat

# 2. 启动程序
启动工资计算器.bat
```

#### Mac/Linux 用户

```bash
# 1. 给脚本执行权限并安装
chmod +x install.sh
./install.sh

# 2. 启动程序
./启动工资计算器.sh
```

#### 手动安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动应用
python start_app.py
```

### 访问地址

- **本地访问**: http://localhost:8501
- **局域网访问**: http://你的 IP 地址:8501

## 🎨 功能展示

### 工资计算

- 支持多种收入项目（基本工资、奖金、津贴等）
- 灵活的扣除项配置（社保、公积金、个税等）
- 实时计算和结果展示

### 员工管理

- 员工信息录入和编辑
- 个性化扣除项选择
- 历史记录查询

### 配置管理

- 可编辑的个人所得税税率表
- 自定义收入项和扣除项
- 配置导入导出功能

### 数据分析

- 收入构成饼图
- 扣除项分析柱状图
- 工资明细报表

## 📱 移动端支持

### 局域网访问设置

1. 确保设备连接同一 WiFi
2. 查看电脑 IP 地址：
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`
3. 手机浏览器访问：`http://电脑IP:8501`

### 防火墙设置

如果无法访问，请检查防火墙是否允许 8501 端口。

## 🔧 高级配置

### 自定义税率表

```json
{
  "tax_brackets": [
    { "min": 0, "max": 5000, "rate": 0, "deduction": 0 },
    { "min": 5000, "max": 8000, "rate": 0.03, "deduction": 150 }
  ]
}
```

### 扣除项配置

- **percentage**: 按比例扣除（如社保）
- **fixed_amount**: 固定金额扣除（如迟到扣款）
- **calculated**: 系统计算扣除（如个税）

## 📁 项目结构

```
工资计算器/
├── salary_calculator_streamlit.py  # 主程序界面
├── salary_calculator_core.py       # 核心计算逻辑
├── start_app.py                     # 启动脚本
├── calculator_component.html       # 计算器组件
├── requirements.txt                 # 依赖列表
├── install.bat                      # Windows安装脚本
├── install.sh                       # Mac/Linux安装脚本
├── 启动工资计算器.bat              # Windows启动脚本
├── 启动工资计算器.sh               # Mac/Linux启动脚本
├── 使用说明.md                     # 详细使用说明
├── README_用户指南.md              # 用户指南
└── 版本说明.txt                    # 版本信息
```

## 🎯 使用场景

### 适用企业

- 中小型企业 HR 部门
- 财务工资核算
- 个体工商户
- 代理记账公司

### 主要用户

- HR 专员
- 财务人员
- 企业管理者
- 会计师

## 🔄 版本历史

### v1.0 (2024-06-17)

- ✅ 完整的工资计算功能
- ✅ 员工管理系统
- ✅ 可配置税率表
- ✅ 局域网多设备访问
- ✅ 数据导出功能
- ✅ 移动端适配

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目！

### 开发环境设置

```bash
git clone https://github.com/Lloyd-lei/Salary-Calculator-for-my-dad-s-company.git
cd Salary-Calculator-for-my-dad-s-company
pip install -r requirements.txt
python start_app.py
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持与反馈

- 🐛 [提交 Bug](https://github.com/Lloyd-lei/Salary-Calculator-for-my-dad-s-company/issues)
- 💡 [功能建议](https://github.com/Lloyd-lei/Salary-Calculator-for-my-dad-s-company/issues)
- 📧 邮箱支持：[创建 Issue 获取支持]

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
