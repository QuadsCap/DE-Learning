-- Creates a schema named "raw" (a namespace/folder for tables)
-- IF NOT EXISTS = safe to rerun; won’t error if it already exists
CREATE SCHEMA IF NOT EXISTS raw;

-- Deletes the table raw.prices_daily if it exists (clean reset during development)
-- IF EXISTS = safe to rerun; won’t error if the table isn’t there
DROP TABLE IF EXISTS raw.prices_daily;

-- Creates a table called prices_daily inside the raw schema
CREATE TABLE raw.prices_daily (
  -- Column "date": DATE type (YYYY-MM-DD, no time)
  -- NOT NULL = every row must have a date value
  date   DATE NOT NULL,

  -- Column "symbol": TEXT type (e.g., BTC, ETH)
  -- NOT NULL = every row must have a symbol value
  symbol TEXT NOT NULL,

  -- Column "close": precise decimal number
  -- NUMERIC(18,6) = up to 18 digits total, 6 digits after the decimal
  -- NOT NULL = every row must have a close price
  close  NUMERIC(18, 6) NOT NULL
);

-- Helpful index for time-series queries (faster lookups by symbol + date)
-- IF NOT EXISTS = safe to rerun; won’t error if the index already exists
CREATE INDEX IF NOT EXISTS idx_prices_daily_symbol_date
  -- Build the index on these columns, in this order (symbol first, then date)
  ON raw.prices_daily(symbol, date);