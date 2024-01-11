# ---------------------------------------------------------------
# import packages
# ---------------------------------------------------------------
from ig_trading_historical_data import IG_API
import user_info
from pprint import pprint
import pandas as pd  # (optional) solely to see more DataFrame rows

pd.set_option('display.max_rows', 500)  # (optional) solely to see more DataFrame rows


# ---------------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------------
DEMO = 1

# format of the 'assets' dict example:
assets = {
    
    'GBPUSD Forward': {  # asset name in normal language (without slashes)
        'instrumentName': 'GBP/USD Forward',  # asset name in EXACT way seen on 
                                              # IG web platform (with slashes if relevant)
        'expiry': 'MAR-24'  # either 'DFB' or the expiration date
    },
    
    'Tesla': {  # another asset example
        'instrumentName': 'Tesla Motors Inc (All Sessions)',  
        'expiry': 'DFB'
    },
}

# historical data details
resolution = 'MINUTE_3'  # price resolution (SECOND, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
rangeType = 'numPoints'  # 'numPoints' or 'dates'
numPoints = 1
startDate = '2023-10-25 00:00:00'  # yyyy-MM-dd HH:mm:ss (inclusive dates and times)
endDate = '2023-11-28 00:00:00'  # yyyy-MM-dd HH:mm:ss (inclusive dates and times)
weekdays = (0, 1, 2, 3, 4, 5)  # 0: Mon, 6: Sun (deactivated if time portion above is equal) 

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

# loaded user information
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

pprint(assets['GBPUSD Forward'].keys())

pprint(assets['GBPUSD Forward']['instrumentName'])
pprint(assets['Tesla']['instrumentName'])

pprint(assets['GBPUSD Forward']['expiry'])
pprint(assets['Tesla']['expiry'])

pprint(assets['GBPUSD Forward']['epic'])
pprint(assets['Tesla']['epic'])

pprint(assets['GBPUSD Forward']['instrumentType'])
pprint(assets['Tesla']['instrumentType'])

pprint(assets['GBPUSD Forward']['prices'])
pprint(assets['Tesla']['prices'])

pprint(assets['GBPUSD Forward']['prices'][['closePxMid', 'lastTradedVolume']])
pprint(assets['Tesla']['prices'][['closePxMid', 'lastTradedVolume']])
