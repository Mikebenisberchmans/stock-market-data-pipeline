# 📈 **STOCK MARKET DATA TRANSFORMATION PIPELINE**
## 📌 Project Overview

This project demonstrates an end-to-end data engineering workflow on historical stock market data.
The pipeline starts with exploratory analysis and visualization and progresses to a production-style transformation pipeline that converts daily OHLCV stock data into monthly aggregated metrics with technical indicators.

The final output is a partitioned dataset, with one CSV file per stock symbol(ticker), ready for downstream analytics or reporting.

## 📂 Project Structure
project_root/

├── README.md

├── requirements.txt

├── data

│    ├── raw

│    │   └── output_file.csv

│    └── output(result_files)

│        ├── result_AAPL.csv

│        ├── result_AMD.csv

│        ├── result_AMZN.csv

│        ├── result_AVGO.csv

│        ├── result_CSCO.csv

│        ├── result_MSFT.csv

│        ├── result_NFLX.csv

│        ├── result_PEP.csv

│        ├── result_TMUS.csv

│        └── result_TSLA.csv

├── notebooks

│    ├── exploration.ipynb

│    └── charts

│        ├── html_files

│        └── png_files
├── src

│    ├── run_pipeline.py

│    ├── transform.py

│    └── writer.py
└── venv

## 🧪 Data Exploration & Visualization

Initial exploration and profiling were performed in:

notebooks/exploration.ipynb

Activities performed:

Schema inspection and data quality checks

Date range validation

Missing value analysis

Candlestick chart visualization using Plotly

Exported charts as:

Interactive HTML

Static PNG images

## 📁 Visual outputs are stored in:

notebooks/charts/


This phase helped validate the correctness and continuity of the time-series data before transformation.

## 🔄 Transformation Logic

The production transformation is implemented in the src/ directory.

Key Steps:

Daily → Monthly Resampling

Open: First trading day of the month

Close: Last trading day of the month

High: Monthly maximum

Low: Monthly minimum

Technical Indicators (Calculated on Monthly Close)

Simple Moving Average:

SMA 10

SMA 20

Exponential Moving Average:

EMA 10

EMA 20

EMA Bootstrapping Rule (Explicit Assumption)

EMA is calculated using the formula:

EMA = (Current Price - Previous EMA) * Multiplier + Previous EMA


For the first EMA value, the corresponding SMA value at the same index is used as the “previous EMA seed”.

EMA values do not exist before SMA availability.

Partitioning

Output is split into one CSV file per stock symbol

Naming convention:

result_<TICKER>.csv

## ⚙️ Execution Flow

The pipeline is executed via:

python src/run_pipeline.py

Internal Responsibilities:

transform.py → All aggregation and indicator logic

writer.py → Output partitioning and file writing

run_pipeline.py → Pipeline orchestration

## 📥 Input Data

Stored in:

data/raw/output_file.csv


Contains 2 years of daily stock data for 10 symbols:

AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA


Columns:

date, volume, open, high, low, close, adjclose, ticker

## 📤 Output Data

Stored in:

data/output/


One CSV per stock symbol

Each file contains:

24 monthly records

Monthly OHLC values

SMA 10, SMA 20

EMA 10, EMA 20

## ✅ Practical Assumptions

The following assumptions were made deliberately and consistently:

Trading Days

Data contains only valid trading days (no weekends/holidays handling required).

Time Zone

All timestamps are assumed to be in a single consistent timezone.

Data Completeness

Each ticker has sufficient data to produce 24 monthly records.

Indicator Scope

SMA and EMA are computed only on monthly closing prices.

EMA Initialization

SMA is used as the EMA seed at the same index where SMA first becomes available.

No External TA Libraries

All calculations are implemented using native Pandas operations for transparency.

## ⚙️ Environment Setup

1. Create and activate virtual environment

python -m venv venv

### Linux / macOS / WSL

source venv/bin/activate


### Windows (PowerShell)

venv\Scripts\Activate.ps1

2. Install dependencies
pip install -r requirements.txt


All dependencies are intentionally kept minimal and limited to core Python data-engineering libraries (primarily Pandas).

## ▶️ How to Run the Pipeline
1. Ensure input data is available

Place the input CSV file at:

data/raw/output_file.csv


Expected schema:

date,volume,open,high,low,close,adjclose,ticker

2. Execute the pipeline

From the project root directory, run:

python src/run_pipeline.py
## 🧪 Unit Testing (Pytest)

This project uses pytest to validate the data transformation logic and ensure correctness of monthly aggregation and technical indicator calculations.

## Why Pytest?

Simple and readable test syntax

Automatic test discovery

Clear failure reports

Widely adopted in Python data engineering projects

## 📁 Test Structure
tests/
└── test_transformation.py


The tests focus on:

Monthly OHLC resampling logic

Correct calculation of SMA (Simple Moving Average)

Correct calculation of EMA (Exponential Moving Average) using SMA as the first EMA value

Data shape and column validations

## ▶️ How to Run Tests

Make sure you are in the project root directory and your virtual environment is activated.

pytest


To run a specific test file:

pytest tests/test_transformation.py

🔍 What Is Being Tested?
✔ Monthly Aggregation

Open → first trading day of the month

Close → last trading day of the month

High → maximum price in the month

Low → minimum price in the month

✔ SMA Calculation

Uses rolling mean over monthly closing prices

Window sizes: 10 and 20

✔ EMA Calculation (Custom Logic)

EMA is calculated using the formula:

EMA_t = (Price_t - Previous_EMA) * α + Previous_EMA


The first EMA value is initialized using the SMA value at the same index

This ensures mathematical correctness and avoids EMA values before SMA availability

## 🧠 Assumptions

EMA values are undefined before the corresponding SMA window

Unit tests use small, deterministic datasets with known expected outputs

Floating-point comparisons allow minimal tolerance using numpy.isclose

## ✅ Benefits

Ensures correctness of financial calculations

Prevents regressions during refactoring

Improves confidence in data quality before downstream consumption

## 🏁 Conclusion

This project demonstrates a realistic data engineering workflow:

Exploratory analysis → validated assumptions

Clean transformation logic → production-ready

Clear separation of concerns → maintainable code

Explicit assumptions → reproducible results

The structure and approach are designed to mirror real-world analytical data pipelines, making the outputs suitable for further financial analysis, reporting, or visualization.