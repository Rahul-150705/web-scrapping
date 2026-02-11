import time
import pandas as pd
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def set_driver():
    options=Options()
    driver=webdriver.Chrome(options=options)
    return driver


def web_driver_wait(driver):
    try:
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"li.product-base"))
        )
        return True
    except TimeoutException:
        return False

# thi s is the code for lazy-loading
def lazy_loading(driver,delay=0.4,step=500):
    old_height=driver.execute_script("return document.body.scrollHeight") # loads until the
    y=0;
    while y<old_height:
        driver.execute_script("window.scrollTo(0,arguments[0]);",y)
        time.sleep(delay)
        y+=step
        old_height=driver.execute_script("return document.body.scrollHeight")
# infinite scroll

def infinite_scroll(driver,delay=0.4,step=500):
    old_height=driver.execute_script("return document.body.scrollHeight")
    y=0;
    while True:
        driver.execute_script("window.scrollTo(0,arguments[0]);",y)
        time.sleep(delay)
        new_height=driver.execute_script("return document.body.scrollHeight")
        if old_height==new_height:
            break
        y+=step
        old_height=new_height


def scroll_to_load_all(driver, delay=0.5):
    """Scrolls down until no new content is loaded"""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load
        time.sleep(delay)

        # Get new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # Check if page height has stopped increasing
        if new_height == last_height:
            break

        last_height = new_height


def looping(driver):
    shirt = []
    product=driver.find_elements(By.CSS_SELECTOR,"li.product-base")
    for p in product:
        brand=p.find_element(By.CSS_SELECTOR,"h3.product-brand").text
        price=p.find_element(By.CSS_SELECTOR,"div.product-price span").text
        try:
            img=p.find_element(By.CSS_SELECTOR,"img.img-responsive").get_attribute("src")
        except NoSuchElementException:
            img=""
        shirt.append([brand,price,img])
    return shirt


def next_page_exist(driver,product):
    try:
        next_page=driver.find_element(By.CSS_SELECTOR,"li.pagination-next")
        if "disabled" in next_page.get_attribute("class"):
            return False
        first_product=product[0] # waiting till previous page product is no longer attached to dom
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});",next_page)
        driver.execute_script("arguments[0].click();",next_page)
        WebDriverWait(driver,10).until(
            EC.staleness_of(first_product)
        )
        return True
    except (NoSuchElementException , TimeoutException ):
        return False
def main():
    driver=set_driver()
    final_product=[]
    driver.get("https://www.myntra.com/h-and-m?rawQuery=h%26m")
    if not web_driver_wait(driver):
        print("ERROR TIMEOUT")
        driver.quit()
    page=1;
    while page<=2:
        lazy_loading(driver)
        products=driver.find_elements(By.CSS_SELECTOR,"li.product-base") # used for pagination logic
        prod=looping(driver)
        final_product.extend(prod)
        if not next_page_exist(driver,products):
            break
        page+=1
    pd.DataFrame(final_product,columns=["brand","price","img"]).to_csv("final_product.csv",index=False,encoding="utf-8")
    driver.quit()
if __name__=="__main__":
    main()






