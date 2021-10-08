import os
from re import template

import cv2
from cv2 import imread
from flask import Flask, flash, jsonify, redirect, render_template, request
from flask.helpers import url_for

from .api import (
    IMG_STORAGE_PATH,
    delete_image,
    get_image,
    img_to_str,
    mark_spots,
    parse_template_form,
    save_image,
    str_to_img,
)

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET"]
from .db import (
    get_all_templates,
    get_template,
    remove_template,
    save_template,
    update_template,
)


@app.get("/")
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
    """parse template definition form and save to db

    Returns:
        redirect: redirects to view_templates with success flash
    """
    question_data = request.form
    template_name = request.form["templateName"]
    template_coords = f'[{request.form["coords"]}]'
    img_str = request.files["uploadedImg"].read()
    img = str_to_img(img_str)
    template = parse_template_form(question_data, img)
    temp_id = save_template(template_name, template_coords, template.to_dict())
    save_image(img, temp_id)
    flash("template created successfully!", "info")
    return redirect(url_for("view_template"))


@app.get("/view")
def view_template():
    templates = get_all_templates()
    return render_template("view_template.html", templates=templates)


@app.get("/delete/<template_id>")
def delete_template(template_id: str):
    deleted = remove_template(template_id)
    img_delete = delete_image(template_id)

    if deleted and img_delete:
        flash("template deleted!", "info")
    else:
        flash("unable to delete template", "danger")
    return redirect(url_for("view_template"))


@app.get("/edit/<template_id>")
def edit_template(template_id):
    template = get_template(template_id)
    img = get_image(template_id)
    template_img = img_to_str(img)
    return render_template(
        "edit_template.html", template=template, template_img=template_img
    )


@app.post("/update-template")
def update_template():
    template_id = request.form.get("template-id")
