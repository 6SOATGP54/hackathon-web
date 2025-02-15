from flask.helpers import redirect, url_for
from vimg.services import UserService, VideoService
from vimg import app
from vimg import login_manager
from flask import render_template, request
from flask_login import login_required, logout_user

@app.route('/', methods=['GET'])
def home():
    return UserService.redirect_home(request)

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
        return UserService.access_signup_or_redirect(request)
    else:
        return UserService.save_and_redirect(request)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return VideoService.load_videos_history(request)
    else:
        return VideoService.upload_and_redirect(request)

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('errors/401.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html')

@app.errorhandler(Exception)
def generic_error(e):
    print(e)
    return render_template('errors/generic.html')