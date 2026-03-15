from statsmodels.tsa.stattools import coint

class Cointegration:

    @staticmethod
    def test_pair(series1, series2):

        score, pvalue, _ = coint(series1, series2)

        return pvalue
