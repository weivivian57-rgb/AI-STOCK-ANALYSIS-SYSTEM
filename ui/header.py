"""
header.py
全局组件 - 顶部查询与状态头部
"""

import tkinter as tk
import time
from ui.styles import BG_PANEL, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB


class Header(tk.Frame):
    def __init__(self, parent, on_search_callback):
        super().__init__(parent, bg=BG_PANEL, height=70, bd=1, relief=tk.FLAT)
        self.pack_propagate(False)
        self.on_search = on_search_callback

        # ======================================================
        # 左侧：查询区域
        # ======================================================
        tk.Label(
            self, 
            text="股票代码:", 
            font=("Microsoft YaHei", 12), 
            bg=BG_PANEL, 
            fg=COLOR_TEXT_MAIN
        ).pack(side=tk.LEFT, padx=(20, 10))

        self.entry_code = tk.Entry(
            self, 
            font=("Microsoft YaHei", 12), 
            width=15,
            bd=1,
            relief=tk.SOLID
        )
        self.entry_code.pack(side=tk.LEFT, padx=5, pady=15)
        self.entry_code.insert(0, "AAPL")

       # ======================================================
        # 💡 终极“障眼法”：Frame (蓝色底) + Label (文字)
        # ======================================================
        # 1. 外层容器负责背景色
        self.btn_container = tk.Frame(self, bg="#3B82F6", bd=0)
        self.btn_container.pack(side=tk.LEFT, padx=15)
        
        # 2. 内层 Label 负责文字，背景设为透明 (systemTransparent 不可用时用父容器色)
        self.btn_search = tk.Label(
            self.btn_container, 
            text="查询分析", 
            font=("Microsoft YaHei", 11, "bold"),
            bg="#3B82F6",    # 必须和父容器颜色一致
            fg="#FFFFFF",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.btn_search.pack()
        
        # 3. 绑定点击
        self.btn_search.bind("<Button-1>", lambda event: self._handle_search())
        
        # 4. 悬停反馈 (同时改变容器和 Label 的颜色)
        def on_enter(e):
            self.btn_container.config(bg="#2563EB")
            self.btn_search.config(bg="#2563EB")
            
        def on_leave(e):
            self.btn_container.config(bg="#3B82F6")
            self.btn_search.config(bg="#3B82F6")
        
        self.btn_search.bind("<Enter>", on_enter)
        self.btn_search.bind("<Leave>", on_leave)
        # ======================================================
        # 右侧：实时动态时间时钟
        # ======================================================
        self.time_label = tk.Label(
            self, 
            text="🕒 正在加载时间...", 
            font=("Microsoft YaHei", 11), 
            bg=BG_PANEL, 
            fg=COLOR_TEXT_SUB
        )
        # 确保挂载在右侧
        self.time_label.pack(side=tk.RIGHT, padx=25)

        # 启动心跳引擎
        self._update_clock()

    def _handle_search(self):
        code = self.entry_code.get().strip()
        if code:
            self.on_search(code)

    def _update_clock(self):
        """每秒更新时间"""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"🕒 {current_time}")
        self.after(1000, self._update_clock)