from dataclasses import dataclass
from typing import List, Optional

import sqlalchemy.exc

from lf_data_explorer.db import Sample, db


def get_all_samples() -> List[Sample]:
    return Sample.query.all()


def get_sample_by_name(sample_name: str) -> Optional[Sample]:
    return Sample.query.filter_by(name=sample_name).first()


def get_sample_by_id(sample_id: int) -> Optional[Sample]:
    return Sample.query.filter_by(id=sample_id).first()


def delete_sample(sample_id: int) -> str:
    """Delete the sample with `sample_id` from the database.
    Return the name of the deleted sample."""
    sample_name = Sample.name
    Sample.query.filter_by(id=sample_id).delete()
    db.session.commit()
    return sample_name


@dataclass
class AddSampleResult:
    success: bool
    message: str


def add_new_sample(sample_name: str) -> AddSampleResult:
    new_sample = Sample(name=sample_name)
    db.session.add(new_sample)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        if e.orig.args[0] == 1062:
            db.session.rollback()
            return AddSampleResult(False, f"Sample name '{sample_name}' already exists. "
                                          f"Record not added.")
        else:
            return AddSampleResult(False, "Sample not added. Unknown error.")
    return AddSampleResult(True, f"Successfully added: '{sample_name}'")
