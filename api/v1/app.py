#!/usr/bin/python3
""" Module for the API """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    Host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    Port = int(os.getenv('HBNB_API_PORT', default=5000))
    app.run(host=Host, port=Port, threaded=True)
