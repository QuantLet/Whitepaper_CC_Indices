
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import yfinance as yf

# --- Parameters you can tweak ---
ticker = "BITW"                 # Nikkei 225 on Yahoo Finance
start_date = "1998-12-31"        # match your previous range (adjust as needed)
end_date = None                  # None = up to today
save_path = "BITW_timeseries.png"

# --- Download Nikkei 225 data from Yahoo Finance ---
# We’ll use the 'Adj Close' (adjusted close) for consistency across corporate actions.
data = yf.download(ticker, start=start_date, end=end_date, progress=False)

# Ensure data is present
if data.empty:
    raise ValueError("No data downloaded. Check ticker symbol or date range.")

# Prepare DataFrame to mirror your original structure
df = data.reset_index()[["Date", "Close"]].dropna()
df.rename(columns={"Close": "Index Level"}, inplace=True)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# --- Plot: minimalist, transparent background, clean axes ---
plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Index Level"],
         color=(255/255, 87/255, 51/255), linewidth=2)

plt.xlabel("Date", fontsize=12)
plt.ylabel("Index Level", fontsize=12)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.grid(False)

plt.tight_layout()
plt.savefig(save_path, transparent=True)
plt.show()
