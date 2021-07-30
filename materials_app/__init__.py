from flask import Flask
from materials_app.db import setup_db, db


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
from materials_app import views

setup_db(app, db)


