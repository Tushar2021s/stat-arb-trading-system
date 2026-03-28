import numpy as np
import pandas as pd
from hedge_ratio import HedgeRatio


class SpreadModel:

    def __init__(self, price1, price2, window=60):
        self.price1 = price1
        self.price2 = price2
        self.window = window

    def compute_spread(self):

        beta = HedgeRatio.rolling_beta(self.price1, self.price2, self.window)
        spread = self.price1 - beta * self.price2

        return spread, beta

    def compute_zscore(self, spread):

        mean = spread.rolling(self.window).mean()
        std = spread.rolling(self.window).std()

        return (spread - mean) / std

    def generate_signals(self, zscore, entry=2, exit=0.5):

        signals = pd.Series(0, index=zscore.index)

        signals[zscore > entry] = -1
        signals[zscore < -entry] = 1
        signals[abs(zscore) < exit] = 0

        return signals


#  MOVE THIS OUTSIDE CLASS
def half_life(spread):

    import numpy as np

    spread = spread.dropna()

    #  Not enough data
    if len(spread) < 20:
        return 20

    spread_lag = spread.shift(1).dropna()
    spread_ret = spread.diff().dropna()

    spread_lag = spread_lag.loc[spread_ret.index]

    #  Still empty after alignment
    if len(spread_lag) == 0 or len(spread_ret) == 0:
        return 20

    try:
        beta = np.polyfit(spread_lag, spread_ret, 1)[0]

        #  Avoid division issues
        if beta >= 0:
            return 20

        halflife = -np.log(2) / beta

        #  sanity bound
        return max(5, min(int(halflife), 100))

    except Exception:
        return 20