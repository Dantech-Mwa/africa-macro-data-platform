from sqlalchemy import create_engine
import pandas as pd

def check_table():
    engine = create_engine(
        "postgresql://postgres:2020@localhost:5432/datawarehouse"
    )

    # Count rows
    count_df = pd.read_sql("SELECT COUNT(*) AS total FROM africa_macro_data", engine)
    print("Total rows:", count_df["total"][0])

    # Preview data
    sample_df = pd.read_sql("SELECT * FROM africa_macro_data LIMIT 10", engine)
    print("\nSample data:\n", sample_df)

if __name__ == "__main__":
    check_table()
