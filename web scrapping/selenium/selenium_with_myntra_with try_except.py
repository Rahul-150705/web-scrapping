from selenium import webdriver
from selenium.webdriver.chrome.options import Options # this is used to open chrome without opening it and runnit it headless
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # waits to locate the css selector in the js
from selenium.webdriver.support import expected_conditions as EC # used in wedriverwait
from selenium.common.exceptions import TimeoutException # to handle webdriver wait no time
from selenium.common.exceptions import NoSuchElementException # to handle Null Values
import os
import pandas as pd # to make the list as csv

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
def scrape(parent,by,location):
    try:
        return parent.find_element(by,location).text
    except NoSuchElementException:
        return ""
products = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
shirt=[]


for p in products:
        brand=scrape(p,By.CSS_SELECTOR, "h3.product-brand")
        product_type = scrape(p,By.CSS_SELECTOR, "h4.product-product")
        product_price=scrape(p,By.CSS_SELECTOR,"span.product-discountedPrice")
        product_actual_price=scrape(p,By.CSS_SELECTOR,"span.product-strike")
        shirt.append([brand,product_type,product_price,product_actual_price])
if(len(shirt)==0):
    print("Shirt Not Found")

df=pd.DataFrame(shirt,columns=["brand","product_type","product_price","product_actual_price"])
if(os.path.exists("shrit.csv")):
    df.to_csv("shirt.csv",mode="a",index=False)
else:
    df.to_csv("shirt.csv",index=False)
df.to_csv("shirt.csv",mode="a",index=False,header=False) # header false avoid writing column name again
print("Finished Scrapping")
driver.quit()
