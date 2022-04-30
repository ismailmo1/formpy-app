from app.formpyapp import login_mgr
from app.formpyapp.db import utils
from app.formpyapp.db.models import User
from app.formpyapp.forms.auth_forms import (
    DeleteUserForm,
    EditUserForm,
    LoginForm,
    RegistrationForm,
)
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("you're already logged in!", "warning")
        return redirect(url_for("home.view_template"))
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
        return redirect(url_for("auth.login"))
    return render_template(
        "register.html", action="/register", title="Register", edit_form=form
    )


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("you're already logged in!", "warning")
        return redirect(url_for("home.view_template"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        flash(f"welcome back {current_user.username}!", "success")
        return redirect(url_for("home.view_template"))
    return render_template("login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("bye!", "success")
    return redirect(url_for("home.view_template"))


@bp.route("/user/edit", methods=["GET", "POST"])
@login_required
def edit_user():
    edit_form = EditUserForm(obj=current_user)
    delete_form = DeleteUserForm()
    if edit_form.validate_on_submit():
        current_user.username = edit_form.username.data
        current_user.first_name = edit_form.first_name.data
        current_user.last_name = edit_form.last_name.data
        current_user.email = edit_form.email.data
        current_user.set_password(edit_form.password.data)
        current_user.save()
        flash("user changed successfully!", "success")
        return redirect(url_for("home.view_template"))
    return render_template(
        "register.html",
        action="/user/edit",
        title="Edit User",
        edit_form=edit_form,
        delete_form=delete_form,
        user=current_user,
    )


@bp.post("/user/delete")
@login_required
def delete_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        template_delete = request.form.get("delete_options")

        if template_delete == "all":
            utils.remove_user_templates(current_user, private_only=False)
        elif template_delete == "private":
            utils.remove_user_templates(current_user, private_only=True)
        elif template_delete == "none":
            utils.make_templates_public(current_user)

        name = current_user.username
        current_user.delete()
        flash(f"user deleted, sorry to see you go {name}!")

    return redirect(url_for("home.view_template"))


@login_mgr.user_loader
def load_user(id):
    return User.objects(id=id).first()
