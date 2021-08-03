import yaml
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def setup_db(app: Flask, db_instance: SQLAlchemy):

    with open("config.yaml") as config_file:
        db_config = yaml.safe_load(config_file)["database"]
    username = db_config["username"]
    password = db_config["password"]

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@localhost/test'
    db_instance.init_app(app)


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Sample: {self.name}>'
