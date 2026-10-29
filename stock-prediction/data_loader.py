import yfinance as yf
import pandas as pd


def get_stock_data(ticker, start, end):
    ticker = ticker.strip().upper()

    data = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        raise ValueError(
            "No stock data found. Check the ticker and dates."
        )

    # Handle column formats returned by different
    # yfinance versions.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()
    data = data.dropna(subset=["Close"])

    return data