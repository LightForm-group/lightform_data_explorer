from materials_app import app
from flask import render_template


@app.route('/')
def show_index():
    return render_template("index.html")


@app.route('/add_sample')
def show_add_sample():
    return render_template('add_sample.html')


@app.route('/about')
def show_about():
    return render_template('about.html')
