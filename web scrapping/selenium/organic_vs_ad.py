from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
import time
import pandas as pd
import logging
# webdriver setup
def set_up_driver():
    options = Options()
    driver=webdriver.Chrome(options=options)
    logging.basicConfig(filename="selenium_log.log",level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return driver

# webdriverwait instead of temp.sleep()
def wait_for(driver):
    try:
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,"li.product-base"))
        )
        logging.info("Page loaded")
        return True
    except TimeoutException:
        logging.error("Page timed out")
        return False
# scrape logic to reuse everytime
def scrape(p,by,location):
    try:
        return p.find_element(by,location).text
    except (NoSuchElementException,NoSuchAttributeException):
        return ""
# scrape logic with attribute for img and product url
def scrape_url(p,by,location,attribute):
    try:
        return p.find_element(by,location).get_attribute(attribute) # dont add text bcz its a link
    except (NoSuchElementException,NoSuchAttributeException):
        return ""
# infinite scroll
#def ensure_lazy_images_loaded(driver, step=100, delay=0.4):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        #or
    old_height = driver.execute_script("return document.body.scrollHeight") # calculate initial height
    y = 0
    while y<old_height: # loop till y is greater
        driver.execute_script(f"window.scrollTo(0, {y});",old_height) # driver.execute_script("window.scrollTo(0,arguments[0]);",y)
        time.sleep(delay) # then wait for some second
        new_height=driver.execute_script("return document.body.scrollHeight")
        if old_height == new_height:
            break
        y += step # then increase y
        old_height=new_height # this will increase if it's infinite scroll page, if not it will remain same

# lazy loading to load image url and upload it in list
def ensure_lazy_images_loaded(driver, step=400, delay=0.4):
    height = driver.execute_script("return document.body.scrollHeight") # calculate initial height
    y = 0
    while y < height: # loop till y is greater
        driver.execute_script(f"window.scrollTo(0, {y});") # will scroll till page end point
        time.sleep(delay) # then wait for some second
        y += step # then increase y
        height=driver.execute_script("return document.body.scrollHeight") # this will increase if its  infinite scroll page if not it will remain same

# looping to add all scraped element to the list
def looping(driver):
        product = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
        sponsor=[]
        organic=[]
        for p in product:
            brand = scrape(p, By.CSS_SELECTOR, "h3.product-brand")
            ad = scrape(p, By.CSS_SELECTOR, "div.product-waterMark")
            product_url = scrape_url(p, By.CSS_SELECTOR, "a", "href")
            actualStrike = scrape(p, By.CSS_SELECTOR, "span.product-strike")
            product_img = scrape_url(p, By.CSS_SELECTOR, "img.img-responsive", "src")
            Discount_price = scrape(p, By.CSS_SELECTOR, "span.product-discountedPrice")
            if actualStrike!="":
                row=[brand,actualStrike,ad,Discount_price,product_url, product_img]
            else :
                price = scrape(p, By.CSS_SELECTOR, ".product-price span")  # same for all
                row=[brand, price, ad,"Nil",product_url, product_img]
            if ad!="":
                sponsor.append(row)
            else:
                organic.append(row)
        return sponsor,organic


# to check if pagination exist or not
def next_pagination(driver,product):
    try:
        next_page=driver.find_element(By.CSS_SELECTOR,"li.pagination-next")
        if "disabled" in next_page.get_attribute("class"):
            return False
        first_product=product[0]
        driver.execute_script(
            "arguments[0].scrollIntoView();",next_page ) # in this argument[0]-> next_page it will load until that is encountered if encountered then
        driver.execute_script("arguments[0].click();",next_page) # it will click that next page this is what makes you move to next page
        WebDriverWait(driver,10).until( # we need remove the first_product from the driver to load next page
            EC.staleness_of(first_product)
        )
        return True
    except (NoSuchElementException,TimeoutException) as e: # if next is not there or webdriver did not fetch any data then it will return false
        logging.error(f"Error: {e}")
        return False
#to load into csv
def to_csv(organic,sponsored):
    df = pd.DataFrame(organic, columns=["brand", "actual_price", "ad", "discount_price", "product_url", "product_img"])
    df1 = pd.DataFrame(sponsored, columns=["brand", "actual_price", "ad", "discount_price", "product_url", "product_img"])
    df.to_csv("Organic.csv", index=False)
    df1.to_csv("Ad.csv", index=False)
    print("Finished Scrapping")
    logging.info("Added to CSV")

# main function
def main():
    driver=set_up_driver()
    driver.get("https://www.myntra.com/h-and-m?rawQuery=h%26m")
    page = 1;
    orgainc_data=[]
    sponsored_data=[]
    if not wait_for(driver):
        print("Timed out")
        driver.quit()
        return
    while page<=2:
        logging.info(f"Scraping page {page}")
        ensure_lazy_images_loaded(driver, step=400, delay=0.4)
        product = driver.find_elements(By.CSS_SELECTOR, "li.product-base") # load the product
        sponsored,organic=looping(driver)
        orgainc_data.extend(organic)
        sponsored_data.extend(sponsored)
        next_page_exist=next_pagination(driver,product)
        if not next_page_exist:
            break
        page+=1
        logging.info(f"Scraped page {page}")
    to_csv(orgainc_data,sponsored_data)
    driver.quit()
# to call main function
if __name__ == "__main__":
    main()


