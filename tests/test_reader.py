"""
test_reader.py

数据获取模块单元测试
"""

import unittest
import pandas as pd
from unittest.mock import patch
from services.data_reader import DataReader


class TestDataReader(unittest.TestCase):
    """
    DataReader 类测试用例
    """

    def setUp(self):
        self.reader = DataReader()
        
        # ==========================
        # 构造包含缺失值的脏数据
        # ==========================
        self.raw_data = pd.DataFrame({
            "Open": [100, 101, None, 103],
            "Close": [105, 106, 107, 108]
        }, index=pd.date_range("2026-01-01", periods=4))

    def test_clean_data(self):
        """测试数据清洗功能（去空与排序）"""
        
        cleaned_df = self.reader.clean_data(self.raw_data)
        
        # ==========================
        # 断言：空值行应被删除，长度变为3
        # ==========================
        self.assertEqual(len(cleaned_df), 3)
        self.assertFalse(cleaned_df.isnull().values.any())

    @patch('services.data_reader.yf.download')
    def test_download_data(self, mock_yf_download):
        """测试数据下载（使用 Mock 隔离真实网络请求）"""
        
        # ==========================
        # 模拟 yfinance 的返回结果
        # ==========================
        mock_yf_download.return_value = pd.DataFrame({
            "Close": [150.0, 151.0, 152.0]
        })
        
        stock = self.reader.download_data("AAPL")
        
        self.assertEqual(stock.code, "AAPL")
        self.assertEqual(stock.latest_price, 152.0)


if __name__ == '__main__':
    unittest.main()