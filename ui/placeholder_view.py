"""
placeholder_view.py
系统占位视图组件 - 用于展示尚未完全实现的功能模块
"""

import tkinter as tk
from ui.styles import *

class PlaceholderView(tk.Frame):
    """
    通用功能建设中占位面板
    """
    def __init__(self, parent, module_name="该功能"):
        super().__init__(parent, bg=BG_APP)
        
        # 使用一个居中的 Frame 来包裹内容
        content_frame = tk.Frame(self, bg=BG_PANEL, bd=1, relief=tk.SOLID)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=600, height=400)
        
        # 图标/Emoji 提示
        tk.Label(content_frame, text="🚧", font=("Arial", 64), bg=BG_PANEL).pack(pady=(50, 20))
        
        # 模块名称
        tk.Label(content_frame, text=f"【{module_name}】模块建设中", font=FONT_H1, bg=BG_PANEL, fg=COLOR_TEXT_MAIN).pack(pady=10)
        
        # 详细说明
        desc_text = (
            "该模块的核心业务逻辑已在底层的 services 层闭环。\n"
            "UI 界面工程师正在全力渲染中，敬请期待！\n\n"
            "您可以先前往【首页概览】体验核心功能。"
        )
        tk.Label(content_frame, text=desc_text, font=FONT_MAIN, bg=BG_PANEL, fg=COLOR_TEXT_SUB, justify=tk.CENTER).pack(pady=20)