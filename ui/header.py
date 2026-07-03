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

        # 查询按钮
        self.btn_search = tk.Button(self, text="查询分析", font=FONT_MAIN, bg=COLOR_PRIMARY, 
                                    fg="#FFFFFF", relief=tk.FLAT, padx=15, cursor="hand2",
                                    command=self._handle_search)
        self.btn_search.pack(side=tk.LEFT, padx=10, pady=15)

    def _handle_search(self):
        code = self.entry_code.get().strip().upper()
        if code:
            # 禁用按钮防止重复点击
            self.btn_search.config(state=tk.DISABLED, text="分析中...")
            self.on_search_callback(code)
            self.btn_search.config(state=tk.NORMAL, text="查询分析")