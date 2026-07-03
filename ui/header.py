"""
header.py
系统顶部工具栏组件 - 负责股票代码输入与查询事件触发
"""

import tkinter as tk
from tkinter import ttk
from ui.styles import *


class Header(tk.Frame):
    def __init__(self, parent, on_search_callback):
        super().__init__(parent, bg=BG_PANEL)
        self.on_search_callback = on_search_callback

        # 股票代码输入
        tk.Label(self, text="股票代码:", font=FONT_MAIN, bg=BG_PANEL).pack(side=tk.LEFT, padx=(20, 5))
        self.entry_code = ttk.Entry(self, width=15, font=FONT_MAIN)
        self.entry_code.pack(side=tk.LEFT, padx=5)
        self.entry_code.insert(0, "AAPL")

        # ==========================
        # 💡 Mac 兼容性修复：使用 Label 模拟 Button 突破背景色限制
        # ==========================
        self.btn_search = tk.Label(
            self, 
            text="查询分析", 
            font=FONT_MAIN, 
            bg=COLOR_PRIMARY,     # 完美呈现主色调蓝色
            fg="#FFFFFF",         # 纯白文字
            padx=20, 
            pady=6, 
            cursor="hand2"        # 鼠标放上去变成小手
        )
        self.btn_search.pack(side=tk.LEFT, padx=10, pady=15)

        # 绑定点击与悬浮交互事件
        self.btn_search.bind("<Button-1>", lambda e: self._handle_search())
        self.btn_search.bind("<Enter>", self._on_hover_enter)
        self.btn_search.bind("<Leave>", self._on_hover_leave)

    def _on_hover_enter(self, event):
        """鼠标悬浮时的反馈色（略微提亮）"""
        if self.btn_search.cget("text") == "查询分析":
            self.btn_search.config(bg="#40A9FF")

    def _on_hover_leave(self, event):
        """鼠标移出时恢复主色调"""
        if self.btn_search.cget("text") == "查询分析":
            self.btn_search.config(bg=COLOR_PRIMARY)

    def _handle_search(self):
        code = self.entry_code.get().strip().upper()
        if code:
            # 点击后变为禁用视觉状态（浅蓝色 + 文字改变）
            self.btn_search.config(text="分析中...", bg="#A0CFFF")
            self.update()  # 强制立即刷新 UI
            
            # 触发主程序的查询路由
            self.on_search_callback(code)
            
            # 恢复正常状态
            self.btn_search.config(text="查询分析", bg=COLOR_PRIMARY)