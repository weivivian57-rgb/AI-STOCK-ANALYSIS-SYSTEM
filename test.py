from services.data_reader import DataReader

reader = DataReader()

stock = reader.download_data("AAPL")

print(stock.code)

print(stock.latest_price)

print(stock.data.head())