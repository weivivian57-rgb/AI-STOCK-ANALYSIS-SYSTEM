"""
sidebar.py

左侧导航栏
"""

import tkinter as tk
from ui import styles


class Sidebar(tk.Frame):

    def __init__(self, master):

        super().__init__(
            master,
            bg=styles.SIDEBAR,
            width=styles.SIDEBAR_WIDTH
        )

        self.pack_propagate(False)

        self.create_widgets()

    def create_widgets(self):

        # Logo
        tk.Label(
            self,
            text="📈",
            font=("Helvetica", 42),
            bg=styles.SIDEBAR
        ).pack(pady=(35, 10))

        # 系统名称
        tk.Label(
            self,
            text="AI Stock\nAnalysis",
            font=styles.FONT_H1,
            fg=styles.TITLE,
            bg=styles.SIDEBAR,
            justify="center"
        ).pack()

        # 分割线
        tk.Frame(
            self,
            bg=styles.BORDER,
            height=1
        ).pack(fill="x", padx=20, pady=30)

        # 菜单
        self.create_menu_button("🏠  Dashboard")
        self.create_menu_button("📊  Stock Analysis")
        self.create_menu_button("🤖  AI Report")
        self.create_menu_button("📁  Export")
        self.create_menu_button("⚙  Settings")

    def create_menu_button(self, text):

        btn = tk.Button(
            self,
            text=text,
            font=styles.FONT_NORMAL,
            bg=styles.SIDEBAR,
            fg=styles.TEXT,
            relief="flat",
            bd=0,
            anchor="w",
            padx=20,
            activebackground=styles.PRIMARY,
            activeforeground="white",
            cursor="hand2"
        )

        btn.pack(
            fill="x",
            padx=15,
            pady=6,
            ipady=8
        )

        return btn