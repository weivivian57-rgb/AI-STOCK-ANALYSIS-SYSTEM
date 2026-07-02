"""
stock.py
股票数据模型
"""

from dataclasses import dataclass, field
import pandas as pd


@dataclass
class Stock:
    """
    股票对象
    """

    code: str                     # 股票代码
    name: str = ""                # 股票名称
    data: pd.DataFrame = field(default_factory=pd.DataFrame)

    # 技术指标
    ma5: float = 0.0
    ma20: float = 0.0
    ma60: float = 0.0

    macd: float = 0.0
    dif: float = 0.0
    dea: float = 0.0

    rsi: float = 0.0

    latest_price: float = 0.0

    def is_empty(self):
        """
        判断股票是否已有历史数据
        """
        return self.data.empty