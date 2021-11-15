from flask_frozen import Freezer

from lf_data_explorer.queries.sample import get_all_samples
from lf_data_explorer import app

app.config["FREEZER"] = True

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
    # Use this line to run a server to check pages before upload.
    freezer.run()


@freezer.register_generator
def select_sample():
    all_samples = get_all_samples()
    for sample in all_samples:
        yield {'sample_name': sample.name}
