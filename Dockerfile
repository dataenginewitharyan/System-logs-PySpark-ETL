# Use a lightweight Python base
FROM python:3.11-slim

# Install Java 21 (Required for PySpark to run)
RUN apt-get update && apt-get install -y openjdk-21-jre-headless && rm -rf /var/lib/apt/lists/*

# Universal Java Path: Find the folder (arm64 or amd64) and link it to 'default-java'
# This makes the project work on M4 Macs AND Windows/Intel machines
RUN ln -s $(ls -d /usr/lib/jvm/java-21-openjdk-*) /usr/lib/jvm/default-java

# Set Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

WORKDIR /app

# Install Python dependencies first (helps with Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our project files into the container
COPY . .

# Start the Python script
CMD ["python", "main.py"]