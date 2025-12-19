import os
import pandas as pd


def write_partitioned_files(df: pd.DataFrame, output_dir: str) -> None:
    """
    Writes one CSV file per stock ticker.

    Output format:
    result_<TICKER>.csv
    """
    os.makedirs(output_dir, exist_ok=True)

    for ticker, group in df.groupby("ticker"):
        output_path = os.path.join(output_dir, f"result_{ticker}.csv")
        group.to_csv(output_path, index=False)
