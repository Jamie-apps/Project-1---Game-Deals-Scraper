from flask import Flask, render_template, request, Response
from scraper import get_game_deals
from urllib.parse import urlencode

app=Flask(__name__)
DEALS_PER_PAGE=20

def calculate_deal_score(game):
    return(
        game["discount"]+(20/(game["sale_price"]+1))
    )

@app.route("/")
def home():
    search=request.args.get("search", "")
    page=request.args.get("page", 1, type=int)
    max_price=request.args.get("max_price", type=float)
    sort=request.args.get("sort", "")
    genre=request.args.get("genre", "")
    store=request.args.get("store", "")
    games=get_game_deals()
    all_genres=set()
    for game in games:
        for genre_name in game["genres"]:
            all_genres.add(genre_name)
    all_genres=sorted(all_genres)
    all_stores=set()
    for game in games:
        all_stores.add(
            game["store"]["name"]
        )
    all_stores=sorted(all_stores)
    if search:
        games=[
            game for game in games if search.lower() in game["title"].lower()
        ]
    if max_price is not None:
        games=[
            game for game in games if game["sale_price"] <= max_price
        ]
    if genre:
        games=[
            game for game in games if genre in game ["genres"]
        ]
    if store:
        games=[
            game for game in games if game["store"]["name"]==store
        ]
    if sort=="discount":
        games.sort(
            key=lambda game: game["discount"], reverse=True
        )
    elif sort=="price":
        games.sort(
            key=lambda game: game["sale_price"]
        )
    elif sort=="title":
        games.sort(
            key=lambda game: game["title"]
        )

    best_deal=None
    top_deal_url=""
    if games:
        best_deal=max(
            games, key=calculate_deal_score 
        )

    top_deal_url=best_deal["deal_url"]

    total_pages= (
        len(games)+DEALS_PER_PAGE-1
    )//DEALS_PER_PAGE

    start=(page-1)*DEALS_PER_PAGE
    end=start+DEALS_PER_PAGE

    games=games[start:end]

    params=request.args.to_dict()
    prev_url=None
    next_url=None
    if page>1:
        prev_params=request.args.to_dict()
        prev_params["page"]=page-1
        prev_url="?"+urlencode(prev_params)
    if page<total_pages:
        next_params=request.args.to_dict()
        next_params["page"]=page+1
        next_url="?"+urlencode(next_params)

    return render_template("index.html", games=games, search=search, max_price=max_price, sort=sort, genre=genre, best_deal=best_deal, all_genres=all_genres, top_deal_url=top_deal_url, all_stores=all_stores, store=store, page=page, total_pages=total_pages, prev_url=prev_url, next_url=next_url)

@app.route("/export")
def export_csv():
    games=get_game_deals()
    csv_data="Title,Sale Price,Original Price,Discount,Store\n"
    for game in games:
        csv_data += (
            f"{game['title']},"
            f"{game['sale_price']},"
            f"{game['original_price']},"
            f"{game['discount']},"
            f"{game['store']['name']}\n"
        )
    return Response(
        csv_data, mimetype="text/csv", headers={"content-disposition": "attachment; filename=game_deals.csv"}
    )

app.run(debug=True)