"""
test_analyzer.py

股票技术指标分析模块单元测试
"""

import unittest
import pandas as pd
import numpy as np
from models.stock import Stock
from services.stock_analyzer import StockAnalyzer


class TestStockAnalyzer(unittest.TestCase):
    """
    StockAnalyzer 类测试用例
    """

    def setUp(self):
        self.analyzer = StockAnalyzer()
        
        # ==========================
        # 构造 100 天的模拟 K 线数据
        # ==========================
        dates = pd.date_range("2026-01-01", periods=100)
        
        # 使用 linspace 模拟一个稳定上涨的收盘价 (从 100 涨到 200)
        closes = np.linspace(100, 200, 100)
        df = pd.DataFrame({"Close": closes}, index=dates)

        self.stock = Stock(code="TEST", data=df)

    def test_analyze(self):
        """测试各项技术指标的计算"""
        
        result_stock = self.analyzer.analyze(self.stock)

        # ==========================
        # 断言：验证指标是否被正确计算并挂载到 Stock 对象上
        # ==========================
        self.assertTrue(result_stock.ma5 > 0)
        self.assertTrue(result_stock.ma20 > 0)
        self.assertTrue(result_stock.ma60 > 0)
        
        self.assertEqual(result_stock.latest_price, 200.0)

        # ==========================
        # 断言：验证 DataFrame 是否扩充了指标列
        # ==========================
        columns = result_stock.data.columns
        self.assertIn("MA5", columns)
        self.assertIn("MACD", columns)
        self.assertIn("RSI", columns)


if __name__ == '__main__':
    unittest.main()