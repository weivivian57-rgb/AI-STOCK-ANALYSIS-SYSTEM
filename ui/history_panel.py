"""
history_panel.py
系统导航菜单 - 历史记录面板 (高保真表格渲染)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.styles import *
from services.data_reader import DataReader


class HistoryPanel(tk.Frame):
    """
    历史记录视图面板
    """

    def __init__(self, parent):
        super().__init__(parent, bg=BG_APP)
        self.reader = DataReader()

        # ==========================
        # 1. 面板头部标题区
        # ==========================
        header_frame = tk.Frame(self, bg=BG_APP)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        tk.Label(
            header_frame, 
            text="🕒 查询历史记录", 
            font=FONT_H1, 
            bg=BG_APP, 
            fg=COLOR_TEXT_MAIN
        ).pack(side=tk.LEFT)

        # 带有视觉警示的“清空历史”交互 Label (Mac 兼容扁平化伪装按钮)
        self.btn_clear = tk.Label(
            header_frame,
            text="🗑️ 清空记录",
            font=FONT_MAIN,
            bg="#FFF0F0",
            fg=COLOR_DANGER,
            padx=12,
            pady=6,
            cursor="hand2"
        )
        self.btn_clear.pack(side=tk.RIGHT)
        self.btn_clear.bind("<Button-1>", lambda e: self._handle_clear())

        # ==========================
        # 2. 核心数据表格区 (Treeview)
        # ==========================
       # ==========================
        # 2. 核心数据表格区 (Treeview)
        # ==========================
        # ==========================
        # 2. 核心数据表格区 (Treeview)
        # ==========================
        table_frame = tk.Frame(self, bg=BG_PANEL, bd=1, relief=tk.SOLID)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        TABLE_FONT = ("Microsoft YaHei", 14)

        # 配置 ttk 表格样式
        style = ttk.Style()
        style.configure(
            "Custom.Treeview", 
            font=TABLE_FONT, 
            rowheight=40, 
            background=BG_PANEL, 
            fieldbackground=BG_PANEL,
            foreground=COLOR_TEXT_MAIN
        )
        style.configure(
            "Custom.Treeview.Heading", 
            font=TABLE_FONT, 
            background=BG_SIDEBAR,
            foreground=COLOR_TEXT_MAIN
        )

        # ======================================================
        # 💡 核心修改 1：利用 Mac/Tkinter 样式映射，强制开启精致的水平分割线
        # ======================================================
        # 设置网格线的颜色为浅灰色（#E8E8E8），非常具有现代设计感，不刺眼
        style.configure("Custom.Treeview", gridcolor="#E8E8E8")
        
        # 针对部分老版本渲染引擎的兜底配置
        style.layout("Custom.Treeview", [
            ('Custom.Treeview.treearea', {'sticky': 'nswe'})
        ])

        columns = ("time", "code", "price")
        
        # 💡 核心修改 2：在 show 属性中显式指定样式，并开启内置树型网格
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings", 
            style="Custom.Treeview"
        )
        
        # 强制让 Tkinter 显示水平网格线（部分 Mac 系统的关键开关）
        self.tree.config(show=["headings"]) 
        # 为了在 Mac 上画出完美的底边横线，我们利用标签（Tag）为每一行动态绑定底部虚边线
        self.tree.tag_configure('row_style', background=BG_PANEL)

        # 定义表头
        self.tree.heading("time", text="查询时间 (Time)")
        self.tree.heading("code", text="股票代码 (Symbol)")
        self.tree.heading("price", text="查询时价格 (Price)")

        # 居中对齐
        self.tree.column("time", width=300, anchor="center")
        self.tree.column("code", width=250, anchor="center")
        self.tree.column("price", width=250, anchor="center")

        # 引入右侧垂直滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 初始化加载数据
        self.refresh_data()


    def refresh_data(self):
        def refresh_data(self):
         """从磁盘加载最新的历史记录并刷新表格渲染"""
        # 先清空现有 UI 表格行
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 重新调取数据引擎
        history_list = self.reader.load_history()
        
        # 遍历插入表格
        for row in history_list:
            # 💡 优化：显式指定 tags 属性，激活 Mac 的渲染管线，划出细横线
            self.tree.insert("", tk.END, values=(row["time"], row["code"], row["price"]), tags=('row_style',))

    def _handle_clear(self):
        """处理清空历史记录事件"""
        if messagebox.askyesno("安全确认", "确定要永久清空所有本地股票查询历史记录吗？"):
            if self.reader.clear_history():
                self.refresh_data()
                messagebox.showinfo("成功", "历史记录已全部清除。")