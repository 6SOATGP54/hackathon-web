import uuid
from vimg.models import User
from vimg.models import db, login_manager, bcrypt
from flask import Flask

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://trois:V13rg3s@localhost/vimg'

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from vimg import routes