import csv
import time
import os
import psutil
import random
from datetime import datetime

FILE_PATH = 'data/server_logs.csv'
HEADER = ['timestamp', 'server_id', 'cpu_usage', 'memory_usage', 'status']
DEVICE_NAME = "MACBOOK-AIR-M4"
LIMIT = 15 

def start_collection():
    os.makedirs('data', exist_ok=True)
    
    # FIX: Open with 'w' to wipe old data from previous runs
    with open(FILE_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
    
    print(f"🧹 Old logs cleared. Starting fresh collection...")
    count = 0

    while count < LIMIT:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent

        # Injected chaos for Spark to clean later
        if random.random() < 0.10:
            cpu = 999.9 
        
        status_raw = "OK" if cpu < 70 else "WARNING"
        status = status_raw.lower() if random.random() < 0.5 else status_raw

        with open(FILE_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, DEVICE_NAME, cpu, memory, status])
            count += 1
        
        print(f"📍 Log {count}/{LIMIT} generated.")
        time.sleep(0.5)

    print(f"✅ Reached {LIMIT} logs. Collector exiting.")

if __name__ == "__main__":
    start_collection()