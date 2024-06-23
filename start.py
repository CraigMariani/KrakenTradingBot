import ccxt
from keys import Keys  as k
import time , schedule 
from pprint import pprint
################################
# initial connection / note you need to be logged in to trade!
kraken = ccxt.kraken({
    'enableRateLimit': True, 
    'apiKey': k.api_key,
    'secret': k.private_key
})

##############################
# fetch the current markets
pprint(kraken.fetch_balance())
pprint(kraken.fetch_positions().methods)
##############################
# fetch ticker labels
# markets = kraken.fetch_markets()
# for m in markets:
#     print(m['symbol'])

#########################
# we want to use BTC/USD so we declare variables
symbol = 'BTC/USD' # symbol we trade
order_type = 'limit' # limit or market
side = 'buy'  # buy or sell
amount = '0.0001' # how much we trade
price = 60000 # price we buy at 

###########################
# create an order
# kraken.create_order(
#         symbol=symbol,
#         type=order_type,
#         side=side,
#         amount=amount,
#         price=price
#     )

#cancel all  orders
# kraken.cancel_all_orders(symbol=symbol)


###########################
# lets combine the two and put into a function to make it callable again
# def run_bot():
#     kraken.create_order(symbol, order_type, side, amount, price)
#     time.sleep(5)
#     kraken.cancel_all_orders(symbol)

# set a scheduled task to run every 2 seconds
# schedule.every(2).seconds.do(run_bot)

# loop that checks for scheduled task and prints error message when not run correctly
# while True:
#     try: 
#         schedule.run_pending()
#     except Exception as e:
#         print('ERROR {}'.format(e))
#         time.sleep(60)


##############################
# Now we try the same thing but we can get the order book and try to modify the price 
# our order is buying at by looking at and adjusting to the bid and asking price

# book = kraken.fetch_order_book(symbol)
# pprint(book)

# spread is difference between bid and ask price
# bids are from buyers looking to buy at lowest price
# asks are from sellers looking to sell at highest price
# since we are buying we are looking to 
# bids = book['bids']
# asks = book['asks']


# orders = list(zip(*bids))[0]
# print(orders)

# bid = bids[0][0] if len (bids) > 0 else None
# ask = asks[0][0] if len (asks) > 0 else None
# spread = (ask - bid) if (bid and ask) else None
# print (kraken.id, 'market price', { 'bid': bid, 'ask': ask, 'spread': spread })

##########################
# now lets try this again but we will change the order based on what we get from our order book
# def run_bot():
#     book = kraken.fetch_order_book(symbol)
#     bids = book['bids']
#     asks = book['asks']

#     bid = bids[0][0] 
#     ask = asks[0][0] 
#     spread = (ask - bid) 
#     print('*')
#     if spread < 0.001:
#         print('price')
#         price = ask
#         print('bought {amount} at {ask}'.format(amount=amount, ask=ask))
    
#     else:
#         price = ask - 1000
#         print('No purchase')
    
#     print('**')
#     print('\n spread: {spread} \n bid: {bid} \n ask: {ask}'.format(spread=spread, bid=bid ,ask=ask))
#     kraken.create_order(symbol, order_type, side, amount, price)
#     time.sleep(5)
#     kraken.cancel_all_orders(symbol)
    

# # set a scheduled task to run every 2 seconds
# schedule.every(2).seconds.do(run_bot)

# # loop that checks for scheduled task and prints error message when not run correctly
# while True:
#     try: 
#         schedule.run_pending()
#     except Exception as e:
#         print('ERROR {}'.format(e))
#         time.sleep(60)