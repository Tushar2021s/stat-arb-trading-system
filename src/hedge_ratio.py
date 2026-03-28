import numpy as np
import pandas as pd

class HedgeRatio:

    @staticmethod
    def rolling_beta(y, x, window=60):

        betas = []

        for i in range(len(y)):

            if i < window:
                betas.append(np.nan)
                continue

            y_window = y.iloc[i-window:i]
            x_window = x.iloc[i-window:i]

            # linear regression: y = beta * x
            beta = np.polyfit(x_window, y_window, 1)[0]
            betas.append(beta)

        return pd.Series(betas, index=y.index)