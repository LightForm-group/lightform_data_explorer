from typing import List

from lf_data_explorer.db import Sample


def get_all_samples() -> List[Sample]:
    return Sample.query.all()
