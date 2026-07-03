"""
sidebar.py
系统侧边栏组件 - 负责导航菜单的渲染与专业高亮事件分发
"""

import tkinter as tk
from ui.styles import *


class Sidebar(tk.Frame):
    def __init__(self, parent, on_menu_click_callback):
        print(f"DEBUG: 正在加载的 sidebar 文件路径: {__file__}")
        super().__init__(parent, bg=BG_SIDEBAR, width=200)
        self.pack_propagate(False)
        
        self.on_menu_click = on_menu_click_callback
        self.buttons = {}

        # ==========================
        # 1. Logo 区域
        # ==========================
        logo_frame = tk.Frame(self, bg=BG_SIDEBAR)
        logo_frame.pack(fill=tk.X, pady=20)
        tk.Label(logo_frame, text="📈 AI股票", font=FONT_H1, bg=BG_SIDEBAR, fg=COLOR_PRIMARY).pack()
        tk.Label(logo_frame, text="智能分析系统", font=FONT_MAIN, bg=BG_SIDEBAR, fg=COLOR_TEXT_SUB).pack()

       
        # ==========================
        # 2. 导航菜单渲染 (精简版)
        # ==========================
        menus = ["🏠 首页概览", "🤖 AI智能分析", "🕒 历史记录", "⭐ 自选股票", "📝 意见反馈", "⚙️ 系统设置"]
        
        for i, menu in enumerate(menus):
            menu_key = menu.split(" ")[1]
            if i == 0:
                btn_fg = COLOR_PRIMARY
                bd_size = 1
                bd_color = COLOR_PRIMARY
            else:
                btn_fg = COLOR_TEXT_MAIN
                bd_size = 0
                bd_color = BG_SIDEBAR
            
            btn_border_container = tk.Frame(self, bg=bd_color, bd=bd_size)
            btn_border_container.pack(fill=tk.X, padx=10, pady=2)
            
            btn = tk.Button(
                btn_border_container, 
                text=menu, 
                font=FONT_MAIN, 
                bg=BG_SIDEBAR,
                fg=btn_fg,
                relief=tk.FLAT, 
                anchor="w", 
                padx=30, 
                pady=10, 
                cursor="hand2",
                command=lambda k=menu_key: self._handle_click(k)
            )
            btn.pack(fill=tk.X, padx=1, pady=1)
            self.buttons[menu_key] = (btn, btn_border_container)

        # ==========================
        # 3. 底部状态栏 (纯净版)
        # ==========================
        bottom_frame = tk.Frame(self, bg=BG_SIDEBAR)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.status_label = tk.Label(
            bottom_frame,
            text="系统状态: 运行正常",
            font=("Microsoft YaHei", 10),
            bg=BG_SIDEBAR,
            fg="#22C55E"
        )
        self.status_label.pack(side=tk.TOP, anchor="w", padx=20, pady=2)

        self.version_label = tk.Label(
            bottom_frame,
            text="系统版本: v1.1.0",
            font=("Microsoft YaHei", 9),
            bg=BG_SIDEBAR,
            fg="#94A3B8"
        )
        self.version_label.pack(side=tk.TOP, anchor="w", padx=20, pady=2)

        self.source_label = tk.Label(
            bottom_frame,
            text="数据引擎: AkShare & yfinance",
            font=("Microsoft YaHei", 9),
            bg=BG_SIDEBAR,
            fg="#94A3B8"
        )
        self.source_label.pack(side=tk.TOP, anchor="w", padx=20, pady=2)

    def _handle_click(self, menu_key: str):
        for key, (btn, container) in self.buttons.items():
            if key == menu_key:
                btn.config(fg=COLOR_PRIMARY)
                container.config(bg=COLOR_PRIMARY, bd=1)
            else:
                btn.config(fg=COLOR_TEXT_MAIN)
                container.config(bg=BG_SIDEBAR, bd=0)
        self.on_menu_click(menu_key)