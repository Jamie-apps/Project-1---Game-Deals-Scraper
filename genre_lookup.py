import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAWG_API_KEY")

def load_genre_cache():
    try:
        with open("genres.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Genre cache missing or corrupted.")
        return {}

def save_genre_cache(cache):
    with open("genres.json", "w") as file:
        json.dump(cache, file, indent = 4)

# RAWG route

def search_rawg(title):
    url = "https://api.rawg.io/api/games"
    params = {
        "key": API_KEY,
        "search": title,
        "page_size": 1
    }
    try:
        response = requests.get(url, params = params, timeout = 10)
        data = response.json()
        if "results" not in data:
            return None
        if not data ["results"]:
            return []
        genres = []
        for genre in data ["results"][0].get("genres", []):
            genres.append(genre["name"])
        return genres
    except (requests.RequestException, ValueError) as error:
        print(f"RAWG lookup failed for {title}")
        return None

# Steam route

def search_steam(app_id):
    url = "https://store.steampowered.com/api/appdetails"
    params = {
        "appids": app_id
    }
    try:
        response = requests.get(url, params = params, timeout = 10, headers = {"User-Agent": "Bigdeal/1.0"})
        response.raise_for_status()
        data = response.json()
        game_data = data.get(str(app_id), {})
        if not game_data.get("success"):
            return None
        game = game_data.get("data", {})
        genres = []
        for genre in game.get("genres", []):
            if "description" in genre:
                genres.append(genre["description"])
            return genres
    except (requests.RequestException, ValueError) as error:
        print(f"Steam lookup failed for {app_id}: {error}")
        return None

# Main lookup function

def get_genres(title, steam_app_id = None):
    cache = load_genre_cache()
    if title in cache:
        return cache[title]
    print (f"Looking up genres: {title}")
    # Trying first with RAWG
    rawg_genres = search_rawg(title)
    if rawg_genres:
        print(f"RAWG found genres for {title}: {rawg_genres}")
        cache[title] = rawg_genres
        save_genre_cache(cache)
        return rawg_genres
    # Trying Steam if RAWG fails
    if steam_app_id:
        print(
            f"RAWG found nothing for {title}. "
            f"Trying Steam App ID {steam_app_id}..."
            )
        steam_genres = search_steam(steam_app_id)
        if steam_genres:
            print(
                f"Steam found genres for {title}: "
                f"{steam_genres}"
            )
            cache[title] = steam_genres
            save_genre_cache(cache)
            return steam_genres
    # If nothing is found in either route
    print(f"No genre found for {title}.")
    return []