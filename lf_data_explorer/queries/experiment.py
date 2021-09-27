from typing import List

import sqlalchemy.exc

from lf_data_explorer import db
from lf_data_explorer.db import Experiment


def get_all_experiments() -> List[Experiment]:
    experiments = Experiment.query.all()
    return sorted(experiments, key=str)


def delete_experiment(experiment_id: int) -> str:
    """Delete the experiment with `experiment_id` from the database."""
    experiment_name = Experiment.query.filter_by(id=experiment_id).first().name
    Experiment.query.filter_by(id=experiment_id).delete()
    db.session.commit()
    return f"Sample '{experiment_name}' successfully deleted."


def add_new_experiment(experiment_name: str) -> str:
    new_experiment = Experiment(name=experiment_name)
    db.session.add(new_experiment)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return "Sample not added. Unknown error."
    return f"Successfully added: '{experiment_name}.'"


def rename_experiment(sample_id: int, new_experiment_name: str) -> str:
    experiment = Experiment.query.filter_by(id=sample_id).first()
    old_name = experiment.name
    experiment.name = new_experiment_name
    db.session.commit()
    return f"Experiment '{old_name}' renamed to '{new_experiment_name}.'"