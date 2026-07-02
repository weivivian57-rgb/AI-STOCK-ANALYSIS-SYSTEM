"""
stock_analyzer.py

股票技术指标分析模块
"""

import pandas as pd
from models.stock import Stock


class StockAnalyzer:
    """
    股票技术指标分析类
    """

    def analyze(self, stock: Stock):
        """
        计算股票技术指标
        """

        if stock.data.empty:
            raise ValueError("股票数据为空！")

        df = stock.data.copy()

        # 兼容新版 yfinance 的 MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        close = df["Close"]

        # ==========================
        # MA
        # ==========================
        stock.ma5 = close.rolling(5).mean().iloc[-1]
        stock.ma20 = close.rolling(20).mean().iloc[-1]
        stock.ma60 = close.rolling(60).mean().iloc[-1]

        # ==========================
        # MACD
        # ==========================
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()

        dif = ema12 - ema26
        dea = dif.ewm(span=9, adjust=False).mean()
        macd = (dif - dea) * 2

        stock.dif = float(dif.iloc[-1])
        stock.dea = float(dea.iloc[-1])
        stock.macd = float(macd.iloc[-1])

        # ==========================
        # RSI
        # ==========================
        delta = close.diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        stock.rsi = float(rsi.iloc[-1])

        return stock