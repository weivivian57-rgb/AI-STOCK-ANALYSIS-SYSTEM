"""
stock_analyzer.py

股票技术指标分析模块
"""

import pandas as pd
from models.stock import Stock


class StockAnalyzer:
    """
    股票技术指标分析
    """

    def analyze(self, stock: Stock) -> Stock:
        def analyze(self, stock):
          print(f"DEBUG: 分析器收到的数据条数: {len(stock.data)}")
           # ... 原有代码 ...
        if stock.data.empty:
            raise ValueError("股票数据为空！")

        df = stock.data.copy()

        # ======================================================
        # 兼容新版 yfinance MultiIndex
        # ======================================================
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # ======================================================
        # MA
        # ======================================================
        df["MA5"] = df["Close"].rolling(window=5).mean()

        df["MA20"] = df["Close"].rolling(window=20).mean()

        df["MA60"] = df["Close"].rolling(window=60).mean()

        stock.ma5 = float(df["MA5"].iloc[-1])

        stock.ma20 = float(df["MA20"].iloc[-1])

        stock.ma60 = float(df["MA60"].iloc[-1])

        # ======================================================
        # MACD
        # ======================================================
        ema12 = df["Close"].ewm(span=12, adjust=False).mean()

        ema26 = df["Close"].ewm(span=26, adjust=False).mean()

        df["DIF"] = ema12 - ema26

        df["DEA"] = df["DIF"].ewm(span=9, adjust=False).mean()

        df["MACD"] = (df["DIF"] - df["DEA"]) * 2

        stock.dif = float(df["DIF"].iloc[-1])

        stock.dea = float(df["DEA"].iloc[-1])

        stock.macd = float(df["MACD"].iloc[-1])

        # ======================================================
        # RSI (14)
        # ======================================================
        delta = df["Close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()

        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        df["RSI"] = 100 - (100 / (1 + rs))

        stock.rsi = float(df["RSI"].iloc[-1])

        # ======================================================
        # 最新价格
        # ======================================================
        stock.latest_price = float(df["Close"].iloc[-1])

        # ======================================================
        # 保存计算结果
        # ======================================================
        stock.data = df

        return stock