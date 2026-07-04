"""
dashboard.py
系统核心工作区 - 首页概览面板（全新智能选股与多参数融合版）
"""

import tkinter as tk
from tkinter import messagebox
import threading

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
        # 传入第二参数（查询逻辑）和第三参数（加入自选逻辑）
        self.header = Header(self, self.run_analysis, self._add_to_watchlist_action)
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
        # 💡 强制在这里初始化空状态！
        # 💡 使用 after 延迟，确保画布准备好后再绘制图片
        self.after(100, lambda: self.chart_view.update_chart(None))
        # ======================================================
        # 右侧：数据看板与 AI 报告 (固定宽度 380)
        # ======================================================
        right_frame = tk.Frame(content_frame, bg=BG_APP, width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)

        # ---------- 上半部分：8 个技术指标卡片 ----------
        metrics_container = tk.Frame(right_frame, bg=BG_APP)
        metrics_container.pack(fill=tk.X, pady=(0, 10)) 

        tk.Label(
            metrics_container, 
            text="核心技术指标", 
            font=("Microsoft YaHei", 14, "bold"), 
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
        self.report_panel = ReportPanel(right_frame)
        self.report_panel.pack(fill=tk.BOTH, expand=True)

    def _create_metric_cards(self, metrics):
        """生成 8 个精致的指标卡片"""
        for idx, item in enumerate(metrics):
            r = idx // 2
            c = idx % 2
            
            card = tk.Frame(self.grid_container, bg="#FFFFFF", bd=0, relief=tk.FLAT, highlightbackground="#E5E7EB")
            card.grid(row=r, column=c, padx=4, pady=3, sticky="nsew")
            
            tk.Label(card, text=item["title"], font=("Microsoft YaHei", 9), bg="#FFFFFF", fg=COLOR_TEXT_SUB).pack(pady=(6, 0))
            
            val_label = tk.Label(card, text=item["val"], font=("Microsoft YaHei", 12, "bold"), bg="#FFFFFF", fg=item["color"])
            val_label.pack(pady=(2, 6))
            
            self.metric_labels[item["key"]] = val_label

    def run_analysis(self, keyword, start_date=None, end_date=None):
        keyword = keyword.strip()
        if not keyword:
            return

        yf_code, stock_name = self.reader.resolve_stock_code(keyword)

        if not yf_code:
            from tkinter import messagebox
            messagebox.showwarning("查询失败", f"未能检索到与 '{keyword}' 相关的股票。")
            return

        # 自动生成报告区间文案
        report_time_range = f"{start_date} 至 {end_date}" if start_date else "过去5年 (全量/稳定区间)"

        for lbl in self.metric_labels.values():
            lbl.config(text="...", fg=COLOR_TEXT_SUB)
        
        # ❌ 已经把你原本放在这里的报错代码删除了
            
        self.report_panel.text_report.delete(1.0, tk.END)
        self.report_panel.text_report.insert(
            tk.END, 
            f"🚀 已识别：{stock_name} ({yf_code})\n⏳ 正在进行 [{report_time_range}] 的 AI 量化分析，请稍候..."
        )

        def task():
            try:
                # 1. 真实的数据对象在这里诞生，它的名字叫 `stock`
                stock = self.reader.download_data(yf_code, start=start_date, end=end_date)
                stock.name = stock_name  
                stock.time_range = report_time_range 
                
                stock = self.analyzer.analyze(stock)
                stock = self.predictor.predict(stock)
                report = self.generator.generate(stock)

                # 💡 [关键修复]：数据完全准备好之后，存入 self.current_stock 供“加入自选”按钮调用
                self.current_stock = stock

                # 更新界面
                self.after(0, self._update_ui, stock, report)

                currency = "人民币" if yf_code.endswith((".SS", ".SZ")) else ("港币" if yf_code.endswith(".HK") else "美元")
                display_name = f"{stock_name} ({yf_code})"
                self.reader.save_to_history(display_name, stock.latest_price, currency)

            except Exception as e:
                err_msg = str(e)
                from tkinter import messagebox
                self.after(0, lambda: messagebox.showerror("错误", f"分析失败:\n{err_msg}"))
                self.after(0, lambda: self.report_panel.text_report.delete(1.0, tk.END))
                
        # 启动后台线程执行 task
        threading.Thread(target=task, daemon=True).start()

    def _update_ui(self, stock, report):
        df = stock.data
        print(f"DEBUG: 接收到的数据起止时间: {df.index[0]} 至 {df.index[-1]}")
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

    def _add_to_watchlist_action(self):
        """将当前查询的股票加入自选股面板"""
        from tkinter import messagebox
        
        # 1. 校验当前是否有查询结果
        # 💡 假设你把当前查询的股票对象存在 self.current_stock 中。
        # 如果你用的是别的变量名（比如 self.stock_data），请相应替换。
        if not hasattr(self, 'current_stock') or self.current_stock is None:
            messagebox.showwarning("提示", "请先输入代码并获取分析数据，再加入自选！")
            return
            
        stock = self.current_stock
        
        # 2. 尝试获取主窗口中的 watchlist_panel 实例并添加数据
        try:
            main_window = self.winfo_toplevel()
            # 确保主窗口已经初始化了自选面板
            if hasattr(main_window, 'watchlist_panel'):
                # 调用自选面板的新增方法 (我们下一步去写这个方法)
                main_window.watchlist_panel.add_dynamic_stock(stock)
                messagebox.showinfo("成功", f"⭐ 已将 {stock.name} ({stock.code}) 加入自选！")
            else:
                print("[错误] 未在主窗口找到 watchlist_panel 实例")
        except Exception as e:
            messagebox.showerror("错误", f"加入自选失败: {e}")