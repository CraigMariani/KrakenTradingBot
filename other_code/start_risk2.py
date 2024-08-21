
import ccxt
from keys2 import Keys  as k
import time , schedule 
from pprint import pprint
import pandas as pd


kraken = ccxt.kraken({
    'enableRateLimit': True, 
    'apiKey': k.api_key,
    'secret': k.private_key
})

# open positions
def open_positions(symbol):
    orders = kraken.fetchOpenOrders(symbol=symbol)
    openpos_sides = []
    openpos_sizes = []
    openpos_bools = []
    longs = []

    for order in orders:
        #pprint(order)
        openpos_side = order['info']['descr']['type'] 
        openpos_sides.append(openpos_side)
        openpos_size = order['amount']
        openpos_sizes.append(openpos_size)
 
        if openpos_side == ('buy'):
            openpos_bools.append(True) 
            longs.append(True) 
        elif openpos_side == ('sell'):
            openpos_bools.append(True)
            longs.append(True)
        else:
            openpos_bools.append(False)
            longs.append(None)

    print(f'open_positions... | openpos_bool {openpos_bools} | openpos_size {openpos_sizes} | long {longs}')
    return open_positions, openpos_bools, openpos_sizes, longs

   
# ask_bid 
def ask_bid(symbol):

    ob = kraken.fetch_order_book(symbol)
    #pprint(ob)

    bid = ob['bids'][0][0]
    ask = ob['asks'][0][0]

    print(f'ask for {symbol} : {ask}')
    print(f'bid for {symbol} : {bid}')
    return ask, bid # ask_bid()[0] = ask , [1] = bid

########## kill switch
def kill_switch(symbol):
    #print(f'openposi: {open_positions(symbol)[0]}')
    print(f'starting the kill switch for {symbol}')
    openposi = open_positions(symbol)[1] # true or false
    

    long = open_positions(symbol)[3]# t or false
    
    kill_size = open_positions(symbol)[2] # size thats open  

    print(f'openposi {openposi}, long {long}, size {kill_size}')

    # right now this is comparing the entire list to one boolean value
    # while openposi == True:
    # this compares any of the values to one boolean
    while any(openposi) == True:
    # this compares all of the values to one boolean
    # while all(openposi) == True:
        print('open posi is True')
        kraken.cancel_all_orders(symbol) # cancel all open orders
        # openposi = open_positions(symbol)[1]
        # long = open_positions(symbol)[3]#t or false
        
        # get current balances/positions
        position = kraken.fetch_balance()
        print('showing position')
        print(position[symbol.split('/')[0]])
        ask = ask_bid(symbol)[0]
        bid = ask_bid(symbol)[1]
        kill_size = position[symbol.split('/')[0]]['total']
        kill_size = int(kill_size)
        print(kill_size)
        try:
            kraken.create_limit_sell_order(symbol, kill_size, ask)
            print(f'just made a SELL to CLOSE order of {kill_size} {symbol} at ${ask}')
            print('sleeping for 30 seconds to see if it fills..')
        except Exception as e:
            print(e)

        time.sleep(30)

        openposi = open_positions(symbol)[1]

target = 2 
max_loss = -1
# pnl close
# pnl_close() [0] pnlclose and [1] in_pos [2]size [3]long TF
def pnl_close(symbol, target=target, max_loss=max_loss):

    print(f'checking to see if its time to exit for {symbol}... ')

    # pos_dict = kraken.fetchOpenOrders(symbol=symbol) 
    # print(pos_dict)
    
    # index_pos = open_positions(symbol)[4] # come back to this
    # pos_dict = pos_dict[index_pos] # btc [3] [0] = doge, [1] ape
    # side = pos_dict['side']
    # size = pos_dict['contracts']
    # entry_price = float(pos_dict['entryPrice'])
    # leverage = float(pos_dict['leverage'])

    orders = kraken.fetchOpenOrders(symbol=symbol)
    #pprint(orders)
    for order in orders:
        current_price = ask_bid(symbol)[1]
        
        side = order['info']['descr']['type'] 
        entry_price = order['info']['descr']['price'] 
        
        leverage = order['info']['descr']['leverage'] 
        print(f'leverage {leverage}')
        if leverage == 'none':
            print('changing leverage')
            leverage = 1
            print('leverage')

        size = order['amount']
        order_id = order['id']
        print(f'order: {order_id} | side: {side} | entry_price: {entry_price} | lev: {leverage}')
        # short or long

        if side == 'buy':
            # print(f'entryprice type {type(entry_price)}')
            # print(f'currentprice type {type(current_price)}')
            print('in buy')
            entry_price = float(entry_price)
            diff = current_price - entry_price
            print(f'e_price {entry_price}')
            print(f'diff {diff}')
            long = True
        else: 
            diff = entry_price - current_price
            long = False

    # try /except 
        print('trying tryexcept')
        try: 
            print('inside try')
            print(diff)
            print(entry_price)
            print(leverage)
            perc = round(((diff/entry_price) * leverage), 10)
        except:
            print('failedtry')
            perc = 0

        perc = 100*perc
        print(f'for {symbol}, order {order_id} this is our PNL percentage: {(perc)}%')

        pnlclose = False 
        in_pos = False
        print(f'percentage {perc} | target {target}')
        if perc > 0:
            in_pos = True
            print(f'for {symbol} we are in a winning postion')
            if perc > target:
                print(':) :) we are in profit & hit target.. checking volume to see if we should start kill switch')
                pnlclose = True
                kill_switch(symbol)
            else:
                print('we have not hit our target yet')

        elif perc < 0: # -10, -20, 
            
            in_pos = True

            if perc <= max_loss: # under -55 , -5
                print(f'we need to exit now down {perc}... so starting the kill switch.. max loss {max_loss}')
                kill_switch(symbol)
            else:
                print(f'we are in a losing position of {perc}.. but chillen cause max loss is {max_loss}')

        else:
            print('we are  not in position')

        print(f' for {symbol} just finished checking PNL close..')

        return pnlclose, in_pos, size, long


# size kill 
def size_kill(symbol):

    max_risk = 1000

    
    #print(open_positions)
    orders = kraken.fetchOpenOrders(symbol=symbol)

    for order in orders:
        try:
            pos_cost = order['cost'] 
            
            openpos_side = open_positions['info']['descr']['type'] 
            openpos_size = open_positions['info']['descr']['amount'] 
        except:
            pos_cost = 0
            openpos_side = 0
            openpos_size = 0
        print(f'position cost: {pos_cost}')
        print(f'openpos_side : {openpos_side}')

        if pos_cost > max_risk:

            print(f'EMERGENCY KILL SWITCH ACTIVATED DUE TO CURRENT POSITION SIZE OF {pos_cost} OVER MAX RISK OF: {max_risk}')
            kill_switch(symbol) # just calling the kill switch cause the code below is long
            time.sleep(30000)
        else:
            print(f'size kill check: current position cost is: {pos_cost} we are gucci')

if __name__ == '__main__':
    # testing open positions 
    # open_positions(symbol='ETH/USD')

    # testing ask/bid
    # ask_bid(symbol='ETH/USD')

    # testing kill switch
    kill_switch(symbol='ETH/USD')

    # testing pnl close
    # pnl_close(symbol='ETH/USD', target=9, max_loss=-8)

    # testing size kill
    # size_kill(symbol = 'ETH/USD')
#start_risk.py
#Displaying start_risk.py.