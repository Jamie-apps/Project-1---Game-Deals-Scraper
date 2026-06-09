from flask import Flask, render_template
from scraper import get_game_deals

app=Flask(__name__)

@app.route("/")
def home():
    games=get_game_deals()
    return render_template("index.html", games=games)

app.run(debug=True)