from data_streamer import DataStreamer
from spread_model import SpreadModel
from logger import log_trade

import pandas as pd

class LivePipeline:

    def __init__(self, tickers):

        self.streamer = DataStreamer(tickers)
        self.history = pd.DataFrame()

    def run(self):

        for prices in self.streamer.stream():

            self.history = pd.concat([self.history, prices.to_frame().T])

            if len(self.history) < 100:
                continue

            s1, s2 = self.history.columns[:2]

            model = SpreadModel(self.history[s1], self.history[s2])

            spread, _ = model.compute_spread()
            zscore = model.compute_zscore(spread)
            signal = model.generate_signals(zscore).iloc[-1]

            log_trade(f"LIVE SIGNAL {s1}-{s2}: {signal}")