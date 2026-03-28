import numpy as np
from statsmodels.tsa.stattools import coint

class PairSelector:

    def __init__(self, prices):
        self.prices = prices

    def find_pairs(self, top_n=5):

        n = self.prices.shape[1]
        pairs = []

        for i in range(n):
            for j in range(i+1, n):

                s1 = self.prices.iloc[:, i]
                s2 = self.prices.iloc[:, j]

                score, pvalue, _ = coint(s1, s2)

                pairs.append((i, j, pvalue))

        # sort by best cointegration
        pairs = sorted(pairs, key=lambda x: x[2])

        return pairs[:top_n]