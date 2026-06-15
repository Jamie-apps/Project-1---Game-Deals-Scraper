import json
import requests

def get_stores():
    response = requests.get("https://www.cheapshark.com/api/1.0/stores")
    return response.json()

def build_store_cache():
    stores = get_stores()
    results = {}
    for store in stores:
        store_id = store["storeID"]
        results[store_id] = {
            "name": store["storeName"],
            "logo": "https://www.cheapshark.com" + store["images"]["logo"]
        }
    return results

stores = build_store_cache()
with open("stores.json", "w")as file:
    json.dump(
        stores,
        file,
        indent = 4
    )