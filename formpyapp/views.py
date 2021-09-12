import numpy as np
from flask import Flask, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect

from .api import read_img, thresh_img

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/create")
def create_template():
    return render_template("create_template.html")


@app.route("/create", methods=["POST"])
def handle_template():
    img_str = request.files["uploadedImg"].read()
    img = read_img(img_str)
    img_processed = thresh_img(img)
    return render_template("view_template.html", img=img_processed)


@app.get("/view")
def view_template():
    return render_template("view_template.html")
