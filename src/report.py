
from __future__ import annotations
import pandas as pd
from pathlib import Path

def write_summary(metrics: dict, forecasts: dict) -> None:
    """
    Write a board-friendly summary report.
    """
    out_path = Path("outputs/summary_report.txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    latest = metrics["latest"]
    yoy = metrics["yoy_pct"]
    direction = metrics["direction"]
    current_vol = metrics["current_vol"]
    vol_thresh = metrics["vol_thresholds"]
    vol_alerts = metrics["vol_alerts"]
    latest_corr = metrics["latest_corr"]

    lines = []
    lines.append("TREASURY FX INSIGHTS — EXECUTIVE SUMMARY\n")
    lines.append(f"Latest observation date: {metrics['clean'].index.max().date()}\n")

    lines.append("1) Latest Exchange Rates (foreign currency per $1):")
    for ccy, val in latest.items():
        lines.append(f"   - {ccy}: {val:.4f}")
    lines.append("")

    lines.append("2) Year-on-Year Change & Direction of Travel:")
    for ccy in yoy.index:
        lines.append(f"   - {ccy}: {yoy[ccy]:.2f}%  →  {direction[ccy]}")
    lines.append("")

    lines.append("3) Volatility (30-day rolling annualised):")
    for ccy in current_vol.index:
        lines.append(
            f"   - {ccy}: current={current_vol[ccy]:.2%}, "
            f"threshold(80th perc)={vol_thresh[ccy]:.2%}  →  {vol_alerts[ccy]}"
        )
    lines.append("")

    lines.append("4) Currency Relationships (latest correlations of daily returns):")
    lines.append(latest_corr.round(2).to_string())
    lines.append("")

    lines.append("5) 30-day Forecast Snapshot (ARIMA baseline):")
    for ccy, fc in forecasts.items():
        lines.append(f"   - {ccy}: forecast end value ≈ {fc.iloc[-1]:.4f}")
    lines.append("")

    lines.append("Recommendations for future platform development:")
    lines.append("   • Schedule automated daily refresh of Treasury data.")
    lines.append("   • Trigger alerts for volatility spikes or large YoY moves.")
    lines.append("   • Extend forecasts with confidence bands and scenario testing.")
    lines.append("   • Integrate into a dashboard for Treasury / Risk teams.\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
