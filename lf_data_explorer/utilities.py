from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING

import yaml
from flask import flash

if TYPE_CHECKING:
    from lf_data_explorer.db import Measurement


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_config():
    with open("config.yaml") as config_file:
        return yaml.safe_load(config_file)


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
