from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor

options = Options()
options.add_argument("--headless")

urls = [
    "https://www.amazon.in/s?k=milk&page=1",
    "https://www.amazon.in/s?k=milk&page=2",
    "https://www.amazon.in/s?k=milk&page=3"
]

def scrape_page(url):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get(url)
    time.sleep(5)
    products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")
    page_data = []
    for p in products[:10]:
        try:
            name = p.find_element(By.CSS_SELECTOR, "h2").text
        except:
            name = None
        try:
            price = p.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            price = price.replace(",", "")
        except:
            price = None
        page_data.append({
            "product_name": name,
            "price": price,
            "platform": "Amazon",
            "timestamp": datetime.now().isoformat()
        })
    driver.quit()
    return page_data

def run_scraper():
    all_products = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(scrape_page, urls)
    for r in results:
        all_products.extend(r)

    df = pd.DataFrame(all_products)
    df = df[df["product_name"].notna()]
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df[df["price"].notna() & (df["price"] > 0)]
    df = df.drop_duplicates(subset=["product_name", "platform"])
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/products_clean_parallel.csv", index=False)
    print("Saved parallel scraped data to CSV")

# DAG definition
default_args = {
    'owner': 'rahul',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'parallel_scraper_dag',
    default_args=default_args,
    description='Parallel Amazon scraper DAG',
    start_date=datetime(2026, 1, 3),
    schedule_interval=None,  # set to '@daily' to run daily
    catchup=False
) as dag:

    run_scraper_task = PythonOperator(
        task_id='run_parallel_scraper',
        python_callable=run_scraper
    )

    run_scraper_task
