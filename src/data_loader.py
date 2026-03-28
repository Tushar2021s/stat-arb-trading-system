import yfinance as yf
import pandas as pd


class DataLoader:

    def __init__(self, tickers, start, end):
        self.tickers = tickers
        self.start = start
        self.end = end

    def fetch_data(self):

        data = yf.download(
            self.tickers,
            start=self.start,
            end=self.end,
            progress=False
        )

        # HANDLE DIFFERENT STRUCTURES

        # Case 1: Multiple tickers → MultiIndex
        if isinstance(data.columns, pd.MultiIndex):

            if "Adj Close" in data.columns.levels[0]:
                data = data["Adj Close"]
            else:
                data = data["Close"]

        # Case 2: Single ticker → normal columns
        else:

            if "Adj Close" in data.columns:
                data = data["Adj Close"]
            else:
                data = data["Close"]

        return data.dropna()