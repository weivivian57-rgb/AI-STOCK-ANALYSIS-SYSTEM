"""
trend_predictor.py

股票趋势预测模块
使用 Linear Regression 预测未来股价
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from models.stock import Stock


class TrendPredictor:

    def __init__(self):
        self.model = LinearRegression()

    def predict(self, stock: Stock, future_days=5):
        """
        预测未来 future_days 天价格
        """

        if stock.data.empty:
            raise ValueError("股票数据为空！")

        df = stock.data.copy()

        # 兼容新版 yfinance
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        close = df["Close"].values

        # 创建训练数据
        x = np.arange(len(close)).reshape(-1, 1)
        y = close

        # 模型训练
        self.model.fit(x, y)

        # 预测未来
        future_x = np.arange(len(close), len(close) + future_days).reshape(-1, 1)

        future_price = self.model.predict(future_x)

        stock.prediction = future_price.tolist()

        return stock