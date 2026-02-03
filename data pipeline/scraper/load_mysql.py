# scraper/load_mysql.py

import pandas as pd
import mysql.connector
import os
import sys
from utils.logger import logger
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add project root to sys.path for config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.mysql_config import MYSQL_CONFIG
logger.info("Loading data into MySQL")
# Load cleaned data
df = pd.read_csv("../data/processed/amazon_milk_clean.csv")

# Connect to MySQL
conn = mysql.connector.connect(**MYSQL_CONFIG)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS amazon_milk_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10,2),
    platform VARCHAR(50),
    scraped_at DATETIME
)
""")

# Insert rows
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO amazon_milk_prices (product_name, price, platform, scraped_at)
        VALUES (%s, %s, %s, %s)
    """, (
        row["product_name"],
        row["price"],
        row["platform"],
        row["scraped_at"]
    ))
logger.info(f"Rows inserted: {len(df)}")
conn.commit()
cursor.close()
conn.close()

logger.info("MySQL load completed")
