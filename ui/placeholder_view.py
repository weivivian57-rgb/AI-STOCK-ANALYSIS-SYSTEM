"""
ui/placeholder_view.py
系统占位视图 - 为尚未开发的模块提供统一的反馈界面
"""

import tkinter as tk
import os

class PlaceholderView(tk.Frame):
    def __init__(self, parent, module_name):
        super().__init__(parent, bg="#F1F5F9")
        
        # 容器卡片
        card = tk.Frame(self, bg="#F1F5F9", bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=600, height=400)
        
        # 1. 加载本地图片
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "assets", "settings.png")
        
        self.icon_img = None
        if os.path.exists(icon_path):
            try:
                # 只加载一次
                self.icon_img = tk.PhotoImage(file=icon_path)
                
                self.icon_img = self.icon_img.subsample(2, 2)
            except Exception as e:
                print(f"⚠️ 图片加载错误: {e}")
        else:
            print(f"⚠️ 找不到路径: {icon_path}")
        
        # 2. 图片在上方 (居中)
        if self.icon_img:
            tk.Label(card, image=self.icon_img, bg="#F1F5F9").pack(pady=(60, 20))
        else:
            # 加载失败时的后备方案，确保模块界面依然可见
            tk.Label(card, text="⚙️", font=("Arial", 60), bg="#F1F5F9", fg="#9CA3AF").pack(pady=(60, 20))
        
        # 3. 标题 (居中)
        tk.Label(
            card, 
            text=f"【{module_name}】模块建设中", 
            font=("Microsoft YaHei", 18, "bold"), 
            bg="#F1F5F9", 
            fg="#111827"
        ).pack(pady=4)
        
        # 4. 提示文字 (居中)
        tk.Label(
            card, 
            text="该模块的已经在努力写代码啦，等我更新哟！", 
            font=("Microsoft YaHei", 12), 
            bg="#F1F5F9", 
            fg="#6B7280", 
            justify=tk.CENTER
        ).pack(pady=4)