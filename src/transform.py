import pandas as pd

RENAME_MAP = {
    "Euro Zone-Euro": "EUR",
    "United Kingdom-Pound": "GBP",
    "Canada-Dollar": "CAD",
}

def clean_and_pivot(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()

    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
    df["exchange_rate"] = pd.to_numeric(df["exchange_rate"], errors="coerce")

    df = df.dropna(subset=["record_date", "exchange_rate"])
    df["currency"] = df["country_currency_desc"].map(RENAME_MAP)

    wide = (
        df.pivot_table(index="record_date", columns="currency",
                       values="exchange_rate", aggfunc="mean")
          .sort_index()
    )

    return wide
