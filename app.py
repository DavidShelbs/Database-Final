import flask
import imdb
from imdb import IMDb
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_from_directory
import tmdbsimple as tmdb
import json
import os
import sqlite3
from werkzeug.utils import secure_filename

tmdb.API_KEY = '3aac901eabe71551bd666ed711135477'

app = Flask(__name__)
movie_api = IMDb()
data = {}
data['movie'] = []

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mkv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
u_id = ''

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

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    if request.method == 'POST':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            db = sqlite3.connect('webserver.db')
            cursor = db.execute("SELECT u_id FROM USERS WHERE u_name = ?", (request.form['search_bar'],))
            for row in cursor:
                f_id2 = row[0]
            f_id1 = u_id
            db.execute("INSERT INTO FRIENDS (f_id1, f_id2) VALUES (?, ?)", (f_id1, f_id2));
            db.commit()
            db.close()

            return flask.render_template('index.html')
    else:
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return flask.render_template('friends.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = filename[:-3]
            filename += "txt"
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return home()
    return home()

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/download")
def download():
    db = sqlite3.connect('webserver.db')
    global u_id
    cursor = db.execute("SELECT u_key FROM USERS WHERE u_id = ?", (u_id,))
    key = 0
    for row in cursor:
        key = row[0]
    if key == 1:
        file = open("static/upload/Divergent.txt", "rb")
        return flask.Response(file, mimetype="video/mp4", headers={"Content-disposition" : "attachment; filename=myplot.mp4"})
        return home()
    else:
        return home()


@app.route('/login', methods=['POST'])
def login():
    global u_id
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
        cursor = db.execute("SELECT u_id FROM USERS WHERE u_name = ?", (request.form['username'],))
        for row in cursor:
            u_id = row[0]
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
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port='80', debug='false')
    # app.run(host='192.168.0.20', port='80', debug='false')
