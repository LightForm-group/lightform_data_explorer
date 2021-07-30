from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def show_index():
    return render_template("index.html")


@app.route('/add_sample')
def show_add_sample():
    return render_template('add_sample.html')


@app.route('/about')
def show_about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
