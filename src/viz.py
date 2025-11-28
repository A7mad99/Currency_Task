import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def ensure_output_dirs():
    charts_dir = Path("outputs/charts")
    charts_dir.mkdir(parents=True, exist_ok=True)
    return charts_dir

def plot_timeseries(wide, out_path):
    ax = wide.plot(figsize=(11,5))
    ax.set_title("Treasury FX Rates vs USD")
    ax.set_xlabel("Date")
    ax.set_ylabel("Foreign currency per $1")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_indexed(wide, out_path):
    """
    Indexed FX performance (base=100) using each currency's first valid value.
    """
    base = wide.apply(lambda s: s.dropna().iloc[0])  # first valid per currency
    indexed = wide.divide(base) * 100

    ax = indexed.plot(figsize=(11,5))
    ax.set_title("Indexed FX Performance (First Valid = 100)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Index")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()  # display on screen
    plt.close()


def plot_volatility(rolling_vol, out_path):
    ax = rolling_vol.plot(figsize=(11,5))
    ax.set_title("30-Day Rolling FX Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
