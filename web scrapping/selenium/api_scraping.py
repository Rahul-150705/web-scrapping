import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.get("https://www.myntra.com/shirt")

time.sleep(5)  # let Akamai + JS settle

cookies = driver.get_cookies()
driver.quit()
session_cookies = {c["name"]: c["value"] for c in cookies}


import requests
session = requests.Session()
session.cookies.update(session_cookies)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Referer": "https://www.myntra.com/shirt",
    "x-myntraweb": "Yes",
    "x-requested-with": "browser",
}

url = "https://www.myntra.com/gateway/v4/search/shirt"

params = {
    "rawQuery": "shirt",
    "rows": 50,
    "o": 0,
    "p": 1,
    "plaEnabled": "true",
    "xdEnabled": "false",
    "isFacet": "true"
}
all_products = []
page = 1
offset = 0
rows = 50

while page<5:
    params["p"] = page
    params["o"] = offset

    res = session.get(url, headers=HEADERS, params=params)
    products = res.json().get("products", [])
    if not products:
        break

    all_products.extend(products)

    page += 1
    offset += rows

df = pd.DataFrame(all_products)
df.to_csv("myntra_shirts.csv", index=False)
print("Total products collected:", len(all_products))
print()
