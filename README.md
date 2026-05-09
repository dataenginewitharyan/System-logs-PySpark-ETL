# Containerized PySpark ETL Pipeline

## How to Run
1. **Start:** `docker-compose down -v && docker-compose up --build`
2. **Wait:** Watch for the `spark_etl` container to say `✅ ETL Successful!`.
3. **Verify:**
   `docker exec -it postgres_db psql -U admin -d opspulse_db -c "SELECT * FROM server_metrics;"`