from formpy.utils.img_processing import ImageAlignmentError
from formpyapp.api.alignment import (
    add_align_rectangle,
    align_img,
    get_bounding_pts,
)
from formpyapp.api.img_proc import (
    img_to_str,
    pdf_upload_to_img,
    read_form_img,
    str_to_img,
)
from formpyapp.api.parsing import read_form, read_form_img
from formpyapp.db import db
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user
from formpyapp.db.models import Template
from mongoengine.errors import NotUniqueError

bp = Blueprint("processing", __name__)


@bp.post("/upload-template")
def upload_template():
    uploaded_template = request.files["uploadedTemplate"]
    if uploaded_template.content_type == "image/jpeg":
        form_img = uploaded_template.read()
        img = read_form_img(form_img)
    elif uploaded_template.content_type == "application/pdf":
        img = pdf_upload_to_img(uploaded_template)
    else:
        raise Exception("file upload failed")
    # change func to accept bounding rect pts
    res_img = img_to_str(img)

    try:
        pts = get_bounding_pts(img).tolist()
    except ImageAlignmentError:
        return {"pts": None, "img": res_img}
    return jsonify({"pts": pts, "img": res_img})


@bp.post("/align-template")
def align_template():
    is_custom_align = True if request.form["custom"] == "true" else False
    pts = request.form["pts"]
    uploaded_template = request.files["uploadedTemplate"]
    if uploaded_template.content_type == "application/pdf":
        img = pdf_upload_to_img(uploaded_template)
    else:
        form_img = request.files["uploadedTemplate"].read()
        img = read_form_img(form_img)
    # change func to accept bounding rect pts
    aligned_img = align_img(img, pts)
    if is_custom_align:
        aligned_img = add_align_rectangle(aligned_img)
    aligned_img_str = img_to_str(aligned_img)
    return jsonify({"img": aligned_img_str})


@bp.post("/define-template/<new_copy>")
def define_template(new_copy):
    """defines new template and saves to db. if new then new image name created and saved, if creating a copy of old template, img name is retrieved and copied to new template without duplicating image in storage.

    Args:
        new_copy : new templates defined from create template page, copies are define from edit page

    Returns:
        json: json response of saved template or error
    """
    template_data = request.json

    img_str = template_data.get("uploadedTemplate").split(
        "data:image/jpeg;base64, "
    )[1]
    img = str_to_img(img_str)

    if current_user.is_authenticated:
        owner = current_user
    else:
        owner = None
    try:
        saved_template = db.save_template(template_data, owner)
    except NotUniqueError as e:
        # flash(f"template save failed: that template name is taken!", "danger")
        # return redirect(request.environ.get("HTTP_REFERER"))
        return jsonify("NotUniqueError")
    if new_copy == "copy":
        curr_template_id = template_data.pop("currTempId")
        old_img_name = Template.objects(id=curr_template_id).first().img_name
        saved_template.img_name = old_img_name
        saved_template.save()
    elif new_copy == "new":
        db.save_template_image(img, saved_template.img_name)
        # add error handling for failed image saves

    return jsonify(saved_template.to_json())
    # flash(f"template '{saved_template.name}' created successfully!", "info")
    # return redirect(url_for("view_template"))


@bp.route("/read", methods=["POST", "GET"])
def read_forms():
    if request.method == "GET":
        templates = db.get_all_templates(current_user)
        return render_template("read_forms.html", templates=templates)
    elif request.method == "POST":
        template_id = request.form.get("templateId")
        form_imgs = request.files.getlist("formImg")
        marked_imgs = []
        for img in form_imgs:
            marked_imgs.append(read_form(template_id, img.read()))

        # return form image overlay with answers, json of question : answer(s)
        res = {
            "imgs": [img_to_str(img[0]) for img in marked_imgs],
            "answers": [img[1] for img in marked_imgs],
        }
        return jsonify(res)
