import tkinter as tk
from tkinter import messagebox
from ui.styles import BG_PANEL, COLOR_PRIMARY, COLOR_TEXT_MAIN

class FeedbackPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PANEL)
        
        # 1. 顶部输入区
        input_frame = tk.Frame(self, bg=BG_PANEL, pady=20)
        input_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(input_frame, text="您的宝贵意见：", font=("Microsoft YaHei", 14), bg=BG_PANEL).pack(anchor="w")
        self.text_area = tk.Text(input_frame, height=5, font=("Microsoft YaHei", 14), bd=1, relief=tk.SOLID)
        self.text_area.pack(fill=tk.X, pady=10)
        
        # 1. 创建按钮（暂时不传 command）
        self.submit_btn = tk.Button(input_frame, text="提交反馈", bg="#E5E7EB", fg="black", relief=tk.FLAT, padx=20)
        self.submit_btn.pack(anchor="e")
        
        # 2. 显式绑定：这样写法几乎不会失效
        self.submit_btn.bind("<Button-1>", lambda event: self._submit_feedback())
        # 2. 底部列表区
        tk.Label(self, text="反馈历史：", font=("Microsoft YaHei", 14), bg=BG_PANEL).pack(anchor="w", padx=20)
        # 将原有 Listbox 替换为固定高度，防止界面布局干扰
        self.list_box = tk.Listbox(self, font=("Microsoft YaHei", 14), bd=1, relief=tk.SOLID, height=10)
        self.list_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def _submit_feedback(self):
        def _submit_feedback(self):
            print("DEBUG: 提交按钮被点击了！") # 如果点击按钮终端不打印，说明按钮根本没绑定上
            content = self.text_area.get("1.0", tk.END).strip()
        # ...
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("提示", "请输入反馈内容")
            return
        
        # 💡 核心代码：在此处写入文件
        # 这样即使程序关闭，你的反馈也不会丢失
        import time # 确保顶部导入了 time 模块
        with open("feedback.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {content}\n")
        
        # 展示在列表中
        self.list_box.insert(tk.END, f"• {content}")
        
        # 清空输入框
        self.text_area.delete("1.0", tk.END)
        messagebox.showinfo("成功", "感谢您的反馈！")