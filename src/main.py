# src/main.py

from data_loader import DataLoader
from correlation import Correlation
from cointegration import Cointegration
from pairs_trading import PairsTrading


def main():

    print("\n===== Statistical Arbitrage Trading System =====\n")

    # USER INPUTS
    tickers_input = input("Enter tickers separated by comma (example: AAPL,MSFT,GOOG,AMZN): ")
    tickers = [t.strip().upper() for t in tickers_input.split(",")]

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    corr_threshold = float(input("Enter correlation threshold (example 0.8): "))

    print("\nFetching market data...\n")

    # LOAD DATA
    loader = DataLoader(
        tickers,
        start_date,
        end_date
    )

    data = loader.fetch_data()

    print("Data Loaded Successfully\n")

    # CORRELATION MATRIX
    corr_matrix = Correlation.compute_matrix(data)

    print("Correlation Matrix:\n")
    print(corr_matrix)
    print()

    # FIND PAIRS
    pairs = Correlation.find_pairs(
        corr_matrix,
        threshold=corr_threshold
    )

    if len(pairs) == 0:
        print("No highly correlated pairs found.")
        return

    print("Candidate Pairs Found:\n")

    for p in pairs:
        print(p)

    print()

    # COINTEGRATION TEST
    print("Testing Cointegration...\n")

    for s1, s2, corr in pairs:

        pvalue = Cointegration.test_pair(
            data[s1],
            data[s2]
        )

        if pvalue < 0.05:

            print(f"Cointegrated Pair Found: {s1} & {s2} (p-value={pvalue})")

            strategy = PairsTrading(data, s1, s2)

            signals = strategy.generate_signals()

            print("\nLatest Signals:\n")
            print(signals.tail())

        else:

            print(f"{s1} & {s2} NOT cointegrated (p-value={pvalue})")


if __name__ == "__main__":
    main()


# from data_loader import DataLoader
# from correlation import Correlation
# from cointegration import Cointegration
# from pairs_trading import PairsTrading

# tickers = ["AAPL","MSFT","GOOG","AMZN"]

# loader = DataLoader(
#     tickers,
#     "2020-01-01",
#     "2024-01-01"
# )

# data = loader.fetch_data()

# corr = Correlation.compute_matrix(data)

# pairs = Correlation.find_pairs(corr)

# print("Candidate Pairs:", pairs)

# for s1, s2, c in pairs:

#     pvalue = Cointegration.test_pair(
#         data[s1],
#         data[s2]
#     )

#     if pvalue < 0.05:

#         print("Cointegrated:", s1, s2)

#         strategy = PairsTrading(data, s1, s2)

#         signals = strategy.generate_signals()

#         print(signals.tail())
