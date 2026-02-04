# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code and folders into container
COPY . .

# Set the command to run your main scraper
# Adjust path if your main script is inside the scraper folder"]
