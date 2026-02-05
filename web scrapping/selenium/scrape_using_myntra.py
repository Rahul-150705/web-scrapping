from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # like time.sleep(5) waits till 10 sec to scrape
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import * #include all the exceptions
import pandas as pd
import os
driver=Chrome()

options=Options()

#option.headless=False

driver=webdriver.Chrome(options=options)

driver.get("https://www.myntra.com/shirt?rawQuery=shirt")

try:
    WebDriverWait(driver,10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR,"li.product-base"))
)
    print("Started Scrapping")
except TimeoutException:
    print("Timed Out")

product=driver.find_elements(By.CSS_SELECTOR,"li.product-base")
shirt=[]
for p in product:
    try:
        brand=p.find_element(By.CSS_SELECTOR,"h3.product-brand").text
    except NoSuchElementException:
        brand=""
    shirt.append(brand)
df=pd.DataFrame(shirt,columns=["brand"])
if(os.path.exists("shrit.csv")):
    df.to_csv("shirt.csv",mode="a",index=False,header=False)
else:
    df.to_csv("shirt.csv",index=False)