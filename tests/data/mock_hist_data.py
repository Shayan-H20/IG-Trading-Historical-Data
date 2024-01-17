""" initialize mock historical prices DataFrames """


import pandas as pd


mock_prices_num_points = pd.DataFrame(
    data={
        "open_px_bid": [12691.00, 12687.40],
        "high_px_bid": [12691.30, 12688.40],
        "low_px_bid": [12684.40, 12685.70],
        "close_px_bid": [12687.30, 12686.20],
        "open_px_ask": [12701.50, 12697.90],
        "high_px_ask": [12701.80, 12698.90],
        "low_px_ask": [12694.90, 12696.20],
        "close_px_ask": [12697.80, 12696.70],
        "open_px_mid": [12696.25, 12692.65],
        "high_px_mid": [12696.55, 12693.65],
        "low_px_mid": [12689.65, 12690.95],
        "close_px_mid": [12692.55, 12691.45],
        "open_px_spread": [10.50, 10.50],
        "high_px_spread": [10.50, 10.50],
        "low_px_spread": [10.50, 10.50],
        "close_px_spread": [10.50, 10.50],
        "last_traded_volume": [431.00, 312.00],
    },
    index=pd.DatetimeIndex(
        ['2024-01-17 10:20:00', '2024-01-17 10:25:00'], 
        dtype='datetime64[ns]', 
        freq=None
    )
)