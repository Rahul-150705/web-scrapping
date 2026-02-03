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
while(status==200):
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
    #for i in range(len(data)):
        # pric=data[i][1].split(".")[0]   #"51.77".split(".")-->['55','77']
        #pric=float(data[i][1])
        #if(int(pric)>50):
            #books.append(data[i])
    d+=1;
df = pd.DataFrame(data,columns=["Name","Price","Stock","Status Code"])
df.to_csv("pagination.csv", index=False)
print("Added to CSV")


    
