"""
verify_prices.py

Goal:
- Confirm that data exists in raw.prices_daily after ingestion.

What this script does:
1) Connects to Postgres (using .env)
2) Runs row count query
3) Shows latest date per symbol
4) Fails (raises error) if the table is empty
5) Prints OK if verification passes

How to run (from repo root):
  python src\python\verify_prices.py
"""

from db import get_engine


def main():
    engine = get_engine()

    with engine.begin() as conn:
        # 1) Count rows
        count = conn.exec_driver_sql(
            "SELECT COUNT(*) FROM raw.prices_daily;"
        ).scalar_one()

        # 2) Basic “sanity” query: latest date per symbol
        latest = conn.exec_driver_sql("""
            SELECT symbol, MAX(date) AS latest_date
            FROM raw.prices_daily
            GROUP BY symbol
            ORDER BY symbol;
        """).all()

    # 3) Print results in a readable way
    print(f"Row count: {count}")
    print("Latest date per symbol:")
    for sym, dt in latest:
        print(f"  {sym}: {dt}")

    # 4) Fail if table is empty (useful for automation/CI later)
    if count == 0:
        raise RuntimeError("ERROR: raw.prices_daily is empty (expected rows after ingestion).")

    print("OK: Verification passed")


if __name__ == "__main__":
    main()