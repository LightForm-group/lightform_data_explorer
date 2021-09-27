from lf_data_explorer import db
from lf_data_explorer.db import Sample, Experiment, Measurement


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
