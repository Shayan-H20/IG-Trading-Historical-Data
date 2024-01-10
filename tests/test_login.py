from ig_trading_historical_data import IG_API
import responses
import json


""" unit tests for login """


class TestLogin:
    
    # initialize class variables
    mock_user_info_demo = {
        "DEMO": 1,
        "username": "test_username",
        "pw": "test_pw",
        "api_key": "test_api_key",
    }


    @responses.activate
    def test_login_demo_via_init(self):
        
        with open("tests/data/mock_acc_info.json", "r") as f:
            mock_response_json = json.load(f)

        # mock the request.post inside the API's class initialization
        mock_url = "https://demo-api.ig.com/gateway/deal/session"
        mock_response_headers = {
            "CST": "test_CST",
            "X-SECURITY-TOKEN": "test_X-SECURITY-TOKEN"
        }

        responses.post(
            mock_url,
            json=mock_response_json,
            status=200,
            headers=mock_response_headers,
        )
        
        ig_api = IG_API(**self.mock_user_info_demo)
        
        assert ig_api.acc_info['accounts'][0]['accountName'] == mock_response_json['accounts'][0]['accountName']
        assert ig_api.acc_info['accounts'][1]['accountName'] == mock_response_json['accounts'][1]['accountName']
        assert ig_api.acc_info['clientId'] == mock_response_json['clientId']
        assert ig_api.acc_info['accountInfo']['balance'] == mock_response_json['accountInfo']['balance']
        assert ig_api.header_base['CST'] == mock_response_headers['CST']
