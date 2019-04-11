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
    return flask.render_template('index.html')

@app.route('/index.html')
def index():
    return flask.render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        out_data = list()
        url_data = list()
        data['movie'].clear()

        search_query = request.form['search']

        search = tmdb.Search()
        response = search.movie(query=search_query)
        for s in search.results:
            out_data.append(s['title'])
            url_data.append(s['poster_path'])
            data['movie'].append({
                'title': s['title'],
                'url': s['poster_path'],
            })

        # movies = movie_api.search_movie(search_query)
        #
        # for movie in movies:
        #     out_data.append(movie['title'])
        #     id = movie.movieID
        #     # film = movie_api.get_movie(id)
        #     # if 'cover url' in film:
        #     #     url_data.append(film['cover url'])
        print(data['movie'])
        with open('static/movies.json', 'w') as outfile:
            json.dump(data, outfile)
        # print(out_data)
        # print(url_data)
        return flask.render_template('index.html', out_data = out_data, url_data = url_data)
    return flask.redirect('')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug='false')
    # app.run(host='192.168.0.16', port='80', debug='false')
