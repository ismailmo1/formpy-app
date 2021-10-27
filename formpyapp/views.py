import os

from flask import Flask, flash, jsonify, redirect, render_template, request
from flask.helpers import url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_wtf.csrf import CSRFProtect

# initialise app and login before import so app is "exported" first"
app = Flask(__name__)  # nosort
login = LoginManager(app)


from . import db
from .api import (
    delete_image,
    get_image,
    img_to_str,
    mark_spots,
    parse_template_form,
    read_form,
    save_image,
    str_to_img,
)
from .forms import LoginForm, RegistrationForm
from .models import User

csrf = CSRFProtect(app)
app.secret_key = os.environ["FLASK_SECRET"]


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
    if current_user.is_authenticated:
        owner = current_user
    else:
        owner = None
    saved_template = db.save_template(request.form, owner)
    img_str = request.files["uploadedImg"].read()
    img = str_to_img(img_str)
    save_image(img, saved_template.id)
    flash(f"template '{saved_template.name}' created successfully!", "info")
    return redirect(url_for("view_template"))


@app.post("/update-template/<template_id>")
def update_template(template_id):
    updated_template = db.update_template(template_id, request.form)
    if updated_template:
        flash("template updated successfully!", "info")
    else:
        flash("something went wrong", "danger")
    return redirect(url_for("view_template"))


@app.get("/view")
def view_template():
    templates = db.get_all_templates()
    return render_template("view_template.html", templates=templates)


@app.get("/delete/<template_id>")
def delete_template(template_id: str):
    deleted = db.remove_template(template_id)
    img_delete = delete_image(template_id)

    if deleted and img_delete:
        flash("template deleted!", "info")
    else:
        flash("unable to delete template", "danger")
    return redirect(url_for("view_template"))


@app.get("/edit/<template_id>")
def edit_template(template_id):
    template = db.get_template(template_id)
    img = get_image(template_id)
    template_img = img_to_str(img)
    return render_template(
        "edit_template.html", template=template, template_img=template_img
    )


@app.route("/read", methods=["POST", "GET"])
def read_forms():
    if request.method == "GET":
        templates = db.get_all_templates()
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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("you're already logged in!", "warning")
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash(f"welcome back {current_user.username}!", "success")
        return redirect(url_for("home"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("you're already logged in!", "warning")
        return redirect(url_for("home"))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        user.save()
        flash("user created successfully! please login", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("bye!", "success")
    return redirect(url_for("home"))
