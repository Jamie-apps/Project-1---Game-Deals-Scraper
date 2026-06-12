import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import time
from genre_lookup import get_genres

CACHE_DURATION=15*60
    
def load_store_cache():
    try:
        with open("stores.json", "r")as file:
            return json.load(file)
    except:
        return{}
    
def load_deal_cache():
    try:
        with open("deals_cache.json", "r")as file:
            return json.load(file)
    except:
        return {
            "timestamp": 0,
            "deals": []
        }


def get_game_deals():
    deal_cache=(load_deal_cache())
    if time.time() - deal_cache["timestamp"] < CACHE_DURATION:
        print("using cached deals.")
        return deal_cache["deals"]
    print("Fetching fresh deals.")
    store_cache=(load_store_cache())
    url=("https://www.cheapshark.com/api/1.0/deals")
    all_deals=[]
    for page in range(5):
        response=requests.get(
            url, params={
                "pageNumber": page,
                "pageSize": 20
            }
        )
        deals=response.json()
        print(f"Fetched page {page + 1}")
        all_deals.extend(deals)
    results=[]
    for deal in all_deals:
        sale_price=float(deal["salePrice"])
        discount=round(float(deal["savings"]))
        if sale_price<=0:
            continue
        results.append(
            {
                "title": deal["title"],
                "sale_price": sale_price,
                "original_price": float(deal["normalPrice"]),
                "discount": discount,
                "genres": get_genres(deal["title"]),
                "store": store_cache.get(deal["storeID"],{}),
                "deal_url": ("https://www.cheapshark.com/redirect?dealID="+deal["dealID"])
            }
        )
    print(f"Total deals processed: {len(results)}")
    save_deals_cache(results)
    return results

def save_deals_cache(deals):
    cache={
        "timestamp": time.time(),
        "deals": deals
    }
    with open("deals_cache.json", "w")as file:
        json.dump(cache, file, indent=4)

def test_deal():
    deal_id = "dua6N5u4HYIU5lUexFlvkjLixz5RHy0a4lzdZENh64A%3D"

    decoded_id = urllib.parse.unquote(deal_id)

    response = requests.get(
        "https://www.cheapshark.com/api/1.0/deals",
        params={
            "id": decoded_id
        }
    )

    print(response.url)
    print(response.json())

if __name__=="__main__":
    deals=get_game_deals()
    print(deals[0])