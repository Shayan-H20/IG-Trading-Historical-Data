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


mock_prices_dates_time_interval = pd.DataFrame(
    data={
        "open_px_bid": [12695.20, 12696.50, 12699.80, 12725.80, 12730.60, 12726.10],
        "high_px_bid": [12699.50, 12702.80, 12704.40, 12734.20, 12732.50, 12726.80],
        "low_px_bid": [12693.00, 12695.80, 12698.40, 12724.80, 12725.60, 12718.60],
        "close_px_bid": [12696.40, 12699.60, 12704.10, 12730.70, 12726.20, 12720.90],
        "open_px_ask": [12705.70, 12707.00, 12709.70, 12735.70, 12740.50, 12736.60],
        "high_px_ask": [12710.00, 12713.30, 12714.90, 12744.30, 12742.40, 12736.80],
        "low_px_ask": [12703.50, 12705.70, 12708.90, 12734.70, 12736.10, 12729.10],
        "close_px_ask": [12706.90, 12709.50, 12714.60, 12740.60, 12736.70, 12730.80],
        "open_px_mid": [12700.45, 12701.75, 12704.75, 12730.75, 12735.55, 12731.35],
        "high_px_mid": [12704.75, 12708.05, 12709.65, 12739.25, 12737.45, 12731.80],
        "low_px_mid": [12698.25, 12700.75, 12703.65, 12729.75, 12730.85, 12723.85],
        "close_px_mid": [12701.65, 12704.55, 12709.35, 12735.65, 12731.45, 12725.85],
        "open_px_spread": [10.50, 10.50, 9.90, 9.90, 9.90, 10.50],
        "high_px_spread": [10.50, 10.50, 10.50, 10.10, 9.90, 10.00],
        "low_px_spread": [10.50, 9.90, 10.50, 9.90, 10.50, 10.50],
        "close_px_spread": [10.50, 9.90, 10.50, 9.90, 10.50, 9.90],
        "last_traded_volume": [958.00, 769.00, 809.00, 742.00, 861.00, 599.00],
    },
    index=pd.DatetimeIndex(
        [
            '2024-01-08 10:00:00', 
            '2024-01-08 10:15:00',
            '2024-01-08 10:30:00', 
            '2024-01-10 10:00:00',
            '2024-01-10 10:15:00', 
            '2024-01-10 10:30:00'
        ],
        dtype='datetime64[ns]', 
        freq=None
    )
)


mock_prices_dates_no_time_interval = pd.DataFrame(
    data={
        "open_px_bid": [12717.00, 12701.40, 12707.90, 12698.10, 12750.20, 12758.30, 12741.00, 12755.80, 12747.20, 12712.70, 12703.20, 12699.30, 12710.40],
        "high_px_bid": [12729.80, 12719.90, 12713.30, 12756.00, 12767.00, 12758.40, 12765.10, 12755.80, 12747.20, 12735.20, 12718.50, 12711.10, 12717.40],
        "low_px_bid": [12698.80, 12697.90, 12673.20, 12697.80, 12739.90, 12740.10, 12740.60, 12733.80, 12706.90, 12700.50, 12689.00, 12698.00, 12698.10],
        "close_px_bid": [12701.50, 12708.00, 12698.00, 12750.10, 12759.10, 12741.10, 12755.90, 12747.10, 12712.80, 12703.10, 12699.20, 12710.10, 12699.10],
        "open_px_ask": [12727.50, 12711.90, 12718.40, 12708.60, 12760.10, 12768.20, 12751.50, 12766.30, 12757.10, 12722.60, 12713.10, 12709.80, 12720.90],
        "high_px_ask": [12740.30, 12730.40, 12723.50, 12765.90, 12776.90, 12768.30, 12775.10, 12766.30, 12757.10, 12745.10, 12728.40, 12727.00, 12727.90],
        "low_px_ask": [12709.30, 12708.40, 12683.70, 12708.30, 12749.80, 12750.80, 12751.10, 12744.10, 12716.80, 12710.70, 12698.90, 12709.70, 12708.00],
        "close_px_ask": [12712.00, 12718.50, 12708.50, 12760.00, 12769.00, 12751.60, 12766.40, 12757.00, 12722.70, 12713.00, 12709.70, 12720.60, 12709.00],
        "open_px_mid": [12722.25, 12706.65, 12713.15, 12703.35, 12755.15, 12763.25, 12746.25, 12761.05, 12752.15, 12717.65, 12708.15, 12704.55, 12715.65],
        "high_px_mid": [12735.05, 12725.15, 12718.40, 12760.95, 12771.95, 12763.35, 12770.10, 12761.05, 12752.15, 12740.15, 12723.45, 12719.05, 12722.65],
        "low_px_mid": [12704.05, 12703.15, 12678.45, 12703.05, 12744.85, 12745.45, 12745.85, 12738.95, 12711.85, 12705.60, 12693.95, 12703.85, 12703.05],
        "close_px_mid": [12706.75, 12713.25, 12703.25, 12755.05, 12764.05, 12746.35, 12761.15, 12752.05, 12717.75, 12708.05, 12704.45, 12715.35, 12704.05],
        "open_px_spread": [10.50, 10.50, 10.50, 10.50, 9.90, 9.90, 10.50, 10.50, 9.90, 9.90, 9.90, 10.50, 10.50],
        "high_px_spread": [10.50, 10.50, 10.20, 9.90, 9.90, 9.90, 10.00, 10.50, 9.90, 9.90, 9.90, 15.90, 10.50],
        "low_px_spread": [10.50, 10.50, 10.50, 10.50, 9.90, 10.70, 10.50, 10.30, 9.90, 10.20, 9.90, 11.70, 9.90],
        "close_px_spread": [10.50, 10.50, 10.50, 9.90, 9.90, 10.50, 10.50, 9.90, 9.90, 9.90, 10.50, 10.50, 9.90],
        "last_traded_volume": [5857.00, 7081.00, 14765.00, 18279.00, 10506.00, 4620.00, 7065.00, 6624.00, 12783.00, 18642.00, 12267.00, 4481.00, 5666.00],
    },
    index=pd.DatetimeIndex(
        [
            '2024-01-08 00:00:00',
            '2024-01-08 04:00:00',
            '2024-01-08 08:00:00',
            '2024-01-08 12:00:00',
            '2024-01-08 16:00:00',
            '2024-01-08 20:00:00',
            '2024-01-09 00:00:00',
            '2024-01-09 04:00:00',
            '2024-01-09 08:00:00',
            '2024-01-09 12:00:00',
            '2024-01-09 16:00:00',
            '2024-01-09 20:00:00',
            '2024-01-10 00:00:00'
        ],
        dtype='datetime64[ns]', 
        freq=None
    )
)
