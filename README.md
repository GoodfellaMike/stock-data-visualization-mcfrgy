# Stock Data Visualization on the Web — Project 3a

This project extends the original command-line visualizer with a Flask web form, CSV-loaded stock choices, input validation, embedded Plotly charts, and Docker Compose.

## Run locally (Windows PowerShell)

1. Open this folder in VS Code.
2. Run `py -m pip install -r requirements.txt`.
3. Create `.env` with `ALPHA_VANTAGE_API_KEY=your_key`. Do not commit this file.
4. Run `py app.py`.
5. Visit http://localhost:5000.

## Run with Docker Desktop

1. Make sure Docker Desktop is running.
2. Stop any local Python server on port 5000.
3. Run `docker compose up --build`.
4. Visit http://localhost:5000.
5. Stop with Ctrl+C (or `docker compose down`).

## Notes

- The original CLI is available through `py main.py`.
- The symbol dropdown loads from `data/stocks.csv`, a snapshot of stock symbols; it is not a live index membership feed.
- Alpha Vantage may rate-limit requests, and free plans may restrict historical data or intraday availability. An on-screen error explains failures.
- Stock market days without trades (weekends/holidays) have no price records.
- For GitHub, exclude `.env` and use `.env.example` instead.
