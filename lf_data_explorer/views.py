from lf_data_explorer import app
from flask import render_template, request

from lf_data_explorer.queries import get_all_samples, add_new_sample


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/samples', methods=['POST', 'GET'])
def samples():
    if request.method == "GET":
        all_samples = get_all_samples()
        return render_template('samples.html', samples=all_samples)
    else:
        new_name = request.form['sample_name']
        result = add_new_sample(new_name)
        all_samples = get_all_samples()
        return render_template('samples.html', samples=all_samples, new_sample=result)


@app.route('/about')
def about():
    return render_template('about.html')
