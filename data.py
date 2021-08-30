import numpy as np
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
from gateway import read_data_dump, write_data_dump

# Get list of all the stocks that have futures
# Stocks excluded- IRCTC.NS, ^NSEBANK, ^NSEI
STOCKS_LIST = []
with open("./future_stocks.txt", "r") as f:
	STOCKS_LIST = f.readlines()
	STOCKS_LIST = list(map(lambda x: x.strip("\n"), STOCKS_LIST))

# Get completely fresh data
def data_download(sym=STOCKS_LIST, start_date='2019-01-01'):
	if not isinstance(sym, list) and not isinstance(sym, str):
		sym = sym.tolist()

	data = yf.download(sym, start_date, str(date.today()))
	if data.empty:
		return None

	data.drop("Close", inplace=True, axis=1)
	data.rename({"Adj Close": "Close"}, axis=1, inplace=True)
	data = data.round(decimals=2)
	try:
		data = data.swaplevel(axis=1)
	except:
		pass

	rows = set(data.index)
	data.dropna(inplace=True)
	remaining_rows = set(data.index)
	dropped_rows = rows.difference(remaining_rows)
	print(f"Dropped rows: {[str(d.date()) for d in dropped_rows]}")

	assert data.isnull().any().sum().sum() == 0

	latest_date = str(data.index[-1])
	latest_date = latest_date[:latest_date.index(" ")]

	print(f"Latest date: {latest_date}")

	return data

# Update the existsing csv
def update_data():
	data = read_data_dump()

	latest_date = str(data.index[-1])
	if latest_date.index("-") == 2:
		latest_date = latest_date[6:] + latest_date[2:6] + latest_date[:2]
	
	if latest_date != str(date.today()):
		start_date = str(date.fromisoformat(latest_date) + timedelta(days=1))

		new_data = data_download(STOCKS_LIST, start_date)

		if new_data is None:
			print(f"Data up to date: {latest_date}")
		else:
			new_data.index = new_data.index.date
			updated_df = pd.concat([data, new_data])
			write_data_dump(updated_df)
	else:		
		print(f"Data up to date: {latest_date}")


# Convery to numpy arrays
def get_lists(d):
	volume = np.flip(np.array(d["Volume"]))
	close = np.flip(np.array(d["Close"]))
	open = np.flip(np.array(d["Open"]))
	high = np.flip(np.array(d["High"]))
	low = np.flip(np.array(d["Low"]))

	latest_date = str(d.index.values[-1])
	try:
		latest_date = latest_date[:latest_date.index("T")]
	except:
		pass

	return open, high, low, close, volume, latest_date


def main():
	# df = data_download()
	# df.index = df.index.date
	# write_data_dump(df)

	update_data()

	# for stock in STOCKS_LIST[:10]:
		# stock_book[stock] = Stock(stock, d[stock])

	# print(stock_book["INFY.NS"])
	# print(stock_book["INFY.NS"].close[:5])
# Have stock book. Now do logistic regression.


main()
