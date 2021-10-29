import os

from flask import (
    Blueprint,
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
)
from flask.helpers import url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_login.utils import login_required
from flask_wtf.csrf import CSRFProtect
from mongoengine.errors import NotUniqueError

# initialise app and login before import so app is "exported" first
app = Flask(__name__)  # nosort
login = LoginManager(app)
login.login_view = "login"


from . import db
from .api import (
    IMG_STORAGE_PATH,
    delete_image,
    get_image,
    img_to_str,
    mark_spots,
    parse_template_form,
    read_form,
    save_image,
    str_to_img,
)
from .forms import EditForm, LoginForm, RegistrationForm
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


@app.post("/define-template/<new_copy>")
def define_template(new_copy):
    """parse template definition form and save to db

    Returns:
        redirect: redirects to view_templates with success flash
    """
    if current_user.is_authenticated:
        owner = current_user
    else:
        owner = None
    try:
        saved_template = db.save_template(request.form, owner)
    except NotUniqueError as e:
        flash(f"template save failed: that template name is taken!", "danger")
        return redirect(request.environ.get("HTTP_REFERER"))
    if new_copy == "copy":
        curr_img_path = url_for(
            "static",
            filename=f"{IMG_STORAGE_PATH}/{request.form['currTempId']}",
        )
        saved_template.img_name = curr_img_path
        saved_template.save()
    elif new_copy == "new":
        img_str = request.files["uploadedImg"].read()
        img = str_to_img(img_str)
        save_image(img, saved_template.img_name)
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
    # show all public templates and user's private templates if logged in
    templates = db.get_public_templates()
    if current_user.is_authenticated:
        user = User.objects(id=current_user.id).first()
        user_templates = db.get_user_templates(user)
        templates.extend(user_templates)

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


@app.route("/user/edit", methods=["GET", "POST"])
@login_required
def edit_user():
    form = EditForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        current_user.save()
        flash("user changed successfully!", "success")
        return redirect(url_for("home"))
    return render_template(
        "register.html", title="Edit User", form=form, user=current_user
    )


@app.route("/logout")
def logout():
    logout_user()
    flash("bye!", "success")
    return redirect(url_for("home"))
