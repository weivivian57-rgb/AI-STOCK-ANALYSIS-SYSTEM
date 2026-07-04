"""
report_panel.py
AI 报告面板 - 仅负责渲染底部的智能分析文本
"""

import tkinter as tk
from tkinter import messagebox  # 💡 引入弹窗组件
from ui.styles import *

class ReportPanel(tk.Frame):
    def __init__(self, parent):
        # 移除原有的固定 width，让它在外部容器中自然拉伸
        super().__init__(parent, bg=BG_PANEL)

        # === 🤖 AI智能分析报告区 ===
        title_frame = tk.Frame(self, bg=BG_PANEL)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 标题文字靠左排列
        tk.Label(
            title_frame, 
            text="🤖 AI智能分析报告", 
            font=FONT_TITLE, 
            bg=BG_PANEL,
            fg=COLOR_TEXT_MAIN
        ).pack(side=tk.LEFT, padx=5, pady=5) # 💡 改为 side=tk.LEFT
        
        # 💡 [完美修复 Mac 灰底] 使用 tk.Label 模拟现代按钮
        # 💡 [颜色对齐] 使用与“获取分析”一致的蓝色主题
        self.btn_copy = tk.Label(
            title_frame,
            text="复制报告",
            font=(FONT_MAIN[0], 9), 
            bg="#3B82F6",          # 💡 更改为与“获取分析”一致的现代蓝
            fg="white",            # 纯白文字
            cursor="hand2",        # 鼠标放上去变成小手
            padx=10,
            pady=4,
            relief=tk.FLAT
        )
        self.btn_copy.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 绑定点击事件
        self.btn_copy.bind("<Button-1>", lambda e: self._copy_report_action())
        
        # 💡 悬停变色特效（同步改为深蓝色）
        self.btn_copy.bind("<Enter>", lambda e: self.btn_copy.config(bg="#2563EB"))
        self.btn_copy.bind("<Leave>", lambda e: self.btn_copy.config(bg="#3B82F6"))
        
        # 报告纯文本框 (去掉了旧版的指标卡片)
        self.text_report = tk.Text(
            self, 
            font=FONT_MAIN, 
            bg="#F8FAFC", 
            fg=COLOR_TEXT_MAIN, 
            relief=tk.FLAT, 
            bd=0,
    
            highlightthickness=0, 
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        # 撑满剩余的所有空间
        self.text_report.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.text_report.insert(tk.END, "请在上方输入股票代码并点击查询...")

    def update_data(self, stock, report_text):
        """只负责更新文本，不再处理那4个废弃的卡片"""
        self.text_report.delete(1.0, tk.END)
        self.text_report.insert(tk.END, report_text)

    # 💡 [新增] 复制按钮的具体执行逻辑
    def _copy_report_action(self):
        """将 AI 分析报告内容复制到剪贴板"""
        report_content = self.text_report.get(1.0, tk.END).strip()
        
        # 拦截没有数据时的无效点击
        if not report_content or report_content.startswith("请在上方输入股票代码"):
            messagebox.showwarning("提示", "当前没有可复制的分析报告数据。")
            return
            
        try:
            self.clipboard_clear()
            self.clipboard_append(report_content)
            self.update() # 确保在 Mac 上切换窗口时剪贴板数据不丢失
            messagebox.showinfo("成功", "✅ 报告内容已成功复制到剪贴板！可以直接粘贴 (Cmd+V)。")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {e}")