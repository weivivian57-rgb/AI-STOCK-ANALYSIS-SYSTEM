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
        super().__init__(parent, bg="#FFFFFF") # 💡 统一使用白底，增强卡片高级感
        self.reader = DataReader()
        
        # 1. 顶部标题栏区域
        title_frame = tk.Frame(self, bg="#FFFFFF")
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(
            title_frame, 
            text="🕒 系统查询历史流水账单", 
            font=("Microsoft YaHei", 16, "bold"), # 对齐自选股标题字号
            bg="#FFFFFF", 
            fg="#111827"
        ).pack(side=tk.LEFT)
        
        # 💡 [修复 Mac 灰底] 使用 tk.Label 模拟现代清空按钮
        self.btn_clear = tk.Label(
            title_frame, 
            text="🗑️ 清空历史", 
            font=("Microsoft YaHei", 12),
            bg="#FEE2E2", 
            fg="#B91C1C", 
            cursor="hand2",
            padx=15,
            pady=6,
            relief=tk.FLAT
        )
        self.btn_clear.pack(side=tk.RIGHT)
        
        # 绑定按钮事件与特效
        self.btn_clear.bind("<Button-1>", lambda e: self._clear_all_history())
        self.btn_clear.bind("<Enter>", lambda e: self.btn_clear.config(bg="#FCA5A5"))
        self.btn_clear.bind("<Leave>", lambda e: self.btn_clear.config(bg="#FEE2E2"))
        
        # 2. 创建带滚动条的表格容器 (完全对齐自选股布局规范)
        self._create_scrollable_table()
        
        # 3. 渲染表头
        self._render_headers()
        
        # 4. 初始化加载真实数据
        self.refresh_data()

    def _create_scrollable_table(self):
        """创建可滚动的画布区域，用于承载自定义列表"""
        self.table_container = tk.Frame(self, bg="#FFFFFF", highlightbackground="#E5E7EB", highlightthickness=1)
        self.table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.canvas = tk.Canvas(self.table_container, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # 划分 4 列对应的权重分配
        for i in range(4):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

    def _render_headers(self):
        """渲染表头（灰色小字，完美对称自选股视觉效果）"""
        headers = ["查询时间", "股票代码与名称", "分析时股价", "货币单位"]
        header_bg = "#F9FAFB"
        
        header_frame = tk.Frame(self.scrollable_frame, bg=header_bg, height=40)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        header_frame.grid_propagate(False)
        
        for col, text in enumerate(headers):
            # 第一列靠左對齊，其他列居中
            anchor_pos = "w" if col == 0 else ""
            pad_x = 20 if col == 0 else 0
            
            lbl = tk.Label(
                self.scrollable_frame, 
                text=text, 
                font=("Microsoft YaHei", 12), 
                bg=header_bg, 
                fg="#6B7280"
            )
            lbl.grid(row=0, column=col, sticky=anchor_pos, padx=pad_x, pady=10)
            
        sep = tk.Frame(self.scrollable_frame, bg="#E5E7EB", height=1)
        sep.grid(row=1, column=0, columnspan=4, sticky="ew")

    def _clear_table_rows(self):
        """清空除静态表头外所有的旧渲染组件"""
        for slave in self.scrollable_frame.grid_slaves():
            info = slave.grid_info()
            if int(info.get("row", 0)) > 1:
                slave.destroy()

    def add_history_row(self, row_idx, timestamp, code_name, price_str, currency):
        """绘制单行流水历史数据"""
        bg_color = "#FFFFFF"
        grid_row = (row_idx * 2) + 2 
        
        # 1. 查询时间 (靠左，浅灰低调)
        tk.Label(
            self.scrollable_frame, 
            text=timestamp, 
            font=("Microsoft YaHei", 12), 
            bg=bg_color, 
            fg="#6B7280"
        ).grid(row=grid_row, column=0, sticky="w", padx=20, pady=12)
        
        # 2. 股票代码与名称 (沿用经典粗体)
        tk.Label(
            self.scrollable_frame, 
            text=code_name, 
            font=("Microsoft YaHei", 12, "bold"), 
            bg=bg_color, 
            fg="#111827"
        ).grid(row=grid_row, column=1)
        
        # 3. 分析时股价 (沿用经典粗体)
        tk.Label(
            self.scrollable_frame, 
            text=price_str, 
            font=("Microsoft YaHei", 12, "bold"), 
            bg=bg_color, 
            fg="#111827"
        ).grid(row=grid_row, column=2)
        
        # 4. 货币单位
        tk.Label(
            self.scrollable_frame, 
            text=currency, 
            font=("Microsoft YaHei", 12), 
            bg=bg_color, 
            fg="#4B5563"
        ).grid(row=grid_row, column=3)
        
        # 行底部分割线 (无缝串联现代极简主义)
        sep = tk.Frame(self.scrollable_frame, bg="#F3F4F6", height=1)
        sep.grid(row=grid_row+1, column=0, columnspan=4, sticky="ew")

    def _clear_all_history(self):
        """清空数据逻辑，确保强制刷新 UI"""
        if messagebox.askyesno("确认清空", "确定要删除所有历史记录吗？\n此操作不可恢复。"):
            if self.reader.clear_history():
                self.refresh_data() # 直接拉起全量重绘刷新
                messagebox.showinfo("成功", "所有历史记录已清理完毕。")
            else:
                messagebox.showerror("错误", "清理历史失败。")

    def refresh_data(self):
        """刷新并重新渲染表格数据"""
        # 1. 先把原有的行完全擦除
        self._clear_table_rows()
            
        # 2. 读取后端真实数据
        history_list = self.reader.load_history()
        
        # 💡 [空状态拦截判断] 如果没有历史流水记录
        if not history_list:
            empty_lbl = tk.Label(
                self.scrollable_frame,
                text="🕒 暂无系统查询历史流水记录",
                font=("Microsoft YaHei", 12),
                bg="#FFFFFF",
                fg="#9CA3AF"
            )
            empty_lbl.grid(row=2, column=0, columnspan=4, pady=80)
            
            self.scrollable_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return
            
        # 3. 倒序循环遍历真实流水
        for i, record in enumerate(reversed(history_list)):
            try:
                price_val = record.get('price', 0)
                price_str = f"{float(price_val):.2f}" if price_val else "--"
                
                # 调用重塑后的精美行渲染方法
                self.add_history_row(
                    row_idx=i,
                    timestamp=record.get("timestamp", "--"),
                    code_name=record.get("code", "--"),
                    price_str=price_str,
                    currency=record.get("currency", "--")
                )
            except Exception as e:
                print(f"[历史记录] 忽略损坏数据: {e}")
                continue
                
        # 4. 强制刷新画布的滚动边界范围
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))