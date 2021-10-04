import os

from werkzeug.utils import secure_filename

import lf_data_explorer.queries.measurement
import lf_data_explorer.queries.sample

import lf_data_explorer.queries.experiment
from lf_data_explorer import app, utilities
from flask import render_template, request, redirect, flash, url_for, Response

from lf_data_explorer.queries.queries import add_new_image
from lf_data_explorer.utilities import allowed_file, flash_result


@app.route('/')
def index():
    all_samples = lf_data_explorer.queries.sample.get_all_samples()
    return render_template("index.html", all_samples=all_samples)


@app.route('/experiments')
def experiments():
    all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
    all_samples = lf_data_explorer.queries.sample.get_all_samples()
    return render_template("experiments.html", experiments=all_experiments, all_samples=all_samples)


@app.route('/samples/manage', methods=['POST', 'GET'])
def sample_management():
    if request.method == "GET":
        all_samples = lf_data_explorer.queries.sample.get_all_samples()
        return render_template('sample_management.html', all_samples=all_samples)
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            new_name = request.form['sample_name']
            parent = int(request.form['parent_selection'])
            result = lf_data_explorer.queries.sample.add_new_sample(new_name, parent)
            flash_result(result)
            all_samples = lf_data_explorer.queries.sample.get_all_samples()
            return render_template('sample_management.html', all_samples=all_samples)
        elif form_button == "rename":
            sample_id = int(request.form["sample_selection"])
            new_sample_name = request.form["new_sample_name"]
            if not new_sample_name:
                new_sample_name = lf_data_explorer.queries.sample.get_sample_by_id(sample_id).name
            parent_sample = int(request.form["parent_selection"])
            if parent_sample == -1:
                parent_sample = None
            result = lf_data_explorer.queries.sample.edit_sample(sample_id, new_sample_name, parent_sample)
            flash(result)
            all_samples = lf_data_explorer.queries.sample.get_all_samples()
            return render_template('sample_management.html', all_samples=all_samples)

        elif form_button == "delete":
            sample_id = int(request.form["sample_selection"])

            result = lf_data_explorer.queries.sample.delete_sample(sample_id)
            flash(result)

            all_samples = lf_data_explorer.queries.sample.get_all_samples()
            return render_template('sample_management.html', all_samples=all_samples)


@app.route('/experiments/manage', methods=['POST', 'GET'])
def experiment_management():
    if request.method == "GET":
        all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
        return render_template('experiment_management.html', all_experiments=all_experiments)
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            new_name = request.form['experiment_name']
            result = lf_data_explorer.queries.experiment.add_new_experiment(new_name)
            flash_result(result)
            all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
            return render_template('experiment_management.html', all_experiments=all_experiments)
        elif form_button == "rename":
            experiment_id = int(request.form["experiment_selection"])
            new_experiment_name = request.form["new_experiment_name"]
            result = lf_data_explorer.queries.experiment.rename_experiment(experiment_id, new_experiment_name)
            flash_result(result)
            all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
            return render_template('experiment_management.html', all_experiments=all_experiments)
        elif form_button == "delete":
            experiment_id = int(request.form["experiment_selection"])
            result = lf_data_explorer.queries.experiment.delete_experiment(experiment_id)
            flash_result(result)

            all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
            return render_template('experiment_management.html', all_experiments=all_experiments)


@app.route('/measurements/manage', methods=['POST', 'GET'])
def measurement_management():
    if request.method == "GET":
        all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
        all_samples = lf_data_explorer.queries.sample.get_all_samples()
        return render_template('measurement_management.html', all_experiments=all_experiments,
                               all_samples=all_samples)
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            sample_id = int(request.form['sample_selection'])
            experiment_id = int(request.form['experiment_selection'])
            url = request.form["url"]
            result = lf_data_explorer.queries.measurement.add_measurement(sample_id, experiment_id, url)
            flash_result(result)
            all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
            all_samples = lf_data_explorer.queries.sample.get_all_samples()
            return render_template('measurement_management.html', all_experiments=all_experiments,
                                   all_samples=all_samples)
        elif form_button == "delete":
            sample_id = int(request.form['delete_sample_selection'])
            experiment_id = int(request.form['delete_measurement_selection'])
            result = lf_data_explorer.queries.measurement.delete_measurement(sample_id, experiment_id)
            flash_result(result)
            all_experiments = lf_data_explorer.queries.experiment.get_all_experiments()
            all_samples = lf_data_explorer.queries.sample.get_all_samples()
            return render_template('measurement_management.html', all_experiments=all_experiments,
                                   all_samples=all_samples)


@app.route('/measurements/_request_measurements', methods=['POST'])
def request_measurements():
    sample_id = int(request.data)
    measurements = lf_data_explorer.queries.sample.get_sample_measurements(sample_id)

    return Response(utilities.measurements_to_json(measurements), status=201,
                    mimetype='application/json')


@app.route('/samples', methods=['POST', 'GET'], strict_slashes=False)
def samples():
    all_samples = lf_data_explorer.queries.sample.get_all_samples()

    return render_template('samples.html', all_samples=all_samples)


@app.route('/samples/<sample_id>', methods=['POST', 'GET'])
def select_sample(sample_id: int):
    if request.method == "GET":
        all_samples = lf_data_explorer.queries.sample.get_all_samples()
        selected_sample = lf_data_explorer.queries.sample.get_sample_by_id(sample_id)
        return render_template('samples.html', all_samples=all_samples,
                               current_sample=selected_sample)


@app.route('/samples/<sample_id>/new_image', methods=['POST', 'GET'])
def add_image(sample_id: int):
    if request.method == "GET":
        sample = lf_data_explorer.queries.sample.get_sample_by_id(sample_id)
        return render_template("add_image.html", sample=sample)
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            add_new_image(filename, sample_id)
            return redirect(url_for("select_sample", sample_id=sample_id))


@app.route('/samples/_request_sample_stats', methods=['POST'])
def _request_sample_stats():
    sample_id = int(request.data)
    measurements = lf_data_explorer.queries.sample.get_sample_measurements(sample_id)
    children = lf_data_explorer.queries.sample.get_sample_children(sample_id)
    stats = f'{{"num_measurements": {len(measurements)}, "num_children": {len(children)}}}'

    return Response(stats, status=201, mimetype='application/json')


@app.route('/about')
def about():
    return render_template('about.html')
