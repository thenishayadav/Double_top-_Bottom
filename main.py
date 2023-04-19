import fetcher
import formatter
import trendline_generator_new
import plotter
import os
import shutil
from datetime import datetime
import double_Top_Bottom

path = 'Plots'
if os.path.exists(path):
	shutil.rmtree(path)
os.makedirs(path)

coin_names = ["26000","26009"]
# coin_names = ["BTC_USDT"]

limit = 1000

time_start = datetime.now()

for coin_name in coin_names:
	api_response = fetcher.fetch(coin_name, limit = limit, interval = 5)

	timestamp, open, high, low, close= formatter.format(api_response)
	double_support, double_extrema = double_Top_Bottom.get_support_doubles(open, high, low, close, limit)
	double_r, doubleR_extrema = double_Top_Bottom.get_resistance_doubles(open, high, low, close, limit)
	doubles = double_support + double_r
	print(sorted(double_support))
	print(coin_name)
	print()

	plotter.plot(api_response = api_response, coin_name = coin_name,doubles=doubles,double_support=double_extrema,double_resistence=doubleR_extrema)

time_delta = datetime.now() - time_start
print(time_delta)