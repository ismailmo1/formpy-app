from app.formpyapp.db import utils
from flask import Blueprint, current_app, render_template
from flask.helpers import send_from_directory
from flask_login import current_user

bp = Blueprint("home", __name__)


@bp.get("/")
@bp.get("/home")
def home():
    return render_template("index.html")


@bp.get("/getting-started")
def start():
    return render_template("getting_started.html")


@bp.get("/starter-doc")
def starter_doc():
    return send_from_directory(
        directory=current_app.config["DOCS_FOLDER_PATH"],
        path="formpy-starter-doc.odt",
    )


@bp.get("/view")
def view_template():
    # show all public templates and user's private templates if logged in
    templates = utils.get_all_templates(current_user)

    return render_template("view_template.html", templates=templates)
