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
import akshare as ak  # 引入 akshare
from models.stock import Stock

class DataReader:
    def __init__(self):
        # 初始化一个空的映射字典
        self.stock_map = {}
        # 加载 A 股名称到代码的映射
        self._load_stock_map()

    def _load_stock_map(self):
        print("正在初始化本地股票映射表，请稍候...")
        try:
            # 获取沪深京 A 股股票列表
            df_stocks = ak.stock_info_a_code_name()

            # 构建 字典: {'平安银行': '000001', '贵州茅台': '600519', ...}
            # 注意：AkShare 返回的代码是纯数字 6 位
            for _, row in df_stocks.iterrows():
                name = str(row['name']).strip()
                code = str(row['code']).strip()
                self.stock_map[name] = code
            print(f"成功加载 {len(self.stock_map)} 只股票映射！")
        except Exception as e:
            print(f"初始化股票映射表失败：{e}")



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