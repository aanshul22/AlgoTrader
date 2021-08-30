# Convert the pine script to python script. 
# One file for strategy and info reporting. 
# Another file for data gathering and cleaning.

from config import *
from functions import *
from tqdm import tqdm
from datetime import date
from gateway import read_data_dump, read_stocks_list


start_from_date = str(date(startYear, startMonth, startDate))

data = read_data_dump()
data = data.loc[start_from_date:]
latest_date = data.index[-1]
STOCKS_LIST = read_stocks_list()
output = []

print(f"Latest date: {latest_date}\n")

print(f"Price Type: {ptype}")
print(f"Lookback Window: {lookback}")
print(f"Normalization Lookback: {nlbk}")
print(f"Filter Signal: {ftype}")
print(f"Sell strategy: {sell_strat}\n")


for STOCK in tqdm(STOCKS_LIST):
	stock = data[STOCK]

	high = stock["High"]
	low = stock["Low"]
	close = stock["Close"]
	volume = stock["Volume"]
	open = stock["Open"]

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

	signals = get_all_signals(high, low, close, open, base, scaled_loss, filter)

	if signals.index[-1] == latest_date:
		if signals.iloc[-1] == BUY:
			output.append(f"BUY {STOCK}")
		elif signals.iloc[-1] == SELL:
			output.append(f"SELL {STOCK}")
		else:
			output.append(f"Not a valid signal {STOCK}")
	
for o in output:
	print(o)
