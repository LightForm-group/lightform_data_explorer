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
