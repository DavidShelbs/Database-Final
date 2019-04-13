import flask
import imdb
from imdb import IMDb
from flask import Flask, flash, redirect, render_template, request, session, abort
import tmdbsimple as tmdb
import json
tmdb.API_KEY = '3aac901eabe71551bd666ed711135477'

app = Flask(__name__)
movie_api = IMDb()
data = {}
data['movie'] = []


@app.route('/')
def home():
    print("/")
    return flask.render_template('index.html')

@app.route('/index.html')
def index():
    print("/index.html")
    return flask.render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # if request.method == 'POST':
    print("/search")
    data['movie'].clear()

    search_query = request.form['search']

    search = tmdb.Search()
    response = search.movie(query=search_query)
    i = 0
    for s in search.results:
        # if i < 4:
            data['movie'].append({
                'title': s['title'],
                'overview': s['overview'],
                'poster_path': s['poster_path'],
                'release_date': s['release_date']
            })
            # i = i + 1

    with open('static/movies.json', 'w') as outfile:
        json.dump(data, outfile)
    print("hi")
    return flask.render_template('index.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug='false')
    # app.run(host='192.168.0.16', port='80', debug='false')
