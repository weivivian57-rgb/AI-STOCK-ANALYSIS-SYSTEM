"""
report_panel.py

AI智能分析报告面板
"""

import tkinter as tk
from tkinter import ttk

from ui import styles


class ReportPanel(tk.Frame):
    """
    AI分析报告区域
    """

    def __init__(self, master):

        super().__init__(
            master,
            bg=styles.CARD,
            bd=1,
            relief="solid"
        )

        self.create_widgets()

    # =====================================================
    # 创建组件
    # =====================================================

    def create_widgets(self):

        # ==========================
        # 标题
        # ==========================

        title_frame = tk.Frame(
            self,
            bg=styles.CARD
        )

        title_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 10)
        )

        tk.Label(
            title_frame,
            text="🤖 AI Analysis Report",
            font=styles.FONT_H2,
            bg=styles.CARD,
            fg=styles.TITLE
        ).pack(
            side="left"
        )

        # ==========================
        # 文本区域
        # ==========================

        text_frame = tk.Frame(
            self,
            bg=styles.CARD
        )

        text_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        scrollbar = ttk.Scrollbar(text_frame)

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.report_text = tk.Text(
            text_frame,
            wrap="word",
            font=styles.FONT_NORMAL,
            bg=styles.REPORT_BG,
            fg=styles.REPORT_TEXT,
            relief="flat",
            padx=10,
            pady=10,
            yscrollcommand=scrollbar.set
        )

        self.report_text.pack(
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.report_text.yview
        )

        # 默认提示
        self.set_report(
            "请输入股票代码，然后点击 Analyze 开始分析。\n\n"
            "系统将自动完成：\n"
            "• 股票历史数据下载\n"
            "• 技术指标计算（MA、MACD、RSI）\n"
            "• 股价趋势预测\n"
            "• AI 智能分析报告生成"
        )

    # =====================================================
    # 更新报告
    # =====================================================

    def set_report(self, report):

        self.report_text.config(state="normal")

        self.report_text.delete("1.0", tk.END)

        self.report_text.insert(
            tk.END,
            report
        )

        self.report_text.config(state="disabled")

    # =====================================================
    # 清空报告
    # =====================================================

    def clear(self):

        self.report_text.config(state="normal")

        self.report_text.delete("1.0", tk.END)

        self.report_text.config(state="disabled")

    # =====================================================
    # 追加内容（调试可用）
    # =====================================================

    def append(self, text):

        self.report_text.config(state="normal")

        self.report_text.insert(
            tk.END,
            text + "\n"
        )

        self.report_text.see(tk.END)

        self.report_text.config(state="disabled")