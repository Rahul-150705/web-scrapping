import time

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

def set_up():
    options=Options()
    driver=webdriver.Chrome(options=options)
    driver.get("https://www.myntra.com/h-and-m?rawQuery=h%26m")
    return driver
def web_driver_wait(driver):
    try:
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR,"li.product-base"))
        )
        return True
    except TimeoutException:
        return False

def looping(driver):
    global shirt
    shirt=[]
    products=driver.find_elements(By.CSS_SELECTOR,"li.product-base")
    for p in products:
        brand=p.find_element(By.CSS_SELECTOR,"h3.product-brand").text
        image=p.find_element(By.CSS_SELECTOR,"img.img-responsive").get_attribute("src")
        shirt.append([brand,image])
    return shirt
def lazy_loading(driver, step=100, delay=0.4):
    old_height = driver.execute_script("return document.body.scrollHeight") # calculate initial height
    y = 0
    while y<old_height: # loop till y is greater
        driver.execute_script(f"window.scrollTo(0,{y});",old_height) # driver.execute_script("window.scrollTo(0,arguments[0]);",y)
        time.sleep(delay) # then wait for some second
        y += step # then increase y
        old_height=driver.execute_script("return document.body.scrollHeight") #
def next_pagination(driver,products):
    try:
        next_page=driver.find_element(By.CSS_SELECTOR,"li.pagination-next")
        if "disabled" in next_page.get_attribute("class"):
            print("Next page is disabled")
            return False
        first_product=products[0]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});",next_page)
        driver.execute_script("arguments[0].click();",next_page)
        WebDriverWait(driver, 10).until(
            expected_conditions.staleness_of(first_product)
        )
        return True
    except (TimeoutException,NoSuchElementException):
        return False
def convert_to_csv(final_product):
    df=pd.DataFrame(final_product,columns=["brand","image"])
    df.to_csv("selenium_test.csv",index=False)
def main():
    driver=set_up()
    print("Driver SetUp Done")
    page=1
    final_product=[]
    if not web_driver_wait(driver):
        print("ERROR")
        driver.quit()
    print("Driver Wait Done")
    while page<=2:
        print("Scrapping page:",page)
        lazy_loading(driver)
        items=looping(driver)
        product=driver.find_elements(By.CSS_SELECTOR,"li.product-base") # for staleness pagination logic
        final_product.extend(items)
        find_page=next_pagination(driver,product)
        if not find_page:
            break
        print(f"Scrapped Page:{page} With Total Product Of {len(items)}")
        page+=1
    convert_to_csv(final_product)
if __name__=="__main__":
    main()


