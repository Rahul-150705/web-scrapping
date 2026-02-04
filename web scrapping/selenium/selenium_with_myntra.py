from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = Options()
# options.add_argument("--headless=new") nott needed now

driver = webdriver.Chrome(options=options)
driver.get("https://www.myntra.com/shirt?rawQuery=shirt")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-base"))
    )
    print("Products loaded")
except TimeoutException:
    print("Timed out")

products = driver.find_elements(By.CSS_SELECTOR, "li.product-base")
for p in products:
    brand = p.find_element(By.CSS_SELECTOR, "h3.product-brand").text
    print(brand)
    break

driver.quit()
