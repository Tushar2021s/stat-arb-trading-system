# stat-arb-trading-system# Statistical Arbitrage Trading System

A Python-based **statistical arbitrage trading system** capable of backtesting and live streaming analysis for equity pairs. The system identifies correlated pairs, computes trading signals based on statistical metrics, and simulates potential trades in backtest mode.

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [System Architecture](#system-architecture)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Backtesting Results](#backtesting-results)  
7. [Live Trading](#live-trading)  
8. [Graphs & Analytics](#graphs--analytics)  
9. [Future Improvements](#future-improvements)  
10. [License](#license)  

---

## Project Overview

This project implements a **pairs trading strategy** for equities. By analyzing historical price correlations and statistical measures like z-scores, the system generates entry and exit signals for trades. It supports:

- Historical backtesting for performance analysis.  
- Live streaming mode for near real-time signal generation.  
- Configurable correlation thresholds and trading parameters.

The system is designed for educational and research purposes and **does not execute live trades** on exchanges.

---

## Features

- **Backtesting Mode:** Evaluate historical trading performance over custom date ranges.  
- **Live Mode:** Stream live market data and generate trading signals for selected tickers.  
- **Correlation Analysis:** Automatically detect correlated stock pairs.  
- **Z-score Trading Signals:** Entry and exit signals based on statistical spread.  
- **Configurable Parameters:** Thresholds, lookback periods, and frequency adjustable for experimentation.

---

## System Architecture
+-----------------+ +------------------+ +----------------+
| Data Collection | ---> | Signal Generator | ---> | Backtest Engine|
+-----------------+ +------------------+ +----------------+
| |
v v
Historical Prices Z-score Calculation

- **Data Collection:** Retrieves historical or live price data from external APIs.  
- **Signal Generator:** Computes spread, moving averages, and z-scores for pair trading.  
- **Backtest Engine:** Simulates trades, P&L, and performance metrics.  

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stat-arb-trading-system.git
cd stat-arb-trading-system
Create a Python virtual environment:
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
Install dependencies:
pip install -r requirements.txt
Usage
Backtest Mode
python3 main.py
Select mode 1 for backtesting.
Enter tickers (comma-separated).
Enter start and end dates.
Enter correlation threshold (default: 0.8).
Live Streaming Mode
python3 main.py
Select mode 2 for live streaming.
Enter tickers.
System collects live data and prints signals in real time.
Backtesting Results

Example backtest output:

Pair	Trades	Win Rate	P&L ($)
AAPL-MSFT	10	70%	245
GOOG-AMZN	8	62%	190

Note: Replace with your actual backtest results.

Live Trading

Live signals are calculated based on z-score thresholds:

Pair	Z-Score	Signal
AAPL-MSFT	0.32	0
MSFT-AMZN	-1.25	1

0 = No Action, 1 = Long, -1 = Short

Graphs & Analytics

1. Correlation Heatmap


2. Spread & Z-Score Over Time


3. Cumulative P&L Curve


Replace the placeholder images with your own generated plots from backtesting.

Future Improvements
Integrate automatic live trading execution with broker APIs.
Use rolling correlations and dynamic thresholds for more adaptive pair selection.
Implement machine learning for better signal prediction.
Support multi-threading and asynchronous data collection for faster live updates.
Add interactive dashboards with Plotly or Streamlit for visualization.