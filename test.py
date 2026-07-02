from services.data_reader import DataReader
from services.stock_analyzer import StockAnalyzer
from services.trend_predictor import TrendPredictor

reader = DataReader()
analyzer = StockAnalyzer()
predictor = TrendPredictor()

stock = reader.download_data("AAPL")

stock = analyzer.analyze(stock)

stock = predictor.predict(stock)

print("=" * 40)

print("股票代码：", stock.code)
print("最新价格：", stock.latest_price)
print("MA5：", stock.ma5)
print("MACD：", stock.macd)
print("RSI：", stock.rsi)

print("\n未来5天预测价格：")

for i, price in enumerate(stock.prediction, start=1):
    print(f"Day {i}: {price:.2f}")