from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login.login_manager import LoginManager
from flask_login import UserMixin
from flask_sqlalchemy.extension import SQLAlchemy
from werkzeug.utils import secure_filename

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(254), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registration_date = datetime.now()
    
    def __str__(self):
        return f'<User name="{self.first_name} {self.last_name}", email="{self.email}">'

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_valid(self):
        valid = True

        if len(self.first_name) < 3 or len(self.first_name) > 50:
            valid = False
        
        if len(self.last_name) < 3 or len(self.last_name) > 50:
            valid = False

        if len(self.email) < 6 or len(self.email) > 100:
            valid = False

        if len(self.password) < 8 or len(self.password) > 254:
            valid = False
        
        return valid

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(20), db.ForeignKey('user.id'))
    upload_date = db.Column(db.DateTime, nullable=True)
    conversion_state = db.Column(db.Boolean, default=False)

    def __init__(self, file, user):
        self.ALLOWED_EXTENSIONS = ['mp4', 'avi', 'mov', 'mkv', 'm4a']

        self.file = file
        self.filename = secure_filename(self.file.filename)
        self.user = user.get_id()
        self.upload_date = datetime.now()
    
    def allowed_file(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def is_valid(self):
        return self.filename != '' and self.allowed_file(self.filename)
    
    def get_secure_filename(self):
        return secure_filename(self.filename)