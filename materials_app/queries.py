from typing import List

from materials_app.db import Sample


def get_all_samples() -> List[Sample]:
    return Sample.query.all()
