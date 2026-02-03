import requests
from bs4 import BeautifulSoup

url="https://quotes.toscrape.com/"

response=requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

quotes=soup.find_all("span",class_="text")
author=soup.find_all("small",class_="author")

for i in range(len(quotes)):
    quote_text=quotes[i].get_text()
    author_text=author[i].get_text()
    print(f"Quote: {quote_text}")
    print(f"Author:{author_text}")
    print("--")
