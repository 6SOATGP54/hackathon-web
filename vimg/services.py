import os
from flask import render_template, Response
import requests
from flask import redirect, flash, send_file
from flask.helpers import url_for
from flask_login.utils import login_user
from flask_login import current_user
from vimg.models import User, Video
from vimg import db
import logging

class UserService:
    def save_and_redirect(request):
        logging.info('Saving user...')
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        user = User(first_name, last_name, email, password)
        logging.info(f'user: {user}')

        logging.info('Saving user...')
        if user.is_valid():
            try:
                db.session.add(user)
                db.session.commit()
                flash('Cadastro realizado com sucesso!', 'success')
                logging.info(f'User {user} saved')
            except Exception as e:
                db.session.rollback()
                logging.error('User not saved')
                logging.error(f'Exception: {e}')
                flash('Erro! Não possível cadastrar seu usuário. Por favor, entre em contato com o suporte.', 'error')
            return redirect(url_for('home'))
        else:
            logging.error('User not saved. Invalid user')
            flash('Erro! As informações fornecidas não são válidas.', 'error')
            return redirect(url_for('home'))

    def login_and_redirect(request):
        logging.info('Logging...')
        email = request.form['email']
        password = request.form['password']

        logging.info('Finding user...')
        found_user = User.query.filter_by(email=email).first()
        logging.info(f'Found user {found_user}')

        logging.info('Validating user...')
        if found_user and found_user.verify_password(password):
            login_user(found_user)
            flash(found_user.first_name, 'user_name')
            logging.info('Validation successful')
            return redirect(url_for('upload'))
        else:
            logging.warn('User not validated')
            flash('Houve um problema com seu usuário. Por favor, entre em contato com o suporte.', 'error')
            return redirect(url_for('home'))
    
    def redirect_home(request):
        if current_user.is_anonymous:
            return render_template('login.html')
        else:
            logging.info('Redirecting user to dashboard')
            found_user = User.query.filter_by(id=current_user.get_id()).first()
            flash(found_user.first_name, 'user_name')
            return redirect(url_for('upload'))
    
    def access_signup_or_redirect(request):
        if current_user.is_anonymous:
            return render_template('signup.html')
        else:
            logging.info('Redirecting user to dashboard')
            found_user = User.query.filter_by(id=current_user.get_id()).first()
            flash(found_user.first_name, 'user_name')
            return redirect(url_for('upload'))

class VideoService:
    def __init__(self):
        self.UPLOAD_FOLDER = '/tmp'

    def load_videos_history(request):
        logging.info(f'Recovery videos from {current_user}')
        videos = Video.query.filter_by(user=current_user.get_id()).order_by(Video.id.desc()).all()
        return render_template('upload.html', videos=videos)

    def upload_and_redirect(request):
        logging.info('Starting video upload')

        if 'file' not in request.files:
            logging.error('Video not found')
            flash('Por favor, envie um arquivo de vídeo para continuar.', 'error')
            return redirect(url_for('upload'))
        
        file = request.files['file']
        user = User.query.filter_by(id=current_user.get_id()).first()
        video = Video(file, user)
        logging.info('Video received')

        logging.debug(file)
        logging.debug(user)
        logging.debug(video)

        if video.is_valid():
            logging.info('Video is valid')
            logging.info('Saving video...')
            file.save(os.path.join('/tmp', video.get_secure_filename()))
            db.session.add(video)
            db.session.commit()
            
            with open(os.path.join('/tmp', video.get_secure_filename()), 'rb') as loaded_file:
                logging.info('Calling API VAPI to convert video into images...')
                imgs = requests.post('http://localhost:5001/download/zip', files={'file': (os.path.join('/tmp', video.get_secure_filename()), loaded_file, "video/mp4")})
                logging.info(f' Status code: {imgs.status_code}')
                logging.info('Saving zip file...')
                with open('/tmp/download.zip', 'wb') as zip_file:
                    zip_file.write(imgs.content)
                flash('Upload realizado com sucesso.', 'success')
                flash(user.first_name, 'user_name')
                video.conversion_state = True
                db.session.commit()
                logging.info('Zip saved')
                logging.info('End process and sending zip file')
                return send_file('/tmp/download.zip')
        else:
            logging.error('Invalid format of video')
            flash('Por favor, envie um arquivo de vídeo válido para continuar.', 'error')
            return Response("{'Error':'error'}", status=500, mimetype='application/json')
    