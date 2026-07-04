import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from ui.styles import *
import matplotlib.image as mpimg  
import os
from matplotlib.font_manager import FontProperties

# 找到 Mac 系统中支持中文的字体
font_path = "/System/Library/Fonts/PingFang.ttc"  # 或者 "/Library/Fonts/Arial Unicode MS.ttf"
font_prop = FontProperties(fname=font_path, size=14)

class ChartView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PANEL)
        
        # 标题
        tk.Label(self, text="股票价格走势与指标图", font=FONT_TITLE, bg=BG_PANEL, anchor="w").pack(fill=tk.X, padx=15, pady=10)
        
        # Matplotlib Figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08, hspace=0.3)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def update_chart(self, stock):
        self.figure.clear()
    
    
        # 判断是否为空状态
        is_empty = (stock is None or not hasattr(stock, 'data') or stock.data is None or stock.data.empty)
        
        if is_empty:
            ax = self.figure.add_subplot(111)
            
            # 使用绝对路径定位
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            img_path = os.path.join(base_dir, "assets", "empty_state.png")
            
            print(f"[DEBUG] 图片路径检查: {img_path}")
            print(f"[DEBUG] 文件是否存在: {os.path.exists(img_path)}")

            if os.path.exists(img_path):
                try:
                    img = mpimg.imread(img_path)
                    # 缩小图片并居中
                    ax.imshow(img, extent=[-0.5, 0.5, -0.5, 0.5])
                    # 文字放在下方
                    ax.text(0, -0.5, '请输入股票名称或代码\n生成分析数据', 
                            ha='center', va='center', 
                            fontproperties=font_prop, color='#64748B')
                except Exception as e:
                    print(f"[ERROR] 图片渲染失败: {e}")
                    # 如果渲染出错， fallback 到仅显示文字
                    ax.text(0, 0, '请输入股票名称或代码\n(图片加载失败)', 
                            ha='center', va='center', fontproperties=font_prop, color='red')
            else:
                # 图片不存在时的标准显示
                ax.text(0, 0, '请输入股票名称或代码\n生成分析数据', 
                        ha='center', va='center', fontproperties=font_prop, color='#64748B')
            
            ax.set_xlim(-1, 1)
            ax.set_ylim(-1, 1)
            ax.axis('off')
            self.canvas.draw()
            return
        # 3. 如果有数据，走正常的绘图逻辑
        print("[调试] 正在渲染股票数据图表...")
        df = stock.data
        # ... 你的原有的绘图代码 (ax1, ax2, ax3 等)
        self.canvas.draw()

        close = df["Close"]
        
        # 1. 价格与均线 (上半部分)
        ax1 = self.figure.add_subplot(311)
        ax1.plot(df.index, close, label='Close', color='#333333', linewidth=1)
        if "MA5" in df.columns: ax1.plot(df.index, df["MA5"], label='MA5', color='#FFA500', linewidth=1)
        if "MA20" in df.columns: ax1.plot(df.index, df["MA20"], label='MA20', color='#1890FF', linewidth=1)
        ax1.legend(loc="upper left", frameon=False)
        ax1.grid(True, linestyle='--', alpha=0.5)

        # 2. 成交量 (中间)
        ax2 = self.figure.add_subplot(312, sharex=ax1)
        colors = [COLOR_DANGER if df['Close'].iloc[i] >= df['Open'].iloc[i] else COLOR_SUCCESS for i in range(len(df))]
        ax2.bar(df.index, df['Volume'], color=colors)
        ax2.set_ylabel("Volume")
        ax2.grid(True, linestyle='--', alpha=0.5)

        # 3. MACD (下半部分)
        ax3 = self.figure.add_subplot(313, sharex=ax1)
        if all(col in df.columns for col in ["DIF", "DEA", "MACD"]):
            ax3.plot(df.index, df["DIF"], label='DIF', color='#1890FF', linewidth=1)
            ax3.plot(df.index, df["DEA"], label='DEA', color='#FFA500', linewidth=1)
            macd_colors = [COLOR_DANGER if val > 0 else COLOR_SUCCESS for val in df["MACD"]]
            ax3.bar(df.index, df["MACD"], color=macd_colors)
        ax3.legend(loc="upper left", frameon=False)
        ax3.grid(True, linestyle='--', alpha=0.5)

        # ... (前面的 ax3 画图代码保持不变)
        ax3.legend(loc="upper left", frameon=False)
        ax3.grid(True, linestyle='--', alpha=0.5)

        # ======================================================
        # 💡 核心修复：在这里强行拉开三个图表的垂直间距
        # ======================================================
        # hspace=0.4 表示上下留出子图高度 40% 的空隙，你可以根据需要调整为 0.4 或 0.5
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08, hspace=0.4)

        # 渲染画布
        self.canvas.draw()