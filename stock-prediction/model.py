import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def train_and_predict(close_prices, days=5):
    prices = np.asarray(close_prices, dtype=float)
    prices = prices[np.isfinite(prices)]

    if len(prices) < 40:
        raise ValueError(
            "At least 40 valid closing prices are required."
        )

    if not 1 <= days <= 30:
        raise ValueError("Choose between 1 and 30 days.")

    window = 5

    # Each input uses five earlier prices.
    X = np.array([
        prices[i - window:i]
        for i in range(window, len(prices))
    ])

    y = prices[window:]

    # Keep the newest observations for testing.
    split = int(len(X) * 0.8)
    if split <= 0 or split >= len(X):
        raise ValueError("Not enough data to split.")

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    test_predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, test_predictions)

    # Forecast recursively: each prediction becomes
    # an input for the next forecast.
    history = list(prices)
    forecast = []

    for _ in range(days):
        features = np.array(history[-window:]).reshape(1, -1)
        next_price = float(model.predict(features)[0])

        forecast.append(next_price)
        history.append(next_price)

    return {
        "forecast": forecast,
        "mae": float(mae),
        "last_close": float(prices[-1])
    }