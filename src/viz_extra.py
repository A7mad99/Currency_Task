"""
viz_extra.py

Extra plots:
- Rolling 90-day correlation between currencies
- Forecast plot overlay
"""

from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd

def plot_rolling_corr(rolling_corr_90d: pd.DataFrame, out_path: str) -> None:
    """
    Plot rolling correlations (90-day) between pairs.
    rolling_corr_90d is a multi-index Series from pandas .corr().
    """
    # Convert multiindex to tidy wide format for key pairs
    pairs = [("EUR", "GBP"), ("EUR", "CAD"), ("GBP", "CAD")]

    series_dict = {}
    for a, b in pairs:
        try:
            s = rolling_corr_90d.xs(a, level=1)[b]
            series_dict[f"{a}-{b}"] = s
        except Exception:
            continue

    corr_df = pd.DataFrame(series_dict).dropna(how="all")
    ax = corr_df.plot(figsize=(11, 5))
    ax.set_title("90-Day Rolling Correlation of FX Returns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Correlation")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()
    plt.close()

def plot_forecast(history: pd.Series, forecast: pd.Series, out_path: str, title: str) -> None:
    """
    Plot forecast overlaid on recent history.
    """
    ax = history.tail(365).plot(figsize=(11, 5), label="History (last 12 months)")
    forecast.plot(ax=ax, label="ARIMA Forecast (next 30d)")
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("FX rate")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()
    plt.close()
