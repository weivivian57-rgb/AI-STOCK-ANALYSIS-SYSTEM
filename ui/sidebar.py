"""
sidebar.py
系统侧边栏组件 - 负责导航菜单的渲染与事件分发
"""



import tkinter as tk
from ui.styles import *


class Sidebar(tk.Frame):
    """
    导航侧边栏类
    """

    # 💡 关键点：确保这里的参数名是 on_menu_click_callback
    def __init__(self, parent, on_menu_click_callback):
        super().__init__(parent, bg=BG_SIDEBAR, width=200)
        self.pack_propagate(False)  # 固定侧边栏宽度
        
        # 将传入的回调函数绑定到实例属性上
        self.on_menu_click = on_menu_click_callback
        self.buttons = {}  # 用于管理按钮状态

        # ... 以下代码保持不变 ...

        # ==========================
        # 1. Logo 区域
        # ==========================
        logo_frame = tk.Frame(self, bg=BG_SIDEBAR)
        logo_frame.pack(fill=tk.X, pady=20)
        tk.Label(logo_frame, text="📈 AI股票", font=FONT_H1, bg=BG_SIDEBAR, fg=COLOR_PRIMARY).pack()
        tk.Label(logo_frame, text="智能分析系统", font=FONT_MAIN, bg=BG_SIDEBAR, fg=COLOR_TEXT_SUB).pack()

        # ==========================
        # 2. 导航菜单渲染与事件绑定
        # ==========================
        menus = ["🏠 首页概览", "📊 股票查询", "📈 技术分析", "🤖 AI智能分析", 
                 "📉 图表分析", "🕒 历史记录", "⭐ 自选股票", "⚙️ 系统设置"]
        
        for i, menu in enumerate(menus):
            # 提取纯文本作为 Key (去除 Emoji 图标)
            menu_key = menu.split(" ")[1]
            
            # 初始化时，“首页概览”默认高亮
            btn_bg = COLOR_PRIMARY if i == 0 else BG_SIDEBAR
            btn_fg = "#FFFFFF" if i == 0 else COLOR_TEXT_MAIN
            
            # 使用 lambda 延迟绑定点击事件，并传入当前的菜单标识
            btn = tk.Button(
                self, 
                text=menu, 
                font=FONT_MAIN, 
                bg=btn_bg, 
                fg=btn_fg,
                relief=tk.FLAT, 
                anchor="w", 
                padx=30, 
                pady=10, 
                cursor="hand2",
                command=lambda k=menu_key: self._handle_click(k)
            )
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.buttons[menu_key] = btn

        # ==========================
        # 3. 底部状态栏
        # ==========================
        tk.Label(self, text="系统状态: 运行正常", font=("Microsoft YaHei", 9), 
                 bg=BG_SIDEBAR, fg=COLOR_SUCCESS).pack(side=tk.BOTTOM, pady=20)

    def _handle_click(self, menu_key: str):
        """
        处理菜单点击事件，切换高亮状态并通知主控制器
        """
        # 1. 刷新所有按钮的视觉状态（恢复默认排版）
        for key, btn in self.buttons.items():
            if key == menu_key:
                btn.config(bg=COLOR_PRIMARY, fg="#FFFFFF")
            else:
                btn.config(bg=BG_SIDEBAR, fg=COLOR_TEXT_MAIN)
                
        # 2. 触发主窗口的视图切换路由
        self.on_menu_click(menu_key)