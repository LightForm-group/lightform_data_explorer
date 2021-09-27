import sqlalchemy.exc

from lf_data_explorer.db import db, SampleImage


def add_new_image(image_path: str, sample_id: int) -> str:
    new_image = SampleImage(path=image_path, sample_id=sample_id)
    db.session.add(new_image)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return "Sample not added. Unknown error."
    return f"Successfully added: '{image_path}'."
