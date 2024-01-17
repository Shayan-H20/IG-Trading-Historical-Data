import json
import responses
import pandas as pd
import pytest_mock

from ig_trading_historical_data import IG_API
import tests.data.mock_user_info_demo as muid
import tests.data.mock_hist_data as mhd


class TestGetHistoricalPrices:
    """ unit tests for get_prices_single_asset() method """

    @responses.activate
    def test_get_prices_single_asset_num_points(self, mocker):
        """ test getting historical prices using the range_type='num_points' version """
        
        """ mocking the class initialization """
        # create mocked object
        mocked_init = mocker.patch.object(
            IG_API, 
            '__init__',
            return_value=None
        )

        # mock initialize
        ig_api = IG_API(**muid.mock_user_info_demo)

        # set mock attributes
        ig_api.url_base = muid.mock_url_base
        ig_api.header_base = muid.mock_header_base


        """ test .get_prices_single_asset() using 'num_points' """

        # prepare historical pricing information
        with open("tests/data/mock_hist_data_num_points.json", "r") as f:
            mock_prices_num_points_response_json = json.load(f)

        # mock the request.get inside the method
        mock_prices_url = "https://demo-api.ig.com/gateway/deal/prices/CF.D.GBPUSD.MAR.IP/MINUTE_5/2"

        responses.get(
            mock_prices_url,
            json=mock_prices_num_points_response_json,
            status=200
        )

        # run method
        prices, allowance, instrument_type = ig_api.get_prices_single_asset(
            epic='CF.D.GBPUSD.MAR.IP',
            resolution='MINUTE_5', 
            range_type='num_points', 
            start_date='2024-01-08 10:00:00',  # from Mon
            end_date='2024-01-10 10:30:00',  # until Wed
            weekdays=(0, 2),  # (Mon, Wed)
            num_points=2,
        )

        assert all(prices.columns == mhd.mock_prices_num_points.columns)
        assert all(prices.index == mhd.mock_prices_num_points.index)
        assert all(prices.round(2).values[0] == mhd.mock_prices_num_points.round(2).values[0])
        assert all(prices.round(2).values[1] == mhd.mock_prices_num_points.round(2).values[1])


    @responses.activate
    def test_get_prices_single_asset_dates_with_time_interval(self, mocker):
        """ test getting historical prices using the range_type='dates' version 
        combined with having a time interval active and specified weekdays for data gathering
        """
        
        """ mocking the class initialization """
        # create mocked object
        mocked_init = mocker.patch.object(
            IG_API, 
            '__init__',
            return_value=None
        )

        # mock initialize
        ig_api = IG_API(**muid.mock_user_info_demo)

        # set mock attributes
        ig_api.url_base = muid.mock_url_base
        ig_api.header_base = muid.mock_header_base


        """ 
        test .get_prices_single_asset() using 'dates'
        WITH time interval and WITH specified weekdays
        """

        # prepare historical pricing information (url 1/2)
        with open("tests/data/mock_hist_data_dates_time_interval_1.json", "r") as f:
            mock_prices_dates_time_interval_1_response_json = json.load(f)

        # prepare historical pricing information (url 2/2)
        with open("tests/data/mock_hist_data_dates_time_interval_2.json", "r") as f:
            mock_prices_dates_time_interval_2_response_json = json.load(f)


        # mock the request.get inside the method (url 1/2)
        mock_prices_url_1 = "https://demo-api.ig.com/gateway/deal/prices/CF.D.GBPUSD.MAR.IP/MINUTE_15/2024-01-08 10:00:00/2024-01-08 10:30:00"

        responses.get(
            mock_prices_url_1,
            json=mock_prices_dates_time_interval_1_response_json,
            status=200
        )

        # mock the request.get inside the method (url 2/2)
        mock_prices_url_2 = "https://demo-api.ig.com/gateway/deal/prices/CF.D.GBPUSD.MAR.IP/MINUTE_15/2024-01-10 10:00:00/2024-01-10 10:30:00"

        responses.get(
            mock_prices_url_2,
            json=mock_prices_dates_time_interval_2_response_json,
            status=200
        )


        # run method
        prices, allowance, instrument_type = ig_api.get_prices_single_asset(
            epic='CF.D.GBPUSD.MAR.IP',
            resolution='MINUTE_15', 
            range_type='dates', 
            start_date='2024-01-08 10:00:00',  # from Mon
            end_date='2024-01-10 10:30:00',  # until Wed
            weekdays=(0, 2),  # (Mon, Wed)
            num_points=2,
        )

        assert all(prices.columns == mhd.mock_prices_dates_time_interval.columns)
        assert all(prices.index == mhd.mock_prices_dates_time_interval.index)
        assert all(prices.round(2).values[0] == mhd.mock_prices_dates_time_interval.round(2).values[0])
        assert all(prices.round(2).values[-1] == mhd.mock_prices_dates_time_interval.round(2).values[-1])


    @responses.activate
    def test_get_prices_single_asset_dates_without_time_interval(self, mocker):
        """ test getting historical prices using the range_type='dates' version 
        combined with NOT having a time interval active and NOT having specified weekdays for data gathering
        """

        """ mocking the class initialization """
        # create mocked object
        mocked_init = mocker.patch.object(
            IG_API, 
            '__init__',
            return_value=None
        )

        # mock initialize
        ig_api = IG_API(**muid.mock_user_info_demo)

        # set mock attributes
        ig_api.url_base = muid.mock_url_base
        ig_api.header_base = muid.mock_header_base


        """ 
        test .get_prices_single_asset() using 'dates'
        WITHOUT time interval and WITHOUT specified weekdays
        """

        # prepare historical pricing information
        with open("tests/data/mock_hist_data_dates_no_time_interval.json", "r") as f:
            mock_prices_dates_no_time_interval_response_json = json.load(f)

        # mock the request.get inside the method
        mock_prices_url = "https://demo-api.ig.com/gateway/deal/prices/CF.D.GBPUSD.MAR.IP/HOUR_4/2024-01-08 00:00:00/2024-01-10 00:00:00"

        responses.get(
            mock_prices_url,
            json=mock_prices_dates_no_time_interval_response_json,
            status=200
        )

        # run method
        prices, allowance, instrument_type = ig_api.get_prices_single_asset(
            epic='CF.D.GBPUSD.MAR.IP',
            resolution='HOUR_4', 
            range_type='dates', 
            start_date='2024-01-08 00:00:00',  # from Mon
            end_date='2024-01-10 00:00:00',  # until Wed
            weekdays=(0, 2),  # (Mon, Wed)
            num_points=2,
        )

        assert all(prices.columns == mhd.mock_prices_dates_no_time_interval.columns)
        assert all(prices.index == mhd.mock_prices_dates_no_time_interval.index)
        assert all(prices.round(2).values[0] == mhd.mock_prices_dates_no_time_interval.round(2).values[0])
        assert all(prices.round(2).values[-1] == mhd.mock_prices_dates_no_time_interval.round(2).values[-1])
