import numpy as np

class Performance:

    @staticmethod
    def sharpe_ratio(returns):

        return np.sqrt(252) * returns.mean() / returns.std()

    @staticmethod
    def max_drawdown(cumulative):

        peak = cumulative.cummax()

        drawdown = (cumulative - peak) / peak

        return drawdown.min()

    @staticmethod
    def volatility(returns):

        return returns.std() * np.sqrt(252)
