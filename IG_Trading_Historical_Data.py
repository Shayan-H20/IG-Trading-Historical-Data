# ---------------------------------------------------------------
# import packages
# ---------------------------------------------------------------
import requests
from pprint import pprint
import pandas as pd
import time


# ---------------------------------------------------------------
# verbose output support function
# ---------------------------------------------------------------
def output_request(
    r, 
    verbose: int = 0
    ) -> dict:
    """
    This support function provides increased clarity if errors occur, 
    OR displays a successful result and its associated return value if verbose=1.
    It is used in other API methods.

    ---
    Args:
        * r: output from requests.get(...)
        * verbose (int, default 0): 
            * 1: print Successful and pprint return value
            * 0: suppress prints when Successful
    ---
    Returns:
        * dict: r.json()
    """
    if r.status_code == 200:
        if verbose:
            print('----------------------')
            print('Successful')
            print('----------------------')
            pprint(r.json()) 
    else:
        print('----------------------')
        print('ERROR OCCURED')
        print('----------------------')
        print(f'STATUS CODE: {r.status_code}')
        print(r.content)
    
    return r.json()


# ---------------------------------------------------------------
# API class definition
# ---------------------------------------------------------------
class IG_API:
    def __init__(
        self, 
        DEMO: int, 
        username: str, 
        pw: str, 
        api_key: str, 
        verbose: int = 0
        ) -> None:
        """
        Log into the IG REST API.
        
        ---
        Args:
            * DEMO (int):
                * 1: use Demo account and environment URL
                * 0: use Live account and environment URL
            * username (str): username
            * pw (str): password
            * api_key(str): API key
            * verbose (int, default 0): more printing for earlier viewing of 
                results in some scenarios
        ---
        Raises:
            * Exception: if status_code != 200 (i.e. could not log in)
        ---
        Returns:
            * Nothing. Instead updates class instance attributes that are 
            used in later methods: 
                * token_CST (str): needed for all further API calls
                * token_X_SECURITY_TOKEN (str): needed for all further API calls
                * ls_addr (str): Lightstream address
                * utc_offset (str): timezoneOffset information
                * acc_info (dict): dict of misc. account data
                
                * header_base (dict): needed for all further API calls
        """
        # instantiate variables
        self.DEMO = DEMO
        self.username = username
        self.pw = pw
        self.api_key = api_key
        self.verbose = verbose
        
        # determine correct URL (API gateway location link)
        self.url_base = 'https://' + 'demo-'*DEMO + 'api.ig.com/gateway/deal'
        
        # log in: variables 
        url = f'{self.url_base}/session'
        header = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'VERSION': '2', 
            'X-IG-API-KEY': api_key
        }
        json = {
            'identifier': username,
            'password': pw
        }

        # log in: POST request
        r = requests.post(
            url=url,
            headers=header,
            json=json
        )

        self.acc_info = r.json()

        # log in: reponse 
        # (response.text or response.json())
        if r.status_code == 200:
            print('----------------------')
            print('Successfully logged in')
            print('----------------------')
            if verbose:
                pprint(self.acc_info) 
        else:
            print('----------------------')
            print('ERROR OCCURED')
            print('----------------------')
            print(f'STATUS CODE: {r.status_code}')
            print(r.content)
            
            raise ValueError(r.content)

        # retrieve tokens that MUST BE PASSED AS HEADERS to ALL subsequent API requests
        # [both tokens valid for 6H?]; get extended up to max of 72H while they are in use
        self.token_CST = r.headers['CST']  # client ID
        self.token_X_SECURITY_TOKEN = r.headers['X-SECURITY-TOKEN']  # current account

        # retreieve Lightstream address (required for all streaming connections)
        self.ls_addr = self.acc_info['lightstreamerEndpoint']
        
        # unpacking timezone info
        self.utc_offset = self.acc_info['timezoneOffset']

        # instantiating reusable variables
        self.header_base = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8',
            'X-IG-API-KEY': api_key,
            'CST': self.token_CST,
            'X-SECURITY-TOKEN': self.token_X_SECURITY_TOKEN
        }


    def get_watchlist(
        self, 
        ) -> dict:
        """
        Print and return dict (r.json()) of Watchlist.

        ---    
        Returns:
            * dict: watchlist
        """
        # watchlist: variables
        url = f'{self.url_base}/watchlists'
        header = self.header_base

        # watchlist: GET request
        r = requests.get(
            url=url,
            headers=header
        )

        # watchlist: response
        return output_request(r, self.verbose)  # !!! DELETE + remove output_request func


    def get_market_search(
        self, 
        searchTerm: str = None, 
        ) -> dict:
        """
        Get list (value of first key) of available assets having match with searchTerm,
        later use another function to get the epic of a specific asset of interest.

        ---
        Args:
            * searchTerm (str, default None): str used in search

        ---
        Returns:
            * dict (1 key, then list with each elem being a dict of that asset's info) 
                * can find epic of desired instrument in results 
                (but first find correct asset in list of results)
        """
        # market_search: variables
        url = f'{self.url_base}/markets?searchTerm={searchTerm}'
        header = self.header_base

        # market_search: GET request
        r = requests.get(
            url=url,
            headers=header
        )

        # market_search: response
        return output_request(r, self.verbose)  # !!! DELETE + remove output_request func


    def find_asset_epic_or_info(
        self, 
        marketSearchDict: dict, 
        instrumentName: str, 
        expiry: str = 'DFB', 
        epic_only: int = 1
        ) -> str:
        """
        Find info for asset of interest, either return the epic only (str), 
        or the info found (dict).
        
        ---
        Args:
            * marketSearchDict (dict): output of 'get_market_search' method
            * instrumentName (str): exactly as seen on IG web platform 
            (i.e. 'GBP/USD' or 'GBP/USD Forward')
            * expiry (str, default='DFB'): either 'DFB' or the expiration date
            (i.e. 'DEC-23' if a Forward etc.)
            * epic_only (int, default=1): 
                * 1: return only the epic str
                * 0: return the info found as a dixt
        ---
        Returns:
            * str or dict: epic string or dict with info found about the asset of interest
        """
        for asset_details in marketSearchDict['markets']:
            if all([
                asset_details['instrumentName'] == instrumentName,
                asset_details['expiry'] == expiry
            ]):
                return asset_details['epic'] if epic_only else asset_details
        
        return 'Asset not found'


    def get_epics(
        self, 
        assets: dict
        ) -> dict:
        """
        Return the 'assets' dict updated with each assets' epic.

        ---
        Args:
            * assets (dict of dict): 
                * example key: 'GBPUSD'
                    * value: dict(key: 'instrumentName', value: 'GBP/USD')
        ---
        Returns:
            * dict of dict: 'assets' input dict updated and returned
        """
        # loop to get epics for all assets in 'assets' dict
        for asset_name, d in assets.items():
            instrumentName = d['instrumentName']
            expiry = d['expiry']
            assets[asset_name]['epic'] = self.find_asset_epic_or_info(
                self.get_market_search(
                    asset_name, 
                ),
                instrumentName,
                expiry,
                epic_only=1
            )
        
        return assets


    def get_prices_single_asset(
        self, 
        epic: str, 
        resolution: str, 
        rangeType: str, 
        startDate: str = None, 
        endDate: str = None, 
        weekdays: tuple[int] = (0, 1, 2, 3, 4, 5, 6), 
        numPoints: int = None
        ) -> tuple:
        """
        Get prices DataFrame (bid/ask/mid/spreads for all OHLC prices and volume) 
        for given parameters and time interval; 
        also returns 'allowance' dict 
        (resets every 7 days to 10,000 historical price data points).

        ---
        Args:
            * epic (str): instrument epic
            * resolution (str): price resolution 
                * SECOND, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, 
                MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH
            * rangeType (str): 
                * 'numPoints': use numPoints argument
                * 'dates': use startDate/endDate arguments with given timeInterval (see below)
            * startDate (str, opt. depending on rangeType): 
                * yyyy-MM-dd HH:mm:ss (inclusive)
                * the time portion indicates timeIntervalStart
                * see full description on how to use this below this 'Args' block
                * defaults to None
            * endDate (str, opt. depending on rangeType): 
                * yyyy-MM-dd HH:mm:ss (inclusive)
                * the time portion indicates timeIntervalEnd
                * see full description on how to use this below this 'Args' block
                * defaults to None
            * weekdays (tup[int], opt.): 
                * which days of the week to get data for (0: Mon, 6: Sun)
                * defaults to all days of the week (0, 1, 2, 3, 4, 5, 6)
                * NOTE: this is only applied to the code when the time portion
                of the date range is different
            * numPoints (int, opt. depending on rangeType): 
                * get last numPoints data points
                * defaults to None
        ---
        Notes to startDate/endDate:
            * if the time portions are the SAME (00:00:00) then data is fetched using ALL the 24 hours
            in EVERY single day available ('weekdays' parameter is IGNORED)
            * if the time portions are DIFFERENT from one another, then the timeInterval and 'weekdays' 
            parameter is applied 
            * during the timeInterval technique, note that the time rounds DOWNWARDS 
                * i.e. if getting HOURLY data from 00:00:00-23:59:59 final value would be 23:00:00 
                instead of: 23:59:59 OR 00:00:00 (which would be midnight the NEXT day, 
                but dates are INCLUSIVE so midnight the next day is technically 
                out of date range)
        ---
        Returns:
            * tuple:
                * prices (DataFrame): bid/ask/mid/spreads for all OHLC prices and volume data 
                for all time periods within time interval
                * allowance (dict): 
                    * remainingAllowance: number of data points still available to fetch 
                    within current allowance period
                    * totalAllowance: number of data points the API key and account 
                    combination is allowed to fetch in any given allowance period
                    * allowanceExpiry: number of seconds till current allowance period 
                    ends and remainingAllowance field is reset
                * instrumentType (str): e.g. CURRENCIES
        """
        # initialize flag at 0
        # i.e. not using and timeInterval (later updated if necessary)
        timeIntervalFlag = 0
        
        # rangeType selection
        if rangeType == 'numPoints':
            
            url = f'{self.url_base}/prices/{epic}/{resolution}/{numPoints}'
            
            # number of times to loop requests.get for this rangeType method
            n = 1  
            
        elif rangeType == 'dates':
            
            # unpack dates to dates and timeInterval
            dateStart, timeIntervalStart = startDate.split()
            dateEnd, timeIntervalEnd = endDate.split()
            
            # condition to exclude time intervals
            # gets all data points possible
            # ignores 'weekdays' selection
            if timeIntervalStart == timeIntervalEnd:
                url = f'{self.url_base}/prices/{epic}/{resolution}/{startDate}/{endDate}'
                
                # number of times to loop requests.get for this rangeType method
                n = 1
                
            else:
                # activate flag ONLY if 'dates' selected and time intervals DIFFER
                # 'weekdays' input only taken into account HERE
                timeIntervalFlag = 1
                
                # create date range taking into account 'weekdays' input
                dateRange = pd.date_range(dateStart, dateEnd)
                dateRange = list(filter(lambda x: x.weekday() in weekdays, dateRange))
                dateRange = [x.strftime('%Y-%m-%d') for x in dateRange]
                
                # number of times to loop requests.get for this rangeType method
                n = len(dateRange)
            
        
        header = self.header_base.copy()
        header['Version'] = '2'

        # initialize list for loop
        pricesHistorical = []

        for i in range(n):
            
            if timeIntervalFlag:
                startDate = f'{dateRange[i]} {timeIntervalStart}'
                endDate = f'{dateRange[i]} {timeIntervalEnd}'
                url = f'{self.url_base}/prices/{epic}/{resolution}/{startDate}/{endDate}'
            
            # prices: GET request
            # every request/loopIteration is 1 call to the API
            # we have limit of max 60 or 30 [unclear] per minute
            # need to sleep this section so that 1 call takes minimum 1s [for limit of 60 per minute] 
            # or 2s [for limit of 30 per minute]
            # in reality, so far 3s sleep throws no error, whereas 1s or 2s still gives error
            timerStart = time.time()
            
            r = requests.get(
                url=url,
                headers=header
            )
            
            timerEnd = time.time()
            
            timeTaken = timerEnd - timerStart
            print(f'{timeTaken:.2f} seconds for asset {epic} to run day {i+1}/{n}')
            
            # if NOT a single API call
            if n != 1:
                # number of seconds to sleep between each API call to avoid exceeding unknown limit
                secondsForceSleep = 3.0  
                
                # sleep if time taken for request is less than value of secondsForceSleep
                if timeTaken < secondsForceSleep:
                    time.sleep(secondsForceSleep - timeTaken)
            
            # store JSON result
            res = r.json()

            # early function exit if error
            if r.status_code != 200:
                print('ERROR OCCURED')
                print(f'STATUS CODE: {r.status_code}')
                print(r.content)
                print(res)
                
                # error codes link: 
                # https://labs.ig.com/rest-trading-api-reference/service-detail?id=684
                
                return res
            
            # append prices info of each iteration in list container
            # NOTE: 
            #   res['prices'] is a list
            #   each elem is a different point in times' price info
            pricesHistorical.extend(res['prices'])   
        
        # unpack result
        allowance = res['allowance']
        instrumentType = res['instrumentType']
        
        ##########################
        # convert pricesHistorical list to 4 DataFrames 
        # and then merge into 1 DataFrame with all fields: bid, ask, mid, spread, volume etc.
        ##########################
        # conversion inputs
        priceTypes = ['openPrice', 'highPrice', 'lowPrice', 'closePrice']
        lastTradedVolumes = []
        snapshotTimes = []
        i = 0  # counter so we only gather snapshotTimes values only ONCE

        # initialize output dict
        prices = {
            'bid': {k: [] for k in priceTypes},
            'ask': {k: [] for k in priceTypes}
        }  

        # retrieve data in correct ordered way and place into DataFrames
        for k in prices:
            for t in pricesHistorical:
                for pType in priceTypes:
                    prices[k][pType].append(t[pType][k])
                
                if i == 0:
                    lastTradedVolumes.append(t['lastTradedVolume'])
                    snapshotTimes.append(pd.to_datetime(t['snapshotTime']))
            
            prices[k] = pd.DataFrame(
                data=prices[k], 
                index=snapshotTimes
            )
            
            i += 1

        # create 'mid' DataFrame
        prices['mid'] = (prices['bid'][priceTypes] + prices['ask'][priceTypes]) / 2

        # create 'spread' DataFrame
        prices['spread'] = prices['ask'][priceTypes] - prices['bid'][priceTypes]
        
        # rename headers to shorten 'Prices' > 'Px' 
        # and append type of field (bid, ask, mid, spread)
        for k in prices:
            prices[k].columns = prices[k].columns.str.replace('Price', f'Px{k.capitalize()}')
        
        # merge the DataFrames and add lastTradedVolume column
        prices = pd.concat([prices[k] for k in prices], axis=1)
        prices['lastTradedVolume'] = lastTradedVolumes
        ##########################
        # end of conversion from list to 1 DataFrame
        ##########################
            
        return prices, allowance, instrumentType


    def get_prices_all_assets(
        self, 
        assets: dict, 
        resolution: str, 
        rangeType: str, 
        startDate: str = None, 
        endDate: str = None, 
        weekdays: tuple[int] = (0, 1, 2, 3, 4, 5, 6), 
        numPoints: int = None
        ) -> tuple[dict]:
        """
        Get prices DataFrame (bid/ask/mid/spreads for all OHLC prices and volume)
        for all assets in 'assets' dict for given parameters and time interval;
        also returns 'allowance' dict 
        (resets every 7 days to 10,000 historical price data points).
        
        ---
        Args:
            * assets (dict): dict of assets with their epics
            * resolution (str): price resolution 
                * SECOND, MINUTE, MINUTE_2, MINUTE_3, MINUTE_5, MINUTE_10, 
                MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3, HOUR_4, DAY, WEEK, MONTH
            * rangeType (str): 
                * 'numPoints': use numPoints argument
                * 'dates': use startDate/endDate arguments with given timeInterval (see below)
            * startDate (str, opt. depending on rangeType): 
                * yyyy-MM-dd HH:mm:ss (inclusive)
                * the time portion indicates timeIntervalStart
                * see full description on how to use this below this 'Args' block
                * defaults to None
            * endDate (str, opt. depending on rangeType): 
                * yyyy-MM-dd HH:mm:ss (inclusive)
                * the time portion indicates timeIntervalEnd
                * see full description on how to use this below this 'Args' block
                * defaults to None
            * weekdays (tup[int], opt.): 
                * which days of the week to get data for (0: Mon, 6: Sun)
                * defaults to all days of the week (0, 1, 2, 3, 4, 5, 6)
                * NOTE: this is only applied to the code when the time portion
                of the date range is different
            * numPoints (int, opt. depending on rangeType): 
                * get last numPoints data points
                * defaults to None
        ---
        Notes to startDate/endDate:
            * if the time portions are the SAME (00:00:00) then data is fetched using ALL the 24 hours
            in EVERY single day available ('weekdays' parameter is IGNORED)
            * if the time portions are DIFFERENT from one another, then the timeInterval and 'weekdays' 
            parameter is applied 
            * during the timeInterval technique, note that the time rounds DOWNWARDS 
                * i.e. if getting HOURLY data from 00:00:00-23:59:59 final value would be 23:00:00 
                instead of: 23:59:59 OR 00:00:00 (which would be midnight the NEXT day, 
                but dates are INCLUSIVE so midnight the next day is technically 
                out of date range)
        ---
        Returns:
            * tuple: 
                * assets (dict): updated with 'prices' and 'instrumentType' keys for each 
                asset (each asset is the first layer of keys)
                    * prices (DataFrame): bid/ask/mid/spreads for all OHLC prices 
                    and volume data for all time periods within time interval
                    * instrumentType (str): e.g. CURRENCIES
                
                * allowance (dict): 
                    * remainingAllowance: number of data points still available to fetch 
                    within current allowance period
                    * totalAllowance: number of data points the API key and account 
                    combination is allowed to fetch in any given allowance period
                    * allowanceExpiry: number of seconds till current allowance period 
                    ends and remainingAllowance field is reset
        """
        for asset in assets:
            epic = assets[asset]['epic']

            prices, allowance, instrumentType = self.get_prices_single_asset( 
                epic, 
                resolution, 
                rangeType, 
                startDate, 
                endDate, 
                weekdays, 
                numPoints
            )

            assets[asset]['prices'] = prices
            assets[asset]['instrumentType'] = instrumentType
            
        return assets, allowance


# EVERYTHING ABOVE THIS POINT IS SUFFICIENT TO:
#   LOG IN
#   GATHER HISTORICAL PRICING INFO FOR ASSETS (INCLUDING THEIR EPICS)



