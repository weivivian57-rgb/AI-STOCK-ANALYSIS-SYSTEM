import tkinter as tk
from tkinter import ttk

class WatchlistPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFFFFF")
        
        # 💡 [数据驱动核心]：所有的自选股票数据统一由这个列表统一管理
        self.stocks_list = []
         
        
        # 1. 顶部标题区域
        title_frame = tk.Frame(self, bg="#FFFFFF")
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        tk.Label(title_frame, text="⭐ 自选股票", font=("Microsoft YaHei", 16, "bold"), bg="#FFFFFF", fg="#111827").pack(side=tk.LEFT)
        
        # 2. 创建带滚动条的表格容器
        self._create_scrollable_table()
        
        # 3. 渲染静态表头
        self._render_headers()
        
        # 4. 💡 全量渲染初始数据
        self.render_all_data()

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
        
        for i in range(7):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

    def _render_headers(self):
        """渲染表头（灰色小字，带排序箭头）"""
        headers = ["全部 ∨", "当前价 ↕", "涨跌幅 ↕", "成交量 ↕", "总市值 ↕", "年初至今 ↕", "操作"]
        header_bg = "#F9FAFB"
        
        header_frame = tk.Frame(self.scrollable_frame, bg=header_bg, height=40)
        header_frame.grid(row=0, column=0, columnspan=7, sticky="nsew")
        header_frame.grid_propagate(False)
        
        for col, text in enumerate(headers):
            anchor_pos = "w" if col == 0 else ("e" if col == 6 else "")
            pad_x = 20 if col == 0 else (20 if col == 6 else 0)
            
            lbl = tk.Label(
                self.scrollable_frame, 
                text=text, 
                font=("Microsoft YaHei", 12), 
                bg=header_bg, 
                fg="#6B7280"
            )
            lbl.grid(row=0, column=col, sticky=anchor_pos, padx=pad_x, pady=10)
            
        sep = tk.Frame(self.scrollable_frame, bg="#E5E7EB", height=1)
        sep.grid(row=1, column=0, columnspan=7, sticky="ew")

    def _clear_table_rows(self):
        """清空除静态表头（row 0 和 row 1）之外的所有渲染组件"""
        for slave in self.scrollable_frame.grid_slaves():
            info = slave.grid_info()
            if int(info.get("row", 0)) > 1:
                slave.destroy()

    def render_all_data(self):
        """💡 根据最新的 stocks_list 数据源进行重绘"""
        self._clear_table_rows()
        
        # 💡 [新增UI打磨]：如果没有数据，展示一句温和的空状态提示
        if not self.stocks_list:
            empty_lbl = tk.Label(
                self.scrollable_frame,
                text="暂无自选股票，请前往【首页概览】搜索并添加 ⭐",
                font=("Microsoft YaHei", 12),
                bg="#FFFFFF",
                fg="#9CA3AF" # 使用优雅的浅灰色
            )
            # 跨越 7 列居中显示，上下留出呼吸感间距
            empty_lbl.grid(row=2, column=0, columnspan=7, pady=80)
            
            # 刷新画布范围并终止下面的渲染流程
            self.scrollable_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return
        
        # 如果有数据，则正常循环渲染每一行
        for i, item in enumerate(self.stocks_list):
            self.add_stock_row(
                row_idx=i,
                name=item["name"],
                code=item["code"],
                price=item["price"],
                change_val=item["change_val"],
                change_pct=item["change_pct"],
                vol=item["vol"],
                cap=item["cap"],
                ytd_pct=item["ytd_pct"]
            )
            
        # 动态刷新滚动范围
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        # 动态刷新滚动范围
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_stock_row(self, row_idx, name, code, price, change_val, change_pct, vol, cap, ytd_pct):
        """渲染单行股票数据"""
        bg_color = "#FFFFFF"
        is_up = float(change_pct.replace('%', '')) > 0
        color_trend = "#DC2626" if is_up else "#16A34A"
        
        grid_row = (row_idx * 2) + 2 
        
        # 1. 股票名称与代码
        name_frame = tk.Frame(self.scrollable_frame, bg=bg_color)
        name_frame.grid(row=grid_row, column=0, sticky="w", padx=20, pady=12)
        tk.Label(name_frame, text=name, font=("Microsoft YaHei", 12, "bold"), bg=bg_color, fg="#111827").pack(anchor="w")
        tk.Label(name_frame, text=code, font=("Microsoft YaHei", 12), bg=bg_color, fg="#9CA3AF").pack(anchor="w", pady=(2, 0))
        
        # 2. 当前价
        tk.Label(self.scrollable_frame, text=price, font=("Microsoft YaHei", 12, "bold"), bg=bg_color, fg="#111827").grid(row=grid_row, column=1)
        
        # 3. 涨跌幅
        change_text = f"{change_val} ({change_pct})"
        tk.Label(self.scrollable_frame, text=change_text, font=("Microsoft YaHei", 12, "bold"), bg=bg_color, fg=color_trend).grid(row=grid_row, column=2)
        
        # 4. 成交量
        tk.Label(self.scrollable_frame, text=vol, font=("Microsoft YaHei", 12, "bold"), bg=bg_color, fg="#111827").grid(row=grid_row, column=3)
        
        # 5. 总市值
        tk.Label(self.scrollable_frame, text=cap, font=("Microsoft YaHei", 12, "bold"), bg=bg_color, fg="#111827").grid(row=grid_row, column=4)
        
        # 6. 年初至今
        tk.Label(self.scrollable_frame, text=ytd_pct, font=("Microsoft YaHei", 12, "bold"), bg=bg_color, fg=color_trend).grid(row=grid_row, column=5)
        
        # 7. 💡 操作图标区域（已剔除无效的铃铛和省略号）
        action_frame = tk.Frame(self.scrollable_frame, bg=bg_color)
        action_frame.grid(row=grid_row, column=6, sticky="e", padx=20)
        
        btn_del = tk.Label(action_frame, text="🗑️", font=("Microsoft YaHei", 12), bg=bg_color, fg="#EF4444", cursor="hand2")
        btn_del.pack(side="left", padx=4)
        btn_del.bind("<Enter>", lambda e: btn_del.config(fg="#DC2626")) 
        btn_del.bind("<Leave>", lambda e: btn_del.config(fg="#EF4444"))
        btn_del.bind("<Button-1>", lambda e, idx=row_idx: self._delete_stock_by_index(idx))
        
        # 行底部分割线
        sep = tk.Frame(self.scrollable_frame, bg="#F3F4F6", height=1)
        sep.grid(row=grid_row+1, column=0, columnspan=7, sticky="ew")

    def _delete_stock_by_index(self, index):
        """💡 根据索引将对应股票移出数据源并重绘列表"""
        from tkinter import messagebox
        target_name = self.stocks_list[index]["name"]
        
        if messagebox.askyesno("确认移除", f"确定要将 【{target_name}】 从自选股票列表中移除吗？"):
            self.stocks_list.pop(index) # 从核心数据列表删除
            self.render_all_data()      # 触发无缝重绘

    def add_dynamic_stock(self, stock):
        """接收来自 Dashboard 的真实 stock 对象，转化为标准字典并渲染"""
        from tkinter import messagebox
        name = getattr(stock, 'name', '未知股票')
        code = getattr(stock, 'yf_code', getattr(stock, 'code', '未知代码'))
        
        # 💡 [智能去重检测]：如果自选列表里已经有了，拦截并提示，不再重复添加
        if any(item["code"] == code for item in self.stocks_list):
            messagebox.showinfo("提示", f"🎬 股票 {name} ({code}) 已经在您的自选列表中。")
            return
            
        price = "0.00"
        if hasattr(stock, 'latest_price') and stock.latest_price is not None:
            price = f"{stock.latest_price:.2f}"
        elif hasattr(stock, 'data') and stock.data is not None and not stock.data.empty:
            price = f"{stock.data['Close'].iloc[-1]:.2f}"
            
        # 构建标准数据模型字典
        new_item = {
            "name": name,
            "code": code,
            "price": price,
            "change_val": "+0.55",
            "change_pct": "+0.85%",
            "vol": "50.12万手",
            "cap": "520.00亿",
            "ytd_pct": "+12.40%"
        }
        
        self.stocks_list.append(new_item) # 追加至数据源
        self.render_all_data()            # 触发全量重绘