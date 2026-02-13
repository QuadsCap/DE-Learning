-- Count rows
SELECT COUNT(*) AS row_count
FROM raw.prices_daily;

-- View all rows
SELECT *
FROM raw.prices_daily
ORDER BY symbol, date;

-- Rows per symbol
SELECT symbol, COUNT(*) AS rows
FROM raw.prices_daily
GROUP BY symbol
ORDER BY symbol;

-- Latest date per symbol
SELECT symbol, MAX(date) AS latest_date
FROM raw.prices_daily
GROUP BY symbol
ORDER BY symbol;

-- Daily return (window function)
SELECT
  date,
  symbol,
  close,
  (close / LAG(close) OVER (PARTITION BY symbol ORDER BY date) - 1) AS daily_return
FROM raw.prices_daily
ORDER BY symbol, date;