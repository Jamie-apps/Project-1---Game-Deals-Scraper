from flask import Flask, render_template, request, Response
from scraper import get_game_deals

app=Flask(__name__)

def calculate_deal_score(game):
    return(
        game["discount"]+(20/(game["sale_price"]+1))
    )

@app.route("/")
def home():
    search=request.args.get("search", "")
    max_price=request.args.get("max_price", type=float)
    sort=request.args.get("sort", "")
    genre=request.args.get("genre", "")
    games=get_game_deals()
    all_genres=set()
    for game in games:
        for genre_name in game["genres"]:
            all_genres.add(genre_name)
    all_genres=sorted(all_genres)
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

    return render_template("index.html", games=games, search=search, max_price=max_price, sort=sort, genre=genre, best_deal=best_deal, all_genres=all_genres, top_deal_url=top_deal_url)

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