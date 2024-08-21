# experimenting with output of fetch balance from kraken account
# we are trying to figure out how to get the positions 

output = {'info': 
            {'error': [], 
                'result': {
                    'XETH': {'balance': '0.0020024400', 'hold_trade': '0.0000000000'}, 
                    'XXBT': {'balance': '0.0000000000', 'hold_trade': '0.0000000000'}, 
                    'ZUSD': {'balance': '291.3589', 'hold_trade': '0.0000'}}}, 
                    'timestamp': None, 'datetime': None, 'ETH': {'free': 0.00200244, 'used': 0.0, 'total': 0.00200244}, 'BTC': {'free': 0.0, 'used': 0.0, 'total': 0.0}, 'USD': {'free': 291.3589, 'used': 0.0, 'total': 291.3589}, 'free': {'ETH': 0.00200244, 'BTC': 0.0, 'USD': 291.3589}, 'used': {'ETH': 0.0, 'BTC': 0.0, 'USD': 0.0}, 'total': {'ETH': 0.00200244, 'BTC': 0.0, 'USD': 291.3589}}


print(output['ETH']['free'])