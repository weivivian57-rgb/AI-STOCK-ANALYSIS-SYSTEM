"""
sidebar.py
系统侧边栏组件 - 负责导航菜单的渲染与专业高亮事件分发
"""

import tkinter as tk
from ui.styles import *


class Sidebar(tk.Frame):
    """
    导航侧边栏类
    """

    def __init__(self, parent, on_menu_click_callback):
        super().__init__(parent, bg=BG_SIDEBAR, width=200)
        self.pack_propagate(False)  # 固定侧边栏宽度
        
        self.on_menu_click = on_menu_click_callback
        self.buttons = {}  # 用于管理按钮状态

        # ==========================
        # 1. Logo 区域
        # ==========================
        logo_frame = tk.Frame(self, bg=BG_SIDEBAR)
        logo_frame.pack(fill=tk.X, pady=20)
        tk.Label(logo_frame, text="📈 AI股票", font=FONT_H1, bg=BG_SIDEBAR, fg=COLOR_PRIMARY).pack()
        tk.Label(logo_frame, text="智能分析系统", font=FONT_MAIN, bg=BG_SIDEBAR, fg=COLOR_TEXT_SUB).pack()

        # ==========================
        # 2. 导航菜单渲染
        # ==========================
        menus = ["🏠 首页概览", "📊 股票查询", "📈 技术分析", "🤖 AI智能分析", 
                 "📉 图表分析", "🕒 历史记录", "⭐ 自选股票", "⚙️ 系统设置"]
        
        for i, menu in enumerate(menus):
            menu_key = menu.split(" ")[1]
            
            # 💡 初始状态样式微调：默认状态下所有按钮背景均为纯白
            # 初始化时，“首页概览”文字高亮为蓝色，且激活边框
            if i == 0:
                btn_fg = COLOR_PRIMARY
                bd_size = 1
                bd_color = COLOR_PRIMARY
            else:
                btn_fg = COLOR_TEXT_MAIN
                bd_size = 0
                bd_color = BG_SIDEBAR
            
            # 创建一个紧包按钮的 Frame，用于模拟边框高亮效果
            btn_border_container = tk.Frame(self, bg=bd_color, bd=bd_size)
            btn_border_container.pack(fill=tk.X, padx=10, pady=2)
            
            btn = tk.Button(
                btn_border_container, 
                text=menu, 
                font=FONT_MAIN, 
                bg=BG_SIDEBAR,          # 💡 背景统一为纯白
                fg=btn_fg,             # 💡 选中文字为蓝色
                relief=tk.FLAT, 
                anchor="w", 
                padx=30, 
                pady=10, 
                cursor="hand2",
                command=lambda k=menu_key: self._handle_click(k)
            )
            btn.pack(fill=tk.X, padx=1, pady=1)
            
            # 将按钮和它的外层容器Frame一起缓存，方便动态修改边框颜色
            self.buttons[menu_key] = (btn, btn_border_container)

        # ==========================
        # 3. 底部状态栏
        # ==========================
        tk.Label(self, text="系统状态: 运行正常", font=("Microsoft YaHei", 9), 
                 bg=BG_SIDEBAR, fg=COLOR_SUCCESS).pack(side=tk.BOTTOM, pady=20)

    def _handle_click(self, menu_key: str):
        """
        处理菜单点击事件，重置其他按钮，并将当前点击的菜单文字变蓝、外框高亮
        """
        # 🔄 遍历刷新所有按钮的视觉状态
        for key, (btn, container) in self.buttons.items():
            if key == menu_key:
                # 💡 选中状态：文字变蓝，容器 Frame 变蓝（显示出边框线）
                btn.config(fg=COLOR_PRIMARY)
                container.config(bg=COLOR_PRIMARY, bd=1)
            else:
                # 💡 常规状态：文字恢复暗灰，容器 Frame 隐藏（变回白色背景）
                btn.config(fg=COLOR_TEXT_MAIN)
                container.config(bg=BG_SIDEBAR, bd=0)
                
        # 触发中心路由视图切换
        self.on_menu_click(menu_key)