"""
header.py

顶部搜索栏
"""

import tkinter as tk
from datetime import datetime
from ui import styles


class Header(tk.Frame):
    """
    顶部标题栏
    """

    def __init__(self, master):

        super().__init__(
            master,
            bg=styles.CARD,
            height=styles.HEADER_HEIGHT,
            bd=1,
            relief="solid"
        )

        self.pack_propagate(False)

        self.create_widgets()

    def create_widgets(self):

        # =====================================
        # 左侧标题
        # =====================================

        title_frame = tk.Frame(
            self,
            bg=styles.CARD
        )

        title_frame.pack(
            side="left",
            padx=20,
            fill="y"
        )

        tk.Label(
            title_frame,
            text="AI Stock Analysis System",
            font=styles.FONT_H1,
            bg=styles.CARD,
            fg=styles.TITLE
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Artificial Intelligence Stock Analysis Platform",
            font=styles.FONT_SMALL,
            bg=styles.CARD,
            fg=styles.LIGHT_TEXT
        ).pack(anchor="w")

        # =====================================
        # 右侧区域
        # =====================================

        right_frame = tk.Frame(
            self,
            bg=styles.CARD
        )

        right_frame.pack(
            side="right",
            padx=20
        )

        # 当前时间
        self.time_label = tk.Label(
            right_frame,
            text=datetime.now().strftime("%Y-%m-%d"),
            font=styles.FONT_SMALL,
            bg=styles.CARD,
            fg=styles.LIGHT_TEXT
        )

        self.time_label.pack(
            side="right",
            padx=(15, 0)
        )

        # Analyze 按钮
        self.analyze_button = tk.Button(
            right_frame,
            text="Analyze",
            width=12,
            bg=styles.BUTTON_BG,
            fg=styles.BUTTON_FG,
            activebackground=styles.BUTTON_ACTIVE_BG,
            activeforeground=styles.BUTTON_ACTIVE_FG,
            relief="flat",
            cursor="hand2",
            font=styles.FONT_NORMAL
        )

        self.analyze_button.pack(
            side="right",
            padx=(10, 0),
            ipady=4
        )

        # 股票代码输入框
        self.symbol_entry = tk.Entry(
            right_frame,
            width=18,
            font=styles.FONT_NORMAL,
            relief="solid",
            bd=1
        )

        self.symbol_entry.insert(0, "AAPL")

        self.symbol_entry.pack(
            side="right",
            ipady=4
        )

        # 标签
        tk.Label(
            right_frame,
            text="Stock:",
            bg=styles.CARD,
            fg=styles.TEXT,
            font=styles.FONT_NORMAL
        ).pack(
            side="right",
            padx=(0, 8)
        )

    # =====================================
    # 获取股票代码
    # =====================================

    def get_symbol(self):
        """
        获取用户输入的股票代码
        """
        return self.symbol_entry.get().strip().upper()

    # =====================================
    # 设置按钮事件
    # =====================================

    def set_analyze_command(self, command):
        """
        绑定 Analyze 按钮事件
        """
        self.analyze_button.config(command=command)

        # 支持按 Enter 键分析
        self.symbol_entry.bind(
            "<Return>",
            lambda event: command()
        )