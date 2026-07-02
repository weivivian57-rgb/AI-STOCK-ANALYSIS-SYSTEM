"""
chart_view.py

股票走势图
负责显示：
1. 历史收盘价
2. 未来预测价格
"""

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ui import styles


class ChartView(tk.Frame):
    """
    股票走势图组件
    """

    def __init__(self, master):

        super().__init__(
            master,
            bg=styles.CARD,
            bd=1,
            relief="solid"
        )

        self.create_widgets()

    def create_widgets(self):

        # ==========================
        # 标题
        # ==========================

        title = tk.Label(
            self,
            text="Stock Price Trend",
            font=styles.FONT_H2,
            bg=styles.CARD,
            fg=styles.TITLE
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        # ==========================
        # Matplotlib Figure
        # ==========================

        self.figure = Figure(
            figsize=(8, 4),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

        self.ax.set_title("Price Chart")

        self.ax.set_xlabel("Trading Days")

        self.ax.set_ylabel("Price ($)")

        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # =====================================================
    # 更新图表
    # =====================================================

    def update_chart(self, stock):
        """
        根据股票对象刷新图表
        """

        if stock.data.empty:
            return

        df = stock.data.copy()

        # 兼容新版 yfinance MultiIndex
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        close = df["Close"].tolist()

        self.ax.clear()

        # ==========================
        # 历史价格
        # ==========================

        self.ax.plot(
            range(len(close)),
            close,
            label="Historical Price",
            linewidth=2
        )

        # ==========================
        # 预测价格
        # ==========================

        if hasattr(stock, "prediction") and len(stock.prediction) > 0:

            start = len(close) - 1

            predict_x = list(
                range(start, start + len(stock.prediction) + 1)
            )

            predict_y = [close[-1]] + stock.prediction

            self.ax.plot(
                predict_x,
                predict_y,
                linestyle="--",
                linewidth=2,
                label="Prediction"
            )

        self.ax.set_title(stock.code)

        self.ax.set_xlabel("Trading Days")

        self.ax.set_ylabel("Price ($)")

        self.ax.grid(True)

        self.ax.legend()

        self.figure.tight_layout()

        self.canvas.draw()