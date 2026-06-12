import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("RAWG_API_KEY")

def load_genre_cache():
    try:
        with open("genres.json", "r")as file:
            return json.load(file)
    except:
        return {}
    
def save_genre_cache(cache):
    with open("genres.json", "w")as file:
        json.dump(cache, file, indent=4)

def search_game(title):
    url="https://api.rawg.io/api/games"
    params={
        "key": API_KEY,
        "search": title,
        "page_size": 1
    }
    response=requests.get(url, params=params)
    return response.json()

def get_genres(title):
    cache=load_genre_cache()
    if title in cache:
        return cache[title]
    print(f"New game found. Searching RAWG: {title}")
    result=search_game(title)
    if not result["results"]:
        cache[title]=[]
        save_genre_cache(cache)
        return[]
    genres=[]
    for genre in result["results"][0]["genres"]:
        genres.append(genre["name"])
    cache[title]=genres
    save_genre_cache(cache)
    return genres