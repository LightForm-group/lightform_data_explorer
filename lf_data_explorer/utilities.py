from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from flask import flash

if TYPE_CHECKING:
    from lf_data_explorer.db import Measurement


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


sample_prep_methods = [Label("Unknown", "grey"), Label("Forging", "red"),
                       Label("Rolling", "green"), Label("Cutting", "blue")]

node_types = [Label("Current", '#7cc95d'), Label("Parent", '#c95d5d'),
              Label("Child", '#5d98c9')]
