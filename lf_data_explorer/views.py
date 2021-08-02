from lf_data_explorer import app
from flask import render_template, request

from lf_data_explorer.queries import get_all_samples


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/list_samples')
def list_samples():
    samples = get_all_samples()
    return render_template('list_samples.html', samples=samples)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_samples', methods=['POST', 'GET'])
def add_samples():
    if request.method == "GET":
        return render_template('add_samples.html')
    else:
        new_name = request.form['sample_name']
        return render_template('add_samples.html', sample=new_name)
