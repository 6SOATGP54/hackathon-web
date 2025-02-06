import os
from flask import render_template
import requests
from flask import redirect, flash, send_file
from flask.helpers import url_for
from flask_login.utils import login_user
from flask_login import current_user
from vimg.models import User, Video
from vimg import db

class UserService:
    def save_and_redirect(request):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        user = User(first_name, last_name, email, password)

        if user.is_valid():
            try:
                db.session.add(user)
                db.session.commit()
                flash('Cadastro realizado com sucesso!', 'success')
            except:
                flash('Erro! Não possível cadastrar seu usuário. Por favor, entre em contato com o suporte.', 'error')
            return redirect(url_for('home'))
        else:
            flash('Erro! As informações fornecidas não são válidas.', 'error')
            return redirect(url_for('home'))

    def login_and_redirect(request):
        email = request.form['email']
        password = request.form['password']

        found_user = User.query.filter_by(email=email).first()

        if found_user and found_user.verify_password(password):
            login_user(found_user)
            flash(found_user.first_name, 'user_name')
            return redirect(url_for('upload'))
        else:
            flash('Houve um problema com seu usuário. Por favor, entre em contato com o suporte.', 'error')
            return redirect(url_for('home'))
    
    def redirect_home(request):
        if current_user.is_anonymous:
            return render_template('login.html')
        else:
            found_user = User.query.filter_by(id=current_user.get_id()).first()
            flash(found_user.first_name, 'user_name')
            return redirect(url_for('upload'))
    
    def access_signup_or_redirect(request):
        if current_user.is_anonymous:
            return render_template('signup.html')
        else:
            found_user = User.query.filter_by(id=current_user.get_id()).first()
            flash(found_user.first_name, 'user_name')
            return redirect(url_for('upload'))

class VideoService:
    def __init__(self):
        self.UPLOAD_FOLDER = '/tmp'

    def load_videos_history(request):
        videos = Video.query.filter_by(user=current_user.get_id()).order_by(Video.id.desc()).all()
        return render_template('upload.html', videos=videos)

    def upload_and_redirect(request):
        if 'file' not in request.files:
            flash('Por favor, envie um arquivo de vídeo para continuar.', 'error')
            return redirect(url_for('upload'))
        
        file = request.files['file']
        user = User.query.filter_by(id=current_user.get_id()).first()
        video = Video(file, user)

        if video.is_valid():
            file.save(os.path.join('/tmp', video.get_secure_filename()))
            db.session.add(video)
            db.session.commit()
            
            with open(os.path.join('/tmp', video.get_secure_filename()), 'rb') as loaded_file:
                print(file)
                imgs = requests.post('http://localhost:5001/download/zip', files={'file': (os.path.join('/tmp', video.get_secure_filename()), loaded_file, "video/mp4")})
                print(imgs.status_code)
                with open('/tmp/download.zip', 'wb') as zip_file:
                    zip_file.write(imgs.content)
                flash('Upload realizado com sucesso.', 'success')
                flash(user.first_name, 'user_name')
                video.conversion_state = True
                db.session.commit()
                return send_file('/tmp/download.zip')
        else:
            flash('Por favor, envie um arquivo de vídeo válido para continuar.', 'error')
            return redirect(url_for('upload'))
    