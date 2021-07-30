from flask import Flask

from lf_data_explorer.db import setup_db, db


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
from lf_data_explorer import views

setup_db(app, db)


