from multiprocessing.context import AuthenticationError

import pandas as pd
import requests


session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.myntra.com/",
}

# Visit homepage FIRST (sets cookies)
home = session.get("https://www.myntra.com/", headers=headers, timeout=10)
print("Home:", home.status_code)

#Now call the API
page=1
row=50
offset=(page-1)*row
list=[]
while page<10:
    try:
        url = "https://www.myntra.com/gateway/v4/search/watches"
        params = {
            "rawQuery": "watches",  # this denotes the name of the search
            "rows": row,  # this defines the row
            "o": offset,  # represents offset if its 50 then it will start from 50 and go unti page end
            "p": page
        }
        response = session.get(url, params=params, headers=headers, timeout=10)
    except AuthenticationError:
        break
    if response.status_code == 200:
        data=response.json()
    else:
        break
    products = data["products"]
    if not products:
        break
    for p in products:
        list.append({
            "brand":p.get("brand"),
            "product_name":p.get("product"),
            "price":p.get("price"),
            "image":p.get("searchImage")
            })
    page =page+1
    offset=row+offset

data=pd.DataFrame(list).to_csv("123.csv",index=False,header=False)
print("added to csv")


