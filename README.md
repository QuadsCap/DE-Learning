# DE-Learning
-The program makes it possible to run a PostGres database locally via a Docker container, and from there perform ETL type operations on said data, preparing it for analysis.

## Features
-Extract data from files
-Normalize fields (Put into a unified schema)
-Load transformed data into PostGres
-Query and inspect results via DBbeaver

## Prerequisits
Dependencies

Programs
-Docker Desktop
-DBbeaver
-Python 3.10 or higher

Python tooling
-pip
-venv


## Installation
git clone https://github.com/QuadsCap/DE-Learning
cd DE-Learning
python -m venv .venv

Activate venv:
macOS / Linux:
source .venv/bin/activate
Windows (PowerShell):
.venv\Scripts\Activate.ps1
Windows (cmd):
.venv\Scripts\activate.bat

pip install -r requirements.txt

## Setup

1) Start the PostGres database (Docker)
If the repo includes a docker-compose.yml:
docker compose up -d

Confirm the container is running:
docker ps

Stop it later with:
docker compose down

2) Environment variables (if used)
If your project uses environment variables, create a .env file (or copy .env.example if it exists).
Example (edit to match your docker-compose.yml):
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=de_learning
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

3) Connect with DBbeaver
Create a new PostgreSQL connection:
-Host: localhost
-Port: 5432
-Database: de_learning (or whatever your docker-compose/.env uses)
-Username: postgres
-Password: postgres

Then Test Connection -> Finish

## Run the pipeline
(Replace these with the actual commands used in the repo)

Option A: run a script
python src/main.py

Option B: run as a module
python -m src.main

## Project structure (example)
DE-Learning/
-data/                  # raw input files (csv, json, etc.)
-src/
--extract/              # reading/parsing input files
--transform/            # cleaning/normalizing
--load/                 # DB inserts/upserts
--main.py               # pipeline entry point
-docker-compose.yml     # PostGres container
-requirements.txt
-README.md

## Verify results
In DBbeaver, open a SQL editor and run:
SELECT * FROM your_table_name LIMIT 50;

Row counts:
SELECT COUNT(*) FROM your_table_name;

## Troubleshooting

-Port already in use (5432)
If 5432 is taken, change the host port in docker-compose.yml (example: 5433:5432)
Then update POSTGRES_PORT and your DBbeaver connection to 5433.

-Windows PowerShell can’t activate venv
Run:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
Then re-activate:
.venv\Scripts\Activate.ps1

-Connection refused from Python
-Make sure Docker is running and the container is up (docker ps)
-Confirm host/port match docker-compose.yml
-Confirm .env matches your DBbeaver connection

## Run the pipeline (recommended)
This project supports automated ingestion + verification (no manual DBeaver import required):

```powershell
.\run_pipeline.ps1


Verification in Dbbeaver

SELECT COUNT(*) FROM raw.prices_daily;

SELECT symbol, MAX(date) AS latest_date
FROM raw.prices_daily
GROUP BY symbol
ORDER BY symbol;