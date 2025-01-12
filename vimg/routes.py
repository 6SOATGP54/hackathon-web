from vimg import app
from flask import render_template

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/upload")
def upload():
    return render_template('upload.html')