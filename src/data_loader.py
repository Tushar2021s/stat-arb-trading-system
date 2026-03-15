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
            end=self.end
        )["Adj Close"]

        return data.dropna()
