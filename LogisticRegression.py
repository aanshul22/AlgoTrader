# Convert the pine script to python script. 
# One file for strategy and info reporting. 
# Another file for data gathering and cleaning.

from data import STOCKS_LIST
# from config import *
from functions import *
from gateway import read_data_dump, read_stocks_list


data = read_data_dump()
STOCKS_LIST = read_stocks_list()

for STOCK in STOCKS_LIST:
	stock = data[STOCK]

	high = data["High"]
	low = data["Low"]
	close = data["Close"]
	volume = data["Volume"]
	open = data["Open"]

	base = get_base_dataset(high, low, close, open)
	synth = get_synthetic_dataset(base)

	[loss, prediction] = logistic_regression(base, synth, lookback)

	scaled_loss = minimax(loss, base, nlbk)

	filter = HOLD
	if ftype == "Volatility":
		filter = volatilityBreak(high, low, close, 1, 10)
	elif ftype == "Volume":
		filter = volumeBreak(49, volume)
	elif ftype == "Both":
		filter = volatilityBreak(high, low, close, 1, 10) and volumeBreak(49, volume)
	else:
		filter = True

	# buy_signals = (base.iloc[nlbk-1:] > scaled_loss)[filter]
	# sell_signals = (base.iloc[nlbk-1:] < scaled_loss)[filter]




