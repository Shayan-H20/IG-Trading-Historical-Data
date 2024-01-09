from ig_trading_historical_data import IG_API
import user_info
import pytest


#@pytest.fixture
#def logged_in_instance():
#    pass

def test_can_login_via_init():
    # user info to log in
    DEMO = 1
    username = user_info.username_demo
    pw = user_info.pw_demo
    api_key = user_info.api_key_demo

    ig_api = IG_API(DEMO, username, pw, api_key)
    
    assert ig_api.acc_info.keys()




pytest.main()