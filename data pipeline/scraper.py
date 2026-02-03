from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

#browser setup
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

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

    if name!=[]:
        data.append({
            "product_name": name,
            "price": price,
            "platform": "Amazon",
            "scraped_at": datetime.now()
        })

# ---------- Save Raw Data ----------
df = pd.DataFrame(data)
df.to_csv("data/raw/amazon_milk_raw.csv", index=False)

print("Scraping completed.")
print(df.head())

driver.quit()
