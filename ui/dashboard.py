"""
dashboard.py
系统核心工作区 - 首页概览面板
"""

import tkinter as tk
from tkinter import messagebox
import threading
import re

from ui.header import Header
from ui.chart_view import ChartView
from ui.report_panel import ReportPanel
from ui.styles import BG_APP

# 导入业务逻辑层
from services.data_reader import DataReader
from services.stock_analyzer import StockAnalyzer
from services.trend_predictor import TrendPredictor
from services.ai_report_generator import AIReportGenerator

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_APP)
        
        # 初始化业务引擎
        self.reader = DataReader()
        self.analyzer = StockAnalyzer()
        self.predictor = TrendPredictor()
        self.generator = AIReportGenerator()

        # 1. 顶部 Header
        self.header = Header(self, self.run_analysis)
        self.header.pack(fill=tk.X, pady=(0, 10))

        # 2. 内容区 (左右分栏)
        content_frame = tk.Frame(self, bg=BG_APP)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # 左侧图表
        self.chart_view = ChartView(content_frame)
        self.chart_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # 右侧报告
        self.report_panel = ReportPanel(content_frame)
        self.report_panel.pack(side=tk.RIGHT, fill=tk.Y)

    def run_analysis(self, stock_code):
        """执行分析流程 (使用多线程防止UI卡死)"""
        stock_code = stock_code.strip()

        # 1. 尝试从 DataReader 的映射表中查找中文名
        if stock_code in self.reader.stock_map:
            # 如果输入的是中文，获取到 6 位纯数字代码
            stock_code = self.reader.stock_map[stock_code]
        else:
            # 如果输入的不是映射表里的中文，统一转大写处理
            stock_code = stock_code.upper()

        # 2. 补全 yfinance 需要的后缀
        if stock_code.isdigit() and len(stock_code) == 6:
            if stock_code.startswith(('6', '688', '900')):
                stock_code = f"{stock_code}.SS"  # 上交所
            else:
                stock_code = f"{stock_code}.SZ"  # 深交所

        # 💡 3. 风控拦截：检查最终代码是否依然包含中文
        if re.search(r'[\u4e00-\u9fa5]', stock_code):
            messagebox.showwarning(
                "查询失败", 
                f"无法识别股票名称 '{stock_code}'。\n可能是网络映射表加载失败，且本地后备字典未收录该股票。\n\n请尝试直接输入 6 位数字代码。"
            )
            return  # 拦截！直接退出函数

        # 更新 UI 提示语（移除了重复的一段）
        self.report_panel.text_report.delete(1.0, tk.END)
        self.report_panel.text_report.insert(tk.END, f"正在获取 {stock_code} 数据并进行AI分析，请稍候...")

        def task():
            try:
                print(f"\n[DEBUG Thread] 线程启动，正在获取 {stock_code} 的在线数据...")
                stock = self.reader.download_data(stock_code)
                stock = self.analyzer.analyze(stock)
                stock = self.predictor.predict(stock)
                report = self.generator.generate(stock)

                print("[DEBUG Thread] 底层算法模型计算完毕，准备调度主线程刷新 UI...")
                self.after(0, self._update_ui, stock, report)

                # ======================================================
                # 💡 追踪重点：触发保存前夕
                # ======================================================
                currency = "人民币" if stock_code.endswith((".SS", ".SZ")) else "美元"
                print(f"[DEBUG Thread] UI 刷新指令已下发，开始接通历史记录管道...")
                self.reader.save_to_history(stock.code, stock.latest_price, currency)

            except Exception as e:
                print(f"[DEBUG Thread 崩溃] 🛑 线程内发生未捕获异常: {e}")
                self.after(0, lambda: messagebox.showerror("错误", f"分析失败:\n{str(e)}"))
                self.after(0, lambda: self.report_panel.text_report.delete(1.0, tk.END))
        threading.Thread(target=task, daemon=True).start()

    def _update_ui(self, stock, report):
        self.chart_view.update_chart(stock)
        self.report_panel.update_data(stock, report)