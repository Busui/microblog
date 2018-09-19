from flask import render_template
from app import app

@app.route("/index")
@app.route("/")
def index():
    user = {"username": "lovekernel"}
    return render_template("index.html", title = "Home page", user = user)