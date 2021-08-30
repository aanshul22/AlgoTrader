import numpy as np
import pandas as pd
from config import *
from math import exp, log
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange
from ta.trend import wma_indicator, CCIIndicator


def hma(close, period):
	p1 = 2 * wma_indicator(close, period//2)
	p2 = wma_indicator(close, period)
	p3 = p1 - p2
	window = int(period**0.5)
	return wma_indicator(p3, window).round(2)


def rsi(close, period):
	return RSIIndicator(close=close, window=period).rsi().round(2)


def atr(high, low, close, window):
	return AverageTrueRange(high=high, low=low, close=close,
						 window=window).average_true_range().round(2)


def cci(high, low, close, window):
	return CCIIndicator(high=high, low=low, close=close, window=window).round(2).cci()


def volumeBreak(thres, volume):
	rsivol   = rsi(volume, 14)
	osc      = hma(rsivol, 10)
	return osc > thres


def volatilityBreak(high, low, close, volmin, volmax):
	return atr(high, low, close, volmin) > atr(high, low, close, volmax)


def dot(v, w, p):
	prod = v * w
	cumsum = prod.cumsum()
	for i in range(1, len(cumsum) + 1 - p):
		cumsum.iloc[-i] -= cumsum.iloc[-i-p]
	return cumsum

# Fix for series
def minimax(ds, base, p):
	scaled_losses = []
	for i in range(len(ds) - p + 1):
		hi = max(ds.iloc[i : i + p])
		lo = min(ds.iloc[i : i + p])
		highest = max(base.iloc[i : i + p])
		lowest = min(base.iloc[i : i + p])

		scaled_losses.append((highest - lowest) * (ds.iloc[i + p - 1] - lo)/(hi - lo) + lowest)

	return pd.Series(scaled_losses, index=ds.index[p-1:]).round(2)



def sigmoid(z):
	return z.apply(lambda x : 1.0 / (1.0 + exp(-x)))


def get_base_dataset(high, low, close, open):
	if ptype == "Open":
		ds = open
	elif ptype == "High":
		ds = high
	elif ptype == "Low":
		ds = low
	elif ptype == "Close":
		ds = close
	elif ptype == "HL2":
		ds = (high + low)/2
	elif ptype == "OC2":
		ds = (open + close)/2
	elif ptype == "OHL3":
		ds = (open + high + low)/3
	elif ptype == "HLC3":
		ds = (high + low + close)/3
	elif ptype == "OHLC4":
		ds = (open + high + low + close)/4
	else:
		print("Not a valid type.")
		exit(1)

	return ds.round(2)


def get_synthetic_dataset(base_ds):
	return (abs(base_ds ** 2 - 1) + 0.5).apply(np.log).round(2)


def getMomentum(high, low, close, open):
	candleHeight = high - low
	bodyHeight = open - close
	ratio = ((bodyHeight/candleHeight)*100)
	ratio = ratio.abs()
	momentum = ratio > 50
	return momentum


def get_low(momentums, high, low, close, open):
	stop = low.iloc[0]
	stops = [stop]
	for day in range(1, len(momentums)):
		if momentums.iloc[day] and close.iloc[day] - open.iloc[day] > 0:
			temp = low.iloc[day]
			num = 1
			while day - num >= 0 and not momentums.iloc[day-num] and close.iloc[day] > high.iloc[day-num]:
				temp = min(temp, low.iloc[day-num])
				num += 1

			if num > 1:
				stop = temp * 0.99

		stops.append(stop)

	stops = pd.Series(stops, index=momentums.index)

	return stops.round(2)


def getPercentage(reso):
	percentage = 0.0
	if reso == "15":
		percentage = 0.0021
	elif reso == "30":
		percentage = 0.0039
	elif reso == "75":
		percentage = 0.0055
	elif reso == "D":
		percentage = 0.01
	elif reso == "W" or reso == "M":
		percentage = 0.03
	return percentage


def get_buy_signals(base, scaled_loss, filter):
	return np.logical_and((base.iloc[nlbk-1:] > scaled_loss), filter)

def get_sell_signals(high, low, close, open, base, scaled_loss, filter):
	momentums = getMomentum(high, low, close, open)
	stop = get_low(momentums, high, low, close, open)

	sell_signals = None
	if sell_strat == "Both":
		logistic = np.logical_and((base.iloc[nlbk-1:] < scaled_loss), filter)
		decisive = close < stop
		sell_signals = (np.logical_or(decisive, logistic))
		assert sum(sell_signals.isna()) == 0
	elif sell_strat == "Decisive":
		sell_signals = close < stop
	elif sell_strat == "Logistic":
		sell_signals = np.logical_and((base.iloc[nlbk-1:] < scaled_loss), filter)
	else:
		print("Not a valid sell_start")
		exit(1)

	return sell_signals


#  Take into account decisive as well
def get_all_signals(high, low, close, open, base, scaled_loss, filter):
	buy_signals = get_buy_signals(base, scaled_loss, filter)
	sell_signals = get_sell_signals(high, low, close, open, base, scaled_loss, filter)
	signals = []
	for buy, sell in zip(buy_signals, sell_signals):
		# If sell and buy both, then sell superseeds
		if sell:
			signals.append(SELL)
		elif buy:
			signals.append(BUY)
		else:
			signals.append(HOLD)
	signals = pd.Series(signals, index=buy_signals.index)
	signals = signals[signals != 0]
	signals = signals.diff()
	signals = signals[signals != 0]
	signals.dropna(inplace=True)
	
	return signals/2


# # Might not work
# def logistic_regression(X, Y, p, lr, iterations):
# 	w = 0.0
# 	loss = 0.0
# 	for _ in range(1, iterations + 1):
# 		hypothesis = sigmoid(dot(X, 0.0, p))  # prediction
# 		loss = -1.0 / p * (dot(dot(Y, log(hypothesis) + (1.0 - Y), p), log(1.0 - hypothesis), p))
# 		gradient = 1.0 / p * (dot(X, hypothesis - Y, p))
# 		w = w - lr * gradient                 # update weights
	
# 	return [loss, sigmoid(dot(X, w, p))]             # current loss & prediction

# def logistic_regression(X, Y, p, lr, iterations):
# 	w = 0.0
# 	loss = 0.0
# 	for _ in range(iterations):
# 		hypothesis = sigmoid(dot(X, 0.0, p))  # prediction
# 		chunk1 = dot(Y, hypothesis.apply(np.log) + (1.0 - Y), p)
# 		loss = -1.0 / p * (dot(chunk1, (1.0 - hypothesis).apply(np.log), p))
# 		gradient = 1.0 / p * (dot(X, hypothesis - Y, p))
# 		loss = -1 / p * dot(Y, Y, p)

# 		w = w - lr * gradient                 # update weights
	
# 	gradient = 1.0 / p * (dot(X, 0.5 - Y, p))

# 	return [loss, sigmoid(dot(X, w, p))]             # current loss & prediction



def logistic_regression(X, Y, p):
	w = 0.0
	# Since hypothesis is always 0.5
	chunk1 = dot(Y, (0.3069 - Y), p)
	loss = -1.0 / p * (dot(chunk1, -0.6931, p))

	return [loss, sigmoid(dot(X, w, p))]             # current loss & prediction
