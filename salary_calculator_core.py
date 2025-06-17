import json
import pandas as pd
from datetime import datetime
import math
import io

class SalaryCalculator:
    def __init__(self):
        self.config = self.load_default_config()
        self.employees = {}  # 存储员工数据
        
    def load_default_config(self):
        """加载默认配置"""
        return {
            "salary_items": {
                "基本工资": {"type": "input", "default": 10000, "required": True},
                "绩效奖金": {"type": "input", "default": 2000, "required": False},
                "加班费": {"type": "input", "default": 0, "required": False},
                "餐补": {"type": "input", "default": 500, "required": False},
                "交通补贴": {"type": "input", "default": 300, "required": False},
                "技能津贴": {"type": "input", "default": 0, "required": False}
            },
            "deduction_items": {
                "社保": {"type": "percentage", "rate": 0.105, "base": "基本工资"},
                "公积金": {"type": "percentage", "rate": 0.12, "base": "基本工资"},
                "个人所得税": {"type": "calculated", "method": "progressive_tax"}
            },
            "calculation_methods": {
                "progressive_tax": {
                    "name": "累进税率计算",
                    "brackets": [
                        {"min": 0, "max": 5000, "rate": 0, "deduction": 0},
                        {"min": 5000, "max": 8000, "rate": 0.03, "deduction": 150},
                        {"min": 8000, "max": 17000, "rate": 0.10, "deduction": 710},
                        {"min": 17000, "max": 30000, "rate": 0.20, "deduction": 2410},
                        {"min": 30000, "max": 40000, "rate": 0.25, "deduction": 3910},
                        {"min": 40000, "max": 60000, "rate": 0.30, "deduction": 5910},
                        {"min": 60000, "max": 85000, "rate": 0.35, "deduction": 8910},
                        {"min": 85000, "max": float('inf'), "rate": 0.45, "deduction": 17410}
                    ]
                }
            }
        }
    
    def calculate_progressive_tax(self, taxable_income):
        """计算累进税"""
        brackets = self.config["calculation_methods"]["progressive_tax"]["brackets"]
        
        for bracket in brackets:
            if bracket["min"] <= taxable_income <= bracket["max"]:
                tax = taxable_income * bracket["rate"] - bracket["deduction"]
                return max(0, tax)
        return 0
    
    def calculate_salary(self, salary_inputs, selected_deductions=None):
        """计算工资"""
        # 如果没有指定选择的扣除项，默认使用所有非可选扣除项
        if selected_deductions is None:
            selected_deductions = [name for name, config in self.config["deduction_items"].items() 
                                 if not config.get("optional", False)]
        
        # 计算总收入
        total_income = 0
        income_breakdown = {}
        
        for item_name, item_config in self.config["salary_items"].items():
            value = salary_inputs.get(item_name, item_config["default"])
            income_breakdown[item_name] = value
            total_income += value
        
        # 计算扣除项
        deductions = {}
        total_deductions = 0
        
        for item_name, item_config in self.config["deduction_items"].items():
            # 只计算选中的扣除项
            if item_name not in selected_deductions:
                continue
                
            if item_config["type"] == "percentage":
                base_amount = income_breakdown.get(item_config["base"], 0)
                deduction = base_amount * item_config["rate"]
            elif item_config["type"] == "fixed_amount":
                # 新增固定金额扣除类型
                deduction = item_config.get("amount", 0)
                # 如果在salary_inputs中有自定义金额，使用自定义金额
                if f"deduction_{item_name}" in salary_inputs:
                    deduction = salary_inputs[f"deduction_{item_name}"]
            elif item_config["type"] == "calculated":
                if item_config["method"] == "progressive_tax":
                    # 计算应税收入（总收入 - 社保公积金 - 起征点5000）
                    social_deductions = sum([
                        v for k, v in deductions.items() 
                        if k in ["社保", "公积金"]
                    ])
                    taxable_income = total_income - social_deductions - 5000
                    deduction = self.calculate_progressive_tax(max(0, taxable_income))
                else:
                    deduction = 0
            else:
                deduction = 0
            
            deductions[item_name] = deduction
            total_deductions += deduction
        
        # 计算税后收入
        net_income = total_income - total_deductions
        
        return {
            "total_income": total_income,
            "income_breakdown": income_breakdown,
            "deductions": deductions,
            "total_deductions": total_deductions,
            "net_income": net_income,
            "selected_deductions": selected_deductions
        }
    
    def add_salary_item(self, name, default=0, required=False):
        """添加收入项"""
        if name and name not in self.config["salary_items"]:
            self.config["salary_items"][name] = {
                "type": "input",
                "default": default,
                "required": required
            }
            return True
        return False
    
    def update_salary_item(self, old_name, new_name=None, default=None, required=None):
        """更新收入项"""
        if old_name not in self.config["salary_items"]:
            return False
        
        item = self.config["salary_items"][old_name]
        
        # 更新名称
        if new_name and new_name != old_name:
            self.config["salary_items"][new_name] = self.config["salary_items"].pop(old_name)
            old_name = new_name
        
        # 更新其他属性
        if default is not None:
            item["default"] = default
        if required is not None:
            item["required"] = required
            
        return True
    
    def delete_salary_item(self, name):
        """删除收入项"""
        if name in self.config["salary_items"]:
            del self.config["salary_items"][name]
            return True
        return False
    
    def add_deduction_item(self, name, deduction_type, rate=None, base=None, amount=None, method=None, optional=True):
        """添加扣除项"""
        if name and name not in self.config["deduction_items"]:
            if deduction_type == "percentage":
                self.config["deduction_items"][name] = {
                    "type": "percentage",
                    "rate": rate or 0.1,
                    "base": base or list(self.config["salary_items"].keys())[0],
                    "optional": optional
                }
            elif deduction_type == "fixed_amount":
                self.config["deduction_items"][name] = {
                    "type": "fixed_amount",
                    "amount": amount or 0,
                    "optional": optional
                }
            else:
                self.config["deduction_items"][name] = {
                    "type": "calculated",
                    "method": method or "custom",
                    "optional": optional
                }
            return True
        return False
    
    def update_deduction_item(self, name, rate=None, base=None, amount=None, optional=None):
        """更新扣除项"""
        if name not in self.config["deduction_items"]:
            return False
            
        item = self.config["deduction_items"][name]
        if item["type"] == "percentage":
            if rate is not None:
                item["rate"] = rate
            if base is not None:
                item["base"] = base
        elif item["type"] == "fixed_amount":
            if amount is not None:
                item["amount"] = amount
        
        if optional is not None:
            item["optional"] = optional
        
        return True
    
    def delete_deduction_item(self, name):
        """删除扣除项"""
        if name in self.config["deduction_items"]:
            del self.config["deduction_items"][name]
            return True
        return False
    
    # 税率表管理方法
    def update_tax_bracket(self, index, min_income=None, max_income=None, rate=None, deduction=None):
        """更新税率表中的某一档"""
        brackets = self.config["calculation_methods"]["progressive_tax"]["brackets"]
        if 0 <= index < len(brackets):
            bracket = brackets[index]
            if min_income is not None:
                bracket["min"] = min_income
            if max_income is not None:
                bracket["max"] = max_income if max_income != -1 else float('inf')
            if rate is not None:
                bracket["rate"] = rate
            if deduction is not None:
                bracket["deduction"] = deduction
            return True
        return False
    
    def add_tax_bracket(self, min_income, max_income, rate, deduction):
        """添加新的税率档次"""
        brackets = self.config["calculation_methods"]["progressive_tax"]["brackets"]
        new_bracket = {
            "min": min_income,
            "max": max_income if max_income != -1 else float('inf'),
            "rate": rate,
            "deduction": deduction
        }
        brackets.append(new_bracket)
        # 按最小收入排序
        brackets.sort(key=lambda x: x["min"])
        return True
    
    def delete_tax_bracket(self, index):
        """删除税率档次"""
        brackets = self.config["calculation_methods"]["progressive_tax"]["brackets"]
        if 0 <= index < len(brackets):
            del brackets[index]
            return True
        return False
    
    def export_config(self):
        """导出配置为JSON字符串"""
        return json.dumps(self.config, ensure_ascii=False, indent=2)
    
    def import_config(self, config_json):
        """从JSON字符串导入配置"""
        try:
            config_data = json.loads(config_json)
            self.config = config_data
            return True, "配置导入成功"
        except Exception as e:
            return False, f"配置导入失败: {str(e)}"
    
    def import_config_from_file(self, file_path):
        """从文件导入配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            self.config = config_data
            return True, "配置导入成功"
        except Exception as e:
            return False, f"配置导入失败: {str(e)}"
    
    def export_config_to_file(self, file_path):
        """导出配置到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True, "配置导出成功"
        except Exception as e:
            return False, f"配置导出失败: {str(e)}"
    
    def reset_config(self):
        """重置为默认配置"""
        self.config = self.load_default_config()
        return True, "已重置为默认配置"
    
    def get_salary_items(self):
        """获取所有收入项"""
        return self.config["salary_items"]
    
    def get_deduction_items(self):
        """获取所有扣除项"""
        return self.config["deduction_items"]
    
    def get_tax_brackets(self):
        """获取税率表"""
        return self.config["calculation_methods"]["progressive_tax"]["brackets"]
    
    def get_calculation_summary(self, salary_inputs, selected_deductions=None):
        """获取计算结果的格式化摘要"""
        result = self.calculate_salary(salary_inputs, selected_deductions)
        
        summary = {
            "总收入": f"¥{result['total_income']:,.2f}",
            "总扣除": f"¥{result['total_deductions']:,.2f}",
            "税后收入": f"¥{result['net_income']:,.2f}",
            "收入明细": {k: f"¥{v:,.2f}" for k, v in result["income_breakdown"].items()},
            "扣除明细": {k: f"¥{v:,.2f}" for k, v in result["deductions"].items()}
        }
        
        return summary, result 
    
    # 员工管理方法
    def add_employee(self, name, salary_data=None, selected_deductions=None):
        """添加员工"""
        if name and name not in self.employees:
            # 如果没有提供薪资数据，使用默认值
            if salary_data is None:
                salary_data = {item: config["default"] for item, config in self.config["salary_items"].items()}
            
            # 如果没有指定扣除项，使用所有非可选扣除项
            if selected_deductions is None:
                selected_deductions = [name for name, config in self.config["deduction_items"].items() 
                                     if not config.get("optional", False)]
            
            self.employees[name] = {
                "salary_data": salary_data,
                "selected_deductions": selected_deductions
            }
            return True
        return False
    
    def update_employee(self, name, salary_data=None, selected_deductions=None):
        """更新员工薪资数据"""
        if name in self.employees:
            if salary_data is not None:
                self.employees[name]["salary_data"] = salary_data
            if selected_deductions is not None:
                self.employees[name]["selected_deductions"] = selected_deductions
            return True
        return False
    
    def delete_employee(self, name):
        """删除员工"""
        if name in self.employees:
            del self.employees[name]
            return True
        return False
    
    def get_employees(self):
        """获取所有员工"""
        return self.employees
    
    def get_employee_data(self, name):
        """获取员工完整数据"""
        return self.employees.get(name, {})
    
    def get_employee_salary(self, name):
        """获取员工薪资数据"""
        employee_data = self.employees.get(name, {})
        return employee_data.get("salary_data", {})
    
    def get_employee_deductions(self, name):
        """获取员工选择的扣除项"""
        employee_data = self.employees.get(name, {})
        return employee_data.get("selected_deductions", [])
    
    def calculate_all_employees(self):
        """计算所有员工的工资"""
        results = {}
        for employee_name, employee_data in self.employees.items():
            salary_data = employee_data.get("salary_data", {})
            selected_deductions = employee_data.get("selected_deductions", [])
            results[employee_name] = self.calculate_salary(salary_data, selected_deductions)
        return results
    
    def export_employees_to_csv(self):
        """导出所有员工工资到CSV"""
        if not self.employees:
            return None
        
        # 计算所有员工的工资
        all_results = self.calculate_all_employees()
        
        # 准备CSV数据
        csv_data = []
        for employee_name, result in all_results.items():
            row = {"员工姓名": employee_name}
            
            # 添加收入项
            for item_name, amount in result["income_breakdown"].items():
                row[f"收入_{item_name}"] = amount
            
            # 添加扣除项
            for item_name, amount in result["deductions"].items():
                row[f"扣除_{item_name}"] = amount
            
            # 添加汇总
            row["总收入"] = result["total_income"]
            row["总扣除"] = result["total_deductions"]
            row["税后收入"] = result["net_income"]
            row["计算时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            csv_data.append(row)
        
        # 创建DataFrame并转换为CSV
        df = pd.DataFrame(csv_data)
        
        # 使用StringIO创建CSV内容
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8')
        csv_content = output.getvalue()
        output.close()
        
        return csv_content 