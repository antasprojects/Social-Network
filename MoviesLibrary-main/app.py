import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, searchmovie

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///movies.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")

def index():





    return redirect("/search")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

         # Ensure passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match")

        username = request.form.get("username")

        # Ensure the username is not in database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 0:
            return apology("username already exist")

        # Generate password hash
        hash = generate_password_hash(request.form.get("password"))


        # Insert username and password hash in the database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)


        # Load session for the user
        userid = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))[0]["id"]
        session["user_id"] = userid

        # Redirect to he mainpage
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# SEARCH FUNCTIONS

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():


    if request.method == "POST":

        title = request.form.get("title")

        data = searchmovie(title)


        return render_template("search.html", data=data)

    else:

        return render_template("search.html")



@app.route("/add_to_watchlist", methods=["POST"])
@login_required
def add_to_watchlist():
    if request.method == "POST":

        movie = request.form.get("movie")


        image, title, actors = movie.split(';;')


        db.execute("INSERT INTO watch (user_id, img, title, actors) VALUES (?, ?, ?, ?)", session["user_id"], image, title, actors)

        return redirect("/search")




@app.route("/add_to_watchedlist", methods=["POST"])
@login_required
def add_to_watchedlist():

    if request.method == "POST":

        movie = request.form.get("movie")


        image, title, actors = movie.split(';;')


        db.execute("INSERT INTO watched (user_id, img, title, actors) VALUES (?, ?, ?, ?)", session["user_id"], image, title, actors)

        return redirect("/search")



## WATCHLIST FUNCTIONS

@app.route("/watch")
@login_required
def watch():


    data = db.execute("SELECT * FROM watch WHERE user_id = ?", session["user_id"])



    return render_template("watch.html", data=data)

@app.route("/add_to_watched", methods=["POST"])
@login_required
def add_to_watched():
    if request.method == "POST":

        movie = request.form.get("movie")
        image, title, actors = movie.split(';;')

        db.execute("INSERT INTO watched (user_id, img, title, actors) VALUES (?, ?, ?, ?)", session["user_id"], image, title, actors)

        db.execute("DELETE FROM watch WHERE user_id = ? AND title = ? ", session["user_id"], title)


    return redirect("/watch")

@app.route("/delete_from_watchlist", methods=["POST"])
@login_required
def delete_from_watchlist():

    if request.method == "POST":

        movie = request.form.get("movie")

        image, title, actors = movie.split(';;')


        db.execute("DELETE FROM watch WHERE user_id = ? AND title = ? ", session["user_id"], title)

        return redirect("/watch")


## WATCHED FUNCTIONS

@app.route("/watched")
@login_required
def watched():


    data = db.execute("SELECT * FROM watched WHERE user_id = ?", session["user_id"])



    return render_template("watched.html", data=data)




@app.route("/delete_from_watchedlist", methods=["POST"])
@login_required
def delete_from_watchedlist():

    if request.method == "POST":

        movie = request.form.get("movie")

        image, title, actors = movie.split(';;')


        db.execute("DELETE FROM watched WHERE user_id = ? AND title = ? ", session["user_id"], title)

        return redirect("/watched")


@app.route("/rate_movie", methods=["POST"])
@login_required
def rate_movie():

    if request.method == "POST":

        movie = request.form.get("rating")

        image, title, actors, rating = movie.split(';;')

        db.execute("DELETE FROM watched WHERE user_id = ? AND title = ? ", session["user_id"], title)

        db.execute("INSERT INTO rated (user_id, img, title, actors, rating) VALUES (?, ?, ?, ?, ?)", session["user_id"], image, title, actors, rating)

        return redirect("/watched")


## RANKING FUNCTIONS

@app.route("/ranking")
@login_required
def ranking():


    data = db.execute("SELECT * FROM rated WHERE user_id = ? ORDER BY rating DESC", session["user_id"])




    return render_template("ranking.html", data=data)

@app.route("/delete_from_ranking", methods=["POST"])
@login_required
def delete_from_ranking():

    if request.method == "POST":

        movie = request.form.get("movie")

        image, title, actors = movie.split(';;')

        db.execute("DELETE FROM rated WHERE user_id = ? AND title = ? ", session["user_id"], title)

        return redirect("/ranking")
