"""Flask website for the original Project 3 stock visualizer."""
import csv
import logging
from datetime import date, timedelta
from pathlib import Path

import requests
from flask import Flask, render_template, request
from plotly.io import to_html

from api_client import get_stock_data, extract_time_series
from validation import validate_date_range
from visualization import generate_chart

app = Flask(__name__)
DATA_FILE = Path(__file__).parent / "data" / "stocks.csv"
CHART_TYPES = {"line": "Line", "bar": "Bar"}
TIME_SERIES = {"daily": "Daily", "weekly": "Weekly", "monthly": "Monthly", "intraday": "Intraday (60 min)"}


def load_stocks():
    """Read the dropdown choices from the external CSV file."""
    with DATA_FILE.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        stocks = [(row["Symbol"].strip().upper(), row["Security"].strip()) for row in reader if row.get("Symbol") and row.get("Security")]
    return sorted(set(stocks))


def form_defaults():
    today = date.today()
    return {"symbol": "AAPL", "chart_type": "line", "time_series": "daily",
            "start_date": (today - timedelta(days=30)).isoformat(), "end_date": today.isoformat()}


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    chart_html = None
    choices = load_stocks()
    fields = form_defaults()
    if request.method == "POST":
        fields = {k: request.form.get(k, "").strip() for k in fields}
        try:
            allowed_symbols = {symbol for symbol, _ in choices}
            fields["symbol"] = fields["symbol"].upper()
            if fields["symbol"] not in allowed_symbols:
                raise ValueError("Please select a valid stock symbol from the list.")
            if fields["chart_type"] not in CHART_TYPES:
                raise ValueError("Please choose a valid chart type.")
            if fields["time_series"] not in TIME_SERIES:
                raise ValueError("Please choose a valid time series.")
            if not fields["start_date"]:
                raise ValueError("Please enter a start date.")
            if not fields["end_date"]:
                raise ValueError("Please enter an end date.")
            start_date, end_date = validate_date_range(fields["start_date"], fields["end_date"])
            response = get_stock_data(fields["symbol"], fields["time_series"])
            data = extract_time_series(response)
            figure = generate_chart(data, fields["symbol"], fields["chart_type"],
                                    start_date, end_date, show_browser=False)
            chart_html = to_html(figure, full_html=False, include_plotlyjs=True)
        except (ValueError, requests.RequestException) as exc:
            error = str(exc)
        except Exception:
            app.logger.exception("Unexpected chart generation problem")
            error = "Something went wrong generating the chart. Please try again."
    return render_template("index.html", stocks=choices, fields=fields,
                           chart_types=CHART_TYPES, time_series=TIME_SERIES,
                           error=error, chart_html=chart_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
