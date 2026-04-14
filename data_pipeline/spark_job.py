from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag, when
from pyspark.sql.window import Window
import os

def run_spark():
    spark = None

    try:
        # =========================
        # 1. SPARK SESSION SETUP
        # =========================
        spark = SparkSession.builder \
            .appName("Africa Macro Curated Pipeline") \
            .master("local[*]") \
            .config("spark.sql.shuffle.partitions", "2") \
            .config("spark.hadoop.fs.file.impl",
                    "org.apache.hadoop.fs.LocalFileSystem") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")

        # =========================
        # 2. LOAD CLEANED DATA
        # =========================
        df = spark.read.parquet("data_lake/cleaned/africa_clean.parquet")

        print("📊 Original Count:", df.count())
        df.show(5)

        # =========================
        # 3. CLEAN TYPES + SAFETY
        # =========================
        df = df.withColumn("year", col("year").cast("int"))

        df = df.withColumn("gdp", col("gdp").cast("double")) \
               .withColumn("population", col("population").cast("double")) \
               .withColumn("inflation", col("inflation").cast("double"))

        # =========================
        # 4. WINDOW DEFINITION (BY COUNTRY)
        # =========================
        window = Window.partitionBy("country").orderBy("year")

        # =========================
        # 5. CORE METRICS
        # =========================

        # GDP per capita
        df = df.withColumn(
            "gdp_per_capita",
            when(col("population") > 0, col("gdp") / col("population"))
        )

        # Previous GDP (for growth)
        df = df.withColumn(
            "prev_gdp",
            lag("gdp").over(window)
        )

        # Growth rate (safe division)
        df = df.withColumn(
            "growth_rate",
            when(
                col("prev_gdp").isNotNull() & (col("prev_gdp") != 0),
                (col("gdp") - col("prev_gdp")) / col("prev_gdp")
            )
        )

        # Inflation-adjusted growth proxy
        df = df.withColumn(
            "real_growth_proxy",
            when(
                col("inflation").isNotNull(),
                col("growth_rate") - (col("inflation") / 100)
            )
        )

        # =========================
        # 6. FILTER CLEAN DATA RANGE
        # =========================
        df_filtered = df.filter(col("year") >= 2000)

        print("📉 Filtered Count:", df_filtered.count())
        df_filtered.show(10)

        # =========================
        # 7. WRITE CURATED DATA
        # =========================
        output_path = "data_lake/curated/africa_curated"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df_filtered.coalesce(1).write \
            .mode("overwrite") \
            .parquet(output_path)

        print(f"✔ Curated dataset saved at: {output_path}")

        # =========================
        # 8. SAMPLE CHECK (DEBUGGING)
        # =========================
        df_filtered.select(
            "country", "year",
            "gdp", "population",
            "gdp_per_capita",
            "growth_rate",
            "inflation"
        ).show(10)

    except Exception as e:
        print(f"❌ Spark Error: {e}")

    finally:
        if spark:
            spark.stop()

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":

    # Ensure dependencies
    try:
        import pyarrow
        print("✓ pyarrow available")
    except ImportError:
        print("⚠️ Installing pyarrow...")
        os.system("pip install pyarrow")

    run_spark()
