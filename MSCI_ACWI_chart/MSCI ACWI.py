
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Load MSCI ACWI data
file_path = "892400 - MSCI ACWI Index  - FULL - 1998-12-31 - 2025-12-08  - Daily.xlsx"
df = pd.read_excel(file_path, sheet_name="Performance Data", skiprows=5, engine="openpyxl")
df.columns = ["Date", "Index Level", "col3", "col4", "col5"]
df = df[["Date", "Index Level"]].dropna()
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Plot only the time series line
plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Index Level"], color=(34/255, 139/255, 34/255), linewidth=2)

# Style: transparent background, no gridlines, clean axes
plt.xlabel("Date", fontsize=12)
plt.ylabel("Index Level", fontsize=12)

# Remove top/right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.grid(False)

# Save with transparent background
plt.tight_layout()
plt.savefig("MSCI_ACWI_timeseries.png", transparent=True)
plt.show()
