"""Module 13: Unit tests for the five Stock Visualizer inputs."""

import unittest
from datetime import datetime


def valid_symbol(value):
    return isinstance(value, str) and 1 <= len(value) <= 7 and value.isascii() and value.isalpha() and value.isupper()


def valid_chart_type(value):
    return isinstance(value, str) and value in ("1", "2")


def valid_time_series(value):
    return isinstance(value, str) and value in ("1", "2", "3", "4")


def valid_date(value):
    if not isinstance(value, str) or len(value) != 10:
        return False
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d") == value
    except ValueError:
        return False


class TestStockVisualizerInputs(unittest.TestCase):
    def test_symbol_valid(self):
        for symbol in ("A", "AAPL", "GOOGL", "ABCDEFG"):
            with self.subTest(symbol=symbol):
                self.assertTrue(valid_symbol(symbol))

    def test_symbol_invalid(self):
        for symbol in ("", "aapl", "AaPL", "ABCDEFGH", "AAPL1", "AAPL!", "A A", "É", None):
            with self.subTest(symbol=symbol):
                self.assertFalse(valid_symbol(symbol))

    def test_chart_type_valid(self):
        for chart_type in ("1", "2"):
            with self.subTest(chart_type=chart_type):
                self.assertTrue(valid_chart_type(chart_type))

    def test_chart_type_invalid(self):
        for chart_type in ("", "0", "3", "12", "a", " 1", 1, None):
            with self.subTest(chart_type=chart_type):
                self.assertFalse(valid_chart_type(chart_type))

    def test_time_series_valid(self):
        for series in ("1", "2", "3", "4"):
            with self.subTest(series=series):
                self.assertTrue(valid_time_series(series))

    def test_time_series_invalid(self):
        for series in ("", "0", "5", "12", "a", " 2", 2, None):
            with self.subTest(series=series):
                self.assertFalse(valid_time_series(series))

    def test_start_date_valid(self):
        for date in ("2026-01-01", "2024-02-29", "2026-11-18"):
            with self.subTest(date=date):
                self.assertTrue(valid_date(date))

    def test_start_date_invalid(self):
        for date in ("", "01-01-2026", "2026-1-01", "2026-02-29", "2026-13-01", "2026-01-32", "2026/01/01", None):
            with self.subTest(date=date):
                self.assertFalse(valid_date(date))

    def test_end_date_valid(self):
        for date in ("2025-12-31", "2024-02-29", "2026-11-18"):
            with self.subTest(date=date):
                self.assertTrue(valid_date(date))

    def test_end_date_invalid(self):
        for date in ("", "12-31-2025", "2025-12-1", "2025-02-29", "2025-00-10", "2025-12-40", "hello", None):
            with self.subTest(date=date):
                self.assertFalse(valid_date(date))


if __name__ == "__main__":
    unittest.main()
