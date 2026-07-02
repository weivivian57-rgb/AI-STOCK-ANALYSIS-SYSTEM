"""
dashboard.py

数据显示区域
"""

import tkinter as tk
from ui import styles


class Dashboard(tk.Frame):

    def __init__(self, master):

        super().__init__(
            master,
            bg=styles.BG
        )

        self.create_widgets()

    # =====================================================
    # 创建界面
    # =====================================================

    def create_widgets(self):

        # 标题
        title = tk.Label(
            self,
            text="Stock Dashboard",
            font=styles.FONT_TITLE,
            bg=styles.BG,
            fg=styles.TITLE
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        # ==========================
        # 四张数据卡片
        # ==========================

        card_frame = tk.Frame(
            self,
            bg=styles.BG
        )

        card_frame.pack(
            fill="x",
            padx=25
        )

        self.price_value = self.create_card(
            card_frame,
            "Current Price",
            "--"
        )

        self.ma20_value = self.create_card(
            card_frame,
            "MA20",
            "--"
        )

        self.rsi_value = self.create_card(
            card_frame,
            "RSI",
            "--"
        )

        self.macd_value = self.create_card(
            card_frame,
            "MACD",
            "--"
        )

        # ==========================
        # AI报告
        # ==========================

        report = tk.Frame(
            self,
            bg=styles.CARD,
            bd=1,
            relief="solid"
        )

        report.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        tk.Label(
            report,
            text="AI Analysis Report",
            font=styles.FONT_H2,
            bg=styles.CARD,
            fg=styles.TITLE
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        self.report_text = tk.Text(
            report,
            wrap="word",
            relief="flat",
            bg=styles.CARD,
            font=styles.FONT_NORMAL
        )

        self.report_text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    # =====================================================
    # 创建指标卡片
    # =====================================================

    def create_card(self, parent, title, value):

        card = tk.Frame(
            parent,
            bg=styles.CARD,
            bd=1,
            relief="solid",
            width=220,
            height=110
        )

        card.pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=styles.FONT_CARD_TITLE,
            bg=styles.CARD,
            fg=styles.TEXT
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=styles.FONT_CARD_VALUE,
            bg=styles.CARD,
            fg=styles.PRIMARY
        )

        value_label.pack(
            anchor="w",
            padx=18
        )

        return value_label

    # =====================================================
    # 更新数据显示
    # =====================================================

    def update_dashboard(self, stock, report):

        self.price_value.config(
            text=f"${stock.latest_price:.2f}"
        )

        self.ma20_value.config(
            text=f"{stock.ma20:.2f}"
        )

        self.rsi_value.config(
            text=f"{stock.rsi:.2f}"
        )

        self.macd_value.config(
            text=f"{stock.macd:.2f}"
        )

        self.report_text.delete("1.0", tk.END)

        self.report_text.insert(
            tk.END,
            report
        )