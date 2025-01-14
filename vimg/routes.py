from vimg.models import User
from flask.helpers import flash, redirect, url_for
from vimg.services import UserService
from vimg import app
from flask import render_template, request
from flask_login import login_required, login_user, logout_user

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        found_user = User.query.filter_by(email=email).first()

        if found_user and found_user.verify_password(password):
            login_user(found_user)
            flash(found_user.first_name, 'success')
            return redirect(url_for('upload'))
        else:
            return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        return UserService.save(request)

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')