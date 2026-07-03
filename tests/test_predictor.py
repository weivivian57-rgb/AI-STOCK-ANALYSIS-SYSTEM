"""
test_predictor.py

股票趋势预测模块单元测试
"""

import unittest
import pandas as pd
import numpy as np
from models.stock import Stock
from services.trend_predictor import TrendPredictor


class TestTrendPredictor(unittest.TestCase):
    """
    TrendPredictor 类测试用例
    """

    def setUp(self):
        self.predictor = TrendPredictor()
        
        # ==========================
        # 构造模拟数据
        # ==========================
        dates = pd.date_range("2026-01-01", periods=50)
        
        # 模拟完美的线性上涨数据 [10, 11, 12 ... 59]
        closes = np.arange(10, 60)
        df = pd.DataFrame({"Close": closes}, index=dates)

        self.stock = Stock(code="TEST", data=df)

    def test_predict(self):
        """测试线性回归对未来趋势的预测"""
        
        result_stock = self.predictor.predict(self.stock, future_days=5)

        # ==========================
        # 断言：是否生成了指定天数的预测数据
        # ==========================
        self.assertEqual(len(result_stock.prediction), 5)

        # ==========================
        # 断言：验证线性回归是否敏锐捕捉到了上涨趋势
        # 最后一天收盘是 59，未来的预测值理应大于 59
        # ==========================
        self.assertTrue(result_stock.prediction[0] > 59)


if __name__ == '__main__':
    unittest.main()