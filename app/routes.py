from flask import render_template
from app import app

@app.route("/index")
@app.route("/")
def index():
    user = {"username": "lovekernel"}
    posts = [
        {
            'author':{'username':'John'},
            'body':'Beautiful day in Portland!'
        },
        {
            'author':{'username':'Susan'},
            'body':'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title = 'Home', user = user, posts = posts)