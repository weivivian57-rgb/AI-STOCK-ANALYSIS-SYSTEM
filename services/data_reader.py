"""
data_reader.py

股票数据读取模块

功能：
1. 在线获取股票历史数据
2. CSV文件读取（后续扩展）
3. 数据清洗
4. 返回Stock对象
"""

import pandas as pd
import yfinance as yf

from models.stock import Stock


class DataReader:
    """
    股票数据读取类
    """

    def __init__(self):
        pass

    def download_data(
        self,
        stock_code: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> Stock:
        """
        下载股票历史数据

        Parameters
        ----------
        stock_code : str
            股票代码，例如：
            AAPL
            TSLA
            NVDA

        period : str
            时间范围
            默认一年

        interval : str
            数据间隔
            默认一天

        Returns
        -------
        Stock
            股票对象
        """

        print(f"正在获取 {stock_code} 数据...")

        df = yf.download(
            tickers=stock_code,
            period=period,
            interval=interval,
            progress=False
        )

        if df.empty:
            raise ValueError(f"无法获取股票：{stock_code}")

        # 创建股票对象
        stock = Stock(
            code=stock_code,
            data=df
        )
        # 获取最新收盘价（兼容 yfinance 新旧版本）

        close_data = df["Close"]

        # 如果是新版 yfinance，会返回 DataFrame（MultiIndex）
        if isinstance(close_data, pd.DataFrame):
          latest_price = close_data.iloc[-1, 0]

        # 老版本返回 Series
        else:
          latest_price = close_data.iloc[-1]

        stock.latest_price = float(latest_price)

        print("数据获取成功！")

        return stock

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        数据清洗

        Parameters
        ----------
        df : DataFrame

        Returns
        -------
        DataFrame
        """

        df = df.dropna()

        df = df.sort_index()

        return df

    def load_csv(self, file_path: str) -> Stock:
        """
        读取CSV文件

        后续实现
        """

        df = pd.read_csv(file_path)

        stock = Stock(
            code="LOCAL",
            data=df
        )

        return stock