# StockVision

StockVision is a small Flask web app for viewing historical stock prices and generating a short-term price forecast. Enter a ticker symbol to see roughly three years of closing-price history, a five-step forecast, and a test-set error metric.

> Forecasts are estimates for demonstration purposes. They are not investment advice, and past performance does not guarantee future results.

## Features

- Looks up historical stock data with Yahoo Finance through `yfinance`.
- Shows historical closing prices in an interactive chart.
- Forecasts the next five price steps using a linear regression model.
- Reports the latest closing price and test-set mean absolute error (MAE).
- Accepts ticker symbols such as `AAPL` or `TCS.NS`.

## How the forecast works

The model uses the previous five closing prices as input features to estimate the next closing price. It trains on the earlier 80% of the available samples and measures MAE on the more recent 20%.

To produce the forecast, the model predicts one step at a time. Each prediction is added to the input history and used to predict the next step.

The chart labels forecast steps with approximate calendar dates. These labels do not account for weekends or market holidays.

## Requirements

- Python 3.9 or newer
- Internet access to retrieve stock data and load the Plotly chart library

Python packages:

- Flask
- NumPy
- pandas
- scikit-learn
- yfinance

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
