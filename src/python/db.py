# db.py
# Purpose:
# - Central place for database connection logic
# - So other scripts can do: "from db import get_conn" (and optionally get_engine)

import os                          # Read environment variables (PGHOST, etc.)
import psycopg                     # PostgreSQL driver (psycopg v3)
from psycopg.rows import dict_row  # Makes query results return as dicts instead of tuples

# OPTIONAL but recommended:
# Loads variables from a local .env file into environment variables,
# so os.getenv(...) works even if you didn't manually export env vars.
from dotenv import load_dotenv


# Load .env from repo root (or current working directory) if it exists.
# This does NOT overwrite already-set environment variables.
load_dotenv()


def get_conn():
    """
    Returns a new connection to Postgres.

    Reads settings from environment variables so we don't hardcode secrets.
    Expected env vars (with defaults):
      PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
    """
    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),           # where Postgres runs (local Docker)
        port=int(os.getenv("PGPORT", "5432")),           # default Postgres port
        dbname=os.getenv("PGDATABASE", "de_db"),         # database name
        user=os.getenv("PGUSER", "de_user"),             # username
        password=os.getenv("PGPASSWORD", "de_pass"),     # password
        row_factory=dict_row,                            # fetchone() returns {"col": value}
    )


def get_engine():
    """
    OPTIONAL helper for pandas/SQLAlchemy workflows (df.to_sql).

    Use this only if your ingestion script wants SQLAlchemy.
    If you prefer pure psycopg ingestion, you can ignore this function.

    Requires: sqlalchemy + psycopg[binary] or psycopg (depending on your setup)
    """
    from sqlalchemy import create_engine

    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    db = os.getenv("PGDATABASE", "de_db")
    user = os.getenv("PGUSER", "de_user")
    password = os.getenv("PGPASSWORD", "de_pass")

    # psycopg v3 SQLAlchemy URL format:
    url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)