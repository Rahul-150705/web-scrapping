from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


options = Options()
driver = webdriver.Chrome(options=options)
driver.get("https://www.zepto.com/search?query=Chocolate+ice+cream+cone")

wait = WebDriverWait(driver, 10)
wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div[data-slot-id='ProductName'] span")
    )
)

# Scroll for lazy loading
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Collect names AFTER scrolling is finished
names = driver.find_elements(
    By.CSS_SELECTOR,
    "div[data-slot-id='ProductName'] span"
)
prices = driver.find_elements(By.CSS_SELECTOR, "div[data-slot-id='EdlpPrice']")
print("Total products:", len(names))
products=[]
for n,x in zip(names,prices):
    namee=n.get_attribute("textContent")
    p=x.get_attribute("textContent").strip()
    products.append({
        "name": namee,
        "price": p,
    })
print(products)
driver.quit()
