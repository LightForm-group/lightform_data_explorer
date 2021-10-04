from typing import Optional

import flask_bcrypt
import sqlalchemy.exc

from lf_data_explorer.db import User, db
from lf_data_explorer.utilities import Result


def get_user_by_name(username: str) -> Optional[User]:
    return User.query.filter_by(username=username).first()


def new_user(username: str, password: str) -> Result:
    hashed_password = flask_bcrypt.generate_password_hash(password)
    user = User(username=username, password_hash=hashed_password, is_active=False)
    db.session.add(user)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return Result(False, "Username already in use.")
    return Result(True, f"Successfully added new user: '{username}'")
