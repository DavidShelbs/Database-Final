import flask
import imdb
from imdb import IMDb
from flask import Flask, flash, redirect, render_template, request, session, abort
import tmdbsimple as tmdb
import json
import os
import sqlite3
tmdb.API_KEY = '3aac901eabe71551bd666ed711135477'

app = Flask(__name__)
movie_api = IMDb()
data = {}
data['movie'] = []


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return flask.render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            data['movie'].clear()

            search_query = request.form['search_bar']

            search = tmdb.Search()
            response = search.movie(query=search_query)
            i = 0
            for s in search.results:
                data['movie'].append({
                    'title': s['title'],
                    'overview': s['overview'],
                    'poster_path': s['poster_path'],
                    'release_date': s['release_date']
                })

            with open('static/movies.json', 'w') as outfile:
                json.dump(data, outfile)
            return flask.render_template('index.html')
    else:
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return flask.render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    db = sqlite3.connect('webserver.db')
    cursor = db.execute("SELECT u_password FROM USERS WHERE u_name = ?", (request.form['username'],))
    password = ''
    for row in cursor:
        password = row[0]
    if password == '':
        db.close()
        return home()
    if request.form['password'] == password:
        session['logged_in'] = True
        db.close()
    return home()

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['confirmpassword'] == request.form['password'] and request.form['username'] != '' and request.form['e-mail'] != '' and request.form['password'] != '':
            session['logged_in'] = True
            db = sqlite3.connect('webserver.db')
            username = ''
            cursor = db.execute("SELECT u_name FROM USERS WHERE u_name = ?", (request.form['username'],))
            for row in cursor:
                username = row[0]
            if username != '':
                db.close()
                return render_template('signup.html')
            else:
                db.execute("INSERT INTO USERS (u_name, u_email, u_password) VALUES (?, ?, ?)", (request.form['username'], request.form['e-mail'], request.form['password']));
                db.commit()
                db.close()
                return render_template('index.html')
    return render_template('signup.html')


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    db = sqlite3.connect('webserver.db')
    db.execute('''CREATE TABLE IF NOT EXISTS USERS
    (
        u_id        INTEGER     PRIMARY KEY,
        u_name      TEXT    NOT NULL,
        u_email     TEXT    NOT NULL,
        u_password  TEXT    NOT NULL
    );''')
    db.close()
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port='80', debug='false')
    # app.run(host='192.168.0.16', port='80', debug='false')
