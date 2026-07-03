"""
report_panel.py
AI 报告面板 - 仅负责渲染底部的智能分析文本
"""

import tkinter as tk
from ui.styles import *

class ReportPanel(tk.Frame):
    def __init__(self, parent):
        # 移除原有的固定 width，让它在外部容器中自然拉伸
        super().__init__(parent, bg=BG_PANEL)

        # === 🤖 AI智能分析报告区 ===
        title_frame = tk.Frame(self, bg=BG_PANEL)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            title_frame, 
            text="🤖 AI智能分析报告", 
            font=FONT_TITLE, 
            bg=BG_PANEL,
            fg=COLOR_TEXT_MAIN
        ).pack(anchor="w", padx=5, pady=5)
        
        # 报告纯文本框 (去掉了旧版的指标卡片)
        self.text_report = tk.Text(
            self, 
            font=FONT_MAIN, 
            bg="#F8FAFC", 
            fg=COLOR_TEXT_MAIN, 
            relief=tk.SOLID, 
            bd=1,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        # 撑满剩余的所有空间
        self.text_report.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.text_report.insert(tk.END, "请在上方输入股票代码并点击查询...")

    def update_data(self, stock, report_text):
        """只负责更新文本，不再处理那4个废弃的卡片"""
        self.text_report.delete(1.0, tk.END)
        self.text_report.insert(tk.END, report_text)