# db.py
# Purpose:
# - Central place for database connection logic
# - So other scripts can do: "from db import get_conn"

import os                  # Read environment variables (PGHOST, etc.)
import psycopg             # PostgreSQL driver (psycopg v3)
from psycopg.rows import dict_row  # Makes query results return as dicts instead of tuples


def get_conn():
    """
    Returns a new connection to Postgres.
    We read settings from environment variables so we don't hardcode secrets.
    """
    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),      # where Postgres runs (local Docker)
        port=int(os.getenv("PGPORT", "5432")),      # default Postgres port
        dbname=os.getenv("PGDATABASE", "de_db"),    # database name
        user=os.getenv("PGUSER", "de_user"),        # username
        password=os.getenv("PGPASSWORD", "de_pass"),# password
        row_factory=dict_row,                       # fetchone() returns {"col": value}
    )