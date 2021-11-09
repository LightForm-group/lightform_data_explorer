import sqlalchemy.exc

from lf_data_explorer.db import db, SampleImage
from lf_data_explorer.utilities import Result


def add_new_image(image_path: str, sample_id: int) -> Result:
    new_image = SampleImage(path=image_path, sample_id=sample_id)
    db.session.add(new_image)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return Result(False, "Sample not added. Unknown error.")
    return Result(True, f"Successfully added: '{image_path}'.")


def try_save_new_record(new_sample_name: str, success_message: str) -> Result:
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:

        db.session.rollback()
        return Result(False, f"Sample name '{new_sample_name}' already exists. "
                             f"Record not added.")

    return Result(True, success_message)
