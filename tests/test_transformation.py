import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.transform import (
    calculate_sma,
    calculate_ema,
    resample_to_monthly,
    add_technical_indicators
)
# to test resample logic
def test_resample_to_monthly_ohlc():
    data = {
        "date": pd.to_datetime([
            "2023-01-01", "2023-01-02", "2023-01-03",
            "2023-02-01", "2023-02-02"
        ]),
        "open":  [10, 12, 14, 20, 22],
        "high":  [15, 16, 18, 25, 26],
        "low":   [9, 11, 13, 19, 21],
        "close": [14, 15, 17, 24, 25],
        "volume":[100, 100, 100, 200, 200],
        "adjclose":[14, 15, 17, 24, 25]
    }

    df = pd.DataFrame(data)

    monthly = resample_to_monthly(df)

    # January checks
    jan = monthly.iloc[0]
    assert jan["open"] == 10
    assert jan["close"] == 17
    assert jan["high"] == 18
    assert jan["low"] == 9
    assert jan["volume"] == 300

    # February checks
    feb = monthly.iloc[1]
    assert feb["open"] == 20
    assert feb["close"] == 25
    assert feb["high"] == 26
    assert feb["low"] == 19
    assert feb["volume"] == 400
# to ensure SMA calculations
def test_calculate_sma():
    series = pd.Series([10, 20, 30, 40, 50])

    sma = calculate_sma(series, window=5)

    assert np.isnan(sma.iloc[0:4]).all()
    assert sma.iloc[4] == 30
# to ensure EMA calculation
def test_calculate_ema_same_index_seed():
    series = pd.Series([10, 20, 30, 40, 50])
    window = 5
    alpha = 2 / (window + 1)

    ema = calculate_ema(series, window)

    sma_value = np.mean([10, 20, 30, 40, 50])

    expected_ema = (50 - sma_value) * alpha + sma_value

    assert np.isnan(ema.iloc[0:4]).all()
    assert np.isclose(ema.iloc[4], expected_ema)

def test_calculate_ema_recursive():
    series = pd.Series([10, 20, 30, 40, 50, 60])
    window = 5
    alpha = 2 / (window + 1)

    ema = calculate_ema(series, window)

    sma_value = np.mean([10, 20, 30, 40, 50])
    first_ema = (50 - sma_value) * alpha + sma_value
    second_ema = (60 - first_ema) * alpha + first_ema

    assert np.isclose(ema.iloc[5], second_ema)

