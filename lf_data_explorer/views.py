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


@app.route('/experiments/manage', methods=['POST', 'GET'])
def experiment_management():
    if request.method == "GET":
        return render_template('experiment_management.html')
    else:
        new_name = request.form['experiment_name']
        result = queries.add_new_experiment(new_name)
        return render_template('experiment_management.html', new_experient=result)


@app.route('/samples/new', methods=['POST', 'GET'])
def new_sample():
    if request.method == "GET":
        return render_template('add_sample.html')
    else:
        new_name = request.form['sample_name']
        result = queries.add_new_sample(new_name)
        return render_template('add_sample.html', new_sample=result)


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
    else:
        delete_id = int(request.view_args['sample_id'])

        sample_name = queries.delete_sample(delete_id)
        message = f"Sample '{sample_name}' was deleted."

        all_samples = queries.get_all_samples()
        return render_template('samples.html', all_samples=all_samples, sample_deleted=message)


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
