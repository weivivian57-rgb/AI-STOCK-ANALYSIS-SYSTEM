"""
main_window.py
系统主窗口控制器 - 负责全局布局调度与视图路由切换
"""

import tkinter as tk
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.placeholder_view import PlaceholderView
from ui.styles import BG_APP


class MainWindow:
    """
    应用主窗口类（视图总控制器）
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI股票智能分析系统")
        
        # ==========================
        # 窗口居中及分辨率自适应设置
        # ==========================
        window_width = 1200
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.root.configure(bg=BG_APP)

        # ==========================
        # 视图容器字典 (用于多页面解耦缓存)
        # ==========================
        self.sub_views = {}
        self.current_view = None

        # ==========================
        # 布局初始化
        # ==========================
        # 1. 实例化侧边栏
        self.sidebar = Sidebar(self.root, on_menu_click_callback=self.switch_view)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # 2. 实例化核心工作区容器
        self.main_container = tk.Frame(self.root, bg=BG_APP)
        self.main_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 💡 核心修复：配置容器的网格权重，保证子组件能撑满整个区域
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # 3. 预加载首页概览
        self.sub_views["首页概览"] = Dashboard(self.main_container)
        # 使用 grid 放到同一坐标格里，而不是 pack
        self.sub_views["首页概览"].grid(row=0, column=0, sticky="nsew")
        
        self.current_view = self.sub_views["首页概览"]

    def switch_view(self, menu_key: str):
        """
        中心视图路由导航引擎（采用层叠置顶策略）
        """
        # 1. 避免重复切换同一个页面导致闪烁
        if self.current_view == self.sub_views.get(menu_key):
            return

        # 2. 如果视图还未被创建过（首次点击），则实例化它
        if menu_key not in self.sub_views:
            self.sub_views[menu_key] = PlaceholderView(self.main_container, module_name=menu_key)
            # 新视图也放在完全相同的位置 (row=0, column=0)
            self.sub_views[menu_key].grid(row=0, column=0, sticky="nsew")

        # 3. 💡 核心修复：不删除旧视图，而是直接把需要的视图“置顶”显示
        view = self.sub_views[menu_key]
        view.tkraise()
        
        # 更新当前视图指针
        self.current_view = view

    def run(self):
        """
        启动 Tkinter 消息主循环
        """
        self.root.mainloop()