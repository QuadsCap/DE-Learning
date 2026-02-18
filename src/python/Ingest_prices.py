# ingest_prices.py
# Purpose:
# - Read a CSV file from /data
# - Insert those rows into Postgres table raw.prices_daily
# - Make it "repeatable": each run reloads the table cleanly (TRUNCATE + INSERT)


#What this script does:
#1) Reads the CSV into a pandas DataFrame
#2) Validates required columns exist: date, symbol, close
#3) Parses the date column into a proper date type
#4) TRUNCATES (clears) the destination table to avoid duplicate loads
#5) Inserts the data into raw.prices_daily
#6) Prints a success message with number of rows loaded

#Prerequisites:
#- Docker Postgres is running: docker compose up -d
#- Table exists: raw.prices_daily (created via your SQL script in DBeaver)
#- CSV exists at: data/prices_daily.csv
#- Python packages installed:
#  pip install pandas sqlalchemy psycopg2-binary python-dotenv
#"""

import pandas as pd
from db import get_engine

# Path to your CSV relative to repo root
CSV_PATH = "data/prices_daily.csv"


def main():
    # 1) Create DB engine (reads .env)
    engine = get_engine()

    # 2) Read CSV
    df = pd.read_csv(CSV_PATH)

    # 3) Validate CSV structure (fail early with clear message)
    required_cols = {"date", "symbol", "close"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"CSV must contain columns {required_cols}. "
            f"Found columns: {set(df.columns)}"
        )

    # 4) Parse and standardize types
    #    Convert date strings (YYYY-MM-DD) into Python date objects
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.date

    # 5) Load to Postgres in a transaction (engine.begin() auto-commits if successful)
    with engine.begin() as conn:
        # 5a) Clear destination table so rerunning script doesn't duplicate rows
        conn.exec_driver_sql("TRUNCATE TABLE raw.prices_daily;")

        # 5b) Append all rows from DataFrame into raw.prices_daily
        #     schema="raw" tells pandas which schema the table is in
        #     if_exists="append" means insert rows into existing table
        df.to_sql(
            name="prices_daily",
            schema="raw",
            con=conn,
            if_exists="append",
            index=False,
            method="multi"  # faster inserts
        )

    # 6) Print a clear success message
    print(f"OK: Loaded {len(df)} rows into raw.prices_daily from {CSV_PATH}")


if __name__ == "__main__":
    r"""How to run (from repo root):
    - Activate venv:
        .\.venv\Scripts\activate
    - Run:
        python src\python\ingest_prices.py
    """
    main()