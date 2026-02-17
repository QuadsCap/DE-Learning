# ingest_prices.py
# Purpose:
# - Read a CSV file from /data
# - Insert those rows into Postgres table raw.prices_daily
# - Make it "repeatable": each run reloads the table cleanly (TRUNCATE + INSERT)

import os
import pandas as pd                 # Used to read CSV easily
from dotenv import load_dotenv      # Loads .env file into environment variables
from db import get_conn             # Our connection helper from db.py


def main():
    # 1) Load environment variables from .env into the process environment
    #    This is how the script learns PGHOST, PGUSER, etc.
    load_dotenv()

    # 2) Define where the CSV file is located (relative to repo root)
    csv_path = os.path.join("data", "prices_daily.csv")

    # 3) Read CSV into a pandas DataFrame (like an in-memory table)
    df = pd.read_csv(csv_path)

    # 4) Convert the date string column into actual date objects
    #    Postgres expects a date type, not "2026-02-01" as text.
    df["date"] = pd.to_datetime(df["date"]).dt.date

    # 5) Convert the DataFrame into a list of tuples for fast insertion.
    #    Each tuple matches the INSERT statement order: (date, symbol, close)
    rows = [
        (r["date"], r["symbol"], float(r["close"]))
        for r in df.to_dict("records")
    ]

    # 6) Open a database connection using our helper
    #    "with" ensures the connection closes cleanly even if something fails.
    with get_conn() as conn:
        # 7) Open a cursor (cursor = the thing that runs SQL statements)
        with conn.cursor() as cur:
            # 8) TRUNCATE clears the table quickly
            #    This makes the script repeatable for learning:
            #    each run starts fresh and loads exactly what's in the CSV.
            cur.execute("TRUNCATE TABLE raw.prices_daily;")

            # 9) Insert all rows in one call (executemany is efficient)
            cur.executemany(
                """
                INSERT INTO raw.prices_daily (date, symbol, close)
                VALUES (%s, %s, %s);
                """,
                rows,
            )

        # 10) Commit saves the changes (TRUNCATE + INSERT) to the database
        conn.commit()

    # 11) Print a success message so you know the script worked
    print(f"Inserted {len(rows)} rows into raw.prices_daily")


if __name__ == "__main__":
    # This line means: only run main() when executing this file directly:
    # python src/python/ingest_prices.py
    main()