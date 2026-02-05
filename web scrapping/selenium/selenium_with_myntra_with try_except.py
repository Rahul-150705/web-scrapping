from packaging.tags import Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options # this is used to open chrome without opening it and runnit it headless
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # waits to locate the css selector in the js
from selenium.webdriver.support import expected_conditions as EC # used in wedriverwait
from selenium.common.exceptions import TimeoutException # to handle webdriver wait no time
from selenium.common.exceptions import NoSuchElementException # to handle Null Values
import os
import pandas as pd # to make the list as csv
import time
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
def scroll_product_into_view(product_element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", product_element)
    time.sleep(0.3)
def scrape(parent,by,location):
    try:
        return parent.find_element(by,location).text
    except NoSuchElementException:
        return ""
def scrape_url(parent):
    try:
        return parent.find_element(By.TAG_NAME,"a").get_attribute("href")
    except NoSuchElementException:
        return ""
products = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
shirt=[]
page=0;
while page<=3:
    products=driver.find_elements(By.CSS_SELECTOR,"li.product-base")
    for p in products:
            scroll_product_into_view(p)
            brand=scrape(p,By.CSS_SELECTOR, "h3.product-brand")
            product_type = scrape(p,By.CSS_SELECTOR, "h4.product-product")
            product_price=scrape(p,By.CSS_SELECTOR,"span.product-discountedPrice")
            product_actual_price=scrape(p,By.CSS_SELECTOR,"span.product-strike")
            product_page_url=scrape_url(p)
            try:
                product_img_url = p.find_element(By.CSS_SELECTOR, "img.img-responsive").get_attribute("src")
                if not product_img_url:
                    product_img_url = p.find_element(By.CSS_SELECTOR, "picture source").get_attribute("srcset")
            except NoSuchElementException:
                product_img_url = ""
            shirt.append([brand,product_type,product_price,product_actual_price,product_page_url,product_img_url])
    try:
        next_page=driver.find_element(By.CSS_SELECTOR,"li.pagination-next")
        if "disabled" in next_page.get_attribute("class"): # to handle disabled last page
            break
        old_page=products[0] # save old page to check if becomes stale
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",next_page) # scroll till next page icon
        driver.execute_script("arguments[0].click();", next_page)
        WebDriverWait(driver, 10).until(
            EC.staleness_of(old_page)
        )
        products=driver.find_elements(By.CSS_SELECTOR,"li.product-base")
        print("Page Loaded",page)
        page+=1
    except (NoSuchElementException,TimeoutException):
        break
df=pd.DataFrame(shirt,columns=["brand","product_type","product_price","product_actual_price","product_page_url","product_img_url"])
df.to_csv("shirt.csv",index=False)
print("Finished Scrapping")
driver.quit()
