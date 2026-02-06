from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import pandas as pd



def set_up_driver():
    options = Options()
    driver=webdriver.Chrome(options=options)
    return driver
def wait_for(driver):
    try:
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,"li.product-base"))
        )
        return True
    except TimeoutException:
        return False
def scrape(p,by,location):
    try:
        return p.find_element(by,location).text
    except (NoSuchElementException,NoSuchAttributeException):
        return ""
def scrape2(p,by,location,attribute):
    try:
        return p.find_element(by,location).get_attribute(attribute) # dont add text bcz its a link
    except NoSuchElementException:
        return ""

def ensure_lazy_images_loaded(driver, step=400, delay=0.4):
    height = driver.execute_script("return document.body.scrollHeight")
    y = 0

    while y < height:
        driver.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(delay)
        y += step
def looping(driver):
        product = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
        sponsor=[]
        organic=[]
        for p in product:
            brand = scrape(p, By.CSS_SELECTOR, "h3.product-brand")
            ad = scrape(p, By.CSS_SELECTOR, "div.product-waterMark")
            product_url = scrape2(p, By.CSS_SELECTOR, "a", "href")
            actualStrike = scrape(p, By.CSS_SELECTOR, "span.product-strike")
            product_img = scrape2(p, By.CSS_SELECTOR, "img.img-responsive", "src")
            if actualStrike!="":
                Discount_price = scrape(p, By.CSS_SELECTOR, "span.product-discountedPrice")
                row=[brand,actualStrike,ad,Discount_price,product_url, product_img]
            else :
                price = scrape(p, By.CSS_SELECTOR, ".product-price span")  # same for all
                row=[brand, price, ad,"Nil",product_url, product_img]
            if ad!="":
                sponsor.append(row)
            else:
                organic.append(row)
        return sponsor,organic
def next_pagination(driver,product):
    try:
        next_page=driver.find_element(By.CSS_SELECTOR,"li.pagination-next")
        if "disabled" in next_page.get_attribute("class"):
            return False
        first_product=product[0]
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",next_page )
        driver.execute_script("arguments[0].click();",next_page)
        WebDriverWait(driver,10).until(
            EC.staleness_of(first_product)
        )
        return True
    except (NoSuchElementException,TimeoutException):
        return False
def to_csv(organic,sponsored):
    df = pd.DataFrame(organic, columns=["brand", "actual_price", "ad", "discount_price", "product_url", "product_img"])
    df1 = pd.DataFrame(sponsored, columns=["brand", "actual_price", "ad", "discount_price", "product_url", "product_img"])
    df.to_csv("organic.csv", index=False)
    df1.to_csv("ad.csv", index=False)
    print("Finished Scrapping")
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
        print("Scrapping:",page)
        ensure_lazy_images_loaded(driver, step=400, delay=0.4)
        product = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
        sponsored,organic=looping(driver)
        orgainc_data.extend(organic)
        sponsored_data.extend(sponsored)
        d=next_pagination(driver,product)
        if not d:
            break
        page+=1
    to_csv(orgainc_data,sponsored_data)
    driver.quit()
if __name__ == "__main__":
    main()


