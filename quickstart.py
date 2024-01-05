# ---------------------------------------------------------------
# import packages
# ---------------------------------------------------------------
from ig_trading_historical_data import IG_API
import user_info
from pprint import pprint

# ---------------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------------
DEMO = 1

assets = {
    'GBPUSD Fwd': {
        'instrumentName': 'GBP/USD Forward',
        'expiry': 'MAR-24'
    },
    'EURUSD': {
        'instrumentName': 'EUR/USD',
        'expiry': 'DFB'
    },
    'US 500': {
        'instrumentName': 'US 500',
        'expiry': 'DFB'
    },
    'Tesla': {
        'instrumentName': 'Tesla Motors Inc (All Sessions)',
        'expiry': 'DFB'
    },
}

# historical data details
resolution = 'HOUR'  # price resolution (SECOND, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
rangeType = 'numPoints'  # 'numPoints' or 'dates'
numPoints = 3
startDate = '2023-11-06 00:00:00'  # yyyy-MM-dd HH:mm:ss (inclusive)
endDate = '2023-12-29 00:00:00'  # yyyy-MM-dd HH:mm:ss (inclusive)
weekdays = (0, 1, 2, 3, 4)  # 0: Mon, 6: Sun
"""API HISTORICAL DATA LIMITS (INDICATION)
------------------------------------------
Resolution	    Days
1 Sec	        4
1 Min	        40
2 Min	        40
3 Min	        40
5 Min	        360
10 Min	        360
15 Min	        360
30 Min	        360
1 Hour	        360
2 Hour	        360
3 Hour	        360
4 Hour	        360
1 Day	        15 years
------------------------------------------
"""

# loaded variables
username = user_info.username_demo if DEMO else user_info.username
pw = user_info.pw_demo if DEMO else user_info.pw
api_key = user_info.api_key_demo if DEMO else user_info.api_key

# ---------------------------------------------------------------
# API USAGE
# ---------------------------------------------------------------
# logging in
ig_api = IG_API(DEMO, username, pw, api_key)

# update 'assets' dict with respective epics
assets = ig_api.get_epics(assets)
pprint(assets)

# retrieve historical data
assets, allowance = ig_api.get_prices_all_assets(
    assets, 
    resolution, 
    rangeType, 
    startDate,
    endDate,
    weekdays,
    numPoints
)
pprint(assets)
pprint(allowance)

# example outputs
pprint(assets.keys())

pprint(assets['GBPUSD Fwd']['instrumentName'])
pprint(assets['EURUSD']['instrumentName'])
pprint(assets['Tesla']['instrumentName'])
pprint(assets['US 500']['instrumentName'])

pprint(assets['GBPUSD Fwd']['expiry'])
pprint(assets['EURUSD']['expiry'])
pprint(assets['Tesla']['expiry'])
pprint(assets['US 500']['expiry'])

pprint(assets['GBPUSD Fwd']['epic'])
pprint(assets['EURUSD']['epic'])
pprint(assets['Tesla']['epic'])
pprint(assets['US 500']['epic'])

pprint(assets['GBPUSD Fwd']['instrumentType'])
pprint(assets['EURUSD']['instrumentType'])
pprint(assets['Tesla']['instrumentType'])
pprint(assets['US 500']['instrumentType'])

pprint(assets['GBPUSD Fwd']['prices'])
pprint(assets['EURUSD']['prices'])
pprint(assets['Tesla']['prices'])
pprint(assets['US 500']['prices'])

pprint(assets['GBPUSD Fwd']['prices'][['closePxMid', 'lastTradedVolume']])
pprint(assets['EURUSD']['prices'][['closePxMid', 'lastTradedVolume']])
pprint(assets['Tesla']['prices'][['closePxMid', 'lastTradedVolume']])
pprint(assets['US 500']['prices'][['closePxMid', 'lastTradedVolume']])
