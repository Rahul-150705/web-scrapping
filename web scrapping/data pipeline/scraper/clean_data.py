# scraper/clean_data.py

import pandas as pd
import os
from utils.logger import logger
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load raw data
logger.info("Cleaning started")
raw_file = "../data/raw/amazon_milk_raw.csv"
processed_file = "../data/processed/amazon_milk_clean.csv"

df = pd.read_csv(raw_file)
logger.info(f"Rows before cleaning: {len(df)}")
# Convert price to numeric
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Drop rows with null product_name or price
df = df.dropna(subset=["product_name", "price"])

# Remove duplicates
df = df.drop_duplicates(subset=["product_name", "platform"])

# Ensure processed folder exists
os.makedirs("../data/processed", exist_ok=True)

# Save cleaned CSV
df.to_csv(processed_file, index=False)

logger.info(f"Rows after cleaning: {len(df)}")
