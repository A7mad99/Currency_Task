
from __future__ import annotations
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast_arima(series: pd.Series, steps: int = 30) -> pd.Series:
    """
    Fit a basic ARIMA(1,1,1) model and forecast 'steps' days ahead.

    Parameters
    ----------
    series : pd.Series
        Daily FX rate series (no NaNs).
    steps : int
        Forecast horizon in days.

    Returns
    -------
    pd.Series forecast indexed by future dates.
    """
    series = series.dropna()

    # ARIMA(1,1,1) is a sensible baseline for FX random-walk-like behavior
    model = ARIMA(series, order=(1, 1, 1))
    fitted = model.fit()

    fc = fitted.forecast(steps=steps)

    # Create future daily index
    future_index = pd.date_range(
        start=series.index.max() + pd.Timedelta(days=1),
        periods=steps,
        freq="D"
    )
    fc.index = future_index
    return fc
