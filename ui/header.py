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
        # 左侧：查询区域容器（确保所有子组件在垂直方向完美居中对齐）
        # ======================================================
        query_container = tk.Frame(self, bg=BG_PANEL)
        query_container.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        # 1. 文本提示
        tk.Label(
            query_container, 
            text="股票代码:", 
            font=("Microsoft YaHei", 12), 
            bg=BG_PANEL, 
            fg=COLOR_TEXT_MAIN
        ).pack(side=tk.LEFT, padx=(0, 10))

        # 2. 股票代码输入框（利用 ipady=4 精准撑高，使其与按钮对齐）
        self.entry_code = tk.Entry(
            query_container, 
            font=("Microsoft YaHei", 12), 
            width=15,
            bd=1,
            relief=tk.SOLID
        )
        self.entry_code.pack(side=tk.LEFT, ipady=4) 
        self.entry_code.insert(0, "AAPL")

        # 3. 终极“障眼法”按钮容器（调整了 pady=5 以配合输入框高度）
        self.btn_container = tk.Frame(query_container, bg="#3B82F6", bd=0)
        self.btn_container.pack(side=tk.LEFT, padx=15)
        
        # 内层 Label 负责文字
        self.btn_search = tk.Label(
            self.btn_container, 
            text="查询分析", 
            font=("Microsoft YaHei", 11, "bold"), # 字体微调到11，使整体观感更像一个紧凑的输入组
            bg="#3B82F6",    
            fg="#FFFFFF",
            padx=15,
            pady=5,          # 💡 与输入框的 ipady=4 形成高度闭环
            cursor="hand2"
        )
        self.btn_search.pack()
        
        # ======================================================
        # 按钮事件绑定
        # ======================================================
        self.btn_search.bind("<Button-1>", lambda event: self._handle_search())
        
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