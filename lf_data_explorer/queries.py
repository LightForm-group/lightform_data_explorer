from typing import List, Optional

import sqlalchemy.exc

from lf_data_explorer.db import Sample, db, SampleImage, Experiment


def get_all_samples() -> List[Sample]:
    return Sample.query.all()


def get_all_experiments() -> List[Experiment]:
    return Experiment.query.all()


def get_sample_by_name(sample_name: str) -> Optional[Sample]:
    return Sample.query.filter_by(name=sample_name).first()


def get_sample_by_id(sample_id: int) -> Optional[Sample]:
    return Sample.query.filter_by(id=sample_id).first()


def delete_sample(sample_id: int) -> str:
    """Delete the sample with `sample_id` from the database.
    Return the name of the deleted sample."""
    sample_name = Sample.query.filter_by(id=sample_id).first().name
    Sample.query.filter_by(id=sample_id).delete()
    db.session.commit()
    return f"Sample '{sample_name}' successfully deleted."


def add_new_sample(sample_name: str) -> str:
    new_sample = Sample(name=sample_name)
    db.session.add(new_sample)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        if e.orig.args[0] == 1062:
            db.session.rollback()
            return f"Sample name '{sample_name}' already exists. Record not added."
        else:
            return "Sample not added. Unknown error."
    return f"Successfully added new sample: '{sample_name}'"


def add_new_image(image_path: str, sample_id: int) -> str:
    new_image = SampleImage(path=image_path, sample_id=sample_id)
    db.session.add(new_image)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return "Sample not added. Unknown error."
    return f"Successfully added: '{image_path}'"


def add_new_experiment(experiment_name: str) -> str:
    new_experiment = Experiment(name=experiment_name)
    db.session.add(new_experiment)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return "Sample not added. Unknown error."
    return f"Successfully added: '{experiment_name}'"


def rename_sample(sample_id: int, new_sample_name: str) -> str:
    sample = Sample.query.filter_by(id=sample_id).first()
    old_name = sample.name
    sample.name = new_sample_name
    db.session.commit()
    return f"Sample '{old_name}' renamed to '{new_sample_name}'"
