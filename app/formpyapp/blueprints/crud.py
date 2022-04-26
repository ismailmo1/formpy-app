from formpyapp.api.alignment import align_img
from formpyapp.api.img_proc import img_to_str
from formpyapp.db import db
from flask import Blueprint, flash, jsonify, redirect, render_template, request
from flask.helpers import url_for
from flask_login import current_user
from flask_login.utils import login_required

bp = Blueprint("crud", __name__)


@bp.get("/view")
def view_template():
    # show all public templates and user's private templates if logged in
    templates = db.get_all_templates(current_user)

    return render_template("view_template.html", templates=templates)


@bp.get("/delete/<template_id>")
@login_required
def delete_template(template_id: str):
    deleted = db.remove_template(template_id)

    if deleted:
        db.delete_image(template_id)
        flash("template deleted!", "info")
    else:
        flash("unable to delete template", "danger")
    return redirect(url_for("view_template"))


@bp.get("/edit/<template_id>")
def edit_template(template_id):
    template = db.get_template(template_id)
    img = db.get_image(template_id)
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
    updated_template = db.update_template(template_id, request.get_json())
    if updated_template:
        return jsonify(updated_template.to_json())
    else:
        return None
