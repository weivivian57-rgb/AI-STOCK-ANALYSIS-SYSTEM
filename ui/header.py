"""
header.py
优化版：原生输入交互 + 极致响应性能 + 现代占位符设计
"""

import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta
from ui.styles import BG_PANEL, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_SUB

class Header(tk.Frame):
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

        # ── 1. 股票代码输入 (全新重构：400px宽度 + 占位符 + 焦点边框) ──
        self.placeholder_text = "请输入股票名称或代码"
        
        # width=30 约等同于 400px 宽度
        self.entry_code = tk.Entry(
            query_container, 
            font=("Microsoft YaHei", 14), 
            bg="#FFFFFF",
            fg="#9CA3AF",                  # 初始灰色字（占位符颜色）
            bd=0, 
            relief=tk.FLAT,
            highlightbackground="#DCDCDC", # 默认浅灰边框
            highlightcolor="#3480FB",      # 获得焦点时的现代科技蓝边框
            highlightthickness=1,
            width=30
        )
        self.entry_code.pack(side=tk.LEFT, padx=(0, 15), ipady=5) # ipady增加纵向呼吸感
        self.entry_code.insert(0, self.placeholder_text)

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
        self.btn_search = self._create_button(query_container, "获取分析")
        
        # ── 4. 加入自选按钮 (琥珀黄主题色) ──
        self.btn_add_watchlist = self._create_button(
            query_container, 
            "⭐ 加入自选", 
            bg_color="#F59E0B", 
            hover_color="#D97706",
            pad_left=10 
        )
        
        # ======================================================
        # 绑定事件
        # ======================================================
        self.btn_search.bind("<Button-1>", lambda e: self._handle_trigger())
        self.entry_code.bind("<Return>", lambda e: self._handle_trigger())
        
        # 💡 绑定焦点事件，完美模拟现代化 Placeholder 交互
        self.entry_code.bind("<FocusIn>", self._on_focus_in)
        self.entry_code.bind("<FocusOut>", self._on_focus_out)
        
        # 绑定加入自选的点击事件
        self.btn_add_watchlist.bind("<Button-1>", lambda e: self._handle_watchlist_trigger())

        # ======================================================
        # 右侧：实时时钟
        # ======================================================
        self.time_label = tk.Label(self, text="", font=("Microsoft YaHei", 11), bg=BG_PANEL, fg=COLOR_TEXT_SUB)
        self.time_label.pack(side=tk.RIGHT, padx=25)
        self._update_clock()

    def _create_label(self, parent, text):
        tk.Label(parent, text=text, font=("Microsoft YaHei", 12), bg=BG_PANEL, fg=COLOR_TEXT_MAIN).pack(side=tk.LEFT)

    def _create_button(self, parent, text, bg_color="#3B82F6", hover_color="#2563EB", pad_left=0):
        btn = tk.Label(parent, text=text, font=("Microsoft YaHei", 12, "bold"), 
                       bg=bg_color, fg="#FFFFFF", padx=15, pady=6, cursor="hand2")
        btn.pack(side=tk.LEFT, padx=(pad_left, 0))
        
        # 闭包绑定颜色
        btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.config(bg=c))
        return btn

    # ======================================================
    # 交互控制逻辑
    # ======================================================
    def _on_focus_in(self, event):
        """当用户点击输入框、光标闪烁（获得焦点）时触发"""
        if self.entry_code.get() == self.placeholder_text:
            self.entry_code.delete(0, tk.END)
            self.entry_code.config(fg="#111827") # 文字切回标准的优雅深黑色

    def _on_focus_out(self, event):
        """当用户点击别处、光标离开（失去焦点）时触发"""
        if not self.entry_code.get().strip():
            self.entry_code.insert(0, self.placeholder_text)
            self.entry_code.config(fg="#9CA3AF") # 文字切回低调的提示浅灰色

    def _handle_trigger(self):
        """智能解析用户输入的日期，支持年份补全"""
        code = self.entry_code.get().strip()
        
        # 💡 [关键拦截] 防止把占位符当成股票代码传给后端
        if code == self.placeholder_text or not code:
            from tkinter import messagebox
            messagebox.showinfo("提示", "请输入有效的股票名称或代码")
            return
            
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
        
        self.on_search(code, start_val, end_val)
            
    def _handle_watchlist_trigger(self):
        if self.on_add_watchlist:
            self.on_add_watchlist()

    def _update_clock(self):
        self.time_label.config(text=f"🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.after(1000, self._update_clock)