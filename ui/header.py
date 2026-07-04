"""
header.py
优化版：原生输入交互 + 极致响应性能
"""

import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta
from ui.styles import BG_PANEL, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB

class Header(tk.Frame):
    # 💡 [修改1] 增加 on_add_watchlist_callback 参数
    def __init__(self, parent, on_search_callback, on_add_watchlist_callback=None):
        super().__init__(parent, bg=BG_PANEL, height=70, bd=0)
        self.pack_propagate(False)
        self.on_search = on_search_callback
        self.on_add_watchlist = on_add_watchlist_callback # 保存回调函数

        # ======================================================
        # 主查询容器
        # ======================================================
        query_container = tk.Frame(self, bg=BG_PANEL)
        query_container.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=15)

        # ── 1. 股票代码输入 ──
        self._create_label(query_container, "股票代码:")
        self.entry_code = tk.Entry(
            query_container, font=("Microsoft YaHei", 12), width=12, bd=1, relief=tk.SOLID
        )
        self.entry_code.pack(side=tk.LEFT, padx=(0, 15), ipady=3)
        self.entry_code.insert(0, "立昂微")

        # ── 2. 日期输入组 ──
        end_d = datetime.now().strftime("%Y-%m-%d")
        start_d = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")

        self._create_label(query_container, "开始:")
        self.entry_start = ttk.Entry(query_container, width=12, font=("Microsoft YaHei", 11))
        self.entry_start.insert(0, start_d)
        self.entry_start.pack(side=tk.LEFT, padx=(0, 5), ipady=2)

        self._create_label(query_container, "至:")
        self.entry_end = ttk.Entry(query_container, width=12, font=("Microsoft YaHei", 11))
        self.entry_end.insert(0, end_d)
        self.entry_end.pack(side=tk.LEFT, padx=(0, 15), ipady=2)

        # ── 3. 查询执行按钮 ──
        # 默认使用蓝色
        self.btn_search = self._create_button(query_container, "获取分析")
        
        # ── 4. 加入自选按钮 ──
        # 💡 [修改2] 使用琥珀黄主题色创建新按钮
        self.btn_add_watchlist = self._create_button(
            query_container, 
            "⭐ 加入自选", 
            bg_color="#F59E0B", 
            hover_color="#D97706",
            pad_left=10 # 距左侧按钮拉开一点间距
        )
        
        # ======================================================
        # 绑定事件
        # ======================================================
        self.btn_search.bind("<Button-1>", lambda e: self._handle_trigger())
        self.entry_code.bind("<Return>", lambda e: self._handle_trigger())
        
        # 💡 [修改3] 绑定加入自选的点击事件
        self.btn_add_watchlist.bind("<Button-1>", lambda e: self._handle_watchlist_trigger())

        # ======================================================
        # 右侧：实时时钟
        # ======================================================
        self.time_label = tk.Label(self, text="", font=("Microsoft YaHei", 11), bg=BG_PANEL, fg=COLOR_TEXT_SUB)
        self.time_label.pack(side=tk.RIGHT, padx=25)
        self._update_clock()

    def _create_label(self, parent, text):
        tk.Label(parent, text=text, font=("Microsoft YaHei", 12), bg=BG_PANEL, fg=COLOR_TEXT_MAIN).pack(side=tk.LEFT)

    # 💡 [修改4] 让按钮创建方法支持自定义颜色和外边距
    def _create_button(self, parent, text, bg_color="#3B82F6", hover_color="#2563EB", pad_left=0):
        btn = tk.Label(parent, text=text, font=("Microsoft YaHei", 11, "bold"), 
                       bg=bg_color, fg="#FFFFFF", padx=15, pady=6, cursor="hand2")
        btn.pack(side=tk.LEFT, padx=(pad_left, 0))
        
        # 闭包绑定颜色
        btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.config(bg=c))
        return btn

    def _handle_trigger(self):
        """智能解析用户输入的日期，支持年份补全"""
        code = self.entry_code.get().strip()
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        
        def format_date(date_str):
            if not date_str:
                return None
            if len(date_str) == 4 and date_str.isdigit():
                return f"{date_str}-01-01"
            return date_str

        start_val = format_date(start)
        end_val = format_date(end)
        
        if code:
            self.on_search(code, start_val, end_val)
            
    # 💡 [修改5] 触发加入自选的回调
    def _handle_watchlist_trigger(self):
        if self.on_add_watchlist:
            self.on_add_watchlist()

    def _update_clock(self):
        self.time_label.config(text=f"🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.after(1000, self._update_clock)