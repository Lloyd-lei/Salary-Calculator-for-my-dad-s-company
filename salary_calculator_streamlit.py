import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from salary_calculator_core import SalaryCalculator

class Calculator:
    """iPhone风格HTML计算器组件"""
    def __init__(self):
        pass
    
    def render(self):
        """渲染HTML计算器界面"""
        st.markdown("### 🧮 计算器")
        
        # 读取HTML文件
        try:
            with open("calculator_component.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            
            # 使用streamlit组件显示HTML计算器
            components.html(html_content, height=800, scrolling=False)
            
        except FileNotFoundError:
            st.error("❌ 计算器组件文件未找到")
            st.info("💡 请确保 calculator_component.html 文件存在")
        except Exception as e:
            st.error(f"❌ 计算器加载失败: {str(e)}")
            # 提供简单的备选方案
            st.write("**简单计算器（备用）**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                num1 = st.number_input("数字1", value=0.0)
            with col2:
                op = st.selectbox("运算符", ["+", "-", "×", "÷"])
            with col3:
                num2 = st.number_input("数字2", value=0.0)
            
            if st.button("计算"):
                try:
                    if op == "+":
                        result = num1 + num2
                    elif op == "-":
                        result = num1 - num2
                    elif op == "×":
                        result = num1 * num2
                    elif op == "÷":
                        if num2 != 0:
                            result = num1 / num2
                        else:
                            st.error("不能除以零")
                            return
                    
                    st.success(f"结果: {result}")
                except Exception as e:
                    st.error(f"计算错误: {str(e)}")

class StreamlitSalaryCalculator:
    def __init__(self):
        if 'calculator' not in st.session_state:
            st.session_state.calculator = SalaryCalculator()
        if 'selected_employee' not in st.session_state:
            st.session_state.selected_employee = None
        if 'show_batch_analysis' not in st.session_state:
            st.session_state.show_batch_analysis = False
        if 'calc_component' not in st.session_state:
            st.session_state.calc_component = Calculator()
    
    @property
    def calculator(self):
        return st.session_state.calculator
    
    def main(self):
        """主界面"""
        st.set_page_config(
            page_title="工资计算器",
            page_icon="💰",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # 自定义CSS样式，防止数字显示被截断
        st.markdown("""
        <style>
        .metric-value {
            font-size: 1.5rem !important;
            font-weight: bold !important;
            white-space: nowrap !important;
            overflow: visible !important;
        }
        .stMetric > div {
            white-space: nowrap !important;
            overflow: visible !important;
        }
        .stMetric > div > div {
            white-space: nowrap !important;
            overflow: visible !important;
        }
        div[data-testid="metric-container"] {
            overflow: visible !important;
        }
        div[data-testid="metric-container"] > div {
            overflow: visible !important;
            text-overflow: unset !important;
        }
        .salary-result {
            font-size: 1.2rem;
            font-weight: bold;
            color: #1f77b4;
            white-space: nowrap;
        }
        .employee-card {
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #e0e0e0;
            margin: 0.5rem 0;
            background-color: #f8f9fa;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 侧边栏配置管理
        self.sidebar_config_management()
        
        # 主标题
        st.title("💰 工资计算器")
        st.markdown("---")
        
        # 创建标签页
        tab1, tab2, tab3, tab4 = st.tabs(["👥 员工工资管理", "⚙️ 收入项配置", "📊 扣除项配置", "📋 税率表管理"])
        
        with tab1:
            self.employee_salary_management_tab()
        
        with tab2:
            self.income_config_tab()
        
        with tab3:
            self.deduction_config_tab()
        
        with tab4:
            self.tax_rate_management_tab()
    
    def sidebar_config_management(self):
        """侧边栏配置管理"""
        st.sidebar.header("🔧 配置管理")
        
        # 导出配置
        if st.sidebar.button("💾 导出配置"):
            config_json = self.calculator.export_config()
            st.sidebar.download_button(
                label="📥 下载配置文件",
                data=config_json,
                file_name=f"salary_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            st.sidebar.success("配置已准备下载")
        
        # 导入配置
        st.sidebar.subheader("📁 导入配置")
        uploaded_file = st.sidebar.file_uploader("选择配置文件", type=['json'])
        if uploaded_file is not None:
            try:
                config_content = uploaded_file.read().decode('utf-8')
                success, message = self.calculator.import_config(config_content)
                if success:
                    st.sidebar.success(message)
                    st.rerun()
                else:
                    st.sidebar.error(message)
            except Exception as e:
                st.sidebar.error(f"导入失败: {str(e)}")
        
        # 重置配置
        if st.sidebar.button("🔄 重置为默认配置"):
            success, message = self.calculator.reset_config()
            st.sidebar.success(message)
            st.rerun()
    
    def employee_salary_management_tab(self):
        """员工工资管理标签页"""
        # 检查是否有选中的员工进行详细查看
        if st.session_state.selected_employee:
            self.employee_detail_view()
            return
        
        # 检查是否要显示批量分析页面
        if st.session_state.show_batch_analysis:
            self.batch_analysis_view()
            return
        
        st.subheader("👥 员工工资管理")
        
        # 员工操作部分
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("**🔧 员工操作**")
            operation = st.selectbox("选择操作", ["添加新员工", "编辑现有员工", "删除员工", "临时计算（不保存）"])
            
            employees = list(self.calculator.get_employees().keys())
            
            if operation == "添加新员工":
                self.add_employee_form()
                
            elif operation == "编辑现有员工":
                if employees:
                    st.write("**✏️ 选择要编辑的员工**")
                    selected_employee = st.selectbox("选择员工", employees, key="edit_employee_select")
                    if selected_employee:
                        self.edit_employee_form(selected_employee)
                else:
                    st.info("暂无员工，请先添加员工")
                    
            elif operation == "删除员工":
                if employees:
                    st.write("**🗑️ 删除员工**")
                    delete_employee = st.selectbox("选择要删除的员工", employees, key="delete_employee_select")
                    if st.button("🗑️ 确认删除", type="secondary", key="confirm_delete"):
                        success = self.calculator.delete_employee(delete_employee)
                        if success:
                            st.success(f"✅ 成功删除员工: {delete_employee}")
                            st.rerun()
                        else:
                            st.error("❌ 删除失败")
                else:
                    st.info("暂无员工，无法删除")
                        
            elif operation == "临时计算（不保存）":
                self.temporary_calculation_form()
        
        with col2:
            # 员工列表和批量操作
            self.display_employee_list_with_calculator()
    
    def temporary_calculation_form(self):
        """临时计算表单（不保存到员工列表）"""
        st.write("**💵 临时工资计算**")
        
        # 默认值填入提示
        st.info("💡 提示：点击\"快速填入默认值\"按钮可以一键填入所有默认配置")
        
        # 快速填入默认值按钮（在表单外）
        if st.button("🚀 快速填入默认值", key="temp_fill_defaults"):
            salary_items = self.calculator.get_salary_items()
            for item_name, item_config in salary_items.items():
                st.session_state[f"temp_salary_{item_name}"] = float(item_config["default"])
            st.rerun()
        
        # 获取收入项配置
        salary_items = self.calculator.get_salary_items()
        salary_inputs = {}
        
        # 动态生成收入项输入框
        for item_name, item_config in salary_items.items():
            required_mark = " *" if item_config["required"] else ""
            
            current_value = st.session_state.get(f"temp_salary_{item_name}", 0.0)
            value = st.number_input(
                f"{item_name}{required_mark}",
                value=float(current_value),
                min_value=0.0,
                step=100.0,
                key=f"temp_salary_{item_name}",
                help=f"默认值: ¥{item_config['default']:,.2f}"
            )
            
            # 如果值为0，使用默认值进行计算
            final_value = value if value > 0 else item_config["default"]
            salary_inputs[item_name] = final_value
        
        # 扣除项选择
        st.write("**📉 扣除项选择**")
        deduction_items = self.calculator.get_deduction_items()
        
        # 默认选择所有非可选扣除项
        default_deductions = [name for name, config in deduction_items.items() 
                            if not config.get("optional", False)]
        
        selected_deductions = st.multiselect(
            "选择适用的扣除项",
            options=list(deduction_items.keys()),
            default=default_deductions,
            key="temp_deductions"
        )
        
        # 固定金额扣除项的输入框
        for deduction_name in selected_deductions:
            deduction_config = deduction_items[deduction_name]
            if deduction_config["type"] == "fixed_amount":
                amount = st.number_input(
                    f"{deduction_name}金额",
                    value=float(deduction_config.get("amount", 0)),
                    min_value=0.0,
                    step=10.0,
                    key=f"temp_deduction_{deduction_name}"
                )
                salary_inputs[f"deduction_{deduction_name}"] = amount
        
        if st.button("💰 计算工资", type="primary", use_container_width=True):
            summary, result = self.calculator.get_calculation_summary(salary_inputs, selected_deductions)
            self.display_calculation_result(summary, result, show_charts=True)
    
    def add_employee_form(self):
        """添加员工表单"""
        st.write("**➕ 添加新员工**")
        
        # 快速填入默认值按钮（在表单外）
        if st.button("🚀 快速填入默认值", key="add_fill_defaults"):
            salary_items = self.calculator.get_salary_items()
            for item_name, item_config in salary_items.items():
                st.session_state[f"add_emp_salary_{item_name}"] = float(item_config["default"])
            st.rerun()
        
        with st.form("add_employee_form", clear_on_submit=True):
            employee_name = st.text_input("员工姓名", placeholder="请输入员工姓名")
            
            # 默认值填入提示
            st.info("💡 提示：使用上方的\"快速填入默认值\"按钮，或者手动输入")
            
            # 薪资信息
            st.write("**💰 薪资信息:**")
            salary_items = self.calculator.get_salary_items()
            employee_salary_data = {}
            
            for item_name, item_config in salary_items.items():
                required_mark = " *" if item_config["required"] else ""
                
                # 获取session_state中的值，如果没有则为0
                current_value = st.session_state.get(f"add_emp_salary_{item_name}", 0.0)
                value = st.number_input(
                    f"{item_name}{required_mark}",
                    value=float(current_value),
                    min_value=0.0,
                    step=100.0,
                    key=f"add_emp_salary_{item_name}",
                    help=f"默认值: ¥{item_config['default']:,.2f}"
                )
                
                # 如果值为0，使用默认值
                final_value = value if value > 0 else item_config["default"]
                employee_salary_data[item_name] = final_value
            
            # 扣除项选择
            st.write("**📉 适用扣除项:**")
            deduction_items = self.calculator.get_deduction_items()
            default_deductions = [name for name, config in deduction_items.items() 
                                if not config.get("optional", False)]
            
            selected_deductions = st.multiselect(
                "选择适用的扣除项",
                options=list(deduction_items.keys()),
                default=default_deductions,
                key="add_emp_deductions",
                help="选择该员工适用的扣除项目"
            )
            
            # 固定金额扣除项输入
            for deduction_name in selected_deductions:
                deduction_config = deduction_items[deduction_name]
                if deduction_config["type"] == "fixed_amount":
                    amount = st.number_input(
                        f"{deduction_name}金额",
                        value=float(deduction_config.get("amount", 0)),
                        min_value=0.0,
                        step=10.0,
                        key=f"add_emp_deduction_{deduction_name}",
                        help=f"该员工的{deduction_name}扣除金额"
                    )
                    employee_salary_data[f"deduction_{deduction_name}"] = amount
            
            st.markdown("**按 Shift+Enter 保存员工信息**")
            submitted = st.form_submit_button("💾 保存员工信息", type="primary", use_container_width=True)
            
            if submitted:
                if employee_name.strip():
                    success = self.calculator.add_employee(
                        employee_name.strip(), 
                        employee_salary_data, 
                        selected_deductions
                    )
                    if success:
                        st.success(f"✅ 成功添加员工: {employee_name}")
                        # 清除session_state中的临时数据
                        for item_name in salary_items.keys():
                            if f"add_emp_salary_{item_name}" in st.session_state:
                                del st.session_state[f"add_emp_salary_{item_name}"]
                        st.rerun()
                    else:
                        st.error("❌ 添加失败：员工姓名已存在")
                else:
                    st.error("❌ 员工姓名不能为空")
    
    def edit_employee_form(self, employee_name):
        """编辑员工表单"""
        existing_salary_data = self.calculator.get_employee_salary(employee_name)
        existing_deductions = self.calculator.get_employee_deductions(employee_name)
        
        st.write(f"**✏️ 编辑员工: {employee_name}**")
        
        # 重置为默认值按钮（在表单外）
        if st.button("🔄 重置所有字段为默认值", key=f"reset_all_{employee_name}"):
            salary_items = self.calculator.get_salary_items()
            for item_name, item_config in salary_items.items():
                st.session_state[f"edit_emp_salary_{employee_name}_{item_name}"] = float(item_config["default"])
            st.rerun()
        
        with st.form(f"edit_employee_form_{employee_name}", clear_on_submit=False):
            # 不可编辑的员工姓名显示
            st.text_input("员工姓名", value=employee_name, disabled=True, key=f"edit_name_{employee_name}")
            
            # 薪资信息
            st.write("**💰 薪资信息:**")
            salary_items = self.calculator.get_salary_items()
            employee_salary_data = {}
            
            for item_name, item_config in salary_items.items():
                current_value = existing_salary_data.get(item_name, item_config["default"])
                required_mark = " *" if item_config["required"] else ""
                
                # 检查session_state是否有更新的值
                session_key = f"edit_emp_salary_{employee_name}_{item_name}"
                if session_key in st.session_state:
                    current_value = st.session_state[session_key]
                
                value = st.number_input(
                    f"{item_name}{required_mark}",
                    value=float(current_value),
                    min_value=0.0,
                    step=100.0,
                    key=session_key,
                    help=f"当前值: ¥{current_value:,.2f}"
                )
                
                employee_salary_data[item_name] = value
            
            # 扣除项选择
            st.write("**📉 适用扣除项:**")
            deduction_items = self.calculator.get_deduction_items()
            
            selected_deductions = st.multiselect(
                "选择适用的扣除项",
                options=list(deduction_items.keys()),
                default=existing_deductions,
                key=f"edit_emp_deductions_{employee_name}",
                help="修改该员工适用的扣除项目"
            )
            
            # 固定金额扣除项输入
            for deduction_name in selected_deductions:
                deduction_config = deduction_items[deduction_name]
                if deduction_config["type"] == "fixed_amount":
                    current_amount = existing_salary_data.get(f"deduction_{deduction_name}", 
                                                            deduction_config.get("amount", 0))
                    amount = st.number_input(
                        f"{deduction_name}金额",
                        value=float(current_amount),
                        min_value=0.0,
                        step=10.0,
                        key=f"edit_emp_deduction_{employee_name}_{deduction_name}",
                        help=f"修改{employee_name}的{deduction_name}扣除金额"
                    )
                    employee_salary_data[f"deduction_{deduction_name}"] = amount
            
            st.markdown("**按 Shift+Enter 更新员工信息**")
            submitted = st.form_submit_button("🔄 更新员工信息", type="primary", use_container_width=True)
            
            if submitted:
                # 编辑员工时不检查姓名重复，因为是同一个员工
                success = self.calculator.update_employee(
                    employee_name, 
                    employee_salary_data, 
                    selected_deductions
                )
                if success:
                    st.success(f"✅ 成功更新员工: {employee_name}")
                    st.rerun()
                else:
                    st.error("❌ 更新失败")
    
    def display_employee_list_with_calculator(self):
        """显示员工列表和计算器"""
        st.write("**📊 员工列表和批量操作**")
        
        employees_data = self.calculator.get_employees()
        if employees_data:
            # 批量分析按钮
            if st.button("📊 进入批量工资分析", type="primary", use_container_width=True):
                st.session_state.show_batch_analysis = True
                st.rerun()
            
            st.markdown("---")
            
            # 员工卡片列表
            st.write("**点击员工查看详情:**")
            for emp_name in employees_data.keys():
                salary_data = self.calculator.get_employee_salary(emp_name)
                selected_deductions = self.calculator.get_employee_deductions(emp_name)
                summary, _ = self.calculator.get_calculation_summary(salary_data, selected_deductions)
                
                if st.button(f"👤 {emp_name} - {summary['税后收入']}", 
                           key=f"view_emp_{emp_name}",
                           use_container_width=True):
                    st.session_state.selected_employee = emp_name
                    st.rerun()
            
            st.markdown("---")
            
            # 添加计算器组件
            st.session_state.calc_component.render()
            
        else:
            st.info("暂无员工数据，请先添加员工")
            st.markdown("---")
            # 即使没有员工也显示计算器
            st.session_state.calc_component.render()
    
    def display_summary_charts(self, all_results):
        """显示汇总图表"""
        st.subheader("📈 员工工资汇总分析")
        
        # 准备数据
        employees = []
        total_incomes = []
        total_deductions = []
        net_incomes = []
        
        for emp_name, result in all_results.items():
            employees.append(emp_name)
            total_incomes.append(result['total_income'])
            total_deductions.append(result['total_deductions'])
            net_incomes.append(result['net_income'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 员工税后收入对比
            fig_bar = px.bar(
                x=employees,
                y=net_incomes,
                title="员工税后收入对比",
                labels={'x': '员工', 'y': '税后收入 (¥)'}
            )
            fig_bar.update_traces(marker_color='lightblue')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # 总收入vs总扣除
            fig_comparison = go.Figure()
            fig_comparison.add_trace(go.Bar(
                name='总收入',
                x=employees,
                y=total_incomes,
                marker_color='lightgreen'
            ))
            fig_comparison.add_trace(go.Bar(
                name='总扣除',
                x=employees,
                y=total_deductions,
                marker_color='lightcoral'
            ))
            fig_comparison.update_layout(
                title='收入与扣除对比',
                barmode='group',
                xaxis_title='员工',
                yaxis_title='金额 (¥)'
            )
            st.plotly_chart(fig_comparison, use_container_width=True)
    
    def batch_analysis_view(self):
        """批量分析页面"""
        # 返回按钮
        if st.button("← 返回员工管理"):
            st.session_state.show_batch_analysis = False
            st.rerun()
        
        st.subheader("📊 批量工资分析")
        
        employees_data = self.calculator.get_employees()
        if not employees_data:
            st.error("暂无员工数据，请先添加员工")
            return
        
        # 计算所有员工工资
        all_results = self.calculator.calculate_all_employees()
        
        # 创建汇总表格
        st.write("### 📋 工资汇总表")
        summary_data = []
        for emp_name, result in all_results.items():
            summary_data.append({
                "员工姓名": emp_name,
                "总收入": f"¥{result['total_income']:,.2f}",
                "总扣除": f"¥{result['total_deductions']:,.2f}",
                "税后收入": f"¥{result['net_income']:,.2f}"
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)
        
        # CSV导出按钮
        csv_content = self.calculator.export_employees_to_csv()
        if csv_content:
            st.download_button(
                label="📥 下载详细CSV工资表",
                data=csv_content.encode('utf-8-sig'),
                file_name=f"员工工资表_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )
        
        st.markdown("---")
        
        # 显示汇总图表
        self.display_summary_charts(all_results)
        
        # 显示统计信息
        st.write("### 📈 统计信息")
        total_company_income = sum(result['total_income'] for result in all_results.values())
        total_company_deductions = sum(result['total_deductions'] for result in all_results.values())
        total_company_net = sum(result['net_income'] for result in all_results.values())
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("员工总数", len(all_results))
        with col2:
            st.metric("公司总支出（总收入）", f"¥{total_company_income:,.2f}")
        with col3:
            st.metric("总扣除金额", f"¥{total_company_deductions:,.2f}")
        with col4:
            st.metric("实际发放总额", f"¥{total_company_net:,.2f}")
    
    def employee_detail_view(self):
        """员工详细查看页面"""
        employee_name = st.session_state.selected_employee
        
        # 返回按钮
        if st.button("← 返回员工列表"):
            st.session_state.selected_employee = None
            st.rerun()
        
        st.subheader(f"👤 {employee_name} 详细信息")
        
        # 获取员工数据
        salary_data = self.calculator.get_employee_salary(employee_name)
        selected_deductions = self.calculator.get_employee_deductions(employee_name)
        summary, result = self.calculator.get_calculation_summary(salary_data, selected_deductions)
        
        # 显示计算结果
        self.display_calculation_result(summary, result, show_charts=True)
        
        # 显示详细信息表格
        st.subheader("📋 详细信息")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**收入项目:**")
            income_data = []
            for item, amount in result["income_breakdown"].items():
                if amount > 0:
                    income_data.append({"项目": item, "金额": f"¥{amount:,.2f}"})
            st.dataframe(pd.DataFrame(income_data), use_container_width=True)
        
        with col2:
            st.write("**扣除项目:**")
            deduction_data = []
            for item, amount in result["deductions"].items():
                if amount > 0:
                    deduction_data.append({"项目": item, "金额": f"¥{amount:,.2f}"})
            st.dataframe(pd.DataFrame(deduction_data), use_container_width=True)
    
    def display_calculation_result(self, summary, result, show_charts=False):
        """显示计算结果"""
        # 显示主要结果卡片
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <h4 style="margin: 0; color: #262730;">💵 总收入</h4>
                <div class="salary-result">{summary["总收入"]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <h4 style="margin: 0; color: #262730;">📉 总扣除</h4>
                <div class="salary-result">{summary["总扣除"]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background-color: #e8f5e8; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <h4 style="margin: 0; color: #262730;">✅ 税后收入</h4>
                <div class="salary-result" style="color: #28a745;">{summary["税后收入"]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if show_charts:
            # 可视化图表
            st.subheader("📈 收支分析")
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # 饼图显示收入构成
                income_data = pd.DataFrame(
                    list(result["income_breakdown"].items()),
                    columns=["项目", "金额"]
                )
                income_data = income_data[income_data["金额"] > 0]
                
                if not income_data.empty:
                    fig_income = px.pie(
                        income_data, 
                        values="金额", 
                        names="项目", 
                        title="收入构成"
                    )
                    st.plotly_chart(fig_income, use_container_width=True)
            
            with col_chart2:
                # 柱状图显示扣除项
                deduction_data = pd.DataFrame(
                    list(result["deductions"].items()),
                    columns=["项目", "金额"]
                )
                deduction_data = deduction_data[deduction_data["金额"] > 0]
                
                if not deduction_data.empty:
                    fig_deduction = px.bar(
                        deduction_data,
                        x="项目",
                        y="金额",
                        title="扣除项分析"
                    )
                    st.plotly_chart(fig_deduction, use_container_width=True)

    def income_config_tab(self):
        """收入项配置标签页"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("➕ 添加收入项")
            
            with st.form("add_income_form"):
                new_item_name = st.text_input("项目名称")
                new_item_default = st.number_input("默认值", value=0.0, min_value=0.0)
                new_item_required = st.checkbox("必填项")
                
                submitted = st.form_submit_button("添加收入项", type="primary")
                
                if submitted:
                    if new_item_name.strip():
                        success = self.calculator.add_salary_item(
                            new_item_name.strip(), 
                            new_item_default, 
                            new_item_required
                        )
                        if success:
                            st.success(f"成功添加收入项: {new_item_name}")
                            st.rerun()
                        else:
                            st.error("添加失败：项目名称已存在")
                    else:
                        st.error("项目名称不能为空")
            
            st.subheader("🗑️ 删除收入项")
            salary_items = list(self.calculator.get_salary_items().keys())
            if salary_items:
                delete_item = st.selectbox("选择要删除的收入项", salary_items)
                if st.button("删除收入项", type="secondary"):
                    success = self.calculator.delete_salary_item(delete_item)
                    if success:
                        st.success(f"成功删除收入项: {delete_item}")
                        st.rerun()
                    else:
                        st.error("删除失败")
        
        with col2:
            st.subheader("📋 当前收入项配置")
            
            salary_items = self.calculator.get_salary_items()
            if salary_items:
                # 创建表格显示
                items_data = []
                for name, config in salary_items.items():
                    items_data.append({
                        "项目名称": name,
                        "默认值": f"¥{config['default']:,.2f}",
                        "必填": "✅" if config["required"] else "⭕",
                        "类型": config["type"]
                    })
                
                df = pd.DataFrame(items_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("暂无收入项配置")
    
    def deduction_config_tab(self):
        """扣除项配置标签页"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("➕ 添加扣除项")
            
            # 扣除类型选择在表单外，避免动态显示问题
            deduction_type = st.selectbox(
                "扣除类型", 
                ["percentage", "fixed_amount", "calculated"],
                format_func=lambda x: {
                    "percentage": "百分比扣除",
                    "fixed_amount": "固定金额扣除", 
                    "calculated": "计算型扣除"
                }[x],
                key="deduction_type_select",
                help="选择扣除方式：百分比按工资比例扣除，固定金额每月扣固定数额，计算型使用系统算法"
            )
            
            # 显示类型说明
            if deduction_type == "percentage":
                st.info("📊 **百分比扣除**：按工资的百分比扣除，如社保8%")
            elif deduction_type == "fixed_amount":
                st.info("💰 **固定金额扣除**：每月扣除固定金额，如迟到扣款50元")
            else:
                st.info("🔢 **计算型扣除**：使用复杂算法计算，如个人所得税累进税率")
            
            with st.form("add_deduction_form"):
                deduction_name = st.text_input("扣除项名称")
                
                # 根据扣除类型显示不同的输入框
                deduction_rate = None
                deduction_base = None
                deduction_amount = None
                
                if deduction_type == "percentage":
                    st.write("**📊 百分比扣除配置：**")
                    deduction_rate = st.number_input("扣除比例 (%)", value=10.0, min_value=0.0, max_value=100.0, step=0.1) / 100
                    salary_items = list(self.calculator.get_salary_items().keys())
                    if salary_items:
                        deduction_base = st.selectbox("计算基数", salary_items, help="选择扣除计算的基础工资项目")
                    else:
                        st.error("请先添加收入项作为计算基数")
                        deduction_base = None
                        
                elif deduction_type == "fixed_amount":
                    st.write("**💰 固定金额扣除配置：**")
                    deduction_amount = st.number_input("固定金额 (¥)", value=0.0, min_value=0.0, step=10.0, help="每月扣除的固定金额")
                    st.info("💡 示例：迟到扣款50元、饭费100元等")
                    
                elif deduction_type == "calculated":
                    st.write("**🔢 计算型扣除配置：**")
                    st.info("💡 计算型扣除项将使用预定义的计算方法（如个人所得税、社保等），无需手动配置参数")
                    st.markdown("""
                    **系统支持的计算型扣除：**
                    - 个人所得税（累进税率）
                    - 社保费用（有上下限计算）
                    - 住房公积金（比例+上限）
                    """)
                
                optional = st.checkbox("可选扣除项", value=True, help="员工可以选择是否适用此扣除项")
                
                submitted = st.form_submit_button("添加扣除项", type="primary")
                
                if submitted:
                    if deduction_name.strip():
                        # 验证必要参数
                        if deduction_type == "percentage" and (deduction_rate is None or deduction_base is None):
                            st.error("百分比扣除需要设置扣除比例和计算基数")
                        elif deduction_type == "fixed_amount" and deduction_amount is None:
                            st.error("固定金额扣除需要设置金额")
                        else:
                            success = self.calculator.add_deduction_item(
                                deduction_name.strip(),
                                deduction_type,
                                deduction_rate,
                                deduction_base,
                                deduction_amount,
                                optional=optional
                            )
                            if success:
                                st.success(f"成功添加扣除项: {deduction_name}")
                                st.rerun()
                            else:
                                st.error("添加失败：扣除项名称已存在")
                    else:
                        st.error("扣除项名称不能为空")
            
            # 删除扣除项
            st.subheader("🗑️ 删除扣除项")
            deduction_items = list(self.calculator.get_deduction_items().keys())
            if deduction_items:
                delete_item = st.selectbox("选择要删除的扣除项", deduction_items)
                if st.button("删除扣除项", type="secondary"):
                    success = self.calculator.delete_deduction_item(delete_item)
                    if success:
                        st.success(f"成功删除扣除项: {delete_item}")
                        st.rerun()
                    else:
                        st.error("删除失败")
        
        with col2:
            st.subheader("📋 当前扣除项配置")
            
            deduction_items = self.calculator.get_deduction_items()
            if deduction_items:
                # 创建表格显示
                items_data = []
                for name, config in deduction_items.items():
                    if config["type"] == "percentage":
                        description = f"{config['rate']*100:.1f}% (基于{config['base']})"
                    elif config["type"] == "fixed_amount":
                        description = f"固定金额 ¥{config.get('amount', 0):,.2f}"
                    else:  # calculated
                        method = config.get('method', '预定义计算')
                        description = f"计算型 - {method}"
                    
                    optional_text = "✅" if config.get("optional", False) else "❌"
                    
                    items_data.append({
                        "扣除项名称": name,
                        "类型": {
                            "percentage": "📊 百分比",
                            "fixed_amount": "💰 固定金额", 
                            "calculated": "🔢 计算型"
                        }[config["type"]],
                        "描述": description,
                        "可选": optional_text
                    })
                
                df = pd.DataFrame(items_data)
                st.dataframe(df, use_container_width=True)
                
                # 添加说明
                st.markdown("""
                **扣除类型说明：**
                - 📊 **百分比**：按工资百分比计算，如社保8%
                - 💰 **固定金额**：每月固定金额，如迟到扣款50元
                - 🔢 **计算型**：复杂算法计算，如个税累进税率
                """)
            else:
                st.info("暂无扣除项配置")
    
    def tax_rate_management_tab(self):
        """税率表管理标签页"""
        st.subheader("📋 个人所得税税率表管理")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 当前税率表显示
            st.write("**当前税率表:**")
            tax_brackets = self.calculator.get_tax_brackets()
            
            # 创建税率表DataFrame
            tax_data = []
            for i, bracket in enumerate(tax_brackets):
                max_display = "无上限" if bracket['max'] == float('inf') else f"¥{bracket['max']:,}"
                tax_data.append({
                    "档次": f"第{i+1}档",
                    "最低收入": f"¥{bracket['min']:,}",
                    "最高收入": max_display,
                    "税率": f"{bracket['rate']*100:.1f}%",
                    "速算扣除数": f"¥{bracket['deduction']:,}"
                })
            
            tax_df = pd.DataFrame(tax_data)
            st.dataframe(tax_df, use_container_width=True)
            
            # 删除税率档次
            st.write("**删除税率档次:**")
            if len(tax_brackets) > 1:  # 至少保留一个档次
                delete_options = [f"第{i+1}档: {bracket['min']:,}-{bracket['max'] if bracket['max'] != float('inf') else '无上限'}" 
                                for i, bracket in enumerate(tax_brackets)]
                delete_selection = st.selectbox("选择要删除的档次", delete_options)
                delete_index = int(delete_selection.split("第")[1].split("档")[0]) - 1
                
                if st.button("删除选中档次", type="secondary"):
                    success = self.calculator.delete_tax_bracket(delete_index)
                    if success:
                        st.success("删除成功")
                        st.rerun()
            else:
                st.info("至少需要保留一个税率档次")
        
        with col2:
            # 添加新税率档次
            st.write("**添加新税率档次:**")
            with st.form("add_tax_bracket_form"):
                new_min = st.number_input("最低收入", value=0.0, min_value=0.0, step=1000.0)
                new_max = st.number_input("最高收入 (-1表示无上限)", value=5000.0, step=1000.0)
                new_rate = st.number_input("税率 (%)", value=3.0, min_value=0.0, max_value=100.0, step=0.1) / 100
                new_deduction = st.number_input("速算扣除数", value=0.0, min_value=0.0, step=10.0)
                
                if st.form_submit_button("添加税率档次"):
                    success = self.calculator.add_tax_bracket(int(new_min), int(new_max), new_rate, int(new_deduction))
                    if success:
                        st.success("成功添加税率档次")
                        st.rerun()
            
            # 编辑现有税率档次
            st.write("**编辑税率档次:**")
            if tax_brackets:
                edit_options = [f"第{i+1}档: {bracket['min']:,}-{bracket['max'] if bracket['max'] != float('inf') else '无上限'}" 
                              for i, bracket in enumerate(tax_brackets)]
                edit_selection = st.selectbox("选择要编辑的档次", edit_options, key="edit_selection")
                edit_index = int(edit_selection.split("第")[1].split("档")[0]) - 1
                
                selected_bracket = tax_brackets[edit_index]
                
                with st.form(f"edit_tax_bracket_form_{edit_index}"):
                    edit_min = st.number_input("最低收入", value=float(selected_bracket['min']), min_value=0.0, step=1000.0)
                    edit_max_value = -1.0 if selected_bracket['max'] == float('inf') else float(selected_bracket['max'])
                    edit_max = st.number_input("最高收入 (-1表示无上限)", value=edit_max_value, step=1000.0)
                    edit_rate = st.number_input("税率 (%)", value=float(selected_bracket['rate']) * 100.0, min_value=0.0, max_value=100.0, step=0.1) / 100
                    edit_deduction = st.number_input("速算扣除数", value=float(selected_bracket['deduction']), min_value=0.0, step=10.0)
                    
                    if st.form_submit_button("更新档次", type="primary"):
                        success = self.calculator.update_tax_bracket(edit_index, int(edit_min), int(edit_max), edit_rate, int(edit_deduction))
                        if success:
                            st.success("更新成功")
                            st.rerun()

def main():
    app = StreamlitSalaryCalculator()
    app.main()

if __name__ == "__main__":
    main() 