from flask import Flask, jsonify, redirect, render_template, request
from flask.helpers import url_for

from .api import img_to_str, mark_spots, parse_template_form, str_to_img

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/create")
def create_template():
    return render_template("create_template.html")


@app.post("/find-spots")
def find_spots():
    img_str = request.files["uploadedImg"].read()
    img = str_to_img(img_str)
    spot_coords, marked_img = mark_spots(img)
    marked_img_str = img_to_str(marked_img)
    num_spots = len(spot_coords)
    return jsonify(
        {"img": marked_img_str, "num_spots": num_spots, "coords": spot_coords}
    )


@app.post("/define-template")
def define_template():
    question_data = request.form
    img_str = request.files["uploadedImg"].read()
    img = str_to_img(img_str)
    template = parse_template_form(question_data, img)
    return jsonify(template.to_json())


@app.get("/view")
def view_template():
    return render_template("view_template.html")
