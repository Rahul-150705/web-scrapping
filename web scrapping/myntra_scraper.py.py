from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = Options()



driver = webdriver.Chrome(options=options)
driver.get("https://www.myntra.com/shirt?rawQuery=shirt")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.product-base"))
    )
    print("Product located")
except TimeoutException:
    print("Timed out")

pro =driver.find_elements(By.CSS_SELECTOR, "li.product-base")
for p in pro:
    brand=p.find_element(By.CSS_SELECTOR, "h3.product-brand").text
    print(brand)