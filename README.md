# 📊 System_Logs: Containerized PySpark ETL Pipeline

A production-grade, containerized ETL pipeline that simulates real-time server metrics collection, applies data cleaning transformations with PySpark, and loads the results into PostgreSQL. Perfect for demonstrating **data engineering best practices** using Docker, PySpark, and PostgreSQL.

## 🎯 Project Overview

This project simulates a real-world monitoring system where:
1. A **log generator** collects CPU/memory metrics from your local machine (yes, it reads *your real system stats*!)
2. Data is saved as CSV files
3. **PySpark** reads, cleans, and transforms the data
4. Cleaned results are stored in **PostgreSQL** for querying

The pipeline intentionally injects "chaos data" (e.g., CPU spikes at 999.9%) to demonstrate Spark's data cleaning capabilities.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔄 **Real-time Metrics** | Collects actual CPU/Memory usage from the host machine using `psutil` |
| 🐳 **Fully Containerized** | Runs entirely with Docker Compose - no local Spark/Java/PostgreSQL installation needed |
| 🧹 **Automated Data Cleaning** | Removes duplicates, standardizes text casing, filters impossible CPU values |
| ⚡ **PySpark Transformations** | Demonstrates `dropDuplicates()`, `withColumn()`, `filter()` operations |
| 🗄️ **Persistent Storage** | Cleaned data stored in PostgreSQL for analysis |
| 🎲 **Chaos Injection** | 10% random chance of generating "invalid" CPU spikes to test ETL logic |
| 🖥️ **Cross-Platform** | Works on Apple Silicon (M1/M2/M4), Intel, and Windows via Docker |

## 📂 Project Structure & File Purposes

```text
├── docker-compose.yml          # Orchestrates 3 services (PostgreSQL, Generator, Spark ETL)
├── Dockerfile                  # Builds Python + Java 21 + PySpark environment
├── main.py                     # PySpark ETL logic (Extract, Transform, Load)
├── real_metrics_collector.py   # Generates metrics from real system stats
├── requirements.txt            # Python dependencies (pyspark, psutil)
├── README.md                   # Project Documentation
└── data/                       # Auto-created folder for CSV storage
    └── server_logs.csv         # Raw metrics (generated at runtime)


### 🔍 File-by-File Explanation

#### `docker-compose.yml`
Defines three connected services:
- **`db`**: PostgreSQL 15 database to store cleaned metrics
- **`generator`**: Runs `real_metrics_collector.py` to produce 15 log entries
- **`app`**: Runs `main.py` (PySpark ETL) after waiting 30 seconds for logs to be generated

#### `Dockerfile`
- Starts from Python 3.11 slim image
- Installs Java 21 (required for PySpark)
- Creates universal Java path symlink (works on ARM64 and AMD64)
- Sets `JAVA_HOME` environment variable
- Copies and installs Python dependencies
- Default command runs `main.py`

#### `real_metrics_collector.py`
- Uses `psutil` to read real CPU and memory percentages from the host machine
- Generates 15 records with timestamps
- Injects 10% "chaos" rows (CPU = 999.9)
- Randomly varies status casing (`OK`, `ok`, `WARNING`, `warning`)
- Saves to `data/server_logs.csv`

#### `main.py` (PySpark ETL)
- **EXTRACT**: Reads CSV with schema inference
- **TRANSFORM**: 
  - Removes duplicate rows
  - Converts status column to uppercase
  - Filters out rows where `cpu_usage > 100` (removes chaos spikes)
- **LOAD**: Writes cleaned data to PostgreSQL `server_metrics` table

#### `requirements.txt`
Lists Python dependencies:
- `pyspark` - Apache Spark Python API
- `psutil` - System metrics collection library

---

### 2. For the Project Architecture
```markdown
## 🧠 Project Architecture

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                      DOCKER COMPOSE                         │
 │                                                             │
 │  ┌──────────────┐     ┌──────────────┐                      │
 │  │   GENERATOR  │────▶│   CSV File   │                      │
 │  │  (Python)    │     │   (Volume)   │                      │
 │  └──────────────┘     └──────┬───────┘                      │
 │                              │                              │
 │                              ▼                              │
 │                       ┌──────────────┐                      │
 │                       │  SPARK ETL   │                      │
 │                       │  (PySpark)   │                      │
 │                       └──────┬───────┘                      │
 │                              │                              │
 │                              ▼                              │
 │                       ┌──────────────┐                      │
 │                       │ POSTGRESQL   │                      │
 │                       │   Database   │                      │
 │                       └──────────────┘                      │
 │                                                             │
 └─────────────────────────────────────────────────────────────┘

## 🚀 How to Run

### Prerequisites
- **Docker Desktop** installed and running
- At least 4GB RAM allocated to Docker
- No local Python/Java/PostgreSQL required!

### Step-by-Step Execution

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/opspulse-etl.git
cd opspulse-etl

# 2. Build and run all services
docker-compose down -v && docker-compose up --build

What happens when you run it?

Time	Event
0s	PostgreSQL container starts
0s	Log generator starts collecting 15 metrics
8s	Log generator finishes (15 records @ 0.5s each)
30s	Spark ETL container begins (waits intentionally)
35s	PySpark reads CSV, cleans data, connects to PostgreSQL
40s	ETL completes, table created

### Expected Output in Terminal
spark_etl  | --- Starting OpsPulse PySpark ETL ---
spark_etl  | 📥 Extracted 15 raw rows from CSV.
spark_etl  | ✨ Cleaned data. Removed chaos spikes. Row count: 13
spark_etl  | 🚀 Loading cleaned data to PostgreSQL...
spark_etl  | ✅ ETL Successful! Table 'server_metrics' created.

###Expected Output & Verification

Step 1: Check the cleaned data in PostgreSQL

docker exec -it postgres_db psql -U admin -d opspulse_db -c "SELECT * FROM server_metrics;"


Expected output (example):
     timestamp      |    server_id     | cpu_usage | memory_usage | status 
--------------------+------------------+-----------+--------------+--------
 2026-05-09 10:30:01| MACBOOK-AIR-M4   | 45.2      | 68.5         | OK
 2026-05-09 10:30:02| MACBOOK-AIR-M4   | 72.1      | 70.2         | WARNING
 2026-05-09 10:30:03| MACBOOK-AIR-M4   | 38.7      | 65.1         | OK

 Note: cpu_usage will never exceed 100 (chaos rows removed). All status values are uppercase.


📚 Technologies Used

Python 3.11 - ETL logic and metric collection
PySpark 3.x - Distributed data processing
PostgreSQL 15 - Data warehousing
Docker & Docker Compose - Container orchestration
psutil - System metrics collection
Java 21 - PySpark runtime dependency

🎓 Learning Outcomes
By studying this project, you will understand:

✅ How to containerize data pipelines with Docker
✅ PySpark DataFrame operations (read, transform, write)
✅ JDBC connections from Spark to PostgreSQL
✅ Service orchestration with Docker Compose
✅ Data quality patterns (deduplication, filtering, standardization)
✅ Chaos engineering principles for testing ETL logic
✅ Cross-platform Docker configurations (ARM64 vs AMD64)






