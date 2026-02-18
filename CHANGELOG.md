# Changelog

All notable changes to this project will be documented in this file.

This project is a beginner-friendly data engineering lab to practice:
- running PostgreSQL locally with Docker Compose
- managing/querying the DB with DBeaver
- loading data from CSV into Postgres (manual import first, then Python automation)
- keeping everything reproducible in a GitHub repo


## [Unreleased]
### Planned
- Add basic data quality checks (duplicate keys, null checks)
- Improve README with “Quickstart” section (start DB → create tables → ingest → verify)


## [0.2.1] - 2026-02-18
### Added
- `src/python/ingest_prices.py` — CSV → Postgres load
- `src/python/verify_prices.py` — verification checks
- `src/python/db.py` — shared connection helper
- `run_pipeline.ps1` — one-command runner

### Changed
- Preferred workflow is now Python ingestion + verification (manual DBeaver import is optional)
- Usage guide is local-only (removed from Git tracking)


## [0.1.0] - 2026-02-16
### Added
- Initial GitHub repository structure for **DE-Learning**
- `.gitignore` to prevent committing secrets (notably `.env`)
- `.env.example` to document required environment variables for local setup
- Docker-based PostgreSQL setup using `docker-compose.yml`
- Initial SQL scripts to create:
  - schema: `raw`
  - table: `raw.prices_daily (date, symbol, close)`
  - index: `idx_prices_daily_symbol_date (symbol, date)`
- Starter dataset file (CSV) for ingestion: `data/prices_daily.csv`
- Documented workflows for:
  - starting/stopping Postgres with Docker Compose
  - connecting to Postgres with DBeaver
  - creating schema/table/index via SQL script
  - importing CSV into Postgres via DBeaver UI
