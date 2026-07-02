"""
main_window.py

AI Stock Analysis System
主窗口（Controller）
"""

import tkinter as tk
from tkinter import messagebox

from ui import styles

from ui.sidebar import Sidebar
from ui.header import Header
from ui.dashboard import Dashboard
from ui.chart_view import ChartView
from ui.report_panel import ReportPanel

from services.data_reader import DataReader
from services.stock_analyzer import StockAnalyzer
from services.trend_predictor import TrendPredictor
from services.ai_report_generator import AIReportGenerator


class MainWindow:

    def __init__(self):

        # ==========================
        # 创建主窗口
        # ==========================

        self.root = tk.Tk()

        self.root.title("AI Stock Analysis System")

        self.root.geometry(
            f"{styles.WINDOW_WIDTH}x{styles.WINDOW_HEIGHT}"
        )

        self.root.configure(bg=styles.BG)

        self.root.minsize(1200, 760)

        # ==========================
        # 初始化业务模块
        # ==========================

        self.reader = DataReader()

        self.analyzer = StockAnalyzer()

        self.predictor = TrendPredictor()

        self.report_generator = AIReportGenerator()

        # ==========================
        # 创建界面
        # ==========================

        self.create_layout()

    # ====================================================
    # 创建整体布局
    # ====================================================

    def create_layout(self):

        # -----------------------------
        # 左侧菜单
        # -----------------------------

        self.sidebar = Sidebar(self.root)

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # -----------------------------
        # 右侧整体
        # -----------------------------

        self.main_frame = tk.Frame(
            self.root,
            bg=styles.BG
        )

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # -----------------------------
        # Header
        # -----------------------------

        self.header = Header(self.main_frame)

        self.header.pack(
            fill="x"
        )

        self.header.set_analyze_command(
            self.analyze_stock
        )

        # -----------------------------
        # Dashboard
        # -----------------------------

        self.dashboard = Dashboard(self.main_frame)

        self.dashboard.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # -----------------------------
        # Chart
        # -----------------------------

        self.chart = ChartView(self.main_frame)

        self.chart.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # -----------------------------
        # Report
        # -----------------------------

        self.report_panel = ReportPanel(self.main_frame)

        self.report_panel.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    # ====================================================
    # 点击 Analyze
    # ====================================================

    def analyze_stock(self):

        symbol = self.header.get_symbol()

        if symbol == "":

            messagebox.showwarning(
                "Warning",
                "Please input stock symbol."
            )

            return

        try:

            # 下载数据
            stock = self.reader.download_data(symbol)

            # 技术分析
            stock = self.analyzer.analyze(stock)

            # 趋势预测
            stock = self.predictor.predict(stock)

            # AI报告
            report = self.report_generator.generate(stock)

            # Dashboard
            self.dashboard.update_dashboard(
                stock,
                report
            )

            # 图表
            self.chart.update_chart(stock)

            # AI报告
            self.report_panel.set_report(report)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ====================================================
    # 启动程序
    # ====================================================

    def run(self):

        self.root.mainloop()