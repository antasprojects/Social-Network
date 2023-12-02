import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import json

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


import requests
import json

def searchmovie(title):

    url = "https://imdb8.p.rapidapi.com/auto-complete"

    headers = {
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': "2487fc5158msh0e1bde7ecf9be4dp11dad9jsndd8c3b2b8dde"
    }

    searchTerm = title

    querystring = {"q": searchTerm}

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = json.loads(response.text)

    formattedData = json.dumps(data, indent=4)

    dataDict = json.loads(formattedData)

    result = (dataDict["d"])



    list = []

    for movie in result:
        try:
            dict = {}
            dict['title'] = movie["l"]
            dict['image'] = movie["i"]["imageUrl"]
            dict['actors'] = movie['s']
            list.append(dict)
        except:
            pass

    return list


