import json
import responses
import pytest_mock

from ig_trading_historical_data import IG_API
import tests.data.mock_user_info_demo as muid
import tests.data.mock_hist_data as mock_hist_data


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
            start_date='2024-01-08 10:00:00',
            end_date='2024-01-10 10:30:00',
            weekdays=(0, 2),
            num_points=2,
        )

        assert all(prices.columns == mock_hist_data.mock_prices_num_points.columns)
        assert all(prices.index == mock_hist_data.mock_prices_num_points.index)
        assert all(prices.values[0] == mock_hist_data.mock_prices_num_points.values[0])
        assert all(prices.values[1] == mock_hist_data.mock_prices_num_points.values[1])
