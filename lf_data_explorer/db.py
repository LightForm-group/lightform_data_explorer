from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from lf_data_explorer.utilities import load_config

db = SQLAlchemy()


def setup_db(app: Flask, db_instance: SQLAlchemy):
    db_config = load_config()["database"]
    username = db_config["username"]
    password = db_config["password"]

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@localhost/test'
    db_instance.init_app(app)


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    images = db.relationship('SampleImage', backref='sample', lazy=True)

    def __repr__(self):
        return f'<Sample: {self.name}>'


class SampleImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(1000), nullable=False)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'), nullable=False)

    def __repr__(self):
        return f'<Image: {self.path}>'
