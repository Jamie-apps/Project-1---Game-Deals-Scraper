import requests
from bs4 import BeautifulSoup
import json
import urllib.parse

def load_genre_cache():
    try:
        with open("genres.json", "r")as file:
            return json.load(file)
    except:
        return {}
    
def load_store_cache():
    try:
        with open("stores.json", "r")as file:
            return json.load(file)
    except:
        return{}

def test_scraper():
    with open("practice.html", "r") as file:
        html=file.read()
    soup=BeautifulSoup(html, "html.parser")
    games=soup.find_all("div")
    results=[]
    for game in games:
        results.append(
            {
                "title": game.text.strip(),
                "price": 0,
                "genre": "unknown",
                "discount": 0
            }
        )
    print(results)
    return(results)

def get_game_deals():
    genre_cache=(load_genre_cache())
    store_cache=(load_store_cache())
    url=("https://www.cheapshark.com/api/1.0/deals")
    response=requests.get(url)
    deals=response.json()
    results=[]
    for deal in deals[:20]:
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
                "genres": genre_cache.get(deal["title"], []),
                "store": store_cache.get(deal["storeID"],{}),
                "deal_url": ("https://www.cheapshark.com/redirect?dealID="+deal["dealID"])
            }
        )
    return results

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
    test_deal()