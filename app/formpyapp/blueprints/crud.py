import cv2
from app.formpyapp.api.alignment import align_img
from app.formpyapp.api.img_proc import img_to_str
from app.formpyapp.db import utils
from app.formpyapp.forms.template_forms import DefineTemplateForm
from flask import Blueprint, flash, jsonify, redirect, render_template, request
from flask.helpers import url_for
from flask_login import current_user
from flask_login.utils import login_required

bp = Blueprint("crud", __name__)


@bp.get("/create")
def create_template():
    form = DefineTemplateForm()
    return render_template("create_template.html", form=form, title="create")


@bp.get("/delete/<template_id>")
@login_required
def delete_template(template_id: str):
    deleted = utils.remove_template(template_id)

    if deleted:
        utils.delete_image(template_id)
        flash("template deleted!", "info")
    else:
        flash("unable to delete template", "danger")
    return redirect(url_for("home.view_template"))


@bp.get("/edit/<template_id>")
def edit_template(template_id):
    template = utils.get_template(template_id)
    img_path = utils.get_image_path(template_id)
    img = cv2.imread(img_path)
    aligned_img = align_img(img)
    template_img = img_to_str(aligned_img)
    is_owner = True if current_user == template.owner else False
    if not is_owner:
        flash(
            "you don't own this template so you must change the name and save a copy!",
            "warning",
        )

    return render_template(
        "create_template.html",
        template=template,
        template_img=template_img,
        title="edit",
        is_owner=is_owner,
        template_json=template.to_json(),
    )


@bp.post("/update-template/<template_id>")
def update_template(template_id):
    updated_template = utils.update_template(template_id, request.get_json())
    if updated_template:
        return jsonify(updated_template.to_json())
    else:
        return None
