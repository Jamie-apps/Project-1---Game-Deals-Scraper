import json
import os
import requests
from dotenv import load_dotenv
from scraper import get_game_deals

games=get_game_deals()[:10]

with open("genres.json", "r")as file:
    cache=json.load(file)

load_dotenv()

API_KEY=os.getenv("RAWG_API_KEY")

def search_game(title):
    url=("https://api.rawg.io/api/games")
    params={
        "key": API_KEY,
        "search": title,
        "page_size": 1
    }
    response=requests.get(
        url, params=params
    )
    data=response.json()
    return data

def get_genres(title):
    result=search_game(title)
    if not result["results"]:
        return[]
    game=result["results"][0]
    genres=[]
    for genre in game["genres"]:
        genres.append(genre["name"])
    return genres

for game in games:
    title=game["title"]
    if title not in cache:
        print(f"Looking up: {title}")
        cache[title]=(get_genres(title))

with open("genres.json", "w")as file:
    json.dump(
        cache, file, indent=4
    )