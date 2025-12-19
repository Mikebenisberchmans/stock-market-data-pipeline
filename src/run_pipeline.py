import pandas as pd

from transform import (
    resample_to_monthly,
    add_technical_indicators
)
from writer import write_partitioned_files


def run_pipeline(input_csv: str, output_dir: str) -> None:
    """
    Orchestrates the full pipeline:
    1. Read CSV
    2. Process each ticker independently
    3. Apply monthly aggregation
    4. Calculate SMA & STRICT EMA
    5. Write partitioned outputs
    """

    # Read input CSV
    df = pd.read_csv(input_csv, parse_dates=["date"])

    results = []

    # Process each stock separately
    for ticker, group in df.groupby("ticker"):
        monthly_df = resample_to_monthly(group)
        monthly_df = add_technical_indicators(monthly_df)
        monthly_df["ticker"] = ticker

        # Optional safety check (interview bonus)
        assert len(monthly_df) == 24, f"{ticker} does not have 24 months"

        results.append(monthly_df)

    final_df = pd.concat(results, ignore_index=True)

    # Write output files
    write_partitioned_files(final_df, output_dir)


if __name__ == "__main__":
    run_pipeline(
        input_csv=r"C:\Users\benij\bigdata_projects\fam_pay_assignment\data\raw\output_file.csv",
        output_dir="data/output"
    )
