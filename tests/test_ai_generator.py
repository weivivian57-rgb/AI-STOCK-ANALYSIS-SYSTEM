import unittest
import sys
import os

# 确保能导入项目根目录的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.stock import Stock
from services.ai_report_generator import AIReportGenerator

class TestAIReportGenerator(unittest.TestCase):
    def setUp(self):
        # 1. 构造一个模拟的 Stock 对象
        self.stock = Stock(code="TEST", name="测试股票")
        self.stock.latest_price = 150.0
        
        # 设置技术指标模拟数据
        self.stock.ma20 = 140.0       # 价格大于MA20，偏强
        self.stock.rsi = 75.0         # 大于70，超买
        self.stock.macd = 1.5         # 大于0，多头
        self.stock.prediction = [152.0, 154.0, 155.0, 156.0, 158.0] # 预测上涨

        self.generator = AIReportGenerator()

    def test_generate(self):
        # 2. 执行生成逻辑
        report = self.generator.generate(self.stock)
        
        # 3. 断言分析结果是否符合预期逻辑
        self.assertIn("TEST", report)
        self.assertIn("偏强", report)
        self.assertIn("超买", report)
        self.assertIn("多头", report)
        self.assertIn("上涨", report)
        self.assertIn("注意回调风险", report)
        
        print("AI报告生成逻辑测试通过！")

if __name__ == '__main__':
    unittest.main()