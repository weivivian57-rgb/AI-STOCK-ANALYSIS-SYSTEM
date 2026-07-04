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
    def __init__(self, parent, on_search_callback):
        super().__init__(parent, bg=BG_PANEL, height=70, bd=0)
        self.pack_propagate(False)
        self.on_search = on_search_callback

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

        # ── 2. 日期输入组 (替换掉 tkcalendar，拒绝崩溃) ──
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
        self.btn_search = self._create_button(query_container, "获取分析")
        
        # ======================================================
        # 绑定事件
        # ======================================================
        self.btn_search.bind("<Button-1>", lambda e: self._handle_trigger())
        self.entry_code.bind("<Return>", lambda e: self._handle_trigger())

        # ======================================================
        # 右侧：实时时钟
        # ======================================================
        self.time_label = tk.Label(self, text="", font=("Microsoft YaHei", 11), bg=BG_PANEL, fg=COLOR_TEXT_SUB)
        self.time_label.pack(side=tk.RIGHT, padx=25)
        self._update_clock()

    def _create_label(self, parent, text):
        tk.Label(parent, text=text, font=("Microsoft YaHei", 12), bg=BG_PANEL, fg=COLOR_TEXT_MAIN).pack(side=tk.LEFT)

    def _create_button(self, parent, text):
        btn = tk.Label(parent, text=text, font=("Microsoft YaHei", 11, "bold"), 
                       bg="#3B82F6", fg="#FFFFFF", padx=15, pady=6, cursor="hand2")
        btn.pack(side=tk.LEFT)
        btn.bind("<Enter>", lambda e: btn.config(bg="#2563EB"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3B82F6"))
        return btn

    def _handle_trigger(self):
        """智能解析用户输入的日期，支持年份补全"""
        code = self.entry_code.get().strip()
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        
        # 💡 智能补全逻辑
        def format_date(date_str):
            if not date_str:
                return None
            # 如果输入的是 "2022"，自动补全为 "2022-01-01"
            if len(date_str) == 4 and date_str.isdigit():
                return f"{date_str}-01-01"
            return date_str

        start_val = format_date(start)
        end_val = format_date(end)
        
        if code:
            self.on_search(code, start_val, end_val)
    def _update_clock(self):
        self.time_label.config(text=f"🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.after(1000, self._update_clock)