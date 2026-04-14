import pandas as pd
import os

def clean_data():
    os.makedirs("data_lake/cleaned", exist_ok=True)

    df = pd.read_csv("data_lake/raw/africa_raw.csv")

    # Pivot indicators into columns
    df_pivot = df.pivot_table(
        index=["country.value", "date"],
        columns="indicator",
        values="value"
    ).reset_index()

    df_pivot.columns = ["country", "year", "gdp", "population", "inflation"]

    # Clean types
    df_pivot["year"] = df_pivot["year"].astype(int)

    # Drop missing rows
    df_pivot = df_pivot.dropna(subset=["gdp"])

    df_pivot.to_parquet("data_lake/cleaned/africa_clean.parquet", index=False)

if __name__ == "__main__":
    clean_data()
