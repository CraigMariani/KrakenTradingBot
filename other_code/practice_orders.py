import ccxt
from keys2 import Keys  as k
import time , schedule 
from pprint import pprint
################################
# initial connection / note you need to be logged in to trade!
kraken = ccxt.kraken({
    'enableRateLimit': True, 
    'apiKey': k.api_key,
    'secret': k.private_key
})

kraken.create_limit_order(symbol='ETH/USD', type='limit', side='buy', amount=0.01, price=3000, params={'takeProfitPrice': 3100, 'stopLossPrice':2900})