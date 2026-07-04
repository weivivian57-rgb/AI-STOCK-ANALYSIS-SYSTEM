"""
history_panel.py
历史记录面板 - 负责展示用户的查询历史
"""
import tkinter as tk
from tkinter import ttk
from services.data_reader import DataReader
from ui.styles import BG_PANEL

class HistoryPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PANEL)
        self.reader = DataReader()
        
        # 1. 顶部标题
        title_frame = tk.Frame(self, bg="#FFFFFF", bd=1, relief=tk.SOLID, highlightbackground="#E2E8F0")
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(
            title_frame, 
            text="🕒 系统查询历史流水账单", 
            font=("Microsoft YaHei", 14, "bold"), 
            bg="#FFFFFF", 
            fg="#1E293B",
            padx=15,
            pady=10
        ).pack(side=tk.LEFT)
        
        # 2. 表格容器
        table_frame = tk.Frame(self, bg=BG_PANEL)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 3. 定义美观的表格 (Treeview)
        columns = ("时间", "股票代码", "最新收盘价", "货币")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # 定义列宽和对齐方式
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
        
        # 5. 注入现代 Mac UI 样式
        style = ttk.Style()
        style.theme_use("default")
        # 表头样式：蓝底白字
        style.configure("Treeview.Heading", font=("Microsoft YaHei", 11, "bold"), background="#3B82F6", foreground="white")
        # 表格内容样式：斑马线与行高
        style.configure("Treeview", font=("Microsoft YaHei", 11), rowheight=30, background="#F8FAFC", fieldbackground="#F8FAFC")
        
        # 初始化拉取数据
        self.refresh_data()

    def refresh_data(self):
        """刷新并重新渲染表格数据"""
        # 第一步：清空现有表格残留
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 第二步：通过 DataReader 重新读取 JSON
        history_list = self.reader.load_history()
        
        # 第三步：倒序插入（让刚查询的最新的记录排在最上面）
        for record in reversed(history_list):
            try:
                # 安全解析浮点数价格
                price_val = record.get('price', 0)
                price_str = f"{float(price_val):.2f}" if price_val else "--"
                
                self.tree.insert("", tk.END, values=(
                    record.get("timestamp", "--"),
                    record.get("code", "--"),
                    price_str,
                    record.get("currency", "--")
                ))
            except Exception as e:
                print(f"[历史记录] 忽略一条格式损坏的数据: {e}")
                continue