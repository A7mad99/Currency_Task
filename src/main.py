from fetch_data import fetch_rates
from transform import clean_and_pivot
from analysis import compute_metrics
from forecast import forecast_arima
from viz import (
    ensure_output_dirs,
    plot_timeseries,
    plot_indexed,
    plot_volatility,
)
from viz_extra import plot_rolling_corr, plot_forecast
from report import write_summary

def run(start_date="2015-01-01"):
    charts_dir = ensure_output_dirs()

    print("Fetching data...")
    raw = fetch_rates(start_date)

    print("Cleaning + transforming...")
    wide = clean_and_pivot(raw)

    print("Computing metrics...")
    metrics = compute_metrics(wide)

    # ---------------- Core required charts ----------------
    print("Generating required charts...")
    plot_timeseries(metrics["clean"], charts_dir / "1_timeseries.png")
    plot_indexed(metrics["clean"], charts_dir / "2_indexed.png")
    plot_volatility(metrics["rolling_vol_30d"], charts_dir / "3_volatility.png")

    # ---------------- Recommended enhancements ----------------
    print("Forecasting next 30 days...")
    forecasts = {}
    for ccy in metrics["clean"].columns:
        forecasts[ccy] = forecast_arima(metrics["clean"][ccy], steps=30)
        plot_forecast(
            metrics["clean"][ccy],
            forecasts[ccy],
            charts_dir / f"forecast_{ccy}.png", # type: ignore
            title=f"{ccy} Forecast vs USD (ARIMA baseline)"
        )

    print("Plotting rolling correlations...")
    plot_rolling_corr(metrics["rolling_corr_90d"], charts_dir / "rolling_corr_90d.png") # type: ignore

    print("Saving summary CSVs...")
    metrics["latest"].to_csv("outputs/latest_rates.csv")
    metrics["yoy_pct"].to_csv("outputs/yoy_pct.csv")
    metrics["direction"].to_csv("outputs/direction.csv")
    metrics["yearly_avg"].to_csv("outputs/yearly_avg.csv")
    metrics["current_vol"].to_csv("outputs/current_vol.csv")
    metrics["vol_alerts"].to_csv("outputs/vol_alerts.csv")
    metrics["latest_corr"].to_csv("outputs/latest_corr.csv")

    print("Writing executive summary report...")
    write_summary(metrics, forecasts)

    print("Done! Check the 'outputs' folder.")

if __name__ == "__main__":
    run()
