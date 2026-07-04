"""
history_panel.py
历史记录面板 - 负责展示查询历史与管理清理
"""
import tkinter as tk
from tkinter import ttk, messagebox
from services.data_reader import DataReader
from ui.styles import BG_PANEL, FONT_TITLE

class HistoryPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PANEL)
        self.reader = DataReader()
        
        # 1. 顶部标题栏区域
        title_frame = tk.Frame(self, bg="#FFFFFF", bd=1, relief=tk.SOLID, highlightbackground="#E2E8F0")
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(
            title_frame, 
            text="🕒 系统查询历史流水账单", 
            font=FONT_TITLE, 
            bg="#FFFFFF", 
            fg="#1E293B",
            padx=15,
            pady=10
        ).pack(side=tk.LEFT)
        
        # 💡 [清空按钮] - 注意这个 command 绑定
        self.btn_clear = tk.Button(
            title_frame, 
            text="🗑️ 清空历史", 
            font=("Microsoft YaHei", 10),
            bg="#FEE2E2", 
            fg="#B91C1C", 
            relief=tk.FLAT,
            cursor="hand2",
            command=self._clear_all_history  # 必须在方法定义之后绑定
        )
        self.btn_clear.pack(side=tk.RIGHT, padx=15)
        
        # 悬停特效
        self.btn_clear.bind("<Enter>", lambda e: self.btn_clear.config(bg="#FCA5A5"))
        self.btn_clear.bind("<Leave>", lambda e: self.btn_clear.config(bg="#FEE2E2"))
        
        # 2. 表格容器
        table_frame = tk.Frame(self, bg=BG_PANEL)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 3. 定义美观的表格 (Treeview)
        columns = ("时间", "股票代码", "最新收盘价", "货币")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("时间", text="查询时间")
        self.tree.column("时间", width=180, anchor="center")
        self.tree.heading("股票代码", text="股票代码")
        self.tree.column("股票代码", width=150, anchor="center")
        self.tree.heading("最新收盘价", text="分析时股价")
        self.tree.column("最新收盘价", width=120, anchor="center")
        self.tree.heading("货币", text="货币单位")
        self.tree.column("货币", width=100, anchor="center")
        
        # 4. 滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 5. 样式注入
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Microsoft YaHei", 11, "bold"), background="#3B82F6", foreground="white")
        style.configure("Treeview", font=("Microsoft YaHei", 11), rowheight=30, background="#F8FAFC", fieldbackground="#F8FAFC")
        
        # 初始化数据
        self.refresh_data()

    # 💡 关键：确保这个方法缩进正确，属于 HistoryPanel 类的方法
    def _clear_all_history(self):
        """清空数据逻辑，确保强制刷新 UI"""
        if messagebox.askyesno("确认清空", "确定要删除所有历史记录吗？\n此操作不可恢复。"):
            if self.reader.clear_history():
                # 1. 显式清空表格所有行
                x = self.tree.get_children()
                for item in x:
                    self.tree.delete(item)
                
                # 2. 强制更新 UI 布局
                self.tree.update_idletasks()
                
                messagebox.showinfo("成功", "所有历史记录已清理完毕。")
            else:
                messagebox.showerror("错误", "清理历史失败。")

    def refresh_data(self):
        """刷新并重新渲染表格数据"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        history_list = self.reader.load_history()
        
        for record in reversed(history_list):
            try:
                price_val = record.get('price', 0)
                price_str = f"{float(price_val):.2f}" if price_val else "--"
                
                self.tree.insert("", tk.END, values=(
                    record.get("timestamp", "--"),
                    record.get("code", "--"),
                    price_str,
                    record.get("currency", "--")
                ))
            except Exception as e:
                print(f"[历史记录] 忽略损坏数据: {e}")
                continue