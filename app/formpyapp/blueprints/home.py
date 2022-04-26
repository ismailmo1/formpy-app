import os

from flask import Blueprint, render_template
from flask.helpers import send_from_directory
from formpyapp.forms.template_forms import DefineTemplateForm

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
        directory=os.environ["DOCS_FOLDER_PATH"], path="formpy-starter-doc.odt"
    )


@bp.get("/create")
def create_template():
    form = DefineTemplateForm()
    return render_template("create_template.html", form=form, title="create")