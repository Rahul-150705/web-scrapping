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
# options.add_argument("--headless=new")  nott needed now

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
# to use try and except for all in one place like a function
def scrape(parent,by,location):
    try:
        return parent.find_element(by,location).text
    except NoSuchElementException:
        return ""
products = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
shirt=[]
page=0
while page<=5:
    products = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
    for p in products:
        brand=scrape(p,By.CSS_SELECTOR, "h3.product-brand")
        product_type = scrape(p,By.CSS_SELECTOR, "h4.product-product")
        product_price=scrape(p,By.CSS_SELECTOR,"span.product-discountedPrice")
        product_actual_price=scrape(p,By.CSS_SELECTOR,"span.product-strike")
        shirt.append((brand,product_type,product_price,product_actual_price))
    try:
        next_button=driver.find_element(By.CSS_SELECTOR, "li.pagination-next") # trying to find next button
        if "disabled" in next_button.get_attribute("class"): # myntra adds disabled in last page class name so if foudn then should be breaked
            break

        first_product=products[0] # we should wait until the first page is stale so we store and use it there
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", next_button
        )
        driver.execute_script("arguments[0].click();",next_button)
        # it is used to make the previous old state staleness
        WebDriverWait(driver, 10).until(
            EC.staleness_of(first_product)
        )
        products=driver.find_elements(By.CSS_SELECTOR, "li.product-base")
        print("Page Loaded:", page)
        page+=1
    except (TimeoutException,NoSuchElementException):
        break
print("Number of Pages Loaded:",page)
df=pd.DataFrame(shirt,columns=["brand","product_type","product_price","product_actual_price"])
df.to_csv("hello.csv",index=False)
print("Finished Scrapping")

