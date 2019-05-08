import flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, send_from_directory
import tmdbsimple as tmdb
import json
import os
import sqlite3
import datetime
from werkzeug.utils import secure_filename

tmdb.API_KEY = '3aac901eabe71551bd666ed711135477'

app = Flask(__name__)
data = {}
data['movie'] = []
friend_data = {}
friend_data['friend'] = []
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mkv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        data['movie'].clear()
        info = ""
        db = sqlite3.connect('webserver.db')
        cursor = db.execute('''SELECT m_title, m_release_date, m_age, r_id, m_poster, m_overview
                            FROM MOVIES, COLLECTIONS
                            WHERE MOVIES.m_id = COLLECTIONS.m_id AND COLLECTIONS.u_id = ?''', (session['u_id'],))
        for row in cursor:
            info += row[0]
            find = db.execute('''SELECT m_rating FROM REVIEWS WHERE r_id = ?''', (row[3],))
            for cell in find:
                rating = cell[0]

            data['movie'].append({
                'title': row[0],
                'overview': row[5],
                'poster_path': row[4],
                'release_date': row[1],
                'vote_average': rating
            })
        with open('static/movies.json', 'w') as outfile:
            json.dump(data, outfile)
        return flask.render_template('index.html', info = info)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            data['movie'].clear()
            info = ""
            db = sqlite3.connect('webserver.db')
            cursor = db.execute('''SELECT m_title, m_release_date, m_age, r_id, m_poster, m_overview
                                FROM MOVIES, COLLECTIONS
                                WHERE MOVIES.m_id = COLLECTIONS.m_id
                                AND COLLECTIONS.u_id = ?
                                AND MOVIES.m_title = ?''', (session['u_id'], request.form['search_bar'],))
            for row in cursor:
                info += row[0]
                find = db.execute('''SELECT m_rating FROM REVIEWS WHERE r_id = ?''', (row[3],))
                for cell in find:
                    rating = cell[0]

                data['movie'].append({
                    'title': row[0],
                    'overview': row[5],
                    'poster_path': row[4],
                    'release_date': row[1],
                    'vote_average': rating
                })
            with open('static/movies.json', 'w') as outfile:
                json.dump(data, outfile)
            return flask.render_template('index.html', info = info)
    else:
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return flask.render_template('index.html')

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    friend_id = ""
    friend = request.args.get('username', 0, type=None)
    friend_data['friend'].clear()
    db = sqlite3.connect('webserver.db')
    friend_select = db.execute("SELECT u_id FROM USERS WHERE u_name = ?", (friend,))
    for row in friend_select:
        friend_id = row[0]



    data['movie'].clear()
    cursor = db.execute('''SELECT m_title, m_release_date, m_age, r_id, m_poster, m_overview
                        FROM MOVIES, COLLECTIONS
                        WHERE MOVIES.m_id = COLLECTIONS.m_id
                        AND COLLECTIONS.u_id = ?''', (friend_id,))
    for row in cursor:
        find = db.execute('''SELECT m_rating FROM REVIEWS WHERE r_id = ?''', (row[3],))
        for cell in find:
            rating = cell[0]

        data['movie'].append({
            'title': row[0],
            'overview': row[5],
            'poster_path': row[4],
            'release_date': row[1],
            'vote_average': rating
        })
    with open('static/movies.json', 'w') as outfile:
        json.dump(data, outfile)




    info = ""
    find1 = db.execute("SELECT f_id2 FROM FRIENDS WHERE f_id1 = ?", (session['u_id'],))
    find2 = db.execute("SELECT f_id1 FROM FRIENDS WHERE f_id2 = ?", (session['u_id'],))
    your_friends = []
    wants_you = []
    x = ""
    for row in find1:
        your_friends.append(row[0])
    for row in find2:
        wants_you.append(row[0])
    for i in wants_you:
      if i not in your_friends:
        find = db.execute("SELECT u_name FROM USERS WHERE u_id = ?", (i,))
        for row in find:
          x += row[0] + ", "
    for i in your_friends:
        if i in wants_you:
            cursor = db.execute('''SELECT u_name, u_email, u_total FROM USERS WHERE u_id = ?''', (i,))
            for row in cursor:
                friend_data['friend'].append({
                    'user_name': row[0],
                    'user_email': row[1],
                    'user_total': row[2]
                })
    with open('static/friend_data.json', 'w') as outfile:
        json.dump(friend_data, outfile)

    x = x[:-2]
    info += str(x)
    db.commit()
    db.close()

    if request.method == 'POST':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            friend_data['friend'].clear()
            db = sqlite3.connect('webserver.db')

            cursor = db.execute("SELECT u_id FROM USERS WHERE u_name = ?", (request.form['search_bar'],))
            f_id2 = ""
            for row in cursor:
                f_id2 = row[0]
            session['f_id1'] = session['u_id']

            if f_id2 != "":
                if f_id2 not in your_friends:
                    db.execute("INSERT INTO FRIENDS (f_id1, f_id2) VALUES (?, ?)", (session['f_id1'], f_id2));
                    info = ""
                    find1 = db.execute("SELECT f_id2 FROM FRIENDS WHERE f_id1 = ?", (session['u_id'],))
                    find2 = db.execute("SELECT f_id1 FROM FRIENDS WHERE f_id2 = ?", (session['u_id'],))
                    your_friends = []
                    wants_you = []
                    x = ""
                    for row in find1:
                        your_friends.append(row[0])
                    for row in find2:
                        wants_you.append(row[0])
                    for i in wants_you:
                      if i not in your_friends:
                        find = db.execute("SELECT u_name FROM USERS WHERE u_id = ?", (i,))
                        for row in find:
                          x += row[0] + ", "
                    for i in your_friends:
                        if i in wants_you:
                            cursor = db.execute('''SELECT u_name, u_email, u_total FROM USERS WHERE u_id = ?''', (i,))
                            for row in cursor:
                                friend_data['friend'].append({
                                    'user_name': row[0],
                                    'user_email': row[1],
                                    'user_total': row[2]
                                })
                    with open('static/friend_data.json', 'w') as outfile:
                        json.dump(friend_data, outfile)
                    x = x[:-2]
                    info += str(x)
                    db.commit()
                    db.close()
        return render_template('friends.html', info = info)

    else:
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return flask.render_template('friends.html', info = info)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not session.get('logged_in'):
        return render_template('login.html')
    db = sqlite3.connect('webserver.db')
    files = list()
    movie_titles = list()
    filename = ""
    file = request.args.get('file', 0, type=None)
    m_id = ""
    j = 0
    age = 99
    collection = ""
    today = datetime.datetime.now()
    for i in range(len(file)):
        if file[i] != ',':
            filename += file[i]
        else:
            files.append(filename)
            movie_titles.append(Title(filename))
            filename = ""

    for i in range(len(movie_titles)):
        search = tmdb.Search()
        response = search.movie(query=movie_titles[i])
        for s in search.results:
            data['movie'].append({
                'title': s['title'],
                'overview': s['overview'],
                'poster_path': s['poster_path'],
                'release_date': s['release_date'],
                'vote_average': s['vote_average'],
                'id': s['id']
            })
            if s['release_date'] != None and s['release_date'] != '':
                age = today.year - int(s['release_date'][0:4])
            cursor = db.execute("SELECT m_id FROM MOVIES WHERE m_id = ?", (s['id'],));
            for row in cursor:
                m_id = row[0]
            if m_id == "":
                db.execute("INSERT INTO MOVIES (m_id, m_release_date, m_title, m_age, m_poster, m_overview) VALUES (?, ?, ?, ?, ?, ?)", (s['id'], s['release_date'], s['title'], age, s['poster_path'], s['overview'],));
                print("Added " + s['title'])
                db.execute("INSERT INTO REVIEWS (m_rating, m_id) VALUES (?, ?)", (s['vote_average'], s['id'],));
                cursor = db.execute("SELECT r_id FROM REVIEWS WHERE m_id = ?", (s['id'],));
                for row in cursor:
                    r_id = row[0]
                db.execute("UPDATE MOVIES SET r_id = ? WHERE m_id = ?", (r_id, s['id'],));
            else:
                print("Updated " + s['title'])
                db.execute("UPDATE REVIEWS SET m_rating = ? WHERE m_id = ?", (s['vote_average'], s['id'],));
                db.execute("UPDATE MOVIES SET m_age = ?, m_overview = ? WHERE m_id = ?", (age, s['overview'], s['id'],));
                m_id = ""
            cursor = db.execute("SELECT m_id, u_id FROM COLLECTIONS WHERE m_id = ? AND u_id = ?", (s['id'], session['u_id'],));
            for row in cursor:
                collection = row[0]
            if collection == "":
                db.execute("INSERT INTO COLLECTIONS (m_id, u_id) VALUES (?, ?)", (s['id'], session['u_id'],))
            else:
                collection = ""
            db.commit()
            break

        with open('static/movies.json', 'w') as outfile:
            json.dump(data, outfile)

    cursor = db.execute("SELECT count(m_id) FROM COLLECTIONS WHERE u_id = ?", (session['u_id'],))
    for row in cursor:
        count = row[0]
    db.execute("UPDATE USERS SET u_total = ? WHERE u_id = ?", (count, session['u_id'],));

    print("\n\n", list(cursor))

    db.commit()
    db.close()
    return home()

# @app.route("/download")
# def download():
#     db = sqlite3.connect('webserver.db')
#     cursor = db.execute("SELECT u_key FROM USERS WHERE u_id = ?", (session['u_id'],))
#     key = 0
#     for row in cursor:
#         key = row[0]
#     if key == 1:
#         file = open("static/upload/Divergent.txt", "rb")
#         return flask.Response(file, mimetype="video/mp4", headers={"Content-disposition" : "attachment; filename=Divergent.mp4"})
#         return home()
#     else:
#         return home()

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
        cursor = db.execute("SELECT u_id FROM USERS WHERE u_name = ?", (request.form['username'],))
        for row in cursor:
            session['u_id'] = row[0]
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
                cursor = db.execute("SELECT u_id FROM USERS WHERE u_name = ?", (request.form['username'],))
                for row in cursor:
                    session['u_id'] = row[0]
                db.commit()
                db.close()
                return render_template('index.html')
    return render_template('signup.html')

def Title(name):
	length = len(name)
	title = ""
	for x in range(0, length):
		if name[x].isdigit() and name[x+1].isdigit() and name[x+2].isdigit() and name[x+3].isdigit():
			return title[:-1]
		if name[x].isdigit() and name[x+1].isdigit() and name[x+2].isdigit() and name[x+3] == 'p':
			return title[:-1]
		if name[x] == 'm' and name[x+1] == 'p' and name[x+2] == '4':
			return title[:-1]
		if name[x] == "(" and name[x+1].isdigit() and name[x+2].isdigit() and name[x+3].isdigit() and name[x+4].isdigit() and name[x+5] == ")":
			return title[:-1]
		if name[x] != '.':
			title = title + name[x]
		else:
			title = title + " "
	return title

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
