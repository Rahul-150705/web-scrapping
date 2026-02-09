import time
import pandas as pd
import requests

session = requests.Session()


base_url="https://www.myntra.com/"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": base_url,
}

# Visit homepage First bcz it sets and create a cookie to access the data if ur not doing this u may get error
home = session.get(base_url, headers=headers, timeout=10)
print("Home:", home.status_code)


#Now call the API
page=1
row=50
offset=(page-1)*row
url = "https://www.myntra.com/gateway/v4/search/h%26m"
items=[]
while page<10:
    params = {
        "rawQuery": "h&m",  # this denotes the name of the search
        "rows": row,  # this defines the row
        "o": offset,  # represents offset if its 50 then it will start from 50 and go unti page end
        "p": page
    }
    response = session.get(url, params=params, headers=headers, timeout=10)
    if response.status_code!=200:
        break
    data = response.json()
    first_product = data["products"]
    if not first_product:
        break
    for p in first_product:
        items.append({
            "Product ID": p.get("productId"),
            "Brand":p.get("brand"),
            "Category":p.get("category"),
            "Image URL":p.get("searchImage"),
            "Price":p.get("price"),
            "Product Name":p.get("productName"),
            "Rating":p.get("rating"),
            "Rating Count":p.get("ratingCount"),
            "Available Size":p.get("sizes")
        })
    time.sleep(2)
    page+=1
    offset=(page-1)*row
data=pd.DataFrame(items,columns=["Product ID","Brand","Category","Image URL","Price","Product Name","Rating","Rating Count","Available Size"])
data.drop_duplicates("Product ID",inplace=True)
data.to_csv("h&m.csv",index=False)
print("Scraped Products:",len(items))

