from flask import Flask

from lf_data_explorer.db import setup_db, db
from lf_data_explorer.utilities import load_config

config = load_config()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "lf_data_explorer/static/sample_images"
app.config['SECRET_KEY'] = config["secret_key"]
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.url_map.strict_slashes = False
app.app_context().push()
from lf_data_explorer import views

setup_db(app, db)
