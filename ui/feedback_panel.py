"""
feedback_panel.py
意见反馈面板 - 融合现代扁平化与数据驱动视图架构
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
import os

class FeedbackPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFFFFF") 
        self.feedback_list = []
        
        # 1. 顶部：输入区 (已提升为标准 16号 大标题规范)
        self._build_input_area()
        
        # 2. 底部：与自选股/历史记录完全一致的带表头数据流表格
        self._create_scrollable_table()
        
        # 3. 渲染静态表头
        self._render_headers()
        
        # 4. 初始化加载数据
        self.load_history()

    def _build_input_area(self):
        # 统一的大标题规范
        title_frame = tk.Frame(self, bg="#FFFFFF")
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        tk.Label(
            title_frame, 
            text="📝 您的宝贵意见", 
            font=("Microsoft YaHei", 14, "bold"), 
            bg="#FFFFFF", 
            fg="#343333"
        ).pack(side=tk.LEFT)
        
        # 输入框容器
        input_frame = tk.Frame(self, bg="#FFFFFF")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.text_area = tk.Text(
            input_frame, 
            height=4, 
            font=("Microsoft YaHei", 12), 
            bg="#FFFFFF",               
            fg="#111827",               
            insertbackground="#000000", 
            bd=1, 
            relief=tk.SOLID,
            highlightbackground="#FFFFFF",
            highlightcolor="#3981FF",
            highlightthickness=1,
            padx=10,
            pady=10
        )
        self.text_area.pack(fill=tk.X, pady=(0, 15))
        
        # 💡 [样式同步] 首页的现代蓝按钮，保持靠右对齐
        self.submit_btn = tk.Label(
            input_frame, 
            text="提交反馈", 
            font=("Microsoft YaHei", 11, "bold"),
            bg="#3B82F6", 
            fg="#FFFFFF", 
            cursor="hand2",
            padx=20,
            pady=8,
            relief=tk.FLAT
        )
        self.submit_btn.pack(side=tk.RIGHT) # 保持在右侧
        
        # 绑定事件与特效
        self.submit_btn.bind("<Button-1>", lambda e: self._submit_feedback())
        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn.config(bg="#2563EB"))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn.config(bg="#3B82F6"))

    def _create_scrollable_table(self):
        """建立与自选股票一模一样的 Canvas 容器架构"""
        table_title = tk.Frame(self, bg="#FFFFFF")
        table_title.pack(fill=tk.X, padx=20, pady=(10, 5))
        tk.Label(
            table_title, 
            text="📜 反馈历史记录", 
            font=("Microsoft YaHei", 14, "bold"), 
            bg="#FFFFFF",
            fg="#111827"
        ).pack(side=tk.LEFT)

        self.table_container = tk.Frame(self, bg="#FFFFFF", highlightbackground="#E5E7EB", highlightthickness=1)
        self.table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.canvas = tk.Canvas(self.table_container, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # 重点：分2列，时间固定宽度，内容自动拉伸
        self.scrollable_frame.grid_columnconfigure(0, weight=0, minsize=200) 
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

    def _render_headers(self):
        """💡 补齐缺失的表头！与系统其他页面完美对齐"""
        headers = ["提交时间", "反馈意见内容"]
        header_bg = "#F9FAFB"
        
        header_frame = tk.Frame(self.scrollable_frame, bg=header_bg, height=40)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        header_frame.grid_propagate(False)
        
        for col, text in enumerate(headers):
            pad_x = 20 if col == 0 else 0
            lbl = tk.Label(
                self.scrollable_frame, 
                text=text, 
                font=("Microsoft YaHei", 12), 
                bg=header_bg, 
                fg="#6B7280"
            )
            lbl.grid(row=0, column=col, sticky="w", padx=pad_x, pady=10)
            
        sep = tk.Frame(self.scrollable_frame, bg="#E5E7EB", height=1)
        sep.grid(row=1, column=0, columnspan=2, sticky="ew")

    def _clear_table_rows(self):
        """清空旧组件，避开表头（row 0, 1）"""
        for slave in self.scrollable_frame.grid_slaves():
            info = slave.grid_info()
            if int(info.get("row", 0)) > 1:
                slave.destroy()

    def load_history(self):
        self.feedback_list = []
        if os.path.exists("feedback.txt"):
            with open("feedback.txt", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(" - ", 1)
                    if len(parts) == 2:
                        self.feedback_list.append({"timestamp": parts[0], "content": parts[1]})
        self.render_all_data()

    def render_all_data(self):
        self._clear_table_rows()

        if not self.feedback_list:
            empty_lbl = tk.Label(
                self.scrollable_frame, 
                text="✨ 暂无反馈记录，期待听到您的声音",
                font=("Microsoft YaHei", 12), 
                bg="#FFFFFF", 
                fg="#9CA3AF"
            )
            empty_lbl.grid(row=2, column=0, columnspan=2, pady=60)
            
            self.scrollable_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return

        for i, item in enumerate(reversed(self.feedback_list)):
            self._add_feedback_row(i, item["timestamp"], item["content"])
            
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _add_feedback_row(self, row_idx, timestamp, content):
        bg_color = "#FFFFFF"
        grid_row = (row_idx * 2) + 2 
        
        # 时间戳 (浅灰)
        tk.Label(
            self.scrollable_frame, 
            text=timestamp, 
            font=("Microsoft YaHei", 14),
            bg=bg_color, 
            fg="#6B7280"
        ).grid(row=grid_row, column=0, sticky="nw", padx=20, pady=15)
        
        # 意见内容 (深色加粗，提升可读性)
        content_lbl = tk.Label(
            self.scrollable_frame, 
            text=content, 
            font=("Microsoft YaHei", 14, "bold"),
            bg=bg_color, 
            fg="#353535", 
            justify="left", 
            wraplength=700 
        )
        content_lbl.grid(row=grid_row, column=1, sticky="nw", pady=15)
        
        # 统一的底部分割线
        sep = tk.Frame(self.scrollable_frame, bg="#F3F4F6", height=1)
        sep.grid(row=grid_row+1, column=0, columnspan=2, sticky="ew")

    def _submit_feedback(self):
        content = self.text_area.get("1.0", tk.END).strip()
        
        if not content:
            messagebox.showwarning("提示", "请输入反馈内容")
            return
            
        safe_content = content.replace('\n', '  ')
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - {safe_content}\n")
        except Exception as e:
            messagebox.showerror("错误", f"保存反馈失败: {e}")
            return
            
        self.feedback_list.append({"timestamp": timestamp, "content": safe_content})
        self.render_all_data()
        
        self.text_area.delete("1.0", tk.END)
        messagebox.showinfo("成功", "感谢您的宝贵建议！")