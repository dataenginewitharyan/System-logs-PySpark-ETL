# Containerized Python ETL Pipeline

## Project Overview
It is a streamlined ETL (Extract, Transform, Load) application designed to process system health logs. It containerizes a Python data processing engine and orchestrates it alongside a PostgreSQL database using Docker Compose.

## Architecture
- **Language:** Python 3.9
- **Libraries:** Pandas (Transformation), SQLAlchemy (Database Loading)
- **Infrastructure:** Docker, Docker Compose
- **Database:** PostgreSQL 15 (Alpine)

## Key Features
- **Automated Cleaning:** Removes duplicate entries and standardizes status labels to uppercase.
- **Data Imputation:** Automatically handles missing values by filling gaps with default metrics.
- **Container Orchestration:** Manages a multi-container environment where the Python application and Database communicate over a private virtual network.
- **Data Persistence:** Loads cleaned data into a structured `server_metrics` table for querying.

## Note
- **Ensure Docker Desktop is running on your Windows or macOS machine before executing any commands.**

## How to Run

1. **Start the Environment:**
   Open your terminal in the project root and run:
   docker-compose up --build
2. **Verify the Data:**
   docker exec -it mycontainer psql -U admin -d opspulse_db -c "SELECT * FROM server_metrics;"
