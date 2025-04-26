
# MACD Indicator Analysis Using Stock Market Data

## Project Overview

This project involves the implementation and analysis of the **MACD (Moving Average Convergence Divergence)** technical indicator, used to identify potential buy and sell signals for stocks. Simulations were performed for three companies representing different market trends: Apple (AAPL), Nestlé (NESN), and Allegro (ALEP).

The project was completed as part of the **Numerical Methods** course.

# Report

A detailed description of algorithms, results interpretation, and diagrams are available in [MACD_MN1.pdf](./MACD_MN1.pdf) (in Polish).

## What is MACD?

MACD is the difference between two exponential moving averages (EMA) — a short-term and a long-term one. The project uses:
- `Nshort = 12` – short-term EMA,
- `Nlong = 26` – long-term EMA,
- `Nsignal = 9` – EMA of the MACD indicator (signal line).

MACD and signal line crossovers are interpreted as:
- **Buy signal** – MACD crosses the signal line from below,
- **Sell signal** – MACD crosses the signal line from above.


## Requirements

- Python 3.10+
- `pandas`
- `numpy`
- `matplotlib`

Install them using:


```bash
pip install requirements.txt
```

## How to Run

1. Place the input data files in the `data/` folder (`AAPL.csv`, `NESN.csv`, `ALEP.csv`).
2. In `main.py`, set the value of `datachoice`:
   - `0` – Apple,
   - `1` – Nestlé,
   - `2` – Allegro.
3. Run the script:

```bash
python main.py
```

The generated plots will appear in the `diagrams/` folder.

## Program objective

- Calculates EMA, MACD, and the signal line.
- Detects crossover points (buy/sell signals).
- Simulates a portfolio based on full transactions at detected points.
- Generates plots:
  - Stock prices with buy/sell signals,
  - MACD and SIGNAL line plot,
  - Portfolio value over time,
  - Number of shares held,
  - Profits and losses from each transaction.


