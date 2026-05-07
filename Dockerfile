FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all your project files at once
COPY . .

# Install your Python libraries
RUN pip install -r app/requirements.txt

# Run the script
CMD ["python", "app/main.py"]