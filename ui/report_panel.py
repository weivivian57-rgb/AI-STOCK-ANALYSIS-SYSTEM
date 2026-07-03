import tkinter as tk
from ui.styles import *

class ReportPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_APP, width=350)
        self.pack_propagate(False)

        # === 1. 技术指标区 ===
        self.ind_frame = tk.Frame(self, bg=BG_PANEL)
        self.ind_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(self.ind_frame, text="核心技术指标", font=FONT_TITLE, bg=BG_PANEL).pack(anchor="w", padx=15, pady=10)
        
        self.ind_data_frame = tk.Frame(self.ind_frame, bg=BG_PANEL)
        self.ind_data_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # 指标Labels字典，方便后续更新
        self.labels = {}
        indicators = [("MA5", 0, 0), ("MA20", 0, 1), ("MACD", 1, 0), ("RSI(14)", 1, 1)]
        for name, r, c in indicators:
            box = tk.Frame(self.ind_data_frame, bg="#FAFAFA", bd=1, relief=tk.SOLID)
            box.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            tk.Label(box, text=name, font=("Arial", 9), bg="#FAFAFA", fg=COLOR_TEXT_SUB).pack(pady=(5,0))
            lbl_val = tk.Label(box, text="--", font=FONT_NUMBER, bg="#FAFAFA", fg=COLOR_TEXT_MAIN)
            lbl_val.pack(pady=(0,5), padx=20)
            self.labels[name] = lbl_val

        # === 2. AI智能分析报告区 ===
        self.ai_frame = tk.Frame(self, bg=BG_PANEL)
        self.ai_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.ai_frame, text="🤖 AI智能分析报告", font=FONT_TITLE, bg=BG_PANEL).pack(anchor="w", padx=15, pady=10)
        
        self.text_report = tk.Text(self.ai_frame, font=FONT_MAIN, bg=BG_PANEL, fg=COLOR_TEXT_MAIN, 
                                   relief=tk.FLAT, wrap=tk.WORD)
        self.text_report.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        self.text_report.insert(tk.END, "请在上方输入股票代码并点击查询...")

    def update_data(self, stock, report_text):
        # 更新指标
        self.labels["MA5"].config(text=f"{stock.ma5:.2f}", fg=COLOR_DANGER if stock.latest_price > stock.ma5 else COLOR_SUCCESS)
        self.labels["MA20"].config(text=f"{stock.ma20:.2f}", fg=COLOR_DANGER if stock.latest_price > stock.ma20 else COLOR_SUCCESS)
        self.labels["MACD"].config(text=f"{stock.macd:.2f}", fg=COLOR_DANGER if stock.macd > 0 else COLOR_SUCCESS)
        self.labels["RSI(14)"].config(text=f"{stock.rsi:.2f}")

        # 更新报告
        self.text_report.delete(1.0, tk.END)
        self.text_report.insert(tk.END, report_text)