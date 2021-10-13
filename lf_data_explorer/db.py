import json

import flask_bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from lf_data_explorer.utilities import load_config

db = SQLAlchemy()


def setup_db(app: Flask, db_instance: SQLAlchemy):
    db_config = load_config()["database"]

    app.config['SQLALCHEMY_DATABASE_URI'] = db_config["uri"]
    db_instance.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def validate_password(self, plaintext: str):
        return flask_bcrypt.check_password_hash(self.password_hash, plaintext)


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    parent_sample = db.Column(db.Integer, db.ForeignKey('sample.id', onupdate="CASCADE",
                                                        ondelete="CASCADE"))
    creation_type = db.Column(db.String(20))
    creation_url = db.Column(db.String(200))
    images = db.relationship('SampleImage', backref='sample', lazy=True)
    measurements = db.relationship('Measurement', backref='sample', lazy=True)
    parent = db.relationship('Sample', backref='children', remote_side='Sample.id', lazy=True)

    def __repr__(self):
        return f'Sample: {self.name}'

    def __str__(self):
        return self.name

    def to_json(self) -> str:
        return json.dumps({"name": self.name, "creation_type": str(self.creation_type),
                           "creation_url": str(self.creation_url), "parent": str(self.parent)})


class SampleImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(1000), nullable=False)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id', onupdate="CASCADE",
                                                    ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'Image: {self.path}'


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    measurements = db.relationship('Measurement', backref='experiment', lazy=True)

    def __repr__(self):
        return f'Experiment: {self.name}'

    def __str__(self):
        return self.name

    def to_json(self) -> str:
        return json.dumps({"name": self.name, "num_measurements": len(self.measurements)})


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id', onupdate="CASCADE",
                                                    ondelete="CASCADE"), nullable=False)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id', onupdate="CASCADE",
                                                        ondelete="CASCADE"), nullable=False)
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'Measurement: {self.url}'

    def __str__(self):
        return f'"{self.experiment.name}: {self.url}"'

    def to_json(self) -> str:
        return f'"{self.id}": {{"sample_id": {self.sample_id}, ' \
               f'"experiment_id": {self.experiment_id}, "url": "{self.url}"}}'
