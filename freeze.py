from flask_frozen import Freezer

from lf_data_explorer.queries.sample import get_all_samples
from lf_data_explorer import app, config

app.config["FREEZER"] = True
app.config["FREEZER_BASE_URL"] = "http://localhost/tifun-data-explorer/"
app.config["FREEZER_DEFAULT_MIMETYPE"] = "text/html"
app.config["FREEZER_REMOVE_EXTRA_FILES"] = True
app.config["FREEZER_DESTINATION_IGNORE"] = ["data.db", ".git", ".gitignore", "README.md"]
app.config["FREEZER_DESTINATION"] = config["build_dir"]
app.config["FREEZER_STATIC_IGNORE"] = ["*manage*", "*add_image*"]

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
