from flask import Flask

from lf_data_explorer.db import setup_db, db


PROJECT_NAME = "tifun-data-explorer"

app = Flask(__name__)

# Flask settings
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///../../{PROJECT_NAME}/data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "lf_data_explorer/static/sample_images"
# Secret doesn't have to be secret because we only run the app locally.
app.config['SECRET_KEY'] = "hLVdtZs3ca8MknSi"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Frozen-Flask settings
app.config["FREEZER_BASE_URL"] = f"http://localhost/{PROJECT_NAME}/"
app.config["FREEZER_DEFAULT_MIMETYPE"] = "text/html"
app.config["FREEZER_REMOVE_EXTRA_FILES"] = True
app.config["FREEZER_DESTINATION_IGNORE"] = ["data.db", ".git", ".gitignore", "README.md"]
app.config["FREEZER_DESTINATION"] = f"../../{PROJECT_NAME}/"
app.config["FREEZER_STATIC_IGNORE"] = ["*manage*", "*add_image*"]


app.url_map.strict_slashes = False
app.app_context().push()
from lf_data_explorer import views

setup_db(app, db)

# These two lines initialise the empty database if it isn't already created.
db.create_all()
db.session.commit()
