from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

import flask
from flask import flash

if TYPE_CHECKING:
    from lf_data_explorer.db import Measurement, Sample


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def measurements_to_json(measurements: List[Measurement]) -> str:
    strings = [measurement.to_json() for measurement in measurements]

    return f'{{{" ,".join(strings)}}}'


@dataclass
class Result:
    success: bool
    message: str


def flash_result(result: Result):
    if result.success:
        flash(result.message)
    else:
        flash(result.message, category="error")


@dataclass()
class Label:
    name: str
    colour: str


# If adding new methods or sample types, you should update graph_style.js to
# include the class and colour on the network graphs.
sample_prep_methods = [Label("Unknown", "grey"), Label("Forging", "red"),
                       Label("Rolling", "green"), Label("Cutting", "blue")]

node_types = [Label("Current", '#7cc95d'), Label("Parent", '#c95d5d'),
              Label("Child", '#5d98c9')]


def output_network_json(all_samples: List[Sample]):
    """This function is run when the app starts and any time the database is updated. It
    writes node and edge data to a javascript file in JSON format. The data is then accessed
    by any page which displays a graph."""
    data = {"nodes": [], "edges": []}

    for sample in all_samples:
        node_data = {"data": {}}
        node_data["data"]["id"] = sample.name
        node_data["data"]["href"] = flask.url_for('select_sample', sample_name=sample.name)
        data["nodes"].append(node_data)

        for child in sample.children:
            edge_data = {"data": {}}
            edge_data["data"]["id"] = f'{sample.name}-{child.name}'
            edge_data["data"]["source"] = sample.name
            edge_data["data"]["target"] = child.name
            edge_data["classes"] = child.creation_type
            data["edges"].append(edge_data)

    with open("lf_data_explorer/static/graphs/graph_data.js", "w") as output_file:
        output_file.write("data = ")
        json.dump(data, output_file)
