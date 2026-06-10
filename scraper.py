import requests
from bs4 import BeautifulSoup
import json

def get_games():
    return[
        {
            "title": "Terraria",
            "price": 4.99,
            "genre": "Sandbox",
            "discount": 50
        }
    ]

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
                "price": float(deal["salePrice"]),
                "genre": genre_cache.get(deal["title"], []),
                "discount": discount
            }
        )
    return results

if __name__ == "__main__":
    deals=get_game_deals()
    print(deals[0])

def load_genre_cache():
    try:
        with open("genres.json", "r")as file:
            return json.load(file)
    except:
        return {}