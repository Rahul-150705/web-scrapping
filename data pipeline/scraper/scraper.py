# scraper/scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime
import os
from utils.logger import logger
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger.info("Scraping started")
# ---------- Browser Setup ----------
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")  # Optional: show browser if debugging

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ---------- Open Amazon ----------
driver.get("https://www.amazon.in/s?k=milk")
time.sleep(5)  # allow page to load

# ---------- Scrape Products ----------
products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")

data = []

for product in products:
    try:
        name = product.find_element(By.CSS_SELECTOR, "h2 span").text
    except:
        name = None

    try:
        price = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        price = price.replace(",", "")
    except:
        price = None

    if name:
        data.append({
            "product_name": name,
            "price": price,
            "platform": "Amazon",
            "scraped_at": datetime.now().isoformat()
        })

# ---------- Save Raw Data ----------
os.makedirs("../data/raw", exist_ok=True)
df = pd.DataFrame(data)
df.to_csv("../data/raw/amazon_milk_raw.csv", index=False)

logger.info(f"Total products scraped: {len(df)}")
print(df.head())
logger.info("Scraping completed successfully")
driver.quit()
