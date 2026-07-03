"""
main_window.py
系统主窗口控制器 - 负责全局布局调度与视图路由切换
"""

import tkinter as tk
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.placeholder_view import PlaceholderView
from ui.styles import BG_APP
from ui.history_panel import HistoryPanel
from ui.feedback_panel import FeedbackPanel


class MainWindow:
    """
    应用主窗口类（视图总控制器）
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI股票智能分析系统")
        
        # 窗口居中及分辨率自适应设置
        window_width = 1200
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.root.configure(bg=BG_APP)

        self.sub_views = {}
        self.current_view = None

        # 1. 实例化侧边栏 (直接挂载在 root 左侧)
        self.sidebar = Sidebar(self.root, on_menu_click_callback=self.switch_view)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # 2. 核心工作区容器 (挂载在右侧剩余空间)
        self.main_container = tk.Frame(self.root, bg=BG_APP)
        self.main_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # 3. 预加载首页
        self.sub_views["首页概览"] = Dashboard(self.main_container)
        self.sub_views["首页概览"].grid(row=0, column=0, sticky="nsew")
        
        self.current_view = self.sub_views["首页概览"]

    def switch_view(self, menu_key: str):
        if self.current_view == self.sub_views.get(menu_key):
            return

        if menu_key not in self.sub_views:
            # 💡 必须精确匹配菜单键名！
            if menu_key == "历史记录":
                self.sub_views[menu_key] = HistoryPanel(self.main_container)
            elif menu_key == "意见反馈": # 确保这里的字符串和你侧边栏里的 menu_key 完全一致
                self.sub_views[menu_key] = FeedbackPanel(self.main_container)
            else:
                self.sub_views[menu_key] = PlaceholderView(self.main_container, module_name=menu_key)
            
            self.sub_views[menu_key].grid(row=0, column=0, sticky="nsew")
        
        # ... 后续逻辑

        if menu_key == "历史记录":
            self.sub_views["历史记录"].refresh_data()

        view = self.sub_views[menu_key]
        view.tkraise()
        
        self.current_view = view

    def run(self):
        self.root.mainloop()