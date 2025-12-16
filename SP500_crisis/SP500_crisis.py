import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os

pickle_file = 'sp500_data.pkl'

if os.path.exists(pickle_file):
    sp500 = pd.read_pickle(pickle_file)
else:
    sp500 = yf.download('^GSPC', start='2006-01-01', end='2015-12-31')
    sp500.to_pickle(pickle_file)

# Flatten MultiIndex columns if present
if isinstance(sp500.columns, pd.MultiIndex):
    sp500.columns = ['_'.join(col).strip() for col in sp500.columns.values]

sp500.reset_index(inplace=True)
sp500['Date'] = pd.to_datetime(sp500['Date'])
close_col = [col for col in sp500.columns if col.startswith('Close')][0]

peak_date = pd.to_datetime("2007-10-01")
peak_price = sp500.loc[sp500['Date'].sub(peak_date).abs().idxmin(), close_col]
trough_date = pd.to_datetime("2009-03-01")
trough_price = sp500.loc[sp500['Date'].sub(trough_date).abs().idxmin(), close_col]
recovery_candidates = sp500[(sp500['Date'] > trough_date) & (sp500[close_col] >= peak_price)]
if not recovery_candidates.empty:
    recovery_date = recovery_candidates.iloc[0]['Date']
    recovery_price = recovery_candidates.iloc[0][close_col]
else:
    recovery_date = sp500.iloc[-1]['Date']
    recovery_price = sp500.iloc[-1][close_col]

peak_date = pd.to_datetime("2007-10-01")
peak_price = sp500.loc[sp500['Date'].sub(peak_date).abs().idxmin(), close_col]
trough_date = pd.to_datetime("2009-03-01")
trough_price = sp500.loc[sp500['Date'].sub(trough_date).abs().idxmin(), close_col]
recovery_candidates = sp500[(sp500['Date'] > trough_date) & (sp500[close_col] >= peak_price)]
if not recovery_candidates.empty:
    recovery_date = recovery_candidates.iloc[0]['Date']
    recovery_price = recovery_candidates.iloc[0][close_col]
else:
    recovery_date = sp500.iloc[-1]['Date']
    recovery_price = sp500.iloc[-1][close_col]

drop_pct = (peak_price - trough_price) / peak_price * 100
recovery_pct = (recovery_price - trough_price) / peak_price * 100

# Calculate durations
days_to_trough = (trough_date - peak_date).days
days_to_recovery = (recovery_date - trough_date).days
years_trough = days_to_trough // 365
extra_days_trough = days_to_trough % 365
years_recovery = days_to_recovery // 365
extra_days_recovery = days_to_recovery % 365

plt.figure(figsize=(10,6))
plt.plot(sp500['Date'], sp500[close_col], label='_nolegend_', color='C0')

plt.scatter([peak_date], [peak_price], color='black', s=120, edgecolor='white', zorder=5)
plt.scatter([trough_date], [trough_price], color='red', s=120, edgecolor='white', zorder=5)
plt.scatter([recovery_date], [recovery_price], color='green', s=120, edgecolor='white', zorder=5)

plt.axvline(peak_date, color='black', linestyle='--', alpha=0.7)
plt.axvline(trough_date, color='red', linestyle='--', alpha=0.7)
plt.axvline(recovery_date, color='green', linestyle='--', alpha=0.7)

# Position offset to avoid overlap
offset_days = pd.Timedelta(days=70)
offset_days_recovery = pd.Timedelta(days=120)

plt.xlabel("Date")
plt.ylabel("Index Level")

# Remove top/right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.grid(False)

plt.tight_layout()
plt.savefig("SP500_crisis.png", transparent=True)
plt.show()
