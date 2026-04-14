import os
import requests
import pandas as pd

COUNTRIES = [
    "KEN", "NGA", "ZAF", "EGY", "ETH", "GHA", "TZA", "UGA", "RWA", "DZA"
]

INDICATORS = {
    "gdp": "NY.GDP.MKTP.CD",
    "population": "SP.POP.TOTL",
    "inflation": "FP.CPI.TOTL.ZG"
}

def fetch_indicator(country, indicator_name, indicator_code):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator_code}?format=json&per_page=20000"
    data = requests.get(url).json()

    if data[1] is None:
        return pd.DataFrame()

    df = pd.json_normalize(data[1])
    df = df[["country.value", "date", "value"]]
    df["indicator"] = indicator_name

    return df

def build_raw_dataset():
    os.makedirs("data_lake/raw", exist_ok=True)

    all_data = []

    for country in COUNTRIES:
        for ind_name, ind_code in INDICATORS.items():
            df = fetch_indicator(country, ind_name, ind_code)
            all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    final_df.to_csv("data_lake/raw/africa_raw.csv", index=False)

if __name__ == "__main__":
    build_raw_dataset()
