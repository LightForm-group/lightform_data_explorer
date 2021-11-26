import os

import flask
from flask import render_template, request, redirect, flash, url_for, Response
from werkzeug.utils import secure_filename

import lf_data_explorer.queries.measurement
import lf_data_explorer.queries.sample
import lf_data_explorer.queries.experiment

from lf_data_explorer import app, utilities

from lf_data_explorer.queries.queries import add_new_image
from lf_data_explorer.utilities import allowed_file, flash_result, sample_prep_methods, node_types, \
    output_network_json


def html_response(response) -> flask.Response:
    return flask.make_response((response, 200, {'Content-Type': 'text/html; charset=utf-8'}))


# The URL routes are slightly different than they would normally be for a Flask app. This is to
# make freezing and serving the pages on github work.
# The route for page which has subpages (e.g. /experiments/ or /measurements/) must end with a
# slash. This causes an index.html page to be generated to serve the content on that page.
# The route for any other page must end with .html to make sure the static pages generated
# have this extension. Normally a webserver would be happy to serve the /about page, but github
# doesn't so it explicitly needs the .html

@app.route('/', methods=["GET"])
def index() -> flask.Response:
    return html_response(render_template("index.html"))


@app.route('/experiments/', methods=["GET"])
def experiments() -> flask.Response:
    all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
    all_samples = lf_data_explorer.queries.sample.get_all_samples()
    return html_response(render_template("experiments.html", experiments=all_experiments,
                                         all_samples=all_samples))


@app.route('/samples/manage', methods=['POST', 'GET'])
def sample_management() -> flask.Response:
    if request.method == "GET":
        return _render_sample_management()
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            new_name = request.form['sample_name']
            parent = int(request.form['parent_selection'])
            creation_method = request.form['creation_method']
            creation_url = request.form['creation_method_url']
            result = lf_data_explorer.queries.sample.add_new_sample(new_name, parent,
                                                                    creation_method, creation_url)
            flash_result(result)
            return _render_sample_management()
        elif form_button == "rename":
            sample_id = int(request.form["sample_selection"])
            new_sample_name = request.form["sample_name"]
            if not new_sample_name:
                new_sample_name = lf_data_explorer.queries.sample.get_sample_by_id(sample_id).name
            parent_sample = int(request.form["parent_selection"])
            if parent_sample == -1:
                parent_sample = None
            creation_method = request.form['creation_method']
            creation_url = request.form['creation_method_url']
            result = lf_data_explorer.queries.sample.edit_sample(sample_id, new_sample_name,
                                                                 parent_sample, creation_method,
                                                                 creation_url)
            flash_result(result)
            return _render_sample_management()

        elif form_button == "delete":
            sample_id = int(request.form["sample_selection"])

            result = lf_data_explorer.queries.sample.delete_sample(sample_id)
            flash_result(result)
            return _render_sample_management()


def _render_sample_management() -> flask.Response:
    all_samples = lf_data_explorer.queries.sample.get_all_samples()
    return html_response(render_template('sample_management.html', all_samples=all_samples,
                                         methods=sample_prep_methods))


@app.route('/experiments/manage', methods=['POST', 'GET'])
def experiment_management() -> flask.Response:
    if request.method == "GET":
        return _render_experiment_management()
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            new_name = request.form['experiment_name']
            result = lf_data_explorer.queries.experiment.add_new_experiment(new_name)
            flash_result(result)
            return _render_experiment_management()
        elif form_button == "rename":
            experiment_id = int(request.form["experiment_selection"])
            new_experiment_name = request.form["new_experiment_name"]
            result = lf_data_explorer.queries.experiment.rename_experiment(experiment_id,
                                                                           new_experiment_name)
            flash_result(result)
            return _render_experiment_management()
        elif form_button == "delete":
            experiment_id = int(request.form["experiment_selection"])
            result = lf_data_explorer.queries.experiment.delete_experiment(experiment_id)
            flash_result(result)
            return _render_experiment_management()


def _render_experiment_management() -> flask.Response:
    all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
    return html_response(render_template('experiment_management.html',
                                         all_experiments=all_experiments))


@app.route('/experiments/_request_experiment_stats', methods=['POST'])
def _request_experiment_stats() -> flask.Response:
    experiment_id = int(request.data)
    experiment = lf_data_explorer.queries.experiment.get_experiment_by_id(experiment_id)

    return Response(experiment.to_json(), status=201, mimetype='application/json')


@app.route('/measurements/manage', methods=['POST', 'GET'])
def measurement_management() -> flask.Response:
    if request.method == "GET":
        return _render_measurement_management()
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            sample_id = int(request.form['sample_selection'])
            experiment_id = int(request.form['experiment_selection'])
            url = request.form["url"]
            result = lf_data_explorer.queries.measurement.add_measurement(sample_id, experiment_id,
                                                                          url)
            flash_result(result)
            return _render_measurement_management()
        elif form_button == "delete":
            sample_id = int(request.form['delete_sample_selection'])
            experiment_id = int(request.form['delete_measurement_selection'])
            result = lf_data_explorer.queries.measurement.delete_measurement(sample_id,
                                                                             experiment_id)
            flash_result(result)
            return _render_measurement_management()


def _render_measurement_management() -> flask.Response:
    all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
    all_samples = lf_data_explorer.queries.sample.get_all_samples()
    return html_response(render_template('measurement_management.html',
                                         all_experiments=all_experiments, all_samples=all_samples))


@app.route('/measurements/_request_measurements', methods=['POST'])
def _request_measurements() -> flask.Response:
    sample_id = int(request.data)
    measurements = lf_data_explorer.queries.sample.get_sample_measurements(sample_id)

    return Response(utilities.measurements_to_json(measurements), status=201,
                    mimetype='application/json')


@app.route('/samples/', methods=['POST', 'GET'], strict_slashes=False)
def samples() -> flask.Response:
    all_samples = lf_data_explorer.queries.sample.get_all_samples()
    output_network_json(all_samples)
    return html_response(render_template('sample_overview.html', all_samples=all_samples,
                                         methods=sample_prep_methods))


@app.route('/samples/<sample_name>.html', methods=['POST', 'GET'])
def select_sample(sample_name: str) -> flask.Response:
    if request.method == "GET":
        all_samples = lf_data_explorer.queries.sample.get_all_samples()
        selected_sample = lf_data_explorer.queries.sample.get_sample_by_name(sample_name)
        output_network_json(all_samples)

        return html_response(render_template('sample_details.html', all_samples=all_samples,
                                             current_sample=selected_sample,
                                             methods=sample_prep_methods, node_types=node_types))


@app.route('/samples/<sample_name>/new_image', methods=['POST', 'GET'])
def add_image(sample_name: str) -> flask.Response:
    if request.method == "GET":
        sample = lf_data_explorer.queries.sample.get_sample_by_name(sample_name)
        return html_response(render_template("add_image.html", sample=sample))
    else:

        # check if the post request has the file part
        if 'image_path' not in request.files:
            flash('No file part.')
            return redirect(request.url)
        file = request.files['image_path']
        if file.filename == '':
            flash('No file selected.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            sample = lf_data_explorer.queries.sample.get_sample_by_name(sample_name)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            add_new_image(filename, sample.id)
            return redirect(url_for("select_sample", sample_name=sample_name))


@app.route('/samples/_request_sample_stats', methods=['POST'])
def _request_sample_stats() -> flask.Response:
    sample_id = int(request.data)
    measurements = lf_data_explorer.queries.sample.get_sample_measurements(sample_id)
    children = lf_data_explorer.queries.sample.get_sample_children(sample_id)
    stats = f'{{"num_measurements": {len(measurements)}, "num_children": {len(children)}}}'

    return Response(stats, status=201, mimetype='application/json')


@app.route('/samples/_request_sample_details', methods=['POST'])
def _request_sample_details() -> flask.Response:
    sample_id = int(request.data)
    sample = lf_data_explorer.queries.sample.get_sample_by_id(sample_id)

    return Response(sample.to_json(), status=201, mimetype='application/json')


@app.route('/about.html')
def about() -> flask.Response:
    return html_response(render_template('about.html'))
