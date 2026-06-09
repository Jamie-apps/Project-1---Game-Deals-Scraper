from flask import Flask, render_template, request, Response
from scraper import get_game_deals

app=Flask(__name__)

@app.route("/")
def home():
    search=request.args.get("search", "")
    max_price=request.args.get("max_price", type=float)
    sort=request.args.get("sort", "")
    games=get_game_deals()
    if search:
        games=[
            game for game in games if search.lower() in game["title"].lower()
        ]
    if max_price is not None:
        games=[
            game for game in games if game["price"] <= max_price
        ]
    if sort=="discount":
        games.sort(
            key=lambda game: game["discount"], reverse=True
        )
    elif sort=="price":
        games.sort(
            key=lambda game: game["price"]
        )
    elif sort=="title":
        games.sort(
            key=lambda game: game["title"]
        )

    best_deal=None
    if games:
        best_deal=max(
            games, key=lambda game: game["discount"]
        )
    return render_template("index.html", games=games, search=search, max_price=max_price, sort=sort, best_deal=best_deal)

@app.route("/export")
def export_csv():
    games=get_game_deals()
    csv_data="Title,Price,Discount\n"
    for game in games:
        csv_data += (
            f"{game['title']},"
            f"{game['price']},"
            f"{game['discount']}\n"
        )
    return Response(
        csv_data, mimetype="text/csv", headers={"content-disposition": "attachment; filename=game_deals.csv"}
    )

app.run(debug=True)