from dataclasses import dataclass, field
import pandas as pd


@dataclass
class Stock:

    code: str
    name: str = ""

    data: pd.DataFrame = field(default_factory=pd.DataFrame)

    # 技术指标
    ma5: float = 0.0
    ma20: float = 0.0
    ma60: float = 0.0

    macd: float = 0.0
    dif: float = 0.0
    dea: float = 0.0

    rsi: float = 0.0

    # AI预测结果
    prediction: list = field(default_factory=list)

    latest_price: float = 0.0

    def is_empty(self):
        return self.data.empty