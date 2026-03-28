# src/main.py

from data_loader import DataLoader
from correlation import Correlation
from cointegration import Cointegration
from spread_model import SpreadModel, half_life
from backtester import Backtester
from performance import Performance
from logger import log_trade
from data_streamer import DataStreamer

import pandas as pd
import time


def run_backtest(tickers, start_date, end_date, corr_threshold):

    print("\nRunning BACKTEST mode...\n")

    loader = DataLoader(tickers, start_date, end_date)
    data = loader.fetch_data()

    corr_matrix = Correlation.compute_matrix(data)
    pairs = Correlation.find_pairs(corr_matrix, threshold=corr_threshold)

    if not pairs:
        print("No correlated pairs found.")
        return

    equity_curves = []

    for s1, s2, corr in pairs:

        print(f"\nProcessing Pair: {s1} - {s2}")

        pvalue = Cointegration.test_pair(data[s1], data[s2])

        if pvalue >= 0.05:
            continue

        # =========================
        # SPREAD MODEL
        # =========================
        model = SpreadModel(data[s1], data[s2])
        spread, _ = model.compute_spread()

        hl = half_life(spread)
        model = SpreadModel(data[s1], data[s2], window=hl)

        spread, _ = model.compute_spread()
        zscore = model.compute_zscore(spread)
        signals = model.generate_signals(zscore)

        # SAVE FOR DASHBOARD
        zscore.to_csv("zscore.csv")
        signals.to_csv("signals.csv")

        # =========================
        # BACKTEST
        # =========================
        backtester = Backtester(spread, signals)
        equity_curve = backtester.run()

        equity_curves.append(equity_curve)

        log_trade(f"[BACKTEST] {s1}-{s2} Signal: {signals.iloc[-1]}")

    if not equity_curves:
        print("No valid strategies.")
        return

    portfolio = pd.concat(equity_curves, axis=1).mean(axis=1)

    # SAVE FOR DASHBOARD
    portfolio.to_csv("equity.csv")

    metrics = Performance.compute_all(portfolio)

    print("\n===== PERFORMANCE =====\n")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")


def run_live(tickers):

    print("\nRunning LIVE STREAMING mode...\n")

    streamer = DataStreamer(tickers)
    history = pd.DataFrame()

    while True:

        latest_prices = streamer.fetch_latest()

        history = pd.concat([history, latest_prices.to_frame().T])

        # wait until enough data
        if len(history) < 10:
            print("Collecting data...")
            time.sleep(10)
            continue

        s1, s2 = history.columns[:2]

        model = SpreadModel(history[s1], history[s2])

        spread, _ = model.compute_spread()
        zscore = model.compute_zscore(spread)
        signals = model.generate_signals(zscore)

        # SAVE FOR DASHBOARD (LIVE UPDATE)
        spread.to_csv("spread.csv")
        zscore.to_csv("zscore.csv")
        signals.to_csv("signals.csv")

        latest_signal = signals.iloc[-1]

        log_trade(f"[LIVE] {s1}-{s2} Signal: {latest_signal}")

        print(f"{s1}-{s2} Signal: {latest_signal}")

        time.sleep(60)  # 1-min frequency


def main():

    print("\n===== Statistical Arbitrage Trading System =====\n")

    mode = input("Select mode (1 = Backtest, 2 = Live): ")

    tickers_input = input("Enter tickers (AAPL,MSFT,...): ")
    tickers = [t.strip().upper() for t in tickers_input.split(",")]

    if mode == "1":

        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        corr_threshold = float(input("Correlation threshold (0.8): "))

        run_backtest(tickers, start_date, end_date, corr_threshold)

    elif mode == "2":

        run_live(tickers)

    else:
        print("Invalid mode selected.")


if __name__ == "__main__":
    main()