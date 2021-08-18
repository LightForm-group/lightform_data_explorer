import os

from werkzeug.utils import secure_filename

from lf_data_explorer import app
from flask import render_template, request, redirect, flash, url_for

import lf_data_explorer.queries as queries
from lf_data_explorer.utilities import allowed_file


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/experiments')
def experiments():
    all_experiments = queries.get_all_experiments()
    return render_template("experiments.html", experiments=all_experiments)


@app.route('/samples/manage', methods=['POST', 'GET'])
def sample_management():
    if request.method == "GET":
        all_samples = queries.get_all_samples()
        return render_template('sample_management.html', all_samples=all_samples)
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            new_name = request.form['sample_name']
            result = queries.add_new_sample(new_name)
            flash(result)
            all_samples = queries.get_all_samples()
            return render_template('sample_management.html', all_samples=all_samples)
        elif form_button == "rename":
            sample_id = int(request.form["sample_selection"])
            new_sample_name = request.form["new_sample_name"]
            result = queries.rename_sample(sample_id, new_sample_name)
            flash(result)
            all_samples = queries.get_all_samples()
            return render_template('sample_management.html', all_samples=all_samples)

        elif form_button == "delete":
            sample_id = int(request.form["sample_selection"])

            result = queries.delete_sample(sample_id)
            flash(result)

            all_samples = queries.get_all_samples()
            return render_template('sample_management.html', all_samples=all_samples)


@app.route('/experiments/manage', methods=['POST', 'GET'])
def experiment_management():
    if request.method == "GET":
        all_experiments = queries.get_all_experiments()
        return render_template('experiment_management.html', all_experiments=all_experiments)
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            new_name = request.form['experiment_name']
            result = queries.add_new_experiment(new_name)
            flash(result)
            all_experiments = queries.get_all_experiments()
            return render_template('experiment_management.html', all_experiments=all_experiments)
        elif form_button == "rename":
            experiment_id = int(request.form["experiment_selection"])
            new_experiment_name = request.form["new_experiment_name"]
            result = queries.rename_experiment(experiment_id, new_experiment_name)
            flash(result)
            all_experiments = queries.get_all_experiments()
            return render_template('experiment_management.html', all_experiments=all_experiments)

        elif form_button == "delete":
            experiment_id = int(request.form["sample_selection"])

            result = queries.delete_experiment(experiment_id)
            flash(result)

            all_experiments = queries.get_all_experiments()
            return render_template('experiment_management.html', all_experiments=all_experiments)


@app.route('/measurments/manage', methods=['POST', 'GET'])
def measurement_management():
    if request.method == "GET":
        all_experiments = queries.get_all_experiments()
        all_samples = queries.get_all_samples()
        return render_template('measurement_management.html', all_experiments=all_experiments,
                               all_samples=all_samples)
    else:
        form_button = request.form["submit"]
        if form_button == "add":
            sample_id = int(request.form['sample_selection'])
            experiment_id = int(request.form['experiment_selection'])
            url = request.form["url"]
            result = queries.add_measurement(sample_id, experiment_id, url)
            flash(result)
            all_experiments = queries.get_all_experiments()
            all_samples = queries.get_all_samples()
            return render_template('experiment_management.html', all_experiments=all_experiments,
                                   all_samples=all_samples)


@app.route('/samples', methods=['POST', 'GET'], strict_slashes=False)
def samples():
    all_samples = queries.get_all_samples()

    return render_template('samples.html', all_samples=all_samples)


@app.route('/samples/<sample_id>', methods=['POST', 'GET'])
def select_sample(sample_id: int):
    if request.method == "GET":
        all_samples = queries.get_all_samples()
        selected_sample = queries.get_sample_by_id(sample_id)
        return render_template('samples.html', all_samples=all_samples,
                               current_sample=selected_sample)


@app.route('/samples/<sample_id>/new_image', methods=['POST', 'GET'])
def add_image(sample_id: int):
    if request.method == "GET":
        sample = queries.get_sample_by_id(sample_id)
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

            queries.add_new_image(filename, sample_id)
            return redirect(url_for("select_sample", sample_id=sample_id))


@app.route('/about')
def about():
    return render_template('about.html')
