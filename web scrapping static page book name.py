import requests

from bs4 import BeautifulSoup
import pandas as pd
import lxml
first_page="https://books.toscrape.com/"
response=requests.get(first_page)
status=response.status_code
print(status)
d=1;
data=[]
books=[]
while(status==200 and d<3):
    url = f"https://books.toscrape.com/catalogue/page-{d}.html"
    response=requests.get(url)
    state=response.status_code
    if(state!=200):
        break;
    soup=BeautifulSoup(response.text,"html.parser")

    book_name=soup.select("article.product_pod h3 a")

    book_price=soup.select("div.product_price p.price_color")

    book_stock=soup.select("p.instock.availability")
    for name,price,stock in zip(book_name,book_price,book_stock):
        pric=price.text.replace("£","").replace("Â","")
        data.append([name.get("title"),pric,stock.text.strip(),state])
    d+=1;
df = pd.DataFrame(data,columns=["Name","Price","Stock","Status Code"])
df.to_csv("xyzz.csv", index=False)
print("Added to CSV with total data",d)


    
