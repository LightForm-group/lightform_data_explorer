from typing import List, Optional

import sqlalchemy.exc

from lf_data_explorer import db
from lf_data_explorer.db import Sample
from lf_data_explorer.utilities import Result


def get_all_samples() -> List[Sample]:
    samples = Sample.query.all()
    return sorted(samples, key=str)


def get_sample_by_name(sample_name: str) -> Optional[Sample]:
    return Sample.query.filter_by(name=sample_name).first()


def get_sample_by_id(sample_id: int) -> Optional[Sample]:
    return Sample.query.filter_by(id=sample_id).first()


def get_sample_children(sample_id: int) -> List[Sample]:
    sample = get_sample_by_id(sample_id)
    if not sample:
        raise IndexError(f"Sample {sample_id} not found.")

    return sample.children


def get_sample_measurements(sample_id: int) -> List[Sample]:
    sample = get_sample_by_id(sample_id)
    if not sample:
        raise IndexError(f"Sample {sample_id} not found.")

    return sample.measurements


def delete_sample(sample_id: int) -> Result:
    """Delete the sample with `sample_id` from the database.
    Return the name of the deleted sample."""
    sample_name = Sample.query.filter_by(id=sample_id).first().name
    Sample.query.filter_by(id=sample_id).delete()
    db.session.commit()
    return Result(True, f"Sample '{sample_name}' successfully deleted.")


def add_new_sample(sample_name: str, parent: int) -> Result:
    if parent == -1:
        parent = sqlalchemy.null()
    new_sample = Sample(name=sample_name, parent_sample=parent)
    db.session.add(new_sample)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        if e.orig.args[0] == 1062:
            db.session.rollback()
            return Result(False, f"Sample name '{sample_name}' already exists. Record not added.")
        else:
            return Result(False, "Sample not added. Unknown error.")
    return Result(True, f"Successfully added new sample: '{sample_name}'.")


def edit_sample(sample_id: int, new_sample_name: str, new_parent: Optional[int]) -> Result:
    sample = Sample.query.filter_by(id=sample_id).first()
    old_name = sample.name
    sample.name = new_sample_name
    if new_parent is not None:
        sample.parent_sample = new_parent
    else:
        sample.parent_sample = sqlalchemy.null()

    db.session.commit()
    return Result(True, f"Sample '{old_name}' record updated.")
