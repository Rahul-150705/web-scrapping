import requests


session = requests.Session()
base_url = "https://www.myntra.com"
headers={
    "User-Agent":"Mozilla/5.0",
    "Accept":"application/json",
    "Refer":base_url,
}
home=session.get(base_url,headers=headers,timeout=10) # to set cookies
if home.status_code==200:
    print("Success")
page=1
row=50
o=(page-1)*row

url="https://www.myntra.com/gateway/v4/search/watches"
params={
        "rawQuery":"watches",
        "rows":row,
        "o":o,
        "p":page,
}

data=session.get(url,params=params,headers=headers,timeout=10)
product=data.json()
print(product)
