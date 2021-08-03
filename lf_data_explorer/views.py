from lf_data_explorer import app
from flask import render_template, request

import lf_data_explorer.queries as queries


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/samples/new', methods=['POST', 'GET'])
def new_sample():
    if request.method == "GET":
        return render_template('add_sample.html')
    else:
        new_name = request.form['sample_selection']
        result = queries.add_new_sample(new_name)
        return render_template('add_sample.html', new_sample=result)


@app.route('/samples', methods=['POST', 'GET'])
def samples():
    all_samples = queries.get_all_samples()

    return render_template('samples.html', all_samples=all_samples)


@app.route('/samples/<sample_id>', methods=['POST', 'GET'])
def select_sample(sample_id):
    all_samples = queries.get_all_samples()
    if request.method == "GET":
        selected_sample = queries.get_sample_by_id(sample_id)
        return render_template('samples.html', all_samples=all_samples, selected_sample=selected_sample)
    else:
        delete_id = int(request.view_args['sample_id'])
        result = queries.delete_sample(delete_id)
        if result:
            message = "Sample was deleted."
        else:
            message = "Sample could not be deleted."
        return render_template('samples.html', all_samples=all_samples, sample_deleted=message)


@app.route('/about')
def about():
    return render_template('about.html')
