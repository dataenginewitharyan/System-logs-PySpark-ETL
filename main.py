from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

def run_etl():
    # Initialize Spark with the Postgres Driver
    spark = SparkSession.builder \
        .appName("OpsPulse-ETL") \
        .config("spark.jars", "postgresql-42.7.11.jar") \
        .getOrCreate()

    print("\n--- Starting OpsPulse PySpark ETL ---")

    # 1. EXTRACT
    try:
        df = spark.read.csv('data/server_logs.csv', header=True, inferSchema=True)
        print(f"📥 Extracted {df.count()} raw rows from CSV.")
    except Exception as e:
        print(f"⚠️ CSV not found or empty yet. Error: {e}")
        return

    # 2. TRANSFORM (The "Cleaning" Logic)
    # Standardize casing and filter out the 999.9 CPU chaos spikes
    df_cleaned = df.dropDuplicates() \
        .withColumn("status", upper(col("status"))) \
        .filter(col("cpu_usage") <= 100)

    print(f"✨ Cleaned data. Removed chaos spikes. Row count: {df_cleaned.count()}")

    # 3. LOAD
    db_url = "jdbc:postgresql://db:5432/opspulse_db"
    
    print("🚀 Loading cleaned data to PostgreSQL...")
    df_cleaned.write.jdbc(
        url=db_url,
        table="server_metrics",
        mode="overwrite", # Use overwrite for a clean portfolio demo
        properties={
            "user": "admin",
            "password": "password",
            "driver": "org.postgresql.Driver"
        }
    )
    
    print("✅ ETL Successful! Table 'server_metrics' created.")
    spark.stop()

if __name__ == "__main__":
    run_etl()