from lf_data_explorer import app
from flask import render_template, request

import lf_data_explorer.queries as queries


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/samples', methods=['POST', 'GET'])
def samples():
    if request.method == "GET":
        all_samples = queries.get_all_samples()
        return render_template('samples.html', all_samples=all_samples)
    else:
        new_name = request.form['sample_selection']
        result = queries.add_new_sample(new_name)
        all_samples = queries.get_all_samples()
        return render_template('samples.html', all_samples=all_samples, new_sample=result)


@app.route('/samples/<sample_id>')
def select_sample(sample_id):
    all_samples = queries.get_all_samples()
    selected_sample = queries.get_sample_by_id(sample_id)
    return render_template('samples.html', all_samples=all_samples, selected_sample=selected_sample)


@app.route('/about')
def about():
    return render_template('about.html')
