"""
sidebar.py
系统侧边栏组件 - 负责导航菜单的渲染与专业高亮事件分发 (纯平现代化重构版)
"""

import tkinter as tk
import os
from ui.styles import *

class Sidebar(tk.Frame):
    def __init__(self, parent, on_menu_click_callback):
        super().__init__(parent, bg="#F8FAFC", width=220) 
        self.pack_propagate(False)
        
        # --- 💡 加载本地图片 ---
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "assets", "logo_icon.png")
        try:
            self.logo_img = tk.PhotoImage(file=icon_path)
            self.logo_img = self.logo_img.subsample(2, 2)
        except Exception as e:
            print(f"⚠️ 无法加载 Logo 图片: {e}")
            self.logo_img = None

        self.on_menu_click = on_menu_click_callback
        self.buttons = {}
        self.current_active = "首页概览"

        # ==========================
        # 1. Logo 区域 (已修正：图标+文字)
        # ==========================
        logo_frame = tk.Frame(self, bg="#F8FAFC")
        logo_frame.pack(fill=tk.X, pady=(24, 24), padx=48)
        
        # 左侧图标
        if self.logo_img:
            tk.Label(logo_frame, image=self.logo_img, bg="#F8FAFC").pack(side=tk.LEFT, padx=(0, 5))
        else:
            tk.Label(logo_frame, text="📈", font=("Microsoft YaHei", 24), bg="#F8FAFC", fg=COLOR_PRIMARY).pack(side=tk.LEFT, padx=(0, 5))
            
        # 右侧文字 (已补回)
        text_container = tk.Frame(logo_frame, bg="#F8FAFC")
        text_container.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(text_container, text="股票智能", font=("Microsoft YaHei", 16, "bold"), bg="#F8FAFC", fg="#111827").pack(anchor="w")
        tk.Label(text_container, text="分析系统", font=("Microsoft YaHei", 16, "bold"), bg="#F8FAFC", fg="#111827").pack(anchor="w")

        # ==========================
        # 2. 导航菜单渲染
        # ==========================
        menus = ["🏠 首页概览", "🤖 AI智能分析", "🕒 历史记录", "⭐ 自选股票", "📝 意见反馈", "⚙️ 系统设置"]
        
        for i, menu in enumerate(menus):
            menu_key = menu.split(" ")[1]
            is_active = (i == 0)
            
            btn_border_container = tk.Frame(self, bg=COLOR_PRIMARY if is_active else "#E5E7EB", bd=1)
            btn_border_container.pack(fill=tk.X, padx=15, pady=4)
            
            btn = tk.Label(
                btn_border_container, 
                text=f"  {menu}", 
                font=("Microsoft YaHei", 14, "bold" if is_active else "normal"), 
                bg="#FFFFFF", 
                fg=COLOR_PRIMARY if is_active else "#475569",
                anchor="w", 
                padx=20, 
                pady=12, 
                cursor="hand2"
            )
            btn.pack(fill=tk.X, padx=1, pady=1)
            btn.bind("<Button-1>", lambda e, k=menu_key: self._handle_click(k))
            self._bind_hover_effects(btn, menu_key)
            self.buttons[menu_key] = (btn, btn_border_container)

        # ==========================
        # 3. 底部状态栏 (已补回数据引擎文字)
        # ==========================
        bottom_frame = tk.Frame(self, bg="#F8FAFC")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        tk.Label(bottom_frame, text="系统状态: 运行正常", font=("Microsoft YaHei", 10), bg="#F8FAFC", fg="#16A34A").pack(side=tk.TOP, anchor="w", padx=20, pady=1)
        tk.Label(bottom_frame, text="系统版本: v1.1.0", font=("Microsoft YaHei", 9), bg="#F8FAFC", fg="#94A3B8").pack(side=tk.TOP, anchor="w", padx=20, pady=1)
        tk.Label(bottom_frame, text="数据引擎: AkShare & yfinance", font=("Microsoft YaHei", 9), bg="#F8FAFC", fg="#94A3B8").pack(side=tk.TOP, anchor="w", padx=20, pady=1)

    def _bind_hover_effects(self, btn, menu_key):
        def on_enter(e):
            if self.current_active != menu_key: btn.config(bg="#F9FAFB")
        def on_leave(e):
            if self.current_active != menu_key: btn.config(bg="#FFFFFF")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _handle_click(self, menu_key: str):
        self.current_active = menu_key
        
        # 定义两种字体状态
        active_font = ("Microsoft YaHei", 14, "bold")   # 加粗
        normal_font = ("Microsoft YaHei", 14, "normal") # 普通
        
        for key, (btn, container) in self.buttons.items():
            if key == menu_key:
                # 💡 激活状态：蓝色 + 加粗
                btn.config(fg=COLOR_PRIMARY, bg="#FFFFFF", font=active_font)
                container.config(bg=COLOR_PRIMARY)
            else:
                # 💡 非激活状态：灰色 + 不加粗
                btn.config(fg="#475569", bg="#FFFFFF", font=normal_font)
                container.config(bg="#E5E7EB")
                
        self.on_menu_click(menu_key)