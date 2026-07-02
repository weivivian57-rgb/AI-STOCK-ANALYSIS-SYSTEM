from services.data_reader import DataReader
from services.stock_analyzer import StockAnalyzer
from services.trend_predictor import TrendPredictor
from services.ai_report_generator import AIReportGenerator

reader = DataReader()
analyzer = StockAnalyzer()
predictor = TrendPredictor()
generator = AIReportGenerator()

stock = reader.download_data("AAPL")

stock = analyzer.analyze(stock)

stock = predictor.predict(stock)

print("=" * 40)

print("股票代码：", stock.code)
print(f"最新价格：{stock.latest_price:.2f}")
print(f"MA5：{stock.ma5:.2f}")
print(f"MA20：{stock.ma20:.2f}")
print(f"MA60：{stock.ma60:.2f}")
print(f"MACD：{stock.macd:.2f}")
print(f"RSI：{stock.rsi:.2f}")

print("\n未来5天预测价格：")

for i, price in enumerate(stock.prediction, start=1):
    print(f"Day {i}: {price:.2f}")
    
report = generator.generate(stock)

print("\n")
print("=" * 40)
print("AI分析报告")
print("=" * 40)

print(report)