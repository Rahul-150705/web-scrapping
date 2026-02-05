from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import *

import pandas as pd

options = Options()
# options.add_argument("--headless=new") nott needed now

driver = webdriver.Chrome(options=options)

driver.get("https://www.myntra.com/shirt?rawQuery=shirt")

print("Started The Scrapping")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-base"))
    )
    print("Products loaded")
except TimeoutException:
    print("Timed out")

products = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
shirt=[]
for p in products:
    try:
        brand = p.find_element(By.CSS_SELECTOR, "h3.product-brand").text
    except NoSuchElementException:
        brand=""
    try:
        product_type = p.find_element(By.CSS_SELECTOR, "h4.product-product").text
    except NoSuchElementException:
        product_type=""
    try:
        product_price=p.find_element(By.CSS_SELECTOR,"span.product-discountedPrice").text
    except NoSuchElementException:
        product_price=""
    try:
        product_actual_price=p.find_element(By.CSS_SELECTOR,"span.product-strike").text
    except NoSuchElementException:
        product_actual_price=""
    try:
        product_img=p.find_element(By.CSS_SELECTOR,"img.img-responsive").get_attribute("src")
    except NoSuchElementException:
        product_img=""
    shirt.append([brand,product_type,product_price,product_actual_price,product_img])

df=pd.DataFrame(shirt,columns=["brand","product_type","product_price","product_actual_price","product_img"])
df.to_csv("img.csv",index=False)
print("Finished Scrapping")
driver.quit()
