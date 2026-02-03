import requests

from bs4 import BeautifulSoup


response=requests.get("https://quotes.toscrape.com")

#makes the html to python understandable form

soup=BeautifulSoup(response.text,'html.parser')

# soup.select is a function and it is used to select the tag u gave inside it like this is css path learn dom to find this path like div.text things
quote=soup.select("div.quote span.text")

authour=soup.select("div.quote  small.author")


for i in range(len(quote)):
    print(quote[i].text)
    print("------",authour[i].text)
    print("")

