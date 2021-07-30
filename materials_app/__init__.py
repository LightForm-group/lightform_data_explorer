from flask import Flask

app = Flask(__name__)
from materials_app import views


if __name__ == '__main__':
    app.run()
