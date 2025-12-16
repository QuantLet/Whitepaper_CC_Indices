# Cache yfinance time series for ^GSPC and ^IXIC in a pickle file and incrementally update

# pip install yfinance pandas matplotlib

import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, timezone

# Use non-interactive backend for safety in headless environments
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CACHE_PATH = "spx_nasdaq_cache.pkl"
TICKERS = ["^GSPC", "^NDX"]
START_DEFAULT = "2000-01-01"


def load_cache(path=CACHE_PATH):
    if os.path.exists(path):
        return pd.read_pickle(path)
    return None


def save_cache(df, path=CACHE_PATH):
    df.to_pickle(path)


def fetch_history(start, end=None):
    df = yf.download(TICKERS, start=start, end=end, interval="1d", progress=False)["Close"]
    return df


def update_cache():
    today = datetime.now(timezone.utc).date()
    cached = load_cache()
    if cached is None:
        data = fetch_history(START_DEFAULT)
    else:
        last_date = cached.index.max().date()
        fetch_start = (last_date + timedelta(days=1)).isoformat()
        new = fetch_history(fetch_start)
        if new is None or new.empty:
            data = cached
        else:
            combined = pd.concat([cached, new])
            data = combined.loc[~combined.index.duplicated(keep="last")]
    save_cache(data)
    return data


if __name__ == "__main__":
    data = update_cache()

    # Plot
    fig, ax = plt.subplots(figsize=(11, 6))
    data.plot(ax=ax)

    # Remove title and legend
    ax.set_title("")
    ax.legend().remove()

    # Remove top and right spines (chart borders)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Transparent background
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    # Label axes
    ax.set_xlabel("Date")
    ax.set_ylabel("Index Level")

    plt.tight_layout()
    plt.savefig("spx_nasdaq_plot.png", transparent=True)
    print("✅ Transparent chart saved as spx_nasdaq_plot.png")
