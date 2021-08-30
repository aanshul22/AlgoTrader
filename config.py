ptype      = 'OHLC4' 		# Price Type = ['Open','High','Low','Close','HL2','OC2','OHL3','HLC3','OHLC4']
reso       = "D"			# ['15', '30', '75', 'D', 'W', 'M']
lookback   = 4       		# Lookback Window Size |2..n|
nlbk       = 3       		# Normalization Lookback |2..240|
lrate      = 0.0009  		# Learning Rate |0.0001..0.01|    minval=0.0001, maxval=0.01, step=0.0001
iterations = 1000    		# Training Iterations |50..20000|
ftype      = 'Volatility'   # Filter Signals by  options=['Volatility','Volume','Both','None'])
# curves     = (true,  'Show Loss & Prediction Curves?')
# easteregg  = (true,   'Optional Calculation?')  
# useprice   = (true,   'Use Price Data for Signal Generation?')
# holding_p  = (5,      'Holding Period |1..n|',                 minval=1)
sell_strat = "Both" 		# options=["Logistic", "Decisive", "Both"])
use_start_date = True   	# Use start date
startDate = 1
startMonth = 1
startYear = 2020

BUY = 1
SELL = -1
HOLD = 0
