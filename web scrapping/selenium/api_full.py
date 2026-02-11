import pprint
import sys

import requests
import time
import logging

session = requests.Session()
logging.basicConfig(filename="logging.log",level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
headers = {
    "User-Agent":"Mozilla/5.0",
    "Accept":"application/json",
    "Referer":"https://www.myntra.com/",
}
def fetch_with_retry(url,params=None,headers=None,timeout=10, retries=3,delay=0.5):
    for attempts in range(retries):
        try:
            response=session.get(url,headers=headers,params=params,timeout=timeout)
            if response.status_code == 200:
                return response
            else:
                logging.warning(f"Retrying Home Page Attempt:{attempts+1}",)
        except Exception as e:
            logging.warning(f"Request Failed Because Of Error on attempt {attempts+1}",e)
        time.sleep(delay * (2 ** (attempts))) # rate limiting added to sleep btw requests
    return None

home=fetch_with_retry("https://www.myntra.com/",headers=headers)
if home and home.status_code == 200:
    logging.info("Home:Success")
else:
    logging.error("Home:Failed")
    sys.exit()
page=1
row=50
list=[]
offset=(page-1)*row
while page<=2:
    params={
        "rawQuery":"h&m",
        "rows":row,
        "page":page,
        "offset":offset,
    }
    pages = fetch_with_retry("https://www.myntra.com/gateway/v4/search/h%26m", params=params, headers=headers,timeout=10)
    if not pages:
        logging.error(f"Page Failed {page}")
    data=pages.json()
    first_product=data['products']
    if not first_product:
        logging.error(f"Product not found  End of Scraping")
    for p in first_product:
        list.append({
            "Brand":p.get("brand"),
            "bestPrice":p.get("couponData",{}).get("couponDescription",{}).get("bestPrice"),
        })
    logging.info(f"Added {len(first_product)} products from page {page}")
    page+=1
    time.sleep(1)
logging.info(f"Added {len(list)} products with total page {page-1}")
print(list)