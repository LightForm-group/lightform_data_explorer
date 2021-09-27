from typing import List, Optional

import sqlalchemy.exc

from lf_data_explorer.db import Sample, db, SampleImage, Experiment, Measurement


def get_all_samples() -> List[Sample]:
    samples = Sample.query.all()
    return sorted(samples, key=str)


def get_all_experiments() -> List[Experiment]:
    experiments = Experiment.query.all()
    return sorted(experiments, key=str)


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


def delete_experiment(experiment_id: int) -> str:
    """Delete the experiment with `experiment_id` from the database."""
    experiment_name = Experiment.query.filter_by(id=experiment_id).first().name
    Experiment.query.filter_by(id=experiment_id).delete()
    db.session.commit()
    return f"Sample '{experiment_name}' successfully deleted."


def add_new_sample(sample_name: str, parent: int) -> str:
    if parent == -1:
        parent = None
    new_sample = Sample(name=sample_name, parent_sample=parent)
    db.session.add(new_sample)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        if e.orig.args[0] == 1062:
            db.session.rollback()
            return f"Sample name '{sample_name}' already exists. Record not added."
        else:
            return "Sample not added. Unknown error."
    return f"Successfully added new sample: '{sample_name}'."


def add_new_image(image_path: str, sample_id: int) -> str:
    new_image = SampleImage(path=image_path, sample_id=sample_id)
    db.session.add(new_image)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return "Sample not added. Unknown error."
    return f"Successfully added: '{image_path}'."


def add_new_experiment(experiment_name: str) -> str:
    new_experiment = Experiment(name=experiment_name)
    db.session.add(new_experiment)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return "Sample not added. Unknown error."
    return f"Successfully added: '{experiment_name}.'"


def edit_sample(sample_id: int, new_sample_name: str, new_parent: Optional[int]) -> str:
    sample = Sample.query.filter_by(id=sample_id).first()
    old_name = sample.name
    sample.name = new_sample_name
    if new_parent is not None:
        sample.parent_sample = new_parent
    else:
        sample.parent_sample = sqlalchemy.null()

    db.session.commit()
    return f"Sample '{old_name}' record updated."


def rename_experiment(sample_id: int, new_experiment_name: str) -> str:
    experiment = Experiment.query.filter_by(id=sample_id).first()
    old_name = experiment.name
    experiment.name = new_experiment_name
    db.session.commit()
    return f"Experiment '{old_name}' renamed to '{new_experiment_name}.'"


def add_measurement(sample_id: int, experiment_id: int, url: str) -> str:
    sample = Sample.query.filter_by(id=sample_id).first()
    experiment = Experiment.query.filter_by(id=experiment_id).first()
    new_measurement = Measurement(sample_id=sample_id, experiment_id=experiment_id, url=url)
    db.session.add(new_measurement)
    db.session.commit()
    return f"Measurement added for experiment '{experiment.name}' on sample '{sample.name}."


def delete_measurement(sample_id: int, measurement_id: int) -> str:
    sample = Sample.query.filter_by(id=sample_id).first()
    measurement = Measurement.query.filter_by(id=measurement_id).first()
    Measurement.query.filter_by(id=measurement_id).delete()
    db.session.commit()
    return f"Measurement '{measurement.url}' successfully deleted from sample {sample.name}."
