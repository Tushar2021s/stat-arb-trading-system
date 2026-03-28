import pandas as pd
import numpy as np

class Backtester:

    def __init__(self, prices, signals, initial_capital=100000):

        self.prices = prices
        self.signals = signals
        self.initial_capital = initial_capital

        # Step 1 params
        self.transaction_cost = 0.001
        self.slippage = 0.0005

        #  Step 2 params
        self.stop_loss = 0.02       # 2% loss
        self.take_profit = 0.04     # 4% profit
        self.position_size_pct = 0.1  # 10% capital per trade

    def run(self):

        capital = self.initial_capital
        position = 0
        entry_price = 0

        equity_curve = []

        for i in range(1, len(self.prices)):

            price = self.prices.iloc[i]
            prev_price = self.prices.iloc[i - 1]
            signal = self.signals.iloc[i]

            # 🔥 POSITION SIZING
            position_size = capital * self.position_size_pct

            # =========================
            # ENTRY LOGIC
            # =========================
            if position == 0:

                if signal == 1:
                    position = 1
                    entry_price = price

                elif signal == -1:
                    position = -1
                    entry_price = price

                # apply cost on entry
                if position != 0:
                    cost = position_size * (self.transaction_cost + self.slippage)
                    capital -= cost

            # =========================
            # EXIT LOGIC (RISK CONTROL)
            # =========================
            else:

                pnl_pct = (price - entry_price) / entry_price * position

                #  STOP LOSS / TAKE PROFIT
                if pnl_pct <= -self.stop_loss or pnl_pct >= self.take_profit:

                    pnl = pnl_pct * position_size
                    capital += pnl

                    # exit cost
                    cost = position_size * (self.transaction_cost + self.slippage)
                    capital -= cost

                    position = 0
                    entry_price = 0

            # =========================
            # MARK-TO-MARKET PnL
            # =========================
            if position != 0:
                price_change = (price - prev_price) / prev_price
                pnl = position * price_change * position_size
                capital += pnl

            equity_curve.append(capital)

        return pd.Series(equity_curve, index=self.prices.index[1:])