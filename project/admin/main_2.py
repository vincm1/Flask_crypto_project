from ssl import HAS_TLSv1_1
from flask import Blueprint, render_template

second = Blueprint("second", __name__, static_folder="static", template_folder="templates")

@second.route("/home")
@second.route("/")
def home():
    return render_template("index.html")

@second.route("/test")
def test():
    return "<h1>Test</h1>"