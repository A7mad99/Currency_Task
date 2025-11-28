import requests
import pandas as pd

BASE_URL = (
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
    "v1/accounting/od/rates_of_exchange"
)

TARGET_CURRENCIES = [
    "Euro Zone-Euro",
    "United Kingdom-Pound",
    "Canada-Dollar",
]

def fetch_rates(start_date="2015-01-01"):
    all_rows = []
    page = 1
    page_size = 10000

    currency_filter = ",".join(TARGET_CURRENCIES)

    params = {
        "fields": "country_currency_desc,exchange_rate,record_date",
        "filter": f"country_currency_desc:in:({currency_filter}),record_date:gte:{start_date}",
        "page[size]": page_size,
        "page[number]": page,
    }

    while True:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        data = payload.get("data", [])
        if not data:
            break

        all_rows.extend(data)

        meta = payload.get("meta", {})
        total_pages = meta.get("total_pages", 1)
        if page >= total_pages:
            break

        page += 1
        params["page[number]"] = page

    return pd.DataFrame(all_rows)
