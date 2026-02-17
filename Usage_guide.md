DE-Learning — Complete Usage Guide (Local Data Engineering Lab)
What you built (high level)

A local “mini data engineering lab” where you can:

run a PostgreSQL database locally using Docker Compose

manage/query the DB using DBeaver

load data (CSV → table) either via DBeaver import or via Python ingestion scripts

keep the whole setup reproducible inside your GitHub repo

1) Setup overview (Program → Program)
A) GitHub (remote)

Purpose: store your project, code, notes, and setup so it’s portfolio-ready.

What you did:

Created repo: DE-Learning

Added:

README.md (project front page)

.gitignore (so secrets like .env don’t get pushed)

B) Windows + VS Code (local workspace)

Purpose: edit code/files and run commands in the integrated terminal.

What you did:

Cloned the repo locally (recommended location):

C:\dev\DE-Learning

Opened the folder in VS Code:

File → Open Folder → C:\dev\DE-Learning

You use the VS Code terminal for commands (PowerShell inside VS Code).

C) Docker Desktop + Docker Compose (database runtime)

Purpose: run PostgreSQL without installing it “natively” on Windows.

What you did:

Installed Docker Desktop

Created:

.env (your local DB config; NOT committed)

.env.example (template; committed)

docker-compose.yml (the recipe that starts Postgres using .env)

Your .gitignore includes:

.env

D) PostgreSQL (the database)

Purpose: store data in tables and learn real DE workflows.

What you did:

PostgreSQL runs inside Docker as a container (service).

E) DBeaver (SQL client)

Purpose: connect to Postgres, run SQL scripts, browse schemas/tables, import CSVs.

What you did:

Created a connection to your Postgres container

Ran SQL to create schema/table/index

Imported CSV into the table (or prepared to)

F) Python (ingestion scripts)

Purpose: automate loading data into Postgres (a real DE skill).

What you did (or are about to do):

Create ingestion scripts in the repo (so you don’t rely on manual import forever)

2) Files in the repo (what each is for)
.env (local only)

Holds your DB settings (example format):

POSTGRES_USER=...

POSTGRES_PASSWORD=...

POSTGRES_DB=...

POSTGRES_PORT=5432

✅ Must be ignored by Git.

.env.example (committed)

A safe template so others know what keys exist.

docker-compose.yml (committed)

Defines how to run Postgres (image, ports, env file, persistent volume).

SQL file (example: src/sql/01_create_tables.sql)

Contains your schema/table creation SQL (raw schema, prices table, index).

Data file (example: data/prices_daily.csv)

The CSV you import/ingest.

3) Day-to-day usage workflows
Workflow A — Start/Stop your database (Docker Compose)
Start Postgres

Open Docker Desktop and ensure it says Running

In VS Code terminal, go to repo root:

cd C:\dev\DE-Learning


Start:

docker compose up -d

Check it’s running
docker compose ps

Stop the database (but keep data)
docker compose down

Reset everything (DANGER: deletes stored DB data)

Only if you want to wipe the database completely:

docker compose down -v

Workflow B — Connect DBeaver to Postgres
Create connection

Open DBeaver

Database → New Database Connection → PostgreSQL

Fill:

Host: localhost

Port: 5432 (or your POSTGRES_PORT)

Database: value from POSTGRES_DB

Username: value from POSTGRES_USER

Password: value from POSTGRES_PASSWORD

Click Test Connection

If asked to download driver → Download

Verify you’re connected

Open SQL Editor in DBeaver and run:

SELECT version();

Workflow C — Create schema/table/index (run SQL)
Where to run it

You run this SQL inside DBeaver (recommended for now).

Steps

Open SQL Editor for your connection

Paste your script (CREATE SCHEMA / CREATE TABLE / CREATE INDEX)

Run it:

In DBeaver: Execute SQL script (or Ctrl+Enter depending on selection)

Confirm table exists

In Database Navigator:

connection → Schemas → raw → Tables → prices_daily

If you don’t see it:

right-click connection → Refresh (or press F5)

4) Importing data (CSV → Postgres) — detailed “X → X → X”

You have two ways:

Option 1 (Beginner-friendly): Import using DBeaver UI
Prerequisites

Postgres running (Docker compose up)

table exists (raw.prices_daily created)

CSV exists (e.g. data/prices_daily.csv)

Steps (X → X → X)

In DBeaver left panel:

connection → Schemas → raw → Tables → prices_daily

Right-click prices_daily

Choose Import Data

Choose source type: CSV

Select file:

data/prices_daily.csv

Mapping step:

Ensure columns map correctly:

date → date

symbol → symbol

close → close

Format step (important):

Delimiter: ,

Header: ON (if your CSV has header row)

Date format: confirm it matches your file (usually YYYY-MM-DD)

Click Start

Verify with SQL:

SELECT COUNT(*) FROM raw.prices_daily;
SELECT * FROM raw.prices_daily ORDER BY date DESC LIMIT 10;

If import fails (common causes)

date format not recognized

decimal separator mismatch

column names don’t match

trying to import into wrong schema/table

Option 2 (Real DE way): Import using Python script

This is what you’ll use long-term because it’s repeatable and automated.

Prerequisites

Python venv created + dependencies installed

Postgres running

table exists

Steps (X → X → X)

Open terminal in repo root:

cd C:\dev\DE-Learning


Create and activate venv (once):

python -m venv .venv
.\.venv\Scripts\activate


Install packages (once):

pip install pandas sqlalchemy psycopg2-binary python-dotenv
pip freeze > requirements.txt


Create a script, e.g.:

src/python/ingest_prices.py

Run script:

python .\src\python\ingest_prices.py


Verify in DBeaver:

SELECT COUNT(*) FROM raw.prices_daily;

IMPORTANT about .env

Python scripts usually read .env using python-dotenv, so you don’t hardcode credentials.

5) Your current status (“where you are”)

Based on what we’ve done in this chat, you are here:

✅ Repo exists and is cloned locally
✅ .env + .env.example exist and .env is ignored
✅ docker-compose.yml exists
✅ Postgres container is running via Docker
✅ DBeaver connection screen is set up / you’re connecting
✅ You created SQL for raw.prices_daily
✅ You’re importing prices_daily.csv into that table (or about to)

Next “milestone” is:

confirm table exists

import CSV

verify row count

then automate it with Python (your first real pipeline)

6) Quick troubleshooting cheat sheet
“Docker won’t run / can’t connect”

Open Docker Desktop → wait for Running

In terminal:

docker version
docker compose ps

“DBeaver can’t connect”

Is Docker Postgres running?

Is port correct?

Are DB/user/password exactly matching .env?

“Python import error: No module named X”

Activate venv:

.\.venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt

7) To make this truly complete, I need 1 screenshot or 1 detail

Right now, I can make this guide even tighter if I know your exact repo structure:

Where did you place the SQL file? (example: src/sql/...)

Where did you place the Python script? (example: src/python/...)

If you paste your repo tree (just the left VS Code explorer view is enough), I’ll rewrite the guide with your exact paths, no placeholders.