from data import get_lists

class Stock:
	def __init__(self, ticker, data):
		self.ticker = ticker
		self.open, self.high, self.low, self.close, self.volume, self.latest_date = get_lists(data)

	def __str__(self):
		return f"{self.latest_date} {self.ticker} {self.close[0]}"



