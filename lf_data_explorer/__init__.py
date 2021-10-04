from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from lf_data_explorer.db import setup_db, db, User
from lf_data_explorer.utilities import load_config


config = load_config()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "lf_data_explorer/static/sample_images"
app.config['SECRET_KEY'] = config["secret_key"]
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['BCRYPT_LOG_ROUNDS'] = 12
app.url_map.strict_slashes = False
app.app_context().push()
from lf_data_explorer import views

bcrypt = Bcrypt(app)
setup_db(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "admin"


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).first()


# Run these two lines to initialise the empty database.
db.create_all()
db.session.commit()
