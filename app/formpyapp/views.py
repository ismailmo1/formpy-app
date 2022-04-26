import os

from app.formpy.utils.img_processing import ImageAlignmentError
from flask import Flask, flash, jsonify, redirect, render_template, request
from flask.helpers import send_from_directory, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_login.utils import login_required
from flask_wtf.csrf import CSRFProtect
from mongoengine.errors import NotUniqueError

from . import auth

# initialise app and login before import so app is "exported" first
app = Flask(__name__)  # nosort
login = LoginManager(app)
login.login_view = "login"
app.register_blueprint(auth.bp)


from . import db
from .api import (
    add_align_rectangle,
    align_img,
    delete_image,
    get_bounding_pts,
    get_image,
    img_to_str,
    pdf_upload_to_img,
    read_form,
    read_form_img,
    save_template_image,
    str_to_img,
)
from .forms import DefineTemplateForm
from .models import Template

csrf = CSRFProtect(app)
app.secret_key = os.environ["FLASK_SECRET"]


@app.get("/")
@app.get("/home")
def home():
    return render_template("index.html")


@app.get("/getting-started")
def start():
    return render_template("getting_started.html")


@app.get("/starter-doc")
def starter_doc():
    return send_from_directory(
        directory=os.environ["DOCS_FOLDER_PATH"], path="formpy-starter-doc.odt"
    )


@app.get("/create")
def create_template():
    form = DefineTemplateForm()
    return render_template("create_template.html", form=form, title="create")


@app.post("/upload-template")
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


@app.post("/align-template")
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


@app.post("/define-template/<new_copy>")
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
        save_template_image(img, saved_template.img_name)
        # add error handling for failed image saves

    return jsonify(saved_template.to_json())
    # flash(f"template '{saved_template.name}' created successfully!", "info")
    # return redirect(url_for("view_template"))


@app.post("/update-template/<template_id>")
def update_template(template_id):
    updated_template = db.update_template(template_id, request.get_json())
    if updated_template:
        return jsonify(updated_template.to_json())
    else:
        return None


@app.get("/view")
def view_template():
    # show all public templates and user's private templates if logged in
    templates = db.get_all_templates(current_user)

    return render_template("view_template.html", templates=templates)


@app.get("/delete/<template_id>")
@login_required
def delete_template(template_id: str):
    deleted = db.remove_template(template_id)

    if deleted:
        delete_image(template_id)
        flash("template deleted!", "info")
    else:
        flash("unable to delete template", "danger")
    return redirect(url_for("view_template"))


@app.get("/edit/<template_id>")
def edit_template(template_id):
    template = db.get_template(template_id)
    img = get_image(template_id)
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


@app.route("/read", methods=["POST", "GET"])
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
