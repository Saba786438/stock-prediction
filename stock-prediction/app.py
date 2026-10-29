from datetime import date, timedelta

from flask import Flask, jsonify, render_template, request

from data_loader import get_stock_data
from model import train_and_predict

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/analyze")
def analyze():
    ticker = request.args.get("ticker", "AAPL").strip().upper()

    end = date.today()
    start = end - timedelta(days=365 * 3)

    try:
        data = get_stock_data(
            ticker,
            start.isoformat(),
            end.isoformat()
        )

        result = train_and_predict(
            data["Close"].to_numpy(),
            days=5
        )

        history = [
            {
                "date": row["Date"].strftime("%Y-%m-%d"),
                "close": float(row["Close"])
            }
            for _, row in data.iterrows()
        ]

        return jsonify({
            "ticker": ticker,
            "history": history,
            "forecast": result["forecast"],
            "mae": result["mae"],
            "last_close": result["last_close"]
        })

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("Stock analysis failed")
        return jsonify({
            "error": "Unable to analyze this stock right now."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)