import tkinter as tk
from tkinter import messagebox
import threading

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
        self.report_panel.text_report.delete(1.0, tk.END)
        self.report_panel.text_report.insert(tk.END, f"正在获取 {stock_code} 数据并进行AI分析，请稍候...")

        def task():
            try:
                # 业务流转
                stock = self.reader.download_data(stock_code)
                stock = self.analyzer.analyze(stock)
                stock = self.predictor.predict(stock)
                report = self.generator.generate(stock)

                # 回到主线程更新UI
                self.after(0, self._update_ui, stock, report)
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("错误", f"分析失败:\n{str(e)}"))
                self.after(0, lambda: self.report_panel.text_report.delete(1.0, tk.END))

        threading.Thread(target=task, daemon=True).start()

    def _update_ui(self, stock, report):
        self.chart_view.update_chart(stock)
        self.report_panel.update_data(stock, report)