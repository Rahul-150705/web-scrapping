import requests
import json

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-device-id": "39913fbf-62dc-44db-85b2-a1f56f053e16",
    "x-store-id": "4f54ea62-0269-4b93-87cd-ef7ed796c6b1",
    "x-city-id": "1",  # optional, can get from frontend if needed
    "Accept": "application/json",
    "Referer": "https://www.zepto.com",
}

# Example search query
params = {
    "rawQuery": "Chocolate ice cream cone",
    "rows": 20,
    "o": 0,
    "p": 1
}

url = "https://bff-gateway.zepto.com/user-search-service/api/v3/search"

response = session.get(url, params=params, headers=headers)
data = response.json()

# Check top-level keys
print(data.keys())

# Extract product names & prices (example)
for product in data.get("products", []):
    name = product.get("product_name", "N/A")
    selling_price = product.get("price", {}).get("selling_price", "N/A")
    mrp = product.get("price", {}).get("mrp", "N/A")
    print(name, selling_price, mrp)
