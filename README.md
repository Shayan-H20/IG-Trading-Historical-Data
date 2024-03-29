A Python wrapper for extracting historical data in a quota-efficient way from IG's Trading API (can specify a daily time range for data gathering).

*PyPI page (published): https://pypi.org/project/ig-trading-historical-data/*

### Slightly more detailed description
This is a quota-efficient method of extracting data as can extract data between the hours of for example 13:00-16:00 on specified days of the week. This is instead of the default action of gathering all 24H of data for every single day of the week (given availability) which consumes increased quota allowance.

*- Quickstart Guide Further Below -*

## Output Format

Data outputted is in the form of a *pandas.DataFrame* with the following columns:

    * open_px_mid
    * high_px_mid
    * low_px_mid
    * close_px_mid

    * open_px_bid
    * high_px_bid
    * low_px_bid
    * close_px_bid

    * open_px_ask
    * high_px_ask
    * low_px_ask
    * close_px_ask

    * open_px_spread
    * high_px_spread
    * low_px_spread
    * close_px_spread

    * last_traded_volume

## Differences with other packages

The difference between this package and others found so far is the following:
* Given that each user has a **limited weekly quota for downloading historical data**, this package allows you to select a **time range** of interest during **whichever days of the week are of interest** (example below)
* Only data in this specified range is fetched, hence **saving your quota**:

> Example:
> * We are interested only in gathering data for Wednesdays and Fridays
> * We are also interested only in data between the hours of 13:00-16:00
> * We want HOURLY data during this time period and days from date X to date Y
> ---
> * Using this package we can get exactly what we want (conserving significant amounts of quota)
> * Using other packages (found so far), you would get data for EVERY day of the week and EVERY hour of the day (where data is available) between dates X and Y

# Quickstart

*Note that you can find all of this in one simple Python file at quickstart.py*

---

## Setup

Install using pip:

```
pip install ig-trading-historical-data
```

Prepare a `user_info.py` file (storage of sensitive information) in your projects directory with the following code:

```python
# DEMO OR LIVE ACCOUNT DETAILS
username = 'example username'
pw = 'example pw'
api_key = 'example api key'
```

Create your main file (i.e. 'quickstart.py') and use the following code segments:

Import packages:
```python
from ig_trading_historical_data import IG_API
import user_info
from pprint import pprint  # for nicer dictionary printing
```

Input user information:
```python
# account details
demo = 1  # 1: using demo account / 0: using live account
username = user_info.username
pw = user_info.pw
api_key = user_info.api_key
```

Let's say you want data for 'Microsoft' and 'GBPUSD Forward'.
The format of the 'assets' dictionary is as follows:
```python
assets = {
    
    'GBPUSD Forward': {  # asset name in normal language (without slashes)
        'instrument_name': 'GBP/USD Forward',  # asset name in EXACT way as seen on IG web platform (with slashes if relevant)
        'expiry': 'MAR-24'  # either 'DFB' or the expiration date
    },

    'Microsoft': {  # another asset example
        'instrument_name': 'Microsoft Corp (All Sessions)',  
        'expiry': 'DFB'
    },
}
```
The API will automatically find the correct EPIC (required to get data) based off these inputs.

Historical data inputs:

```python
resolution = 'MINUTE_5'  # price resolution (SECOND, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH)
range_type = 'dates'  # 'num_points' or 'dates'
num_points = 10  # ignored if range_type == 'dates'
start_date = '2024-01-08 10:00:00'  # yyyy-MM-dd HH:mm:ss (inclusive dates and times)
end_date = '2024-01-10 10:30:00'  # yyyy-MM-dd HH:mm:ss (inclusive dates and times)
weekdays = (0, 2)  # 0: Mon, 6: Sun (deactivated if time portion above is equal) 
```
Since the `range_type='dates'` and the time portion of `start_date` and `end_date` are different, historical data will be obtained between 8th January 2024 until 10th January 2024, but ONLY during the hours of 10am-10:30am.

Additionally, only the `weekdays` with values 0 and 2 will have their data gathered (i.e. Monday and Wednesday in this example). 

Since we are gathering **5-minutely** data over the **specified time range** (10am and 10:30am included) and over only **2 days**, we expect: **7 * 2 * 2 = 28 data points** (taking into account 2 assets, and 7 is the number of 5-minutes in our time range).

This significantly saves **quota** (measued in number of data points gathered), compared to getting every 5-minutely data point available in a 24 hour period and for every day of the week where data is available.

> **Of course, this is assuming you only care about data during a given time interval and given days of the week.**

You can of course still get every data point available by simply keeping the time portion above the same for both `start_date` and `end_date`.

## API key usage

#### Logging in / make a class instance:
```python
ig_api = IG_API(demo, username, pw, api_key)
```
Output:

    ----------------------
    Successfully logged in
    ----------------------

#### Get epics:

```python
# get epics automatically and update 'assets' dict with respective epics
assets = ig_api.get_epics(assets)

# views epics
pprint(assets) 
```

Output:

    {'GBPUSD Forward': {'epic': 'CF.D.GBPUSD.MAR.IP',
                        'expiry': 'MAR-24',
                        'instrument_name': 'GBP/USD Forward'},
    'Microsoft': {'epic': 'UC.D.MSFT.DAILY.IP',
                'expiry': 'DFB',
                'instrument_name': 'Microsoft Corp (All Sessions)'}}

#### Get historical prices:

```python
assets, allowance = ig_api.get_prices_all_assets(
    assets, 
    resolution, 
    range_type, 
    start_date,
    end_date,
    weekdays,
    num_points
)
```

Output:

    0.30 seconds for asset CF.D.GBPUSD.MAR.IP to run day 1/2
    0.28 seconds for asset CF.D.GBPUSD.MAR.IP to run day 2/2
    0.29 seconds for asset UC.D.MSFT.DAILY.IP to run day 1/2
    0.25 seconds for asset UC.D.MSFT.DAILY.IP to run day 2/2

When gathering data a loop is run for each asset and (if a time interval is specified) for each day as well. 

> To prevent exceeding the unknown limit of number of calls per minute to the REST Trading API (the limits specified [here](https://labs.ig.com/faq) do not seem to apply to the Demo account), each loop is set to sleep so that it lasts exactly 3 seconds (so far this value has not had any call limit errors). NOTE: This means it can take some time to gather the required data when specifying a time interval.

View prices DataFrame for *GBPUSD Forward* (17 columns of data fields and 14 rows):

```python
print(assets['GBPUSD Forward']['prices'])
```

Output:

                        open_px_bid  high_px_bid  low_px_bid  close_px_bid  open_px_ask  high_px_ask  low_px_ask  close_px_ask  open_px_mid  high_px_mid  low_px_mid  close_px_mid  open_px_spread  high_px_spread  low_px_spread  close_px_spread  last_traded_volume
    2024-01-08 10:00:00    12695.2    12697.0   12693.0     12694.6    12705.7    12707.5   12703.5     12705.1   12700.45   12702.25  12698.25    12699.85          10.5          10.5         10.5           10.5               341
    2024-01-08 10:05:00    12694.7    12698.2   12693.4     12697.8    12705.2    12708.7   12703.9     12708.3   12699.95   12703.45  12698.65    12703.05          10.5          10.5         10.5           10.5               311
    2024-01-08 10:10:00    12697.7    12699.5   12695.4     12696.4    12708.2    12710.0   12705.9     12706.9   12702.95   12704.75  12700.65    12701.65          10.5          10.5         10.5           10.5               306
    2024-01-08 10:15:00    12696.5    12702.7   12695.8     12699.2    12707.0    12713.2   12705.7     12709.7   12701.75   12707.95  12700.75    12704.45          10.5          10.5          9.9           10.5               272
    2024-01-08 10:20:00    12699.0    12702.8   12697.6     12701.9    12709.5    12713.3   12707.9     12712.4   12704.25   12708.05  12702.75    12707.15          10.5          10.5         10.3           10.5               273
    2024-01-08 10:25:00    12701.8    12702.6   12699.3     12699.6    12712.3    12713.1   12709.2     12709.5   12707.05   12707.85  12704.25    12704.55          10.5          10.5          9.9            9.9               224
    2024-01-08 10:30:00    12699.8    12704.1   12699.4     12703.9    12709.7    12714.6   12709.7     12714.4   12704.75   12709.35  12704.55    12709.15           9.9          10.5         10.3           10.5               226
    2024-01-10 10:00:00    12725.8    12733.5   12724.8     12733.2    12735.7    12743.4   12734.7     12743.1   12730.75   12738.45  12729.75    12738.15           9.9           9.9          9.9            9.9               212
    2024-01-10 10:05:00    12733.4    12734.2   12730.0     12730.3    12743.3    12744.3   12739.9     12740.2   12738.35   12739.25  12734.95    12735.25           9.9          10.1          9.9            9.9               271
    2024-01-10 10:10:00    12730.4    12731.4   12728.8     12730.7    12740.3    12741.3   12738.9     12740.6   12735.35   12736.35  12733.85    12735.65           9.9           9.9         10.1            9.9               259
    2024-01-10 10:15:00    12730.6    12732.5   12728.3     12728.3    12740.5    12742.4   12738.8     12738.8   12735.55   12737.45  12733.55    12733.55           9.9           9.9         10.5           10.5               235
    2024-01-10 10:20:00    12728.5    12731.7   12725.6     12729.5    12739.0    12741.6   12736.1     12740.0   12733.75   12736.65  12730.85    12734.75          10.5           9.9         10.5           10.5               230
    2024-01-10 10:25:00    12729.8    12730.6   12725.9     12726.2    12740.3    12740.8   12736.4     12736.7   12735.05   12735.70  12731.15    12731.45          10.5          10.2         10.5           10.5               396
    2024-01-10 10:30:00    12726.1    12726.3   12722.5     12724.6    12736.6    12736.8   12733.0     12735.1   12731.35   12731.55  12727.75    12729.85          10.5          10.5         10.5           10.5               291

The columns are: 

    [
        'open_px_bid', 'high_px_bid', 'low_px_bid', 'close_px_bid', 
        'open_px_ask', 'high_px_ask', 'low_px_ask', 'close_px_ask', 
        'open_px_mid', 'high_px_mid', 'low_px_mid', 'close_px_mid', 
        'open_px_spread', 'high_px_spread', 'low_px_spread', 'close_px_spread', 
        'last_traded_volume'
    ]

Allowance can be viewed using:

```python
pprint(allowance)
```

# Other details


## API historical data limits (indication)

    Resolution	|    Days
    ---------------------------
    1 Sec	    |    4
    1 Min	    |    40
    2 Min	    |    40
    3 Min	    |    40
    5 Min	    |    360
    10 Min	    |    360
    15 Min	    |    360
    30 Min	    |    360
    1 Hour	    |    360
    2 Hour	    |    360
    3 Hour	    |    360
    4 Hour	    |    360
    1 Day	    |    15 years


## Other class methods

*See class methods' docstrings for fully detailed information regarding: argument types, default values, output types, additional notes.*

---

**.get_watchlist()**: 
* Print and return dict (r.json()) of Watchlist.

**get_market_search(search_term)**: 
* Get list (value of first key) of available assets having match with search_term, later use another function to get the epic of a specific asset of interest.

**find_asset_epic_or_info(market_search_dict, instrument_name, expiry, epic_only)**:
* Find info for asset of interest, either return the epic only (str), or the info found (dict).

**get_epics(assets)**:
* Return the 'assets' dict updated with each assets' epic.

**get_prices_single_asset(epic, resolution, range_type, start_date, end_date, weekdays, num_points)**:
* Get prices DataFrame (bid/ask/mid/spreads for all OHLC prices and volume) for given parameters and time; also returns 'allowance' dict (resets every 7 days to 10,000 historical price data points).
