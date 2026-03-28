import pandas as pd
import numpy as np

class PortfolioBacktester:

    def __init__(self, prices, signals_dict, initial_capital=100000):

        self.prices = prices
        self.signals_dict = signals_dict
        self.initial_capital = initial_capital

        self.transaction_cost = 0.001
        self.slippage = 0.0005

        self.position_size_pct = 0.1

    def run(self):

        capital = self.initial_capital
        equity_curve = []

        positions = {pair: 0 for pair in self.signals_dict}
        entry_prices = {pair: 0 for pair in self.signals_dict}

        for t in range(1, len(self.prices)):

            for pair, signals in self.signals_dict.items():

                i, j = pair

                price1 = self.prices.iloc[t, i]
                price2 = self.prices.iloc[t, j]

                spread = price1 - price2
                signal = signals.iloc[t]

                position = positions[pair]
                position_size = capital * self.position_size_pct / len(self.signals_dict)

                # ENTRY
                if position == 0:
                    if signal == 1:
                        positions[pair] = 1
                        entry_prices[pair] = spread

                    elif signal == -1:
                        positions[pair] = -1
                        entry_prices[pair] = spread

                # EXIT
                else:
                    pnl = (spread - entry_prices[pair]) * position
                    capital += pnl * position_size * 0.01

                    positions[pair] = 0

                # COST
                if positions[pair] != position:
                    cost = position_size * (self.transaction_cost + self.slippage)
                    capital -= cost

            equity_curve.append(capital)

        return pd.Series(equity_curve, index=self.prices.index[1:])