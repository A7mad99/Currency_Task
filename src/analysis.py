
from __future__ import annotations
import pandas as pd

def compute_metrics(wide: pd.DataFrame) -> dict:
    # 1. Clean + stabilise index
    clean = wide.dropna(how="all").sort_index()
    if clean.empty:
        raise ValueError("No valid FX data available after cleaning.")

    # Daily frequency for rolling measures
    clean = clean.asfreq("D").ffill()

    # 2. Latest FX levels
    latest = clean.iloc[-1]

    # 3. YoY % change + direction
    one_year_ago_date = clean.index.max() - pd.DateOffset(years=1)
    nearest_pos = clean.index.get_indexer([one_year_ago_date], method="nearest")[0]
    one_year_ago = clean.iloc[nearest_pos]

    yoy_pct = (latest / one_year_ago - 1) * 100
    direction = yoy_pct.apply(
        lambda x: "USD stronger vs currency" if x > 0 else "USD weaker vs currency"
    )

    # 
    # 4. Yearly averages
    yearly_avg = clean.resample("YE").mean()
    yearly_avg.index = pd.DatetimeIndex(yearly_avg.index).year

    # 5. Rolling 30-day volatility
    daily_returns = clean.pct_change()

    rolling_vol_30d = (
        daily_returns
        .rolling(window=30, min_periods=10)
        .std()
        * (252 ** 0.5)
    )

    # 6. Volatility alerts
    # Alert if current vol > 80th percentile of historical vol
    vol_thresholds = rolling_vol_30d.quantile(0.80)
    current_vol = rolling_vol_30d.iloc[-1]

    vol_alerts = (current_vol > vol_thresholds).rename("vol_alert")
    vol_alerts = vol_alerts.apply(lambda x: "ALERT: high volatility" if x else "Normal range")

    
    # 7. Rolling correlations
    rolling_corr_90d = (
        daily_returns
        .rolling(window=90, min_periods=30)
        .corr()
    )

    # Latest correlation matrix 
    latest_corr = daily_returns.dropna().corr()

    return {
        "clean": clean,
        "latest": latest,
        "yoy_pct": yoy_pct,
        "direction": direction,
        "yearly_avg": yearly_avg,
        "daily_returns": daily_returns,
        "rolling_vol_30d": rolling_vol_30d,
        "vol_thresholds": vol_thresholds,
        "current_vol": current_vol,
        "vol_alerts": vol_alerts,
        "rolling_corr_90d": rolling_corr_90d,
        "latest_corr": latest_corr,
    }
