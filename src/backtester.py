import pandas as pd

class Backtester:

    def __init__(self, prices, signals):

        self.prices = prices
        self.signals = signals

    def run(self):

        returns = self.prices.pct_change()

        strategy_returns = returns * self.signals.shift(1)

        cumulative_returns = (1 + strategy_returns).cumprod()

        return cumulative_returns
