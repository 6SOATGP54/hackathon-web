from flask_bcrypt import Bcrypt
from flask_login.login_manager import LoginManager
from flask_login import UserMixin
from flask_sqlalchemy.extension import SQLAlchemy

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

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

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