import numpy as np
import pandas as pd

class PairsTrading:

    def __init__(self, data, stock1, stock2):

        self.s1 = data[stock1]
        self.s2 = data[stock2]

    def compute_spread(self):

        beta = np.polyfit(self.s2, self.s1, 1)[0]

        spread = self.s1 - beta * self.s2

        return spread
    def generate_signals(self, entry=1, exit=0):

        spread = self.compute_spread()

        mean = spread.mean()
        std = spread.std()

        zscore = (spread - mean) / std

        signals = pd.DataFrame(index=spread.index)

        signals["zscore"] = zscore
        signals["long"] = zscore < -entry
        signals["short"] = zscore > entry
        signals["exit"] = abs(zscore) < exit

        return signals


    # def generate_signals(self):

    #     spread = self.compute_spread()

    #     mean = spread.mean()
    #     std = spread.std()

    #     zscore = (spread - mean) / std

    #     signals = pd.DataFrame(index=spread.index)

    #     signals["zscore"] = zscore
    #     signals["long"] = zscore < -1
    #     signals["short"] = zscore > 1

    #     return signals
