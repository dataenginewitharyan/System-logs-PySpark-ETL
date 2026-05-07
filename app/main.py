import pandas as pd
from sqlalchemy import create_engine

def run_etl():
    print("--- Starting OpsPulse ETL ---")

    # 1. EXTRACT
    df = pd.read_csv('data/server_logs.csv')
    print(f"Read {len(df)} rows.")

    # 2. TRANSFORM
    df = df.drop_duplicates()                       # Remove doubles
    df['status'] = df['status'].str.upper()         # OK, ok -> OK
    df = df[df['cpu_usage'] <= 100]                 # Remove errors (>100%)
    df['cpu_usage'] = df['cpu_usage'].fillna(50.0)  # Fill blanks with 50%
    
    print(f"Cleaned data down to {len(df)} rows.")

    # 3. LOAD
    # Note: 'mycontainer' is the name you gave in docker-compose
    engine = create_engine("postgresql://admin:password@mycontainer:5432/opspulse_db")
    df.to_sql('server_metrics', engine, if_exists='replace', index=False)
    
    print("Data loaded to Database!")

if __name__ == "__main__":
    run_etl()