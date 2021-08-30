import pandas as pd
import numpy as np
# from data import df

FILEPATH = "./data_dump.csv"
FILEPATH_STOCKS = "./future_stocks.txt"

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