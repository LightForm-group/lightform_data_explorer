import json
from typing import List, Union

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from lf_data_explorer.utilities import load_config

db = SQLAlchemy()


def setup_db(app: Flask, db_instance: SQLAlchemy):
    db_config = load_config()["database"]

    app.config['SQLALCHEMY_DATABASE_URI'] = db_config["uri"]
    db_instance.init_app(app)


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

    def __lt__(self, other):
        """A special less than comparator which attempts to sort samples by their names
        treating any numbers contained within the name as numbers not strings."""

        self_len = len(self.name.split("-"))
        other_len = len(other.name.split("-"))
        # If a name has fewer parts then it is lesser
        if self_len < other_len:
            return True
        elif other_len < self_len:
            return False

        self_parts = self.digits_to_int(self.name.split("-"))
        other_parts = self.digits_to_int(other.name.split("-"))

        # If a name has the same number of parts then compare the parts
        for self_part, other_part in zip(self_parts, other_parts):
            if isinstance(self_part, type(other_part)):
                # If the parts are of the same type then compare them
                if self_part < other_part:
                    return True
                elif self_part > other_part:
                    return False
                # If the parts are identical then consider the nex parts.
            else:
                # If parts are of different type then the string part is lesser
                if isinstance(self_part, str):
                    return True
                else:
                    return False
        # If all parts are identical return True
        return True

    @staticmethod
    def digits_to_int(string_list: List[str]) -> List[Union[int, str]]:
        """Given a list of strings, convert any numerical strings to integers."""
        converted_list = []
        for x in string_list:
            if x.isdigit():
                converted_list.append(int(x))
            else:
                converted_list.append(x)
        return converted_list

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
