import time
import pandas as pd
import yfinance as yf

class DataStreamer:

    def __init__(self, tickers, interval="1m"):
        self.tickers = tickers
        self.interval = interval

    def fetch_latest(self):

        data = yf.download(
            tickers=self.tickers,
            period="1d",
            interval=self.interval,
            progress=False
        )["Close"]

        return data.iloc[-1]

    def stream(self):

        while True:

            latest_prices = self.fetch_latest()

            yield latest_prices

            time.sleep(60)  # 1 min frequency