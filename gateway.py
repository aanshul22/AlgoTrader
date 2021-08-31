import numpy as np
import pandas as pd
from os import startfile

# FILEPATH = "./data_dump.csv"
FILEPATH = "./data_dump_0.csv"
# FILEPATH_STOCKS = "./future_stocks.txt"
FILEPATH_STOCKS = "./f&o_stocks.txt"
FILEPATH_SIGNALS = "./signals.txt"

def read_data_dump():
	data = pd.read_csv(FILEPATH, header=[0, 1], index_col=0)
	return data


def write_data_dump(data):
	try:
		data.to_csv(FILEPATH, na_rep="NA")
	except:
		print("Permission denied. File may be open.\n")
		return
	
	print("Data successfully written.\n")


def read_stocks_list():
	STOCKS_LIST = []

	with open(FILEPATH_STOCKS, "r") as f:
		STOCKS_LIST = f.readlines()
		STOCKS_LIST = list(map(lambda x: x.strip("\n"), STOCKS_LIST))

	return STOCKS_LIST


def write_signals(output):
	with open(FILEPATH_SIGNALS, mode="w") as f:
		for o in output:
			print(o, file=f)

	# startfile(FILEPATH_SIGNALS[2:])
	
