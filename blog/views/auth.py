from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from blog.models.database import db
from blog.models import User
from blog.forms.user import RegistrationForm, LoginForm
from werkzeug.exceptions import NotFound

def login():
    if current_user.is_authenticated:
        return redirect("index")
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one_or_none()
    if user is None:
        return render_template("auth/login.html", form=form, error="username doesn't exist")
    if not user.validate_password(form.password.data):
        return render_template("auth/login.html", form=form, error="invalid username or password")
    login_user(user)
    return redirect(url_for("index"))
    return render_template("auth/login.html", form=form)


@auth_app.route("/login-as/", methods=["GET", "POST"], endpoint="login-as")
def login-as():
        if not (current_user.is_authenticated and current_user.is_staff):
            raise NotFound

    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("auth/register.html", form=form)

        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("auth/register.html", form=form)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("index"))

    return render_template("auth/register.html", form=form, error=error)
