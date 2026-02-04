import requests
from bs4 import BeautifulSoup

url="https://quotes.toscrape.com/"

req=requests.get(url)


if req.status_code==200:
    print("successfull")
else:
    print("failed")
