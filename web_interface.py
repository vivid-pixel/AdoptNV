from flask import Flask, render_template
from adoptnv_core import flask_test

# Flask essentials
app = Flask(__name__)


@app.route("/")
def web_interface():
    result = flask_test()
    return f"Well, Flask [still] works and provided a test result of: {result}"
