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

            # 构建 字典
            for _, row in df_stocks.iterrows():
                name = str(row['name']).strip()
                code = str(row['code']).strip()
                self.stock_map[name] = code
            print(f"成功加载 {len(self.stock_map)} 只股票映射！")
        except Exception as e:
            print(f"初始化股票映射表失败：{e}")
            print("[系统提示] 启用本地 30 只中美科技龙头应急后备字典应对网络波动...")
            
            # ======================================================
            # 💡 专业级容灾配置：30只全球科技龙头核心映射表
            # ======================================================
            self.stock_map = {
                # ------------------ A股半导体与硬科技 ------------------
                "立昂微": "605358",
                "长电科技": "600584",
                "通富微电": "002156",
                "北方华创": "002371",
                "中芯国际": "688981",
                "韦尔股份": "603501",
                "兆易创新": "603986",
                "闻泰科技": "600745",
                "紫光国微": "002049",
                "海康威视": "002415",
                
                # ------------------ A股新能源与核心资产 ------------------
                "宁德时代": "300750",
                "阳光电源": "300274",
                "比亚迪": "002594",
                "隆基绿能": "601012",
                "亿纬锂能": "300014",
                "贵州茅台": "600519",
                "平安银行": "000001",
                "五粮液": "000858",
                
                # ------------------ 美股AI及全球科技巨头 ------------------
                "苹果": "AAPL",
                "英伟达": "NVDA",
                "特斯拉": "TSLA",
                "微软": "MSFT",
                "谷歌": "GOOGL",
                "亚马逊": "AMZN",
                "Meta": "META",
                "超微半导体": "AMD",
                "高通": "QCOM",
                "英特尔": "INTC",
                "博通": "AVGO",
                "台积电": "TSM"
            }



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