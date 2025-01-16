from flask.helpers import redirect, url_for
from vimg.services import UserService
from vimg import app
from vimg import login_manager
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

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('errors/401.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html')

@app.errorhandler(Exception)
def generic_error(e):
    return render_template('errors/generic.html')