from dataclasses import dataclass
from typing import List

import sqlalchemy.exc

from lf_data_explorer.db import Sample, db


def get_all_samples() -> List[Sample]:
    return Sample.query.all()


@dataclass
class AddSampleResult:
    success: bool
    message: str


def add_new_sample(sample_name: str) -> AddSampleResult:
    new_sample = Sample(sample_name=sample_name)
    db.session.add(new_sample)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        if e.orig.args[0] == 1062:
            return AddSampleResult(False, f"Sample name '{sample_name}' already exists. "
                                          f"Record not added.")
        else:
            return AddSampleResult(False, "Sample not added. Unknown error.")
    return AddSampleResult(True, f"Successfully added: '{sample_name}'")
