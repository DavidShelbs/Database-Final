import flask
from flask import Flask, flash, redirect, render_template, request, session, abort
app = Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', debug='true')
