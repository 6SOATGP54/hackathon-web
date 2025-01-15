from flask.helpers import redirect, url_for
from vimg.services import UserService
from vimg import app
from flask import render_template, request
from flask_login import login_required, logout_user

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    return UserService.login_and_redirect(request)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        return UserService.save_and_redirect(request)

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')