'''
My custom risk management system
'''


import ccxt
from keys2 import Keys  as k
import time , schedule 
from pprint import pprint
import pandas as pd
import numpy as np

kraken = ccxt.kraken({
    'enableRateLimit': True, 
    'apiKey': k.api_key,
    'secret': k.private_key
})


# check the ask and bid price (start_risk2.py)
# enter position with stop loss and take profit if spread is favorable, be sure to calculate the stop loss and take 
# profit based on percentages (how much you are able to lose or want to gain) (start.py)
# when in open position check the current price compared to stop loss and take profit (start_risk2.py)
# kill switch for exiting all positions when hitting stop loss or max loss (start_risk2.py)



# get the ask and bid price
def ask_bid(symbol):
    ob = kraken.fetch_order_book(symbol)
    #pprint(ob)

    bid = ob['bids'][0][0]
    ask = ob['asks'][0][0]

    print(f'ask for {symbol} : {ask}')
    print(f'bid for {symbol} : {bid}')
    return ask, bid # ask_bid()[0] = ask , [1] = bid

# determine if favorable position to enter in on and execute
# also claculate the stop loss and take profit here
def enter_pos(symbol, amount):
    ask, bid = ask_bid(symbol)
    spread = (ask - bid) 

    if spread < 0.1:
        price = ask
        print('good spread, entering at asking price')
        

    else:
        price = ask - 1000
        print('bad spread purchase at lower amount')

    # create a stop limit order based on price, if it goes to low we abort the order
    # kraken.create_stop_limit_order(
    #         symbol=symbol,
    #         side='buy',
    #         amount=amount,
    #         price=price,
    #         stopPrice=price - 100)
    
    # market order for experimenting with kill switch
    kraken.create_market_order(
            symbol=symbol,
            side='buy',
            amount=amount,
            price=price)
    
    # for tracking the positions we enter
    global order_ids 
    order_id = kraken.fetch_trades(symbol=symbol)[0]['id']
    print(order_id)
    order_ids = np.append(order_ids, order_id)
    print(order_ids)
    print('bought {amount} at {price}'.format(amount=amount, price=price))
    

# pull the plug when things go south
def kill_switch(symbol, in_pos):
    print('ran kill switch')
    kraken.cancel_all_orders() # cancels open orders

    # need to find a way to get the most recent trades we have done
    trades = kraken.fetch_trades(symbol=symbol)
    # pprint(trades[0])

    # figure out a way to know when we have entered a position (edit enterpos)
    print(in_pos)
    # know the amount of positions we have 
    global order_ids
    count_ids = len(order_ids)

    # use that number to get the number of most recent trades from the most recent trades list
    traded_positions = trades[0:count_ids]
    # use that list length to get the amounts and order ids
    for t in traded_positions:
        pos_id = t['id']
        pos_am = t['amount']

        # cancel each one of these orders based on the amounts and order ids by selling their positions
        print(pos_id)
        print(pos_am)
        kraken.create_order(
            symbol=symbol,
            type='market',
            side='sell',
            amount=pos_am
        )
# check the current position to stop loss and take profit
def pnl_close(symbol, in_pos):
    # fetching open orders
    # orders = kraken.fetchOpenOrders(symbol=symbol)
    # pprint(orders)
    
    # fetching balance
    # bal = kraken.fetch_balance()
    # pprint(bal)

    # fetches most recent trade
    trades = kraken.fetch_trades(symbol=symbol)
    pprint(trades[0])
    amount = trades[0]['amount']
    idn = trades[0]['id']
    entry_price = trades[0]['price']
    side = trades[0]['type']

    print(f'order: {idn} | side: {side} | entry_price: {entry_price} | amount: {amount}')
    # declare max loss (stop loss)
    max_loss = -1 # 1 percent loss
    # declare target (target price)
    target = 2 # 2 percent take profit

    # fetch entry price
    entry_price = trades[0]['price']
    # fetch current price
    current_price = ask_bid(symbol)[1]
    
    # calculating difference and percentage
    diff = current_price - entry_price
    perc = round(((diff/entry_price)), 10)
    print(perc)
    print(perc*100)
    in_pos = False
    hit_target = False
    if perc > 0:
        in_pos = True
        print(f'for {symbol} we are in a winning postion')
        if perc > target:
            print('in profit & hit target.. checking volume to see if we should start kill switch')
            hit_target = True
            kill_switch(symbol, in_pos)
        else:
            print('we have not hit our target yet')

    elif perc < 0: # -10, -20, 
        in_pos = True
        if perc <= max_loss: # under -55 , -5
            print(f'exiting now down {perc}... so starting the kill switch.. max loss {max_loss}')
            kill_switch(symbol, in_pos)
        else:
            print(f'we are in a losing position of {perc}.. have not hit max loss of {max_loss}')
    
    return hit_target, in_pos, amount,
        


if __name__ == '__main__':
    symbol = 'ETH/USD'
    amount = 0.002
    
    order_ids = np.array([])

    #ask_bid(symbol)
    # schedule.every(2).seconds.do(enter_pos(symbol, amount))

    # while True:

        
    #     # schedule.run_pending()
    #     enter_pos(symbol=symbol, amount=amount)
    #     time.sleep(300)
    
    enter_pos(symbol, amount)
    # print(pnl_close(symbol))
    kill_switch(symbol=symbol, in_pos=True)
