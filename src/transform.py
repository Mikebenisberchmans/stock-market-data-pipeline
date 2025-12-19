import pandas as pd
import numpy as np


def calculate_sma(series: pd.Series, window: int) -> pd.Series:
    """
    Simple Moving Average (SMA)
    """
    return series.rolling(window).mean()


def calculate_ema(series: pd.Series, window: int) -> pd.Series:
    """
    EMA calculation EXACTLY as requested:

    EMA_t = (Price_t - PrevEMA) * alpha + PrevEMA

    For the FIRST EMA:
    PrevEMA is taken as SMA_t (same index)
    """

    alpha = 2 / (window + 1)
    ema = pd.Series(index=series.index, dtype="float64")

    # Step 1: Calculate SMA
    sma = series.rolling(window).mean()

    start_idx = window - 1

    # Step 2: First EMA at SAME index as SMA
    ema.iloc[start_idx] = (
        (series.iloc[start_idx] - sma.iloc[start_idx]) * alpha
        + sma.iloc[start_idx]
    )

    # Step 3: Recursive EMA
    for i in range(start_idx + 1, len(series)):
        ema.iloc[i] = (
            (series.iloc[i] - ema.iloc[i - 1]) * alpha
            + ema.iloc[i - 1]
        )

    return ema



def resample_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Daily → Monthly OHLC aggregation
    """
    df = df.sort_values("date").set_index("date")

    monthly = df.resample("ME").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
        "adjclose": "last"
    })

    return monthly.reset_index()


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add SMA & STRICT EMA indicators on monthly close
    """
    close = df["close"]

    df["sma_10"] = calculate_sma(close, 10)
    df["sma_20"] = calculate_sma(close, 20)

    df["ema_10"] = calculate_ema(close, 10)
    df["ema_20"] = calculate_ema(close, 20)

    return df
