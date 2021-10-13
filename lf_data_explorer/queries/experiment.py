from typing import List, Optional

import sqlalchemy.exc

from lf_data_explorer import db
from lf_data_explorer.db import Experiment
from lf_data_explorer.utilities import Result


def get_all_experiments() -> List[Experiment]:
    experiments = Experiment.query.all()
    return sorted(experiments, key=str)


def get_experiment_by_id(experiment_id: int) -> Optional[Experiment]:
    return Experiment.query.filter_by(id=experiment_id).first()


def delete_experiment(experiment_id: int) -> Result:
    """Delete the experiment with `experiment_id` from the database."""
    experiment_name = Experiment.query.filter_by(id=experiment_id).first().name
    Experiment.query.filter_by(id=experiment_id).delete()
    db.session.commit()
    return Result(True, f"Sample '{experiment_name}' successfully deleted.")


def add_new_experiment(experiment_name: str) -> Result:
    new_experiment = Experiment(name=experiment_name)
    db.session.add(new_experiment)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return Result(False, "Sample not added. Unknown error.")
    return Result(True, f"Successfully added: '{experiment_name}.'")


def rename_experiment(sample_id: int, new_experiment_name: str) -> Result:
    experiment = Experiment.query.filter_by(id=sample_id).first()
    old_name = experiment.name
    experiment.name = new_experiment_name
    db.session.commit()
    return Result(True, f"Experiment '{old_name}' renamed to '{new_experiment_name}.'")