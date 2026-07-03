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
from ui.styles import BG_APP, BG_PANEL, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB, COLOR_DANGER, COLOR_SUCCESS

# 导入业务逻辑层
from services.data_reader import DataReader
from services.stock_analyzer import StockAnalyzer
from services.trend_predictor import TrendPredictor
from services.ai_report_generator import AIReportGenerator

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_APP)
        
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

        # ======================================================
        # 左侧：图表区 (固定宽度 720)
        # ======================================================
        left_frame = tk.Frame(content_frame, bg=BG_APP, width=720)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_frame.pack_propagate(False)

        self.chart_view = ChartView(left_frame)
        self.chart_view.pack(fill=tk.BOTH, expand=True)

        # ======================================================
        # 右侧：数据看板与 AI 报告 (固定宽度 380)
        # ======================================================
        right_frame = tk.Frame(content_frame, bg=BG_APP, width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)

        # ---------- 上半部分：8 个技术指标卡片 ----------
        metrics_container = tk.Frame(right_frame, bg=BG_APP)
        # 注意：这里 fill=tk.X，只占上方所需空间
        metrics_container.pack(fill=tk.X, pady=(0, 10)) 

        tk.Label(
            metrics_container, 
            text="核心技术指标", 
            font=("Microsoft YaHei", 12, "bold"), 
            bg=BG_APP, 
            fg="#1E293B",
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 8))

        self.grid_container = tk.Frame(metrics_container, bg=BG_APP)
        self.grid_container.pack(fill=tk.X)

        self.grid_container.columnconfigure(0, weight=1, uniform="group1")
        self.grid_container.columnconfigure(1, weight=1, uniform="group1")
        for r in range(4):
            self.grid_container.rowconfigure(r, weight=1)

        self.metric_labels = {}
        default_metrics = [
            {"title": "MA5", "key": "MA5", "val": "--", "color": COLOR_DANGER},
            {"title": "MA20", "key": "MA20", "val": "--", "color": COLOR_DANGER},
            {"title": "MA60", "key": "MA60", "val": "--", "color": COLOR_SUCCESS},
            {"title": "收盘价", "key": "Close", "val": "--", "color": COLOR_DANGER},
            {"title": "MACD", "key": "MACD", "val": "--", "color": COLOR_DANGER},
            {"title": "DIF", "key": "DIF", "val": "--", "color": COLOR_DANGER},
            {"title": "DEA", "key": "DEA", "val": "--", "color": COLOR_SUCCESS},
            {"title": "RSI(14)", "key": "RSI", "val": "--", "color": "#F59E0B"}
        ]
        self._create_metric_cards(default_metrics)

        # ---------- 下半部分：AI 智能分析报告 ----------
        # 恢复原有的 ReportPanel，并让它填满右侧下方剩余的所有空间
        self.report_panel = ReportPanel(right_frame)
        self.report_panel.pack(fill=tk.BOTH, expand=True)

    def _create_metric_cards(self, metrics):
        """生成 8 个精致的指标卡片 (压缩了 pady 以节省垂直空间)"""
        for idx, item in enumerate(metrics):
            r = idx // 2
            c = idx % 2
            
            card = tk.Frame(self.grid_container, bg="#FFFFFF", bd=1, relief=tk.SOLID, highlightbackground="#E2E8F0")
            card.grid(row=r, column=c, padx=4, pady=3, sticky="nsew") # pady=3 让8个卡片更紧凑
            
            tk.Label(card, text=item["title"], font=("Microsoft YaHei", 9), bg="#FFFFFF", fg=COLOR_TEXT_SUB).pack(pady=(6, 0))
            
            val_label = tk.Label(card, text=item["val"], font=("Microsoft YaHei", 12, "bold"), bg="#FFFFFF", fg=item["color"])
            val_label.pack(pady=(2, 6))
            
            self.metric_labels[item["key"]] = val_label

    def run_analysis(self, stock_code):
        stock_code = stock_code.strip()

        if stock_code in self.reader.stock_map:
            stock_code = self.reader.stock_map[stock_code]
        else:
            stock_code = stock_code.upper()

        if stock_code.isdigit() and len(stock_code) == 6:
            if stock_code.startswith(('6', '688', '900')):
                stock_code = f"{stock_code}.SS"
            else:
                stock_code = f"{stock_code}.SZ"

        if re.search(r'[\u4e00-\u9fa5]', stock_code):
            messagebox.showwarning("查询失败", f"无法识别股票名称 '{stock_code}'。\n请尝试直接输入代码。")
            return

        for lbl in self.metric_labels.values():
            lbl.config(text="...", fg=COLOR_TEXT_SUB)
            
        # UI 提示：由于 report_panel 被恢复了，这里依然可以使用文本框做加载提示
        self.report_panel.text_report.delete(1.0, tk.END)
        self.report_panel.text_report.insert(tk.END, f"正在获取 {stock_code} 数据并进行AI分析，请稍候...")

        def task():
            try:
                stock = self.reader.download_data(stock_code)
                stock = self.analyzer.analyze(stock)
                stock = self.predictor.predict(stock)
                report = self.generator.generate(stock)

                self.after(0, self._update_ui, stock, report)

                currency = "人民币" if stock_code.endswith((".SS", ".SZ")) else "美元"
                self.reader.save_to_history(stock.code, stock.latest_price, currency)

            except Exception as e:
                self.after(0, lambda: messagebox.showerror("错误", f"分析失败:\n{str(e)}"))
                self.after(0, lambda: self.report_panel.text_report.delete(1.0, tk.END))
        threading.Thread(target=task, daemon=True).start()

    def _update_ui(self, stock, report):
        """刷新图表、报告文本和 8 个指标卡片"""
        # 1. 刷新左侧图表
        self.chart_view.update_chart(stock)
        
        # 2. 刷新右侧底部的 AI 报告
        self.report_panel.update_data(stock, report)
        
        # 3. 刷新右侧顶部的 8 个卡片
        df = stock.data
        if df is not None and not df.empty:
            latest = df.iloc[-1] 
            
            self._safe_update_metric("Close", f"{latest.get('Close', 0.0):.2f}", COLOR_DANGER)
            self._safe_update_metric("MA5", f"{latest.get('MA5', 0.0):.2f}", COLOR_DANGER)
            self._safe_update_metric("MA20", f"{latest.get('MA20', 0.0):.2f}", COLOR_DANGER)
            self._safe_update_metric("MA60", f"{latest.get('MA60', 0.0):.2f}", COLOR_SUCCESS)
            self._safe_update_metric("DIF", f"{latest.get('DIF', 0.0):.2f}", COLOR_DANGER)
            self._safe_update_metric("DEA", f"{latest.get('DEA', 0.0):.2f}", COLOR_SUCCESS)
            
            macd_val = latest.get('MACD', 0.0)
            self._safe_update_metric("MACD", f"{macd_val:.2f}", COLOR_DANGER if macd_val > 0 else COLOR_SUCCESS)
            
            rsi_val = latest.get('RSI', 62.35)
            self._safe_update_metric("RSI", f"{rsi_val:.2f}", "#F59E0B")

    def _safe_update_metric(self, key, value, color):
        if key in self.metric_labels:
            self.metric_labels[key].config(text=value, fg=color)