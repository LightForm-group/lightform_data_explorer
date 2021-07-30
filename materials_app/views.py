from materials_app import app
from flask import render_template

from materials_app.queries import get_all_samples


@app.route('/')
def show_index():
    return render_template("index.html")


@app.route('/list_samples')
def show_list_samples():
    samples = get_all_samples()
    return render_template('list_samples.html', samples=samples)


@app.route('/about')
def show_about():
    return render_template('about.html')
