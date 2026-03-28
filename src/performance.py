import numpy as np
import pandas as pd


class Performance:

    @staticmethod
    def sharpe_ratio(returns):

        if returns.std() == 0:
            return 0

        return np.sqrt(252) * returns.mean() / returns.std()

    @staticmethod
    def sortino_ratio(returns):

        downside = returns[returns < 0]

        if downside.std() == 0:
            return 0

        return np.sqrt(252) * returns.mean() / downside.std()

    @staticmethod
    def max_drawdown(cumulative):

        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak

        return drawdown.min()

    @staticmethod
    def volatility(returns):

        return returns.std() * np.sqrt(252)

    @staticmethod
    def win_rate(returns):

        return (returns > 0).mean()

    @staticmethod
    def total_return(cumulative):

        return cumulative.iloc[-1] / cumulative.iloc[0] - 1

    @staticmethod
    def compute_all(equity_curve):

        returns = equity_curve.pct_change().dropna()

        metrics = {
            "Total Return": Performance.total_return(equity_curve),
            "Sharpe Ratio": Performance.sharpe_ratio(returns),
            "Sortino Ratio": Performance.sortino_ratio(returns),
            "Max Drawdown": Performance.max_drawdown(equity_curve),
            "Volatility": Performance.volatility(returns),
            "Win Rate": Performance.win_rate(returns),
        }

        return metrics